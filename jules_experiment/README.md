# Jules Opportunity Intelligence Experiment

This repository contains a miniature, autonomous business opportunity intelligence system built and executed entirely within a Google Jules session.

## Architecture

- **Agent A (Discovery)**: `agent_a_discovery.py` & `agent_a_cycle2.py` - Fetches live data from two independent RSS feeds, deduplicates URLs, and stores them in SQLite.
- **Agent B (Verification)**: `agent_b_verification.py` - Visits original URLs, scrapes full text, checks HTTP status, and updates the database.
- **Agents C & D (Evaluation & Learning)**: Jules acts as these agents, reading the DB, writing evaluation scripts (`cycle_1_evaluation.py`, `cycle_2_evaluation.py`), and adapting strategies (`LEARNING.md`).
- **Memory**: `db.py` / `research_memory.db` - Persistent SQLite storage.

## Reproduction Commands

To reproduce this experiment in a standard Linux environment:

```bash
# 1. Setup Environment
python3 -m venv venv
source venv/bin/activate
pip install requests beautifulsoup4 pytest feedparser

# 2. Run Tests (Uses isolated test_memory.db)
export PYTHONPATH=.
pytest tests/test_system.py -v

# 3. Inspect the Production Database
sqlite3 research_memory.db "SELECT s.title, v.full_text, e.is_opportunity FROM sources s JOIN verifications v ON s.id = v.source_id LEFT JOIN evaluations e ON s.id = e.source_id LIMIT 10;"
```
