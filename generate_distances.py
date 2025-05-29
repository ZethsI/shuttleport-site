import requests
import time
import json

import os

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
if not API_KEY:
    raise Exception("GOOGLE_MAPS_API_KEY ortam değişkeni tanımlı değil!")
    
API_KEY = "GOOGLE_MAPS_API_KEY"  # Buraya kendi güvenli Maps API anahtarını yaz!

prices_json_path = 'prices.json'
output_json_path = 'airport_hotel_distances.json'

# prices.json'dan havalimanı ve otel listesini oku
with open(prices_json_path, encoding='utf-8') as f:
    data = json.load(f)

airports = data['airports']      # {'IST': ..., 'SAW': ..., ...}
hotels = data['hotels']          # {'IST': [otel1, otel2, ...], ...}

results = []

def get_distance_km(origin, destination, api_key):
    url = (
        f"https://maps.googleapis.com/maps/api/directions/json"
        f"?origin={origin}&destination={destination}&key={api_key}"
    )
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        distance_m = data['routes'][0]['legs'][0]['distance']['value']
        return round(distance_m / 1000, 2)  # km cinsinden
    except Exception as e:
        print(f"Distance not found: {origin} -> {destination} ({e})")
        return None

for airport_code, airport_name in airports.items():
    for hotel in hotels[airport_code]:
        origin = airport_name
        destination = hotel + " Hotel"  # Çoğu otel adı için "Hotel" uzantısı eklemek daha doğru sonuç verebilir, istersen kaldırabilirsin.
        km = get_distance_km(origin, destination, API_KEY)
        results.append({
            "airport_code": airport_code,
            "airport": airport_name,
            "hotel": hotel,
            "distance_km": km
        })
        print(f"{airport_code} - {hotel}: {km} km")
        time.sleep(1.2)  # API limiti için bekleme

# Sonuçları JSON olarak kaydet
with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"\nTüm mesafeler {output_json_path} dosyasına kaydedildi.")
