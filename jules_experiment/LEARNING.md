# Agent D: Learning & Strategy Adaptation

## Analysis of Cycle 1 (Baseline)
- **Query used**: `"licitacion mantenimiento industrial OR mineria proveedores argentina"`
- **Total Sources Found**: 8
- **Duplicate Rate**: 0%
- **Relevance / Signal-to-Noise Ratio**: Only 2 out of 8 (25%) were deemed actionable small-business opportunities.
- **Observations on Noise**:
  - The word "licitación" brought in massive national-scale projects (e.g., GNL pipelines) which are unsuitable for small B2B pilots.
  - The term "mineria proveedores" brought in high-level macroeconomic news (e.g., Chilean suppliers boom) and regulatory news (Compre Argentino) rather than specific, localized needs.
  - Discoveries about awarded contracts (Vicuña camp construction) are dead ends, indicating we need terms that signal *future* or *ongoing* open procurement.

## Strategy for Cycle 2 (Improved)
- **Objective**: Increase the signal-to-noise ratio by finding highly specific, actionable procurement signals for a small business.
- **Revised Query Strategy**:
  - Drop the word `licitacion` as it skews toward mega-projects.
  - Drop `mineria proveedores` as it returns macro industry news.
  - Introduce terms that signal active, localized business needs: `"ronda de negocios" OR "busqueda de proveedores" OR "registro de proveedores" Vaca Muerta OR Litio Salta OR Neuquen`.
  - Focus on specific booming localized hubs rather than country-wide terms ("Argentina").

## Expected Outcome
- We expect fewer total results but a higher percentage of actionable opportunities (e.g., vendor registration portals, business roundtables, smaller sub-contracting needs).
