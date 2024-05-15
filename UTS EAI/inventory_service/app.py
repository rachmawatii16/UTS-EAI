from flask import Flask, request, jsonify
import redis

app = Flask(__name__)
redis_client = redis.Redis(host='redis', port=6379)

inventory = {}


@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory)

@app.route('/inventory', methods=['POST'])
def create_item():
    data = request.json
    item_id = data.get('id')
    if item_id in inventory:
        return jsonify({'error': 'Item already exists'}), 400
    inventory[item_id] = data
    redis_client.publish('inventory_updates', 'Inventory updated!')
    return jsonify({'message': 'Item created successfully'})

@app.route('/inventory/<item_id>', methods=['GET'])
def get_item(item_id):
    if item_id not in inventory:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(inventory[item_id])

@app.route('/inventory/<item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    if item_id not in inventory:
        return jsonify({'error': 'Item not found'}), 404
    inventory[item_id] = data
    redis_client.publish('inventory_updates', 'Inventory updated!')
    return jsonify({'message': 'Item updated successfully'})

@app.route('/inventory/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    if item_id not in inventory:
        return jsonify({'error': 'Item not found'}), 404
    del inventory[item_id]
    redis_client.publish('inventory_updates', 'Inventory updated!')
    return jsonify({'message': 'Item deleted successfully'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
