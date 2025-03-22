from flask import Flask, jsonify, request
from flask_socketio import SocketIO
import pandas as pd
import os

CSV_FILE = 'data.csv'

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w') as f:
        f.write("name,age,city\n")

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

# Shared state to store processed CSV data
processed_data = []

@app.route('/data', methods=['GET'])
def get_data():
    df = pd.read_csv(CSV_FILE)
    return jsonify(df.to_dict(orient='records'))

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/update', methods=['POST'])
def update_data():
    new_data = request.json
    df = pd.DataFrame(new_data)
    df.to_csv(CSV_FILE, index=False)
    socketio.emit('csv_update', new_data)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    socketio.run(app, debug=True)