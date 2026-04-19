import requests
import json

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

response = requests.get(
    'https://api.coto.com.ar/api/v1/ms-digital-sitio-bff-web/api/v1/products/categories/catv00000612?key=key_r6xzz4IAoTWcipni&num_results_per_page=24&pre_filter_expression=%7B%22name%22:%22store_availability%22,%22value%22:%22200%22%7D&c=cio-fe-web-coto-3.2.2&i=ce1af638-df8a-4114-a0a9-4c323ee3af76&s=9&origin_referrer=/sitios/cdigi/productos/categorias/catalogo-electro-audio-auriculares/catv00000612',
    headers=headers,
)
print("Status Code:", response.status_code)
if response.status_code == 200:
    data = response.json()
    items = data.get('response', {}).get('results', [])
    for item in items[:1]:
        print(json.dumps(item, indent=2))
