import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, jsonify
from common.utils import load_item, save_item
from common.vars import USERS_API_URL, PRODUCTS_API_URL
import requests
from datetime import datetime

app = Flask(__name__)
PURCHASES_FILE = os.path.join(os.path.dirname(__file__), 'purchases.json')

# 🔹 Obtener compras de un usuario
@app.route('/api/purchases/<int:user_id>', methods=['GET'])
def get_purchases(user_id):
    purchases = load_item(PURCHASES_FILE)
    user_purchases = [p for p in purchases if p['user_id'] == user_id]

    # Consultar productos para mostrar nombres
    try:
        products_resp = requests.get(f"{PRODUCTS_API_URL}/api/products")
        products_resp.raise_for_status()
        products = products_resp.json()['products']
    except Exception as e:
        return jsonify({'error': f'Error consultando productos: {e}'}), 500

    result = []
    for p in user_purchases:
        product = next((prod for prod in products if prod['id'] == p['product_id']), None)
        if product:
            result.append({
                'id': p['id'],
                'product_id': product['id'],
                'product_name': product['name'],
                'timestamp': p.get('timestamp', 'N/A')
            })

    return jsonify({
        'user_id': user_id,
        'purchased_products': result
    })


# 🔹 Crear una nueva compra
@app.route('/api/purchases', methods=['POST'])
def create_purchase_api():
    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')

    if not user_id or not product_id:
        return jsonify({'error': 'user_id y product_id son requeridos'}), 400

    # Validar usuario
    try:
        user_resp = requests.get(f"{USERS_API_URL}/api/users")
        user_resp.raise_for_status()
        users = user_resp.json()['users']
    except Exception as e:
        return jsonify({'error': f'Error consultando usuarios: {e}'}), 500

    if not any(u['id'] == user_id for u in users):
        return jsonify({'error': 'Usuario no encontrado'}), 400

    # Validar producto
    try:
        prod_resp = requests.get(f"{PRODUCTS_API_URL}/api/products")
        prod_resp.raise_for_status()
        products = prod_resp.json()['products']
    except Exception as e:
        return jsonify({'error': f'Error consultando productos: {e}'}), 500

    if not any(p['id'] == product_id for p in products):
        return jsonify({'error': 'Producto no encontrado'}), 400

    # Guardar compra
    purchases = load_item(PURCHASES_FILE)
    purchase = {
        'id': len(purchases) + 1,
        'user_id': user_id,
        'product_id': product_id,
        'timestamp': datetime.now().isoformat()
    }
    purchases.append(purchase)
    save_item(PURCHASES_FILE, purchases)

    return jsonify({'message': 'Compra registrada', 'purchase': purchase}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5007)
