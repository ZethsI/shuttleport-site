import requests
from bs4 import BeautifulSoup
import re

def check_page_structure(url, selectors):
    """
    Verilen URL'deki sayfanın belirtilen CSS selector'larına göre
    eleman bulup bulamadığını kontrol eder.
    selectors: dict -> {'name': 'css_selector'}
    Eğer hiçbir selector sonuç vermezse False döner, yoksa True.
    """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"[ERROR] {url} sayfasına erişilemedi, durum kodu: {response.status_code}")
            return False
        soup = BeautifulSoup(response.text, 'html.parser')

        for name, selector in selectors.items():
            elems = soup.select(selector)
            if elems:
                print(f"[OK] {name} için element bulundu.")
                return True

        print(f"[WARNING] {url} sayfasında belirtilen selector'lar bulunamadı!")
        return False
    except Exception as e:
        print(f"[ERROR] {url} sayfası kontrolünde hata: {e}")
        return False


def scrape_safeairporttransfer():
    """
    safeairporttransfer.com sitesinden güzergah isimleri ve fiyatları çeker.
    Güzergahlar ana sayfadaki 'airport-transfer' içeren linklerde ve fiyatları
    yanındaki span içinde yer alır.
    """
    url = "https://safeairporttransfer.com"
    selectors = {
        'route_links': 'a[href*="airport-transfer"]',
        'price_spans': 'a[href*="airport-transfer"] span',
    }
    if not check_page_structure(url, selectors):
        print("[SKIP] SafeAirportTransfer scraper atlandı.")
        return {}

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = {}

        # Güzergah linkleri ve fiyatlar birlikte listeleniyor, parse edelim
        links = soup.select('a[href*="airport-transfer"]')
        for link in links:
            route_name = link.get_text(strip=True)
            price_span = link.find('span')
            price_text = price_span.get_text(strip=True) if price_span else None

            if price_text:
                match = re.search(r'(\d+)', price_text)
                price = int(match.group(1)) if match else None
                if price and route_name:
                    data[route_name] = price

        return data

    except Exception as e:
        print(f"[ERROR] SafeAirportTransfer scraping hatası: {e}")
        return {}


def scrape_istanbulelitetransfer():
    """
    istanbulelitetransfer.com sitesinden güzergah ve fiyat bilgilerini çeker.
    Site yapısında fiyatlar '.price' class'ında, güzergahlar ise hemen üstündeki
    başlıklarda ('h3' veya 'h2') yer alıyor.
    """
    url = "https://istanbulelitetransfer.com"
    selectors = {
        'price_elements': '.price',
    }
    if not check_page_structure(url, selectors):
        print("[SKIP] IstanbulEliteTransfer scraper atlandı.")
        return {}

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = {}

        price_elements = soup.select('.price')
        for elem in price_elements:
            # Fiyatın üstündeki başlığı alalım (güzergah adı)
            header = elem.find_previous(['h2', 'h3'])
            route_name = header.get_text(strip=True) if header else None

            price_text = elem.get_text(strip=True)
            match = re.search(r'(\d+)', price_text)
            price = int(match.group(1)) if match else None

            if price and route_name:
                data[route_name] = price

        return data

    except Exception as e:
        print(f"[ERROR] IstanbulEliteTransfer scraping hatası: {e}")
        return {}


def scrape_istanbulrides():
    """
    istanbulrides.com sitesinden güzergah ve fiyat bilgilerini çeker.
    Güzergahlar 'h3' etiketlerinde, fiyatlar ise '.transfer-price' class'ında.
    """
    url = "https://istanbulrides.com"
    selectors = {
        'price_elements': '.transfer-price',
    }
    if not check_page_structure(url, selectors):
        print("[SKIP] IstanbulRides scraper atlandı.")
        return {}

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = {}

        price_elements = soup.select('.transfer-price')
        for elem in price_elements:
            header = elem.find_previous('h3')
            route_name = header.get_text(strip=True) if header else None

            price_text = elem.get_text(strip=True)
            match = re.search(r'(\d+)', price_text)
            price = int(match.group(1)) if match else None

            if price and route_name:
                data[route_name] = price

        return data

    except Exception as e:
        print(f"[ERROR] IstanbulRides scraping hatası: {e}")
        return {}


def scrape_all():
    print("Starting scraping all sites...")

    safe_prices = scrape_safeairporttransfer()
    elite_prices = scrape_istanbulelitetransfer()
    rides_prices = scrape_istanbulrides()

    print("Scraping finished.")
    return {
        "safeairporttransfer": safe_prices,
        "istanbulelitetransfer": elite_prices,
        "istanbulrides": rides_prices
    }


if __name__ == "__main__":
    all_prices = scrape_all()
    print(all_prices)
