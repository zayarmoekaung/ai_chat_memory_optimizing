def load_prompt(name): 
    return open(f"prompts/{name}").read()

SYSTEM_PROMPT = load_prompt("system.txt")
DECIDE_PROMPT = load_prompt("decide_action.txt")
FACT_PROMPT = load_prompt("extract_facts.txt")
REFLECT_PROMPT = load_prompt("update_reflection.txt")