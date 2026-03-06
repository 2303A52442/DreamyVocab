import sqlite3
import os
import sys
from datetime import date
import sys

if getattr(sys, 'frozen', False):
    # Installed app: write user data to %APPDATA%\PersonalVocabTracker
    # so the install directory (Program Files) never needs write access.
    _app_data = os.environ.get("APPDATA") or os.path.expanduser("~")
    base_dir = os.path.join(_app_data, "PersonalVocabTracker")
    os.makedirs(base_dir, exist_ok=True)
else:
    # Dev/source run: keep db next to the source files
    base_dir = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(base_dir, "vocabulary.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS words (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            word      TEXT    NOT NULL UNIQUE,
            meaning   TEXT    NOT NULL,
            source    TEXT,
            added_on  DATE    DEFAULT (date('now'))
        )
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_word ON words (word)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_added_on ON words (added_on)')
    conn.commit()
    conn.close()

def add_word(word, meaning, source="manual"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        if len(word) > 100 or len(meaning) > 5000:
            return False # Schema logic constraint test
            
        cursor.execute('''
            INSERT INTO words (word, meaning, source, added_on)
            VALUES (?, ?, ?, ?)
        ''', (word.lower(), meaning, source, date.today().isoformat()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_word(word):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT meaning, source FROM words WHERE word = ?', (word.lower(),))
    res = cursor.fetchone()
    conn.close()
    if res:
        return {"meaning": res[0], "source": res[1]}
    return None

def edit_word(word, new_meaning):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE words SET meaning = ? WHERE word = ?', (new_meaning, word.lower()))
    changed = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return changed

def delete_word(word):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM words WHERE word = ?', (word.lower(),))
    changed = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return changed

def count_today():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM words WHERE added_on = ?', (date.today().isoformat(),))
    res = cursor.fetchone()
    conn.close()
    return res[0] if res else 0

def count_total():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM words')
    res = cursor.fetchone()
    conn.close()
    return res[0] if res else 0

def list_words(limit=300):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT word FROM words ORDER BY added_on DESC, id DESC LIMIT ?', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

init_db()
