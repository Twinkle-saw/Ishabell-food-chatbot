from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

PROJECT_ID = "isabell-food-chatbot"
FIRESTORE_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/menu"

def get_menu():
    try:
        res = requests.get(FIRESTORE_URL, timeout=10).json()
        menu = []
        for doc in res.get('documents', []):
            f = doc['fields']
            def get_val(k):
                v = f.get(k, {})
                return v.get('stringValue') or v.get('integerValue') or v.get('doubleValue') or ""
            menu.append({
                'name': get_val('name'),
                'price': get_val('price'),
                'category': get_val('category'),
                'image': get_val('image')  # <-- ye image firestore se lega
            })
        return menu
    except Exception as e:
        print(e)
        return []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/menu')
def api_menu():
    return jsonify(get_menu())

if __name__ == '__main__':
    app.run(debug=True)