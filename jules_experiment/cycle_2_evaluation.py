from db import record_evaluation

evaluations = [
    {
        "source_id": 9,
        "named_buyer": "Proyectos RIGI (Grandes Inversores)",
        "economic_problem": "Necesidad de proveedores locales (Networking y Rondas de Negocios en Rosario)",
        "hypothesis": "Las grandes empresas bajo el RIGI buscan proveedores locales, lo que representa una oportunidad para ofrecer servicios de BPO o datos.",
        "is_opportunity": True,
        "jules_notes": "Highly actionable. 3300 meetings indicates massive activity. A small business could register for these specific networking events."
    },
    {
        "source_id": 10,
        "named_buyer": "Franquicias en Neuquén (Inversores)",
        "economic_problem": "Demanda de servicios para instalación de nuevas franquicias cerca de Vaca Muerta",
        "hypothesis": "El ecosistema de Vaca Muerta genera demanda secundaria (comercios/franquicias) que requieren servicios de IT/automatización.",
        "is_opportunity": True,
        "jules_notes": "Very interesting niche. B2B services (IT, setup) for franchises entering the Vaca Muerta boom."
    },
    {
        "source_id": 17,
        "named_buyer": "Empresas de Texas (Operadoras)",
        "economic_problem": "Ronda de negocios con más de 150 proveedores locales de Vaca Muerta",
        "hypothesis": "Empresas extranjeras buscan alianzas o contratistas locales en Neuquén.",
        "is_opportunity": True,
        "jules_notes": "Direct B2B opportunity. Shows active procurement matching events."
    },
    {
        "source_id": 22,
        "named_buyer": "Gobierno de Río Negro / Operadoras",
        "economic_problem": "Registro de Proveedores Rionegrinos",
        "hypothesis": "Inscribirse en el registro oficial es el primer paso obligatorio para licitar como proveedor local.",
        "is_opportunity": True,
        "jules_notes": "Extremely actionable. Having a concrete registry to apply to is exactly what a small business needs to enter the supply chain."
    },
    {
        "source_id": 15,
        "named_buyer": "Misión Alemana en Vaca Muerta",
        "economic_problem": "Rondas B2B",
        "hypothesis": "Empresas alemanas buscan socios o proveedores en Neuquén.",
        "is_opportunity": True,
        "jules_notes": "Another direct matching event indicating active B2B demands."
    }
]

for ev in evaluations:
    record_evaluation(ev['source_id'], ev['named_buyer'], ev['economic_problem'], ev['hypothesis'], ev['is_opportunity'], ev['jules_notes'])

print("Cycle 2 evaluations recorded.")
