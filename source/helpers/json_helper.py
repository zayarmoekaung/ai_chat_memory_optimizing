import json

def extract_first_json(text: str) -> dict:
    """Extract the first valid JSON object from any garbage."""
    text = text.strip()
    depth = 0
    start = None
    for i, char in enumerate(text + "}"):   # safety padding
        if char == '{':
            if depth == 0:
                start = i
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0 and start is not None:
                try:
                    return json.loads(text[start:i+1])
                except:
                    continue
    return {}