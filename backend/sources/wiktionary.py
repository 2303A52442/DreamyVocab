import requests

def fetch_wiktionary(word):
    url = f"https://en.wiktionary.org/api/rest_v1/page/definition/{word}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "en" in data and len(data["en"]) > 0:
                # Get the first definition of the first part of speech
                definitions = data["en"][0].get("definitions", [])
                if definitions:
                    # Wiktionary definitions can contain HTML, we should strip it or keep it simple
                    import re
                    raw_def = definitions[0].get("definition", "")
                    clean_def = re.sub('<[^<]+>', '', raw_def)
                    return clean_def
    except Exception:
        pass
    return None
