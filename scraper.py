import requests
import sqlite3
from datetime import datetime

DB_NAME = "coto_prices.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            product_name TEXT,
            sku TEXT,
            list_price REAL,
            discount_price REAL
        )
    ''')
    conn.commit()
    conn.close()

def scrape_coto():
    print(f"Scraping Coto at {datetime.now()}")
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9,es;q=0.8,pt;q=0.7,pl;q=0.6,es-AR;q=0.5',
        'Connection': 'keep-alive',
        'Origin': 'https://www.cotodigital.com.ar',
        'Referer': 'https://www.cotodigital.com.ar/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36 Edg/147.0.0.0',
        'sec-ch-ua': '"Microsoft Edge";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    try:
        response = requests.get(
            'https://api.coto.com.ar/api/v1/ms-digital-sitio-bff-web/api/v1/products/categories/catv00000612?key=key_r6xzz4IAoTWcipni&num_results_per_page=24&pre_filter_expression=%7B%22name%22:%22store_availability%22,%22value%22:%22200%22%7D&c=cio-fe-web-coto-3.2.2&i=ce1af638-df8a-4114-a0a9-4c323ee3af76&s=9&origin_referrer=/sitios/cdigi/productos/categorias/catalogo-electro-audio-auriculares/catv00000612',
            headers=headers,
        )
        if response.status_code == 200:
            data = response.json()
            items = data.get('response', {}).get('results', [])

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Scrape up to 5 items to keep the chart clean
            for item in items[:5]:
                product = item.get('data', {})
                name = product.get('sku_display_name')
                sku = product.get('sku_id')
                list_price = product.get('product_list_price')

                discount_price = list_price
                discounts = product.get('discounts', [])
                if discounts:
                    try:
                        # Extract number from '$18899.30'
                        discount_str = discounts[0].get('discountPrice', '').replace('$', '')
                        if discount_str:
                            discount_price = float(discount_str)
                    except ValueError:
                        pass

                if name and list_price is not None:
                    cursor.execute(
                        "INSERT INTO prices (timestamp, product_name, sku, list_price, discount_price) VALUES (?, ?, ?, ?, ?)",
                        (now, name, sku, list_price, discount_price)
                    )
            conn.commit()
            conn.close()
            print("Successfully scraped and saved.")
        else:
            print(f"Failed to fetch data: {response.status_code}")
    except Exception as e:
        print(f"Scraper error: {e}")

if __name__ == "__main__":
    init_db()
    scrape_coto()
