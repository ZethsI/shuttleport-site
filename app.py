from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# prices.json'u yükle
def load_prices():
    with open('prices.json', encoding='utf-8') as f:
        return json.load(f)

@app.route('/api/get_price', methods=['GET'])
def get_price():
    airport = request.args.get('airport')
    hotel = request.args.get('hotel')
    vehicle = request.args.get('vehicle')

    data = load_prices()
    base_prices = data['basePrices']
    distance_km = data['distanceKm']
    km_price = data['kmPrice']
    discount = data['discount']

    key = f"{airport}-{hotel}"
    base = base_prices.get(vehicle, 0)
    dist = distance_km.get(key, 20)  # Varsayılan 20km, eğer mesafe yoksa

    # Dinamik fiyat hesaplama (km + taban fiyat + indirim)
    calc_price = max(
        discount["minPercent"] * (base + dist * km_price) - discount["fixedAmount"],
        15
    )
    final_price = round(calc_price, 2)

    return jsonify({
        "airport": airport,
        "hotel": hotel,
        "vehicle": vehicle,
        "distance_km": dist,
        "price": final_price,
        "currency": "EUR"
    })

if __name__ == '__main__':
    # Render'da start command ile başlatılır, burada local test için:
    app.run(debug=True)
