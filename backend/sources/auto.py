import requests

def fetch_auto(word):
    # Free dictionary API
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list):
                meanings = data[0].get("meanings", [])
                if meanings:
                    definitions = meanings[0].get("definitions", [])
                    if definitions:
                        return definitions[0].get("definition", "Meaning not found")
    except Exception as e:
        # Ignore for now but could route to app logs
        pass
    return None
