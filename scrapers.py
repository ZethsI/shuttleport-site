import requests
from bs4 import BeautifulSoup
import json

def scrape_safeairporttransfer():
    url = "https://safeairporttransfer.com"
    response = requests.get(url)
    if response.status_code != 200:
        print("SafeAirportTransfer sayfasına erişilemedi.")
        return {}

    soup = BeautifulSoup(response.text, 'html.parser')

    # Burada sayfanın HTML yapısına göre fiyat ve güzergahları çekmeliyiz
    # Örnek olarak:
    prices = {}

    # Örnek selector — gerçek site incelenmeli:
    route_elements = soup.select('.route-class')  # Hayali class

    for route in route_elements:
        route_name = route.select_one('.route-name-class').text.strip()
        price_text = route.select_one('.price-class').text.strip()
        price = float(price_text.replace('€','').strip())

        prices[route_name] = price

    return prices

def scrape_istanbulelitetransfer():
    url = "https://istanbulelitetransfer.com"
    response = requests.get(url)
    if response.status_code != 200:
        print("IstanbulEliteTransfer sayfasına erişilemedi.")
        return {}

    soup = BeautifulSoup(response.text, 'html.parser')
    prices = {}

    # Site yapısına göre:
    route_elements = soup.select('.price-route')  # Örnek class

    for route in route_elements:
        route_name = route.select_one('.route-name').text.strip()
        price_text = route.select_one('.price').text.strip()
        price = float(price_text.replace('€','').strip())

        prices[route_name] = price

    return prices

def scrape_istanbulrides():
    url = "https://istanbulrides.com"
    response = requests.get(url)
    if response.status_code != 200:
        print("IstanbulRides sayfasına erişilemedi.")
        return {}

    soup = BeautifulSoup(response.text, 'html.parser')
    prices = {}

    # Yine örnek selector
    route_elements = soup.select('.ride-route')

    for route in route_elements:
        route_name = route.select_one('.ride-name').text.strip()
        price_text = route.select_one('.ride-price').text.strip()
        price = float(price_text.replace('€','').strip())

        prices[route_name] = price

    return prices

if __name__ == "__main__":
    safe_prices = scrape_safeairporttransfer()
    elite_prices = scrape_istanbulelitetransfer()
    rides_prices = scrape_istanbulrides()

    print("SafeAirportTransfer:", safe_prices)
    print("IstanbulEliteTransfer:", elite_prices)
    print("IstanbulRides:", rides_prices)
