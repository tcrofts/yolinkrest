from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# SQLite database path
DB_PATH = '/dev/shm/yolink.db'

# Endpoint to retrieve the last open or close time for a specific device
@app.route('/yolink/last_state_time', methods=['GET'])
def get_last_state_time():
    device_id = request.args.get('deviceId')

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get the last open or close time for the specified device
    cursor.execute("SELECT MAX(stateChangedAt) FROM yolink WHERE state IN ('open', 'closed', 'normal', 'alert') AND deviceId = ?",
                   (device_id,))
    result = cursor.fetchone()
    last_state_time = result[0] if result[0] is not None else 'No records found'

    conn.close()

    return jsonify({'last_state_time': last_state_time})

# Endpoint to retrieve the current battery value for a specific device
@app.route('/yolink/current_battery', methods=['GET'])
def get_current_battery():
    device_id = request.args.get('deviceId')

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if device_id:
        # Get battery level for the specified device
        cursor.execute("SELECT deviceId, battery FROM yolink WHERE deviceId = ?",
                       (device_id,))
    else:
        # Get battery value for all devices
        cursor.execute("SELECT deviceId, battery FROM yolink ")

    rows = cursor.fetchall()

    current_readings = []
    for row in rows:
        record = {
            'deviceId': row[0],
            'current_battery': row[1]
        }
        current_readings.append(record)

    conn.close()

    return jsonify(current_readings)

# Endpoint to retrieve sensor readings (temperature and humidity) for a specific device
@app.route('/yolink/sensor_readings', methods=['GET'])
def get_sensor_readings():
    device_id = request.args.get('deviceId')

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if device_id:
        # Get sensor readings for the specified device
        cursor.execute("SELECT deviceId, temperature, humidity FROM yolink WHERE deviceId = ?",
                       (device_id,))
    else:
        # Get sensor readings for all devices
        cursor.execute("SELECT deviceId, temperature, humidity FROM yolink WHERE event like 'THSensor%'")

    rows = cursor.fetchall()

    sensor_readings = []
    for row in rows:
        record = {
            'deviceId': row[0],
            'temperature': row[1],
            'humidity': row[2]
        }
        sensor_readings.append(record)

    conn.close()

    return jsonify(sensor_readings)

# Endpoint to retrieve all data for a specific device
@app.route('/yolink/device_data', methods=['GET'])
def get_device_data():
    device_id = request.args.get('deviceId')

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if device_id:
        # Get data for the specified device
        cursor.execute("SELECT * FROM yolink WHERE deviceId = ?", (device_id,))
    else:
        # Get data for all devices
        cursor.execute("SELECT * FROM yolink")

    rows = cursor.fetchall()
    device_data = []
    for row in rows:
        record = {
            'deviceId': row[0],
            'stateChangedAt': row[1],
            'time': row[2],
            'state': row[3],
            'alertType': row[4],
            'event': row[5],
            'temperature': row[6],
            'humidity': row[7],
            'battery': row[8]
        }
        device_data.append(record)

    conn.close()

    return jsonify({device_id: device_data})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008)

