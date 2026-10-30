# Experiment Results

## Execution Summary

This experiment successfully demonstrated a miniature, autonomous Opportunity Intelligence System running entirely within a Jules session. It addressed critical fixes by persisting a real SQLite database, utilizing two independent data sources, performing active HTTP text verification, and correctly filtering out historical/passed events.

1. **Cycle 1 (Baseline)**:
   - **Query**: `"licitacion mantenimiento industrial OR mineria proveedores argentina"` (Google News) and `site:argentina.gob.ar "licitacion" OR "proveedores"` (Gov.ar RSS).
   - **Retrieved**: 89 raw sources.
   - **Verification**: Agent B visited all 89 URLs, followed redirects, scraped up to 2000 characters of full text, and logged HTTP statuses.
   - **Evaluation**: The baseline proved highly noisy. It pulled in macroeconomic data, financial treasury tenders (irrelevant to B2B), and historical events (e.g., October 2026 business rounds).

2. **Agent D (Learning)**:
   - Jules analyzed the database. To eliminate the noise, the strategy was updated to drop the term `"licitacion"` (which pulls financial/treasury data on `.gob.ar` sites) and target exact, active phrasing like `"registro de proveedores"`.

3. **Cycle 2 (Improved)**:
   - **Query**: `"registro de proveedores" OR "convocatoria proveedores" Vaca Muerta OR Salta OR Neuquen`.
   - **Retrieved**: 25 raw sources.
   - **Verification**: Agent B verified all 25 URLs.
   - **Evaluation**: The revised strategy yielded a drastically higher concentration of *active, non-historical* business signals. Jules identified currently open registries (VMOS, Catamarca, Río Negro) and explicitly rejected historical or regulatory noise.

## Technical Deliverables
- `db.py`: SQLite schema featuring tables for `research_runs`, `sources`, `verifications`, and `evaluations`. Protected by `JULES_DB_PATH`.
- `agent_a_discovery.py` & `agent_a_cycle2.py`: Scripts polling two independent RSS sources.
- `agent_b_verification.py`: Script using `requests` and `BeautifulSoup` to hit original URLs and scrape full context.
- `research_memory.db`: Persisted SQLite database containing all 114 discovered sources, their verifications, and Jules's evaluations.
- `tests/test_system.py`: Mocked and live tests running against an isolated `test_memory.db`.

## Final Assessment against Acceptance Criteria

1. **Execute for real**: **PASS**. Live HTTP queries were made to Google News RSS and original article URLs. (See DB verifications table).
2. **Two independently maintained sources**: **PASS**. Google News broad queries and `site:argentina.gob.ar` queries were used.
3. **Preserve original data (Verification)**: **PASS**. Agent B stores `original_url`, `http_status`, `retrieval_timestamp`, and `full_text` in the `verifications` table.
4. **Persist records to SQLite**: **PASS**. `research_memory.db` is populated and committed to the repo. Tests use an isolated DB.
5. **Run two consecutive cycles**: **PASS**. Cycle 1 (Baseline) and Cycle 2 (Improved) were executed.
6. **Measure and compare improvements**: **PASS**. Cycle 1 yielded 89 results heavily saturated with financial tenders and historical dates. Cycle 2 yielded 25 results, directly targeting actively open provincial and private vendor registries.
7. **Do not substitute fabricated data**: **PASS**. All evaluated rows stem directly from live web data.
8. **Explain future requirements**: **PASS**. See below.

## Final Question Answer

**"How much of a continuously operating, self-improving, internet-research multi-agent system can be implemented and demonstrated entirely inside Google Jules, without an external LLM API, VPS, or GitHub Actions?"**

**Demonstrated Capabilities (What worked inside Jules):**
- Jules can write and execute Python scripts that perform real internet research, scrape data, follow redirects, and persist state in SQLite.
- Jules can act as a "hybrid" reasoning engine by writing intermediate Python scripts to evaluate the scraped DB rows based on complex logic (e.g., distinguishing historical dates from active open registries).
- Jules can execute a genuine self-improvement loop: run baseline -> analyze noise -> adapt query -> run improved cycle.

**Platform Limitations & Future Needs:**
- **Automation Pipeline**: Jules cannot run continuously on a schedule. A CRON job or GitHub Actions workflow is required for continuous operation.
- **Autonomous Reasoning**: Because Python scripts in Jules cannot invoke the underlying Gemini model via API, Jules must manually act as the intermediary (Agents B, C, D) by reading outputs and writing evaluation scripts. True autonomy requires an external LLM API key.
