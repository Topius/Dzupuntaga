from flask import Flask, jsonify, request, send_from_directory

from flask_cors import CORS
import threading
import time


app = Flask(__name__)
CORS(app)

all_trackers_data = {
    'TRK1': {
        'name': 'Tracker 1',
        'history': [{'latitude': 51.5074, 'longitude': -0.1278, 'timestamp': time.time()}]
    },
    'TRK2': {
        'name': 'Tracker 2',
        'history': [{'latitude': 51.5074, 'longitude': -0.1278, 'timestamp': time.time()}]
    }
}

stop_server_flag = threading.Event()

@app.route('/tracker/<tracker_id>', methods=['GET', 'POST'])
def tracker(tracker_id):
    if request.method == 'GET':
        return jsonify(all_trackers_data[tracker_id]['history']) if tracker_id in all_trackers_data else ('Tracker not found', 404)
    elif request.method == 'POST':
        data = request.json
        print(f"Received data for {tracker_id}: {data}")  # Debugging output
        if tracker_id in all_trackers_data:
            all_trackers_data[tracker_id]['history'].append({'latitude': data['latitude'], 'longitude': data['longitude'], 'timestamp': time.time()})
            print(f"Updated data for {tracker_id}: {all_trackers_data[tracker_id]['history']}")  # Further debugging output
            return jsonify({'message': 'Data received successfully'})
        else:
            return jsonify({'error': 'Tracker not found'}), 404

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    print(f"Received data: {data}")  # Debugging output
    return jsonify({'message': 'Data received successfully'})

@app.route('/all_trackers')
def get_all_trackers():
    return jsonify([{ 'tracker_id': k, 'tracker_name': v['name'], 'data': v['history']} for k, v in all_trackers_data.items()])

@app.route('/command')
def get_command():
    # Read command from command.txt file
    try:
        with open('command.txt', 'r') as file:
            command = file.read().strip()
        return command
    except FileNotFoundError:
        return 'Command file not found'

@app.route('/inputcom', methods=['POST'])
def update_command():
    data = request.form.get('command')  # Get the command from the form
    try:
        with open('command.txt', 'w') as file:
            file.write(data)  # Write the command to command.txt
        return 'Command updated successfully'
    except Exception as e:
        return f'Error: {str(e)}'

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
