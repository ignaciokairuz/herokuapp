import requests
from bs4 import BeautifulSoup
from db import get_unverified_sources, record_verification, init_db
import re

def verify_sources():
    init_db()
    sources = get_unverified_sources()
    print(f"Agent B: Found {len(sources)} unverified sources.")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    for source_id, url, title in sources:
        try:
            # Google news URLs redirect, so we need to follow them to get the real content
            print(f"Verifying {title[:50]}...")
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            status = response.status_code
            original_url = response.url

            if status == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Extract main paragraphs
                paragraphs = soup.find_all('p')
                full_text = " ".join([p.get_text().strip() for p in paragraphs if len(p.get_text()) > 20])
                # Clean up multiple spaces
                full_text = re.sub(r'\s+', ' ', full_text)[:2000] # store up to 2000 chars for context
                record_verification(source_id, original_url, status, full_text, is_verified=True)
            else:
                record_verification(source_id, original_url, status, "HTTP Error", is_verified=False)

        except Exception as e:
            print(f"Failed to verify {url}: {e}")
            record_verification(source_id, url, 0, str(e), is_verified=False)

if __name__ == "__main__":
    verify_sources()
