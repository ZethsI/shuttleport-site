import requests
from bs4 import BeautifulSoup
import json

def fetch_istanbulrides_prices(url="https://istanbulrides.com/istanbul-airport-taxi-transfers/"):
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table")
    results = []
    if table:
        rows = table.find_all("tr")[1:]  # başlık hariç satırlar
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:
                hotel = cols[0].get_text(strip=True)
                one_way = cols[1].get_text(strip=True).replace("€", "").replace(",", ".")
                round_trip = cols[2].get_text(strip=True).replace("€", "").replace(",", ".")
                try:
                    one_way = float(one_way)
                except:
                    one_way = None
                try:
                    round_trip = float(round_trip)
                except:
                    round_trip = None
                results.append({
                    "site": "istanbulrides.com",
                    "hotel": hotel,
                    "one_way": one_way,
                    "round_trip": round_trip
                })
    return results

def fetch_safeairporttransfer_prices():
    all_results = []
    for page in range(2, 17):
        url = f"https://istanbul.safeairporttransfer.com/Sabiha-Gokcen-Airport-SAW/transfer-price-list-hotel?page={page}"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        for row in soup.select('.price-row'):
            cells = row.find_all(class_='price-cell')
            if len(cells) >= 4:
                hotel = cells[0].get_text(strip=True)
                prices = [cell.get_text(strip=True).replace('Euro','').replace('€','').replace(',','.').strip() for cell in cells[1:]]
                prices = [float(p) if p.replace('.','',1).isdigit() else None for p in prices]
                all_results.append({
                    "site": "safeairporttransfer.com",
                    "hotel": hotel,
                    "vehicle_type_1": prices[0] if len(prices) > 0 else None,
                    "vehicle_type_2": prices[1] if len(prices) > 1 else None,
                    "vehicle_type_3": prices[2] if len(prices) > 2 else None
                })
    return all_results

def save_prices_to_json(prices, filename="prices.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(prices, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    all_prices = []
    all_prices += fetch_istanbulrides_prices()
    all_prices += fetch_safeairporttransfer_prices()
    save_prices_to_json(all_prices)
    print(f"{len(all_prices)} fiyat kaydı prices.json dosyasına yazıldı.")
