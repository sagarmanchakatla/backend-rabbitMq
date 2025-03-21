from flask import Flask, jsonify, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

# Shared state to store processed CSV data
processed_data = []

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(processed_data)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/update', methods=['POST'])
def update_data():
    global processed_data
    new_data = request.json
    processed_data = new_data
    socketio.emit('csv_update', processed_data)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    socketio.run(app, debug=True)