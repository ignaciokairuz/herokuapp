import sqlite3
import os

DB_PATH = 'research_memory.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS research_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cycle_name TEXT,
        query TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_id INTEGER,
        url TEXT UNIQUE,
        title TEXT,
        published_date TEXT,
        content_snippet TEXT,
        status TEXT,
        FOREIGN KEY (run_id) REFERENCES research_runs (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id INTEGER,
        named_buyer TEXT,
        economic_problem TEXT,
        hypothesis TEXT,
        is_opportunity BOOLEAN,
        jules_notes TEXT,
        FOREIGN KEY (source_id) REFERENCES sources (id)
    )
    ''')

    conn.commit()
    conn.close()

def record_run(cycle_name, query):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO research_runs (cycle_name, query) VALUES (?, ?)', (cycle_name, query))
    run_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return run_id

def record_source(run_id, url, title, published_date, content_snippet, status='extracted'):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO sources (run_id, url, title, published_date, content_snippet, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (run_id, url, title, published_date, content_snippet, status))
        source_id = cursor.lastrowid
        conn.commit()
    except sqlite3.IntegrityError:
        # Duplicate URL
        source_id = None
    finally:
        conn.close()
    return source_id

def get_unevaluated_sources(run_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, url, title, content_snippet
        FROM sources
        WHERE run_id = ?
        AND id NOT IN (SELECT source_id FROM evaluations)
    ''', (run_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def record_evaluation(source_id, named_buyer, economic_problem, hypothesis, is_opportunity, jules_notes):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO evaluations (source_id, named_buyer, economic_problem, hypothesis, is_opportunity, jules_notes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (source_id, named_buyer, economic_problem, hypothesis, is_opportunity, jules_notes))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
