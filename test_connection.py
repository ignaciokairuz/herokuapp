import requests

def test_connectivity():
    urls = [
        "https://news.google.com/rss/search?q=licitacion+mantenimiento+industrial+argentina&hl=es-419&gl=AR&ceid=AR:es-419",
        "https://www.boletinoficial.gob.ar/"
    ]
    for url in urls:
        print(f"Testing {url}...")
        try:
            response = requests.get(url, timeout=10)
            print(f"Status Code: {response.status_code}")
            print(f"Content snippet: {response.text[:100]}")
        except Exception as e:
            print(f"Failed: {e}")

if __name__ == "__main__":
    test_connectivity()
