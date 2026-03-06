import sys
import json
import os

# Suppress stderr to prevent breaking the Java-side JSON parser
sys.stderr = open(os.devnull, 'w')

# Force stdout to be unbuffered so responses reach Java immediately.
# When spawned as a subprocess with stdout=PIPE (as Java does), Python
# switches to block-buffered mode and sys.stdout.flush() may not reach
# the OS pipe in a frozen PyInstaller exe. os.write(1,...) writes directly
# to file descriptor 1, bypassing all Python buffering.
def _write_stdout(data: str):
    os.write(1, (data + "\n").encode("utf-8"))

import db
import suggestions
import fetcher


def process_request(req):
    action = req.get("action")
    word = req.get("word", "")
    
    if action == "lookup":
        # Check local DB
        local_res = db.get_word(word)
        if local_res:
            return {
                "status": "found",
                "word": word,
                "meaning": local_res["meaning"],
                "source": "local",
                "suggestions": []
            }
            
        # Try fetching
        source_pref = req.get("source", "auto")
        fetched_meaning = fetcher.fetch_meaning(word, source_pref)
        if fetched_meaning:
            db.add_word(word, fetched_meaning, "dictionary_api")
            return {
                "status": "fetched",
                "word": word,
                "meaning": fetched_meaning,
                "source": "dictionary_api",
                "suggestions": []
            }
            
        # Suggestions fallback
        sugs = suggestions.get_suggestions(word)
        if sugs:
            return {
                "status": "suggestions",
                "word": word,
                "meaning": "",
                "source": "",
                "suggestions": sugs
            }
            
        return {
            "status": "not_found",
            "word": word,
            "meaning": "",
            "source": "",
            "suggestions": []
        }
        
    elif action == "add":
        meaning = req.get("meaning", "")
        success = db.add_word(word, meaning)
        return {"status": "success" if success else "error"}
        
    elif action == "edit":
        meaning = req.get("meaning", "")
        success = db.edit_word(word, meaning)
        return {"status": "success" if success else "error"}
        
    elif action == "delete":
        success = db.delete_word(word)
        return {"status": "success" if success else "error"}
        
    elif action == "stats":
        today = db.count_today()
        total = db.count_total()
        return {
            "status": "success",
            "today": today,
            "total": total
        }

    elif action == "list_words":
        words = db.list_words()
        return {"status": "success", "words": words}
        
    return {"status": "error", "message": f"Unknown action: {action}"}

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = process_request(req)
        except Exception as e:
            resp = {"status": "error", "message": str(e)}
            
        _write_stdout(json.dumps(resp))

if __name__ == "__main__":
    main()
