from db import record_evaluation

evaluations = [
    {
        "source_id": 1,
        "named_buyer": "Minera en Argentina (General)",
        "economic_problem": "Necesidad de proveedores para proyectos mineros",
        "hypothesis": "Las empresas mineras argentinas requieren proveedores de servicios e infraestructura.",
        "is_opportunity": False,
        "jules_notes": "Not a specific commercial opportunity, too broad. Indicates a macroeconomic trend rather than an actionable lead."
    },
    {
        "source_id": 2,
        "named_buyer": "Proyecto Vicuña",
        "economic_problem": "Ronda de negocios para proveedores",
        "hypothesis": "El proyecto Vicuña está buscando proveedores locales.",
        "is_opportunity": True,
        "jules_notes": "Actionable: 'ronda de negocios' implies active procurement. A small service provider could attend or contact the organizers."
    },
    {
        "source_id": 3,
        "named_buyer": "Proyecto Vicuña",
        "economic_problem": "Construcción de campamentos",
        "hypothesis": "Existen necesidades de construcción e infraestructura para el proyecto minero Vicuña.",
        "is_opportunity": False,
        "jules_notes": "Too late: Contract already awarded to a Chinese-Santafesina joint venture."
    },
    {
        "source_id": 4,
        "named_buyer": "N/A",
        "economic_problem": "Despliegue de 5G retrasado",
        "hypothesis": "N/A",
        "is_opportunity": False,
        "jules_notes": "Macroeconomic/political news. Irrelevant to target B2B niche."
    },
    {
        "source_id": 5,
        "named_buyer": "Proyectos GNL (YPF/Petronas)",
        "economic_problem": "Licitación de caños para gasoducto",
        "hypothesis": "Se requieren insumos industriales (caños) para proyectos GNL.",
        "is_opportunity": False,
        "jules_notes": "Scale is too large for a small business pilot. Highly competitive international tender."
    },
    {
        "source_id": 6,
        "named_buyer": "Empresas en Vaca Muerta",
        "economic_problem": "Necesidad de radicación en parque industrial para prestar servicios",
        "hypothesis": "El nuevo parque industrial facilita el acceso de proveedores a operadoras de Vaca Muerta.",
        "is_opportunity": True,
        "jules_notes": "Actionable: Establishes a geographic hub. We could target companies setting up in this park for secondary services (e.g., data automation, IT for new offices)."
    },
    {
        "source_id": 7,
        "named_buyer": "N/A",
        "economic_problem": "Regulación de compras estatales",
        "hypothesis": "N/A",
        "is_opportunity": False,
        "jules_notes": "Regulatory news (Ley de Compre Argentino). Not a direct opportunity."
    },
    {
        "source_id": 8,
        "named_buyer": "Ministerio de Defensa",
        "economic_problem": "Provisión al sector aeroespacial",
        "hypothesis": "Existen demandas gubernamentales para el clúster aeroespacial.",
        "is_opportunity": False,
        "jules_notes": "State-level defense procurement is highly bureaucratic and likely out of scope for a quick small pilot."
    }
]

for ev in evaluations:
    record_evaluation(ev['source_id'], ev['named_buyer'], ev['economic_problem'], ev['hypothesis'], ev['is_opportunity'], ev['jules_notes'])

print("Cycle 1 evaluations recorded.")
