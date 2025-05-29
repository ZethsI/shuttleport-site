import json
from datetime import datetime

# Kaynak dosyalar
AIRPORT_DISTANCES_PATH = "airport_hotel_distances.json"
PRICES_JSON_PATH = "prices.json"

# Hedef dosya (overwrite)
PRICES_JSON_OUT = "prices.json"

# 1. Mesafeleri ve orijinal fiyat yapılarını oku
with open(AIRPORT_DISTANCES_PATH, encoding="utf-8") as f:
    distances = json.load(f)
with open(PRICES_JSON_PATH, encoding="utf-8") as f:
    old_data = json.load(f)

airports = old_data["airports"]        # Kısaltma: tam isim
hotels = old_data["hotels"]            # Havalimanı kısaltma: oteller listesi
vehicles = old_data["vehicles"]        # Araç tipleri
base_prices = old_data["basePrices"]   # Araç tiplerine göre base price
km_price = old_data["kmPrice"]         # km başı fiyat
discount = old_data["discount"]        # {"fixedAmount": 5, "minPercent": 0.85}
scraperSources = old_data.get("scraperSources", [])

# 2. Mesafeleri dict biçimine dönüştür
distanceKm = {
    f"{item['airport_code']}-{item['hotel']}": item["distance_km"] for item in distances
}

# 3. Fiyat hesaplama fonksiyonu
def calculate_price(base, km, km_price, discount):
    raw = base + km * km_price
    discounted = max(discount["minPercent"] * raw - discount["fixedAmount"], 15)
    return round(discounted, 2)

# 4. Her kombinasyon için fiyat tablosu oluştur
prices_table = {}
for airport_code, airport_name in airports.items():
    for hotel in hotels[airport_code]:
        combo_key = f"{airport_code}-{hotel}"
        km = distanceKm.get(combo_key, 20)  # 20 km default
        prices_table[combo_key] = {}
        for vehicle in vehicles:
            base = base_prices[vehicle]
            price = calculate_price(base, km, km_price, discount)
            prices_table[combo_key][vehicle] = price

# 5. Tüm verileri yeni prices.json formatında birleştir
out_data = {
    "airports": airports,
    "hotels": hotels,
    "vehicles": vehicles,
    "basePrices": base_prices,
    "distanceKm": distanceKm,
    "kmPrice": km_price,
    "discount": discount,
    "scraperSources": scraperSources,
    "generatedAt": datetime.utcnow().isoformat() + "Z",
    "prices": prices_table
}

with open(PRICES_JSON_OUT, "w", encoding="utf-8") as f:
    json.dump(out_data, f, indent=2, ensure_ascii=False)

print("prices.json başarıyla güncellendi!")
