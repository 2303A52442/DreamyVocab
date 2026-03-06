import difflib
import sqlite3
import os
import sys

if getattr(sys, 'frozen', False):
    _app_data = os.environ.get("APPDATA") or os.path.expanduser("~")
    DB_PATH = os.path.join(_app_data, "PersonalVocabTracker", "vocabulary.db")
else:
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vocabulary.db")

def get_suggestions(word, limit=5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # In a real app we might load a bigger dictionary, 
    # but here we suggest from the ones already in the DB
    cursor.execute('SELECT word FROM words')
    words = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    matches = difflib.get_close_matches(word.lower(), words, n=limit, cutoff=0.6)
    return matches
