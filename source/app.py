# app.py
from flask import Flask, render_template, jsonify
import json, datetime, threading, time, os
from sentence_transformers import SentenceTransformer
from database.db import db_connect, db_init
from agents.kobold import kobold
import numpy as np
import re
from prompts import SYSTEM_PROMPT, DECIDE_PROMPT, FACT_PROMPT, REFLECT_PROMPT

from helpers import extract_first_json
app = Flask(__name__)
DB = "world.db"
KOBOLD_URL = "http://192.168.1.9:5001/api/v1/generate"
MODEL = SentenceTransformer('all-MiniLM-L6-v2')  

conn = db_connect(DB)
c = db_init(conn)

# === INITIAL CHARACTERS (create if not exist) ===
def ensure_character(name, base_personality):
    if not c.execute("SELECT 1 FROM reflections WHERE character=?", (name,)).fetchone():
        reflection = f"{name} is a new inhabitant of the village. {base_personality}"
        c.execute("INSERT INTO reflections (character, reflection, last_updated_turn) VALUES (?,?,?)",
                  (name, reflection, 0))
        conn.commit()

ensure_character("Alice", "She is a curious 24-year-old adventurer who loves exploring.")
ensure_character("Bob", "He is a 35-year-old grumpy but kind-hearted blacksmith.")
ensure_character("Lira", "She is a mysterious elven merchant who arrived recently.")


def embed(text):
    return MODEL.encode(text)

def save_fact(character, fact, importance=7.0, turn=None):
    emb = embed(fact)
    c.execute("INSERT INTO facts (character, fact, importance, embedding, turn) VALUES (?,?,?,?,?)",
              (character, fact, importance, emb.tobytes(), turn or current_turn()))
    conn.commit()

def get_relevant_facts(character, query, top_k=10):
    q_emb = embed(query)
    c.execute("SELECT fact FROM facts WHERE character=?", (character,))
    rows = c.fetchall()
    if not rows: return ""
    facts = [r[0] for r in rows]
    embs = [np.frombuffer(c.execute("SELECT embedding FROM facts WHERE fact=?", (f,)).fetchone()[0], dtype=np.float32) for f in facts]
    scores = [np.dot(q_emb, e) for e in embs]
    top_idx = np.argsort(scores)[-top_k:][::-1]
    return "\n".join(f"- {facts[i]}" for i in top_idx)

def current_turn():
    c.execute("SELECT MAX(turn) FROM events")
    return c.fetchone()[0] or 0

# === CORE WORLD LOOP ===
world_running = True

def world_loop():
    global world_running
    turn = current_turn() + 1

    while world_running:
        print(f"\n{'='*20} TURN {turn} {'='*20}")

        # Load characters once per turn
        characters = c.execute("SELECT character, reflection FROM reflections").fetchall()

        for name, reflection in characters:
            # ── Recent events (chronological) ──
            rows = c.execute(
                "SELECT narration FROM events ORDER BY id DESC LIMIT 20"
            ).fetchall()
            recent_lines = [row[0] for row in reversed(rows) if row[0]]
            recent = "Recent events:\n" + "\n".join(recent_lines) if recent_lines else ""

            # ── Relevant permanent facts ──
            facts = get_relevant_facts(
                name,
                f"{name}'s current goals, relationships, possessions and key memories",
                top_k=10
            )
            facts_block = ("Important facts you must never forget:\n" + facts) if facts else ""

            # ── Build final prompt using your external files ──
            prompt = SYSTEM_PROMPT.format(
                name=name,
                reflection=reflection.strip(),
                facts=facts_block,
                recent=recent or "The world has just begun."
            ) + "\n\n" + DECIDE_PROMPT.format(name=name) + "\n\nJSON:"   # ← this line is magic

            raw = kobold(prompt, max_tokens=450, temp=0.82)

            print(f"{name} → {raw.replace(chr(10), ' ').replace('  ', ' ')[:140]}")

            # ── Ultra-robust JSON extraction ──
            data = extract_first_json(raw)
            if not data or "narration" not in data:
                data = {"narration": f"{name} pauses, lost in thought."}

            narration = data["narration"].strip()
            print(f"   → {narration}")

            # ── Save event ──
            c.execute(
                """INSERT INTO events (turn, character, narration, data, timestamp)
                   VALUES (?,?,?,?,?)""",
                (turn, name, narration, json.dumps(data), datetime.datetime.now().isoformat())
            )
            conn.commit()

            # ── Memory maintenance (still uses your external prompt files) ──
            if turn % 15 == 0:                                          # Fact extraction
                fact_prompt = FACT_PROMPT.format(
                    name=name,
                    narration=narration,
                    recent=recent or "none"
                )
                facts_text = kobold(fact_prompt, temp=0.2, max_tokens=200)
                for line in facts_text.split("\n"):
                    line = line.strip(" -*•·[]0123456789.")
                    if len(line) > 15:
                        save_fact(name, line.capitalize(), turn=turn)

            if turn % 150 == 0:                                         # Reflection update
                reflect_prompt = REFLECT_PROMPT.format(
                    name=name,
                    reflection=reflection
                )
                new_ref = kobold(reflect_prompt, temp=0.7, max_tokens=350).strip()
                if new_ref and len(new_ref) > 60:
                    c.execute(
                        "UPDATE reflections SET reflection=?, last_updated_turn=? WHERE character=?",
                        (new_ref, turn, name)
                    )
                    conn.commit()
                    print(f"   Reflection updated for {name}")

        turn += 1
        time.sleep(6)        # ~6–10 sec per turn feels perfect
# === ROUTES ===
@app.route("/")
def index():
    events = c.execute("SELECT * FROM events ORDER BY id DESC LIMIT 100").fetchall()
    chars = c.execute("SELECT character, reflection FROM reflections").fetchall()
    turn = current_turn()
    return render_template("index.html", events=reversed(events), chars=chars, turn=turn)

@app.route("/api/events")
def api_events():
    events = c.execute("SELECT * FROM events ORDER BY id DESC LIMIT 50").fetchall()
    return jsonify([{
        "turn": e[1], "character": e[2], "narration": e[3], "time": e[5]
    } for e in events])

# === START WORLD THREAD ===
threading.Thread(target=world_loop, daemon=True).start()

if __name__ == "__main__":
    print("World starting... Open http://127.0.0.1:5000")
    app.run(debug=False, port=5000)