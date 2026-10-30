import feedparser
import urllib.parse
from db import record_run, record_source, init_db

def run_discovery(cycle_name, query):
    init_db()

    print(f"[{cycle_name}] Running discovery for query: '{query}'")
    run_id = record_run(cycle_name, query)

    # Constructing Google News RSS query for Argentina
    encoded_query = urllib.parse.quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=es-419&gl=AR&ceid=AR:es-419"

    print(f"Fetching RSS feed: {rss_url}")
    feed = feedparser.parse(rss_url)

    new_sources = 0
    duplicates = 0

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        published = getattr(entry, 'published', 'Unknown date')
        snippet = getattr(entry, 'summary', '')

        # Simple heuristic to clean HTML from snippet if present
        if '<' in snippet and '>' in snippet:
            import re
            snippet = re.sub('<[^<]+>', '', snippet)

        source_id = record_source(run_id, link, title, published, snippet)
        if source_id:
            new_sources += 1
        else:
            duplicates += 1

    print(f"[{cycle_name}] Discovery complete. Added {new_sources} new sources. Found {duplicates} duplicates.")
    return run_id

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        cycle_name = sys.argv[1]
        query = " ".join(sys.argv[2:])
        run_discovery(cycle_name, query)
    else:
        print("Usage: python agent_a_discovery.py <cycle_name> <query>")
