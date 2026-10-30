from db import record_evaluation, get_source_id_by_title, init_db

init_db()

evaluations = [
    {
        "title_snippet": "VMOS abrió el registro de proveedores para la operación del nuevo oleoducto",
        "named_buyer": "VMOS (Vaca Muerta Oil Sur)",
        "economic_problem": "Buscan proveedores para la operación del nuevo oleoducto.",
        "hypothesis": "Empresa privada abriendo padrón de proveedores específicos.",
        "is_opportunity": True,
        "jules_notes": "Extremely actionable. A private operator explicitly seeking vendors."
    }
]

for ev in evaluations:
    source_id = get_source_id_by_title(ev['title_snippet'])
    if source_id:
        record_evaluation(source_id, ev['named_buyer'], ev['economic_problem'], ev['hypothesis'], ev['is_opportunity'], ev['jules_notes'])
