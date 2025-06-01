import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

# ----------------------------
# Web Scraping Fonksiyonları
# ----------------------------

def fetch_price_from_safeairporttransfer():
    try:
        url = "https://safeairporttransfer.com"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        # Örnek selector - ihtiyaç halinde güncelle!
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
# JSON Yazma / Okuma
# ----------------------------

def save_prices_to_json(prices, file_path="prices.json"):
    data = {
        "timestamp": datetime.utcnow().isoformat(),
        "prices": prices
    }
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_prices_from_json(file_path="prices.json"):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

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
# Ana Script
# ----------------------------

def main():
    print("🔍 Web sitelerinden fiyatlar çekiliyor...")

    prices = {
        "safeairporttransfer": fetch_price_from_safeairporttransfer(),
        "istanbulelitetransfer": fetch_price_from_istanbulelitetransfer(),
        "istanbulrides": fetch_price_from_istanbulrides()
    }

    print("\n📦 Çekilen fiyatlar:")
    for site, price in prices.items():
        print(f"  {site}: {'YOK' if price is None else f'{price} €'}")

    dynamic_price = calculate_dynamic_price(prices)
    print("\n💰 Dinamik fiyatımız:", f"{dynamic_price} €" if dynamic_price else "Hesaplanamadı")

    print("\n💾 Fiyatlar prices.json dosyasına kaydediliyor...")
    save_prices_to_json(prices)
    print("✅ Kayıt tamamlandı.")

if __name__ == "__main__":
    main()

#from notifier import send_email

#subject = "ShuttlePort - Yeni Fiyatlar Hesaplandı"
#body = "Merhaba Serdar,\n\nYeni fiyatlar başarıyla hesaplandı ve prices.json güncellendi.\n\nSelamlar,\nShuttlePort Bot"
#send_email(subject, body)
