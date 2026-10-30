from db import record_evaluation, get_source_id_by_title, init_db

init_db()

evaluations = [
    {
        "title_snippet": "Inauguran el Parque Industrial Vaca Muerta",
        "named_buyer": "Empresas en Vaca Muerta",
        "economic_problem": "Necesidad de radicación en parque industrial para prestar servicios",
        "hypothesis": "El nuevo parque industrial facilita el acceso de proveedores a operadoras de Vaca Muerta.",
        "is_opportunity": True,
        "jules_notes": "Actionable: Establishes a geographic hub. We could target companies setting up in this park for secondary services."
    },
    {
        "title_snippet": "Ronda de negocios RIGI - Argentina.gob.ar",
        "named_buyer": "RIGI Investors",
        "economic_problem": "Ronda de negocios oficial (Agenda)",
        "hypothesis": "Official state portal confirming networking event.",
        "is_opportunity": False,  # As requested, classify historical as false
        "jules_notes": "Historical event (October 2026). Too late for current registration."
    },
    {
        "title_snippet": "Vicuña: una empresa china junto a una santafesina",
        "named_buyer": "Proyecto Vicuña",
        "economic_problem": "Construcción de campamentos",
        "hypothesis": "Existen necesidades de construcción e infraestructura para el proyecto minero Vicuña.",
        "is_opportunity": False,
        "jules_notes": "Too late: Contract already awarded."
    },
    {
        "title_snippet": "Registro Federal de Proveedores Mineros",
        "named_buyer": "Operadoras Mineras (General)",
        "economic_problem": "Inscripción obligatoria o recomendada para proveer a mineras.",
        "hypothesis": "Inscribirse en este registro nacional facilita el acceso a compras mineras.",
        "is_opportunity": True,
        "jules_notes": "Actionable: Official active government registry. A direct action item for a small B2B firm."
    }
]

recorded_count = 0
for ev in evaluations:
    source_id = get_source_id_by_title(ev['title_snippet'])
    if source_id:
        record_evaluation(source_id, ev['named_buyer'], ev['economic_problem'], ev['hypothesis'], ev['is_opportunity'], ev['jules_notes'])
        recorded_count += 1
    else:
        print(f"Warning: Could not find source ID for title snippet: {ev['title_snippet']}")

print(f"Cycle 1 evaluations recorded: {recorded_count}")
