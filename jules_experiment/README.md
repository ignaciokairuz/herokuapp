# Jules Opportunity Intelligence Experiment

This repository contains a miniature, autonomous business opportunity intelligence system built and executed entirely within a Google Jules session.

## Architecture

- **Agent A (Discovery)**: `agent_a_discovery.py` - Fetches live data from public RSS feeds using Python, deduplicates URLs, and stores them in SQLite.
- **Agent B & C (Verification & Commercial Evaluation)**: Jules acts as these agents, reading the SQLite database, verifying claims, and writing evaluation scripts (`cycle_1_evaluation.py`, `cycle_2_evaluation.py`) to record structured assessments.
- **Agent D (Learning & Strategy)**: Jules acts as this agent, analyzing Cycle 1 metrics to adapt the search strategy for Cycle 2, documented in `LEARNING.md`.
- **Memory**: `db.py` / `research_memory.db` - Persistent SQLite storage across the session.

## Reproduction Commands

To reproduce this experiment in a standard Linux environment with Python 3:

```bash
# 1. Setup Environment
python3 -m venv venv
source venv/bin/activate
pip install requests beautifulsoup4 pytest feedparser

# 2. Run Tests
export PYTHONPATH=.
pytest tests/test_system.py -v

# 3. Initialize Database
python db.py

# 4. Run Cycle 1
python agent_a_discovery.py "Cycle 1" "licitacion mantenimiento industrial OR mineria proveedores argentina"
python cycle_1_evaluation.py

# 5. Run Cycle 2
python agent_a_discovery.py "Cycle 2" '"ronda de negocios" OR "registro de proveedores" Vaca Muerta OR Salta'
python cycle_2_evaluation.py

# 6. Inspect Results
sqlite3 research_memory.db "SELECT * FROM evaluations INNER JOIN sources ON evaluations.source_id = sources.id;"
```
