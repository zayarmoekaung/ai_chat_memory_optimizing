import requests

KOBOLD_URL = "http://192.168.1.9:5001/api/v1/generate"

def kobold(prompt, stop=None, temp=0.8, max_tokens=400):
    if stop is None: stop = []
    payload = {
        "prompt": prompt,
        "temperature": temp,
        "max_length": max_tokens,
        "stop_sequence": stop
    }
    try:
        r = requests.post(KOBOLD_URL, json=payload, timeout=180)
        return r.json()["results"][0]["text"].strip()
    except:
        return ""