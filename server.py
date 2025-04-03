from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Store sensor values in memory
sensor_data = {
    "temperature": 0,
    "humidity": 0,
    "soil_moisture": 0,
    "threshold": 50  # Default threshold
}

# Endpoint for ESP32 / M5Stack to get sensor values and threshold
@app.route('/', methods=['GET'])
def get_data():
    return jsonify(sensor_data)

# Endpoint for ESP32 to POST updated sensor values
@app.route('/', methods=['POST'])
def update_data():
    data = request.get_json()
    if data:
        sensor_data.update(data)
        return jsonify({"status": "success"}), 200
    return jsonify({"error": "Invalid data"}), 400

# GUI to view and update threshold
@app.route('/set_threshold', methods=['GET', 'POST'])
def set_threshold():
    message = ""
    if request.method == 'POST':
        try:
            new_threshold = int(request.form['threshold'])
            sensor_data['threshold'] = new_threshold
            message = "✅ Threshold updated to " + str(new_threshold)
        except:
            message = "❌ Invalid input. Please enter a number."

    # Render simple HTML GUI
    html = '''
    <html>
        <head>
            <title>Set Threshold</title>
        </head>
        <body style="font-family:sans-serif; max-width: 500px; margin: auto; padding: 20px;">
            <h2>🌱 IoT Control Panel</h2>
            <p>Current Threshold: <b>{{ threshold }}</b></p>
            <form method="POST">
                <label for="threshold">New Threshold:</label><br>
                <input type="number" name="threshold" min="0" max="100" value="{{ threshold }}" required>
                <br><br>
                <button type="submit">Update</button>
            </form>
            <p style="color: green;">{{ message }}</p>
        </body>
    </html>
    '''
    return render_template_string(html, threshold=sensor_data["threshold"], message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
