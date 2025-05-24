import requests
from bs4 import BeautifulSoup

def scrape_safeairporttransfer():
    url = "https://safeairporttransfer.com"
    response = requests.get(url)
    if response.status_code != 200:
        print("SafeAirportTransfer sayfasına erişilemedi.")
        return {}

    soup = BeautifulSoup(response.text, 'html.parser')
    prices = {}
    rows = soup.select('table.prices-table tr')
    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) >= 2:
            route = cols[0].text.strip()
            price_text = cols[1].text.strip().replace('€','').replace(',', '.')
            try:
                price = float(price_text)
                prices[route] = price
            except:
                continue
    return prices

def scrape_istanbulelitetransfer():
    url = "https://istanbulelitetransfer.com"
    response = requests.get(url)
    if response.status_code != 200:
        print("IstanbulEliteTransfer sayfasına erişilemedi.")
        return {}

    soup = BeautifulSoup(response.text, 'html.parser')
    prices = {}
    items = soup.select('.price-list li')
    for item in items:
        route_tag = item.select_one('.route')
        price_tag = item.select_one('.price')
        if route_tag and price_tag:
            route = route_tag.text.strip()
            price_text = price_tag.text.strip().replace('€','').replace(',', '.')
            try:
                price = float(price_text)
                prices[route] = price
            except:
                continue
    return prices

def scrape_istanbulrides():
    url = "https://istanbulrides.com"
    response = requests.get(url)
    if response.status_code != 200:
        print("IstanbulRides sayfasına erişilemedi.")
        return {}

    soup = BeautifulSoup(response.text, 'html.parser')
    prices = {}
    rides = soup.select('.ride-item')
    for ride in rides:
        route_tag = ride.select_one('.ride-route')
        price_tag = ride.select_one('.ride-price')
        if route_tag and price_tag:
            route = route_tag.text.strip()
            price_text = price_tag.text.strip().replace('€','').replace(',', '.')
            try:
                price = float(price_text)
                prices[route] = price
            except:
                continue
    return prices

if __name__ == "__main__":
    print("SafeAirportTransfer fiyatları:", scrape_safeairporttransfer())
    print("IstanbulEliteTransfer fiyatları:", scrape_istanbulelitetransfer())
    print("IstanbulRides fiyatları:", scrape_istanbulrides())
