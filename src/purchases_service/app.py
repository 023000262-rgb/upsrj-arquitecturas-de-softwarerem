from flask import Flask, render_template, request, redirect, url_for
import json, os
from datetime import datetime

app = Flask(__name__, template_folder="templates")

DATA_FILE = os.path.join(os.path.dirname(__file__), "purchases.json")

def load_purchases():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_purchases(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route('/purchases')
def list_purchases():
    purchases = load_purchases()
    return render_template("purchases.html", purchases=purchases)

@app.route('/purchases/create', methods=['GET', 'POST'])
def create_purchase():
    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        product_id = int(request.form['product_id'])

        purchases = load_purchases()
        new_purchase = {
            "id": len(purchases) + 1,
            "user_id": user_id,
            "product_id": product_id,
            "timestamp": datetime.now().isoformat()
        }
        purchases.append(new_purchase)
        save_purchases(purchases)
        return redirect(url_for('list_purchases'))
    
    return render_template("create_purchase.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5006, debug=True)
