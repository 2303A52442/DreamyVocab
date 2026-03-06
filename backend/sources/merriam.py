import requests
from bs4 import BeautifulSoup

def fetch_merriam(word):
    url = f"https://www.merriam-webster.com/dictionary/{word}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Look for the first meaning definition text
            def_elem = soup.find('span', class_='dtText')
            if def_elem:
                return def_elem.get_text().strip(': ')
    except Exception:
        pass
    return None
