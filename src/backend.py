from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# Default destination
current_destination = -1
delivery_done = False  # New state to track delivery status

@app.route('/set_destination', methods=['POST'])
def set_destination():
    global current_destination
    data = request.json
    destination = data.get('destination')

    if destination in [1, 2, 3, 4]:
        current_destination = destination
        return jsonify({'message': 'Destination set successfully', 'destination': current_destination}), 200
    else:
        return jsonify({'message': 'Invalid destination. Choose between 1 and 4.'}), 400

@app.route('/get_destination', methods=['GET'])
def get_destination():
    return jsonify({'current_destination': current_destination}), 200

@app.route('/delivery_done', methods=['POST'])
def delivery_done_route():
    global delivery_done
    delivery_done = True  # Set delivery state to done
    return jsonify({'message': 'Delivery marked as done!'}), 200

@app.route('/get_delivery_done', methods=['GET'])
def get_delivery_done_route():
    global delivery_done
    return jsonify({'delivery': delivery_done})

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
