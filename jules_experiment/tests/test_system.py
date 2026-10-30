import pytest
import sqlite3
import os
import requests
from unittest.mock import patch, MagicMock

# Set test DB before importing db module
os.environ['JULES_DB_PATH'] = 'test_memory.db'

from db import init_db, get_db_path, record_run, record_source, get_unverified_sources, record_verification, get_unevaluated_verified_sources

@pytest.fixture(autouse=True)
def test_db():
    db_path = get_db_path()
    if os.path.exists(db_path):
        os.remove(db_path)
    init_db()
    yield
    if os.path.exists(db_path):
        os.remove(db_path)

def test_db_recording():
    run_id = record_run("Test Cycle", "test query")
    assert run_id == 1

    source_id = record_source(run_id, "http://test.com", "Test Title", "2023-01-01", "Snippet")
    assert source_id == 1

    unverified = get_unverified_sources()
    assert len(unverified) == 1

    record_verification(source_id, "http://test.com/orig", 200, "Full text", True)

    unevaluated = get_unevaluated_verified_sources(run_id)
    assert len(unevaluated) == 1
    assert unevaluated[0][3] == "Full text"

def test_live_connectivity():
    url = "https://news.google.com/rss/search?q=test&hl=es-419&gl=AR&ceid=AR:es-419"
    response = requests.get(url, timeout=10)
    assert response.status_code == 200
    assert "<?xml" in response.text
