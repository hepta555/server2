from flask import Flask, request, jsonify

app = Flask(__name__)

# ตัวแปรเก็บข้อมูลล่าสุดจาก ESP32
sensor_data = {
    "temperature": 0,
    "humidity": 0,
    "soil_moisture": 0,
    "threshold": 50  # ค่าตั้งต้น
}

@app.route('/', methods=['GET'])
def get_data():
    return jsonify(sensor_data)

@app.route('/', methods=['POST'])
def update_data():
    data = request.get_json()
    if data:
        sensor_data.update(data)
        return jsonify({"status": "success"}), 200
    return jsonify({"error": "Invalid data"}), 400

if __name__ == '__main__':
    app.run()
