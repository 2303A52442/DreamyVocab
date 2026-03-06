from sources.auto import fetch_auto
from sources.merriam import fetch_merriam
from sources.wiktionary import fetch_wiktionary

def fetch_meaning(word, source="auto"):
    if source == "auto":
        res = fetch_auto(word)
        if res: return res
        
        res = fetch_merriam(word)
        if res: return res
        
        return fetch_wiktionary(word)
        
    elif source == "merriam":
        return fetch_merriam(word)
    elif source == "wiktionary":
        return fetch_wiktionary(word)
        
    return fetch_auto(word) # fallback
