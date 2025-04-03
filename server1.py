from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows cross-origin requests

# Store sensor data and threshold
sensor_data = {
    "temperature": 0,
    "humidity": 0,
    "soil_moisture": 0,
    "threshold": 30  # Default threshold
}

# 🔹 ESP32 sends data here
@app.route('/update', methods=['POST'])
def update_data():
    global sensor_data
    data = request.json
    if "temperature" in data and "humidity" in data and "soil_moisture" in data:
        sensor_data.update(data)
        return jsonify({"message": "Data updated successfully"}), 200
    return jsonify({"error": "Invalid data format"}), 400

# 🔹 M5Core2 fetches data here
@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify(sensor_data), 200

# 🔹 PC sets pump threshold here
@app.route('/set_threshold', methods=['POST'])
def set_threshold():
    global sensor_data
    data = request.json
    if "threshold" in data:
        sensor_data["threshold"] = data["threshold"]
        return jsonify({"message": "Threshold updated"}), 200
    return jsonify({"error": "Invalid threshold format"}), 400

# 🔹 Home route for testing
@app.route('/')
def home():
    return "Flask Server Running!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)  # Runs on Render