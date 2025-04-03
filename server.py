from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

sensor_data = {
    "temperature": 0,
    "humidity": 0,
    "soil_moisture": 0,
    "threshold": 50
}

@app.route('/', methods=['GET'])
def get_data():
    return jsonify(sensor_data)

@app.route('/set_threshold', methods=['GET', 'POST'])
def set_threshold():
    message = ""
    if request.method == 'POST':
        try:
            new_threshold = int(request.form['threshold'])
            sensor_data['threshold'] = new_threshold
            message = "✅ Threshold updated to " + str(new_threshold)
        except:
            message = "❌ Invalid input"

    html = '''
    <html>
        <head>
            <title>Set Threshold</title>
        </head>
        <body style="font-family:sans-serif;">
            <h2>🌱 IoT Control Panel</h2>
            <p>Current Threshold: <b>{{ threshold }}</b></p>
            <form method="POST">
                New Threshold: <input type="number" name="threshold" required>
                <button type="submit">Update</button>
            </form>
            <p style="color: green;">{{ message }}</p>
        </body>
    </html>
    '''
    return render_template_string(html, threshold=sensor_data["threshold"], message=message)
