import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# ----------------------------
# Sitelerden En Düşük Fiyatları Çeken Fonksiyonlar
# ----------------------------

def fetch_price_from_safeairporttransfer():
    try:
        url = "https://safeairporttransfer.com"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        price_elements = soup.select(".price .amount")
        prices = [float(p.get_text(strip=True).replace("€", "").replace(",", ".")) for p in price_elements if "€" in p.get_text()]
        return min(prices) if prices else None
    except Exception as e:
        print(f"[ERROR] safeairporttransfer: {e}")
        return None

def fetch_price_from_istanbulelitetransfer():
    try:
        url = "https://istanbulelitetransfer.com"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        price_elements = soup.select(".price")
        prices = [float(p.get_text(strip=True).replace("€", "").replace(",", ".")) for p in price_elements if "€" in p.get_text()]
        return min(prices) if prices else None
    except Exception as e:
        print(f"[ERROR] istanbulelitetransfer: {e}")
        return None

def fetch_price_from_istanbulrides():
    try:
        url = "https://istanbulrides.com"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        price_elements = soup.select(".price-wrapper .price")
        prices = [float(p.get_text(strip=True).replace("€", "").replace(",", ".")) for p in price_elements if "€" in p.get_text()]
        return min(prices) if prices else None
    except Exception as e:
        print(f"[ERROR] istanbulrides: {e}")
        return None

# ----------------------------
# Detaylı Tablo Çeken Fonksiyonlar
# ----------------------------

def fetch_istanbulrides_prices(url="https://istanbulrides.com/istanbul-airport-taxi-transfers/"):
    try:
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
    except Exception as e:
        print(f"[ERROR] fetch_istanbulrides_prices: {e}")
        return []

def fetch_safeairporttransfer_prices():
    all_results = []
    for page in range(2, 17):
        try:
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
        except Exception as e:
            print(f"[ERROR] fetch_safeairporttransfer_prices page {page}: {e}")
    return all_results

# ----------------------------
# Dinamik Fiyat Hesaplama
# ----------------------------

def calculate_dynamic_price(prices_dict):
    valid_prices = [v for v in prices_dict.values() if v is not None]
    if not valid_prices:
        return None
    min_price = min(valid_prices)
    proposed_price = round(min_price - 5, 2)
    minimum_allowed = round(min_price * 0.85, 2)
    if proposed_price < minimum_allowed:
        proposed_price = minimum_allowed
    return proposed_price

# ----------------------------
# JSON Yazma
# ----------------------------

def save_prices_to_json(min_prices, detailed_prices, file_path="prices.json"):
    data = {
        "timestamp": datetime.utcnow().isoformat(),
        "prices": min_prices,
        "dynamic_price": calculate_dynamic_price(min_prices),
        "detailed_prices": detailed_prices
    }
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ----------------------------
# Ana Script
# ----------------------------

def main():
    print("🔍 Web sitelerinden fiyatlar çekiliyor...")
    min_prices = {
        "safeairporttransfer": fetch_price_from_safeairporttransfer(),
        "istanbulelitetransfer": fetch_price_from_istanbulelitetransfer(),
        "istanbulrides": fetch_price_from_istanbulrides()
    }

    print("\n📦 Çekilen fiyatlar:")
    for site, price in min_prices.items():
        print(f"  {site}: {'YOK' if price is None else f'{price} €'}")

    dynamic_price = calculate_dynamic_price(min_prices)
    print("\n💰 Dinamik fiyatımız:", f"{dynamic_price} €" if dynamic_price else "Hesaplanamadı")

    print("\n🔎 Detaylı fiyatlar çekiliyor...")
    detailed_prices = []
    detailed_prices += fetch_istanbulrides_prices()
    detailed_prices += fetch_safeairporttransfer_prices()

    print(f"\n💾 Fiyatlar prices.json dosyasına kaydediliyor... (Toplam kayıt: {len(detailed_prices)})")
    save_prices_to_json(min_prices, detailed_prices)
    print("✅ Kayıt tamamlandı.")

if __name__ == "__main__":
    main()
