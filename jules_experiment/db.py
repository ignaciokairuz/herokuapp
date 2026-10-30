import sqlite3
import os
from datetime import datetime

def get_db_path():
    return os.environ.get('JULES_DB_PATH', 'research_memory.db')

def init_db():
    conn = sqlite3.connect(get_db_path())
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

    # Add new table for verification
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS verifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id INTEGER UNIQUE,
        original_url TEXT,
        retrieval_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        http_status INTEGER,
        full_text TEXT,
        is_verified BOOLEAN,
        FOREIGN KEY (source_id) REFERENCES sources (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id INTEGER UNIQUE,
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
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute('INSERT INTO research_runs (cycle_name, query) VALUES (?, ?)', (cycle_name, query))
    run_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return run_id

def record_source(run_id, url, title, published_date, content_snippet, status='discovered'):
    conn = sqlite3.connect(get_db_path())
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

def get_unverified_sources():
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, url, title
        FROM sources
        WHERE status = 'discovered'
        AND id NOT IN (SELECT source_id FROM verifications)
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows

def record_verification(source_id, original_url, http_status, full_text, is_verified):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    timestamp = datetime.utcnow().isoformat()
    cursor.execute('''
        INSERT INTO verifications (source_id, original_url, retrieval_timestamp, http_status, full_text, is_verified)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (source_id, original_url, timestamp, http_status, full_text, is_verified))

    # Update source status
    cursor.execute("UPDATE sources SET status = 'verified' WHERE id = ?", (source_id,))
    conn.commit()
    conn.close()

def get_unevaluated_verified_sources(run_id):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.id, s.title, s.content_snippet, v.full_text
        FROM sources s
        JOIN verifications v ON s.id = v.source_id
        WHERE s.run_id = ?
        AND v.is_verified = 1
        AND s.id NOT IN (SELECT source_id FROM evaluations)
    ''', (run_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_source_id_by_title(title_snippet):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM sources WHERE title LIKE ? LIMIT 1", (f"%{title_snippet}%",))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def record_evaluation(source_id, named_buyer, economic_problem, hypothesis, is_opportunity, jules_notes):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO evaluations (source_id, named_buyer, economic_problem, hypothesis, is_opportunity, jules_notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (source_id, named_buyer, economic_problem, hypothesis, is_opportunity, jules_notes))
        conn.commit()
    except sqlite3.IntegrityError:
        pass # Already evaluated
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
