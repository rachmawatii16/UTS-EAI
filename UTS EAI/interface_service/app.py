from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
inventory_service_url = "http://192.168.56.1:5000"

@app.route('/')
def index():
    response = requests.get(f"{inventory_service_url}/inventory")
    items = response.json() if response.status_code == 200 else []
    return render_template('index.html', items=items)

@app.route('/create_item_form')
def create_item_form():
    return render_template('create_item.html')

@app.route('/create_item', methods=['POST'])
def create_item():
    data = request.form
    response = requests.post(f"{inventory_service_url}/inventory", json=data)
    return response.text

@app.route('/update_item_form')
def update_item_form():
    return render_template('update_item.html')

@app.route('/update_item', methods=['POST'])
def update_item():
    data = request.form
    item_id = data.get('id')
    response = requests.put(f"{inventory_service_url}/inventory/{item_id}", json=data)
    return response.text

@app.route('/delete_item_form')
def delete_item_form():
    return render_template('delete_item.html')

@app.route('/delete_item', methods=['POST'])
def delete_item():
    item_id = request.form.get('id')
    response = requests.delete(f"{inventory_service_url}/inventory/{item_id}")
    return response.text

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
