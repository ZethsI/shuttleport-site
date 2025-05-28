from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Fiyat verilerini yükle
with open('prices.json', encoding='utf-8') as f:
    prices_data = json.load(f)

@app.route('/api/get_price', methods=['GET'])
def get_price():
    airport = request.args.get('airport')
    hotel = request.args.get('hotel')
    vehicle = request.args.get('vehicle')

    # Fiyatı bul
    for item in prices_data:
        if (item.get('hotel') == hotel
            and item.get('site')
            and (item.get('one_way') or item.get('vehicle_type_1'))):

            # Basit örnek: İstanbul için, one_way veya vehicle_type_1 fiyatı
            if vehicle and 'vehicle_type_1' in item:
                price = item.get('vehicle_type_1')
            else:
                price = item.get('one_way')
            return jsonify({'price': price, 'site': item.get('site')})

    return jsonify({'price': None, 'site': None})

if __name__ == '__main__':
    app.run(debug=True)
