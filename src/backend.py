from flask import Flask, request, jsonify, send_from_directory
import threading

app = Flask(__name__)

# Default destination
current_destination = -1


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


@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')


def run_backend():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    pass
    # app.run(host='0.0.0.0', port=5000)