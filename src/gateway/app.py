# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: app.py
# Descripción: Gateway de Microservicios
# ============================================================

import sys, os
import requests
from flask import Flask, render_template

# Permitir importar el módulo common
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.vars import USER_API_URL, PRODUCT_API_URL, PURCHASES_API_URL

app = Flask(__name__, template_folder="templates")

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/all')
def get_all():
    """Muestra todos los usuarios y productos"""
    try:
        # Pedir usuarios
        users_resp = requests.get(f"{USER_API_URL}/api/users")
        users_resp.raise_for_status()
        users = users_resp.json().get('users', [])

        # Pedir productos
        products_resp = requests.get(f"{PRODUCT_API_URL}/api/products")
        products_resp.raise_for_status()
        products = products_resp.json().get('products', [])
        
        # Renderizar la plantilla con ambos datos
        return render_template("all.html", users=users, products=products)

    except Exception as e:
        return render_template("error.html", error=str(e)), 500


@app.route('/user/<int:user_id>/purchases')
def user_with_purchases(user_id):
    """Muestra un usuario junto con sus productos comprados"""
    try:
        # Obtener usuario
        users_resp = requests.get(f"{USER_API_URL}/api/users")
        users_resp.raise_for_status()
        users = users_resp.json().get('users', [])
        user = next((u for u in users if u['id'] == user_id), None)
        if not user:
            return f"Usuario {user_id} no encontrado", 404

        # Obtener compras
        purchases_resp = requests.get(f"{PURCHASES_API_URL}/api/purchases/{user_id}")
        purchases_resp.raise_for_status()
        purchased_products = purchases_resp.json().get('purchased_products', [])

        return render_template("user_purchases.html", user=user, purchased_products=purchased_products)

    except Exception as e:
        return render_template("error.html", error=str(e)), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
