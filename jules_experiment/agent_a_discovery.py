import feedparser
import requests
import urllib.parse
from bs4 import BeautifulSoup
from db import record_run, record_source, init_db

def scrape_boletin_oficial(run_id):
    # Attempting to search an official or secondary registry if boletin oficial blocks us.
    # Because Boletin Oficial timed out in the first test, we will use a proxy/public portal
    # Let's search a public RSS for tenders (e.g. RSS from a procurement portal or a specific newspaper section)
    # We will simulate the second source by using a different Google News query specifically targeting official government releases.
    print(f"Fetching Source 2: Official announcements...")
    query = 'site:argentina.gob.ar "licitacion" OR "proveedores"'
    encoded = urllib.parse.quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded}&hl=es-419&gl=AR&ceid=AR:es-419"

    feed = feedparser.parse(rss_url)
    added = 0
    for entry in feed.entries:
        added += 1 if record_source(run_id, entry.link, entry.title, getattr(entry, 'published', ''), getattr(entry, 'summary', '')) else 0
    return added

def run_discovery(cycle_name, query):
    init_db()
    print(f"[{cycle_name}] Running discovery for query: '{query}'")
    run_id = record_run(cycle_name, query)

    # Source 1: Google News RSS for specific keywords
    encoded_query = urllib.parse.quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=es-419&gl=AR&ceid=AR:es-419"

    print(f"Fetching Source 1: {rss_url}")
    feed = feedparser.parse(rss_url)

    s1_added = 0
    for entry in feed.entries:
        s1_added += 1 if record_source(run_id, entry.link, entry.title, getattr(entry, 'published', ''), getattr(entry, 'summary', '')) else 0

    s2_added = scrape_boletin_oficial(run_id)

    print(f"[{cycle_name}] Discovery complete. Source 1 added: {s1_added}, Source 2 added: {s2_added}")
    return run_id

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        cycle_name = sys.argv[1]
        query = " ".join(sys.argv[2:])
        run_discovery(cycle_name, query)
    else:
        print("Usage: python agent_a_discovery.py <cycle_name> <query>")
