import pytest
import sqlite3
import os
import requests
from unittest.mock import patch, MagicMock
from db import init_db, DB_PATH, record_run, record_source, get_unevaluated_sources
from agent_a_discovery import run_discovery

@pytest.fixture
def test_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db()
    yield
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

def test_db_recording(test_db):
    run_id = record_run("Test Cycle", "test query")
    assert run_id == 1

    source_id = record_source(run_id, "http://test.com", "Test Title", "2023-01-01", "Snippet")
    assert source_id == 1

    # Test duplicate URL
    source_id_dup = record_source(run_id, "http://test.com", "Title 2", "2023-01-02", "Snippet 2")
    assert source_id_dup is None

    sources = get_unevaluated_sources(run_id)
    assert len(sources) == 1
    assert sources[0][1] == "http://test.com"

@patch("agent_a_discovery.feedparser.parse")
def test_agent_a_discovery(mock_parse, test_db):
    mock_feed = MagicMock()
    mock_entry1 = MagicMock()
    mock_entry1.title = "Licitacion 1"
    mock_entry1.link = "http://licitacion1.com"
    mock_entry1.published = "2023-10-01"
    mock_entry1.summary = "Se busca proveedor"

    mock_entry2 = MagicMock()
    mock_entry2.title = "Licitacion 2"
    mock_entry2.link = "http://licitacion2.com"
    mock_entry2.published = "2023-10-02"
    mock_entry2.summary = "<b>Mantenimiento industrial</b>"

    mock_feed.entries = [mock_entry1, mock_entry2]
    mock_parse.return_value = mock_feed

    run_id = run_discovery("Test Cycle", "mantenimiento")
    sources = get_unevaluated_sources(run_id)
    assert len(sources) == 2
    assert sources[1][3] == "Mantenimiento industrial"  # HTML stripped

def test_live_connectivity():
    url = "https://news.google.com/rss/search?q=test&hl=es-419&gl=AR&ceid=AR:es-419"
    response = requests.get(url, timeout=10)
    assert response.status_code == 200
    assert "<?xml" in response.text
