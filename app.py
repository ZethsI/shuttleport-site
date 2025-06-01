from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

def load_prices():
    with open('prices.json', encoding='utf-8') as f:
        return json.load(f)

@app.route('/api/get_price', methods=['GET'])
def get_price():
    airport = request.args.get('airport')
    hotel = request.args.get('hotel')
    vehicle = request.args.get('vehicle')

    try:
        data = load_prices()
        base_prices = data['basePrices']
        distance_km = data['distanceKm']
        km_price = data['kmPrice']
        discount = data['discount']

        key = f"{airport}-{hotel}"

        # base, eğer "auto" ise sıfır kabul edilecek, yoksa float'a çevrilecek
        base = base_prices.get(vehicle, 0)
        if base == "auto":
            base_val = 0
        else:
            try:
                base_val = float(base)
            except Exception:
                base_val = 0

        dist = distance_km.get(key, 20)  # mesafe yoksa 20km varsay
        try:
            dist_val = float(dist)
        except Exception:
            dist_val = 20

        calc_price = max(
            discount["minPercent"] * (base_val + dist_val * km_price) - discount["fixedAmount"],
            15
        )
        final_price = round(calc_price, 2)

        # Eğer hiç fiyat yoksa, frontend'e anlamlı bilgi gönder
        if base == "auto" or final_price == 15:
            return jsonify({"error": "Fiyat bulunamadı!", "price": None}), 404

        return jsonify({
            "airport": airport,
            "hotel": hotel,
            "vehicle": vehicle,
            "distance_km": dist_val,
            "price": final_price,
            "currency": "EUR"
        })
    except Exception as e:
        return jsonify({"error": f"Hata oluştu: {str(e)}", "price": None}), 500

if __name__ == '__main__':
    app.run(debug=True)
