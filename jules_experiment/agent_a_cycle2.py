import urllib.parse
import feedparser
from db import record_run, record_source, init_db

def run_cycle_2():
    init_db()
    cycle_name = "Cycle 2"
    query = '"registro de proveedores" OR "convocatoria proveedores" Vaca Muerta OR Salta OR Neuquen'
    print(f"[{cycle_name}] Running discovery for query: '{query}'")
    run_id = record_run(cycle_name, query)

    # Source 1
    encoded_query = urllib.parse.quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=es-419&gl=AR&ceid=AR:es-419"
    feed = feedparser.parse(rss_url)
    s1_added = sum(1 for e in feed.entries if record_source(run_id, e.link, e.title, getattr(e, 'published', ''), getattr(e, 'summary', '')))

    # Source 2 (Government focused)
    q2 = 'site:argentina.gob.ar "registro de proveedores" (mineria OR energia)'
    encoded_q2 = urllib.parse.quote(q2)
    rss_url2 = f"https://news.google.com/rss/search?q={encoded_q2}&hl=es-419&gl=AR&ceid=AR:es-419"
    feed2 = feedparser.parse(rss_url2)
    s2_added = sum(1 for e in feed2.entries if record_source(run_id, e.link, e.title, getattr(e, 'published', ''), getattr(e, 'summary', '')))

    print(f"[{cycle_name}] Discovery complete. Source 1 added: {s1_added}, Source 2 added: {s2_added}")

if __name__ == "__main__":
    run_cycle_2()
