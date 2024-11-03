from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
socketio = SocketIO(app)

roads = [
    {
        'name': 'Chingiz Aitmatov Street',
        'coordinates': [
            {'lat': 51.1694, 'lng': 71.4491},
            {'lat': 51.1750, 'lng': 71.4500},
            {'lat': 51.1800, 'lng': 71.4550}
        ],
        'status': 'free'  
    }
]

@app.route('/')
def index():
    return render_template('road_map.html')

@socketio.on('update_traffic')
def handle_update_traffic(data):
    road_name = data['road_name']
    car_count = data['car_count']

    for road in roads:
        if road['name'] == road_name:
            if car_count >= 30:
                road['status'] = 'congested'
            elif car_count >= 20:
                road['status'] = 'medium'
            else:
                road['status'] = 'free'
            break
    
    emit('traffic_update', roads, broadcast=True)

@app.route('/manual_update', methods=['POST'])
def manual_update():
    road_name = request.json['Chingiz Aitmatov']
    new_status = request.json['status']

    for road in roads:
        if road['name'] == road_name:
            road['status'] = new_status
            break

    socketio.emit('traffic_update', roads, broadcast=True)
    return jsonify({'success': True, 'message': 'The road has been updated successfully'})

if __name__ == '__main__':
    socketio.run(app, debug=True)