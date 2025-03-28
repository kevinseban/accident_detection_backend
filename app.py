from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from pymongo import MongoClient
import json

app = Flask(__name__)
# Correctly initialize Flask-SocketIO with cors_allowed_origins to allow all origins
socketio = SocketIO(app, cors_allowed_origins="*")

# Enable CORS for all routes and all domains
CORS(app, resources={r"/*": {"origins": "*"}})

# MongoDB connection URI
# MONGO_URI = "mongodb+srv://kevinseban03:pass123word@cluster0.eums9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# client = MongoClient(MONGO_URI)
# db = client.get_database('accident_detection')  # Create the 'accident_detection' database
# alerts_collection = db.alerts  # Create the 'alerts' collection

@app.route('/send_alert', methods=['POST'])
def send_alert():
    try:
        # Get JSON data from the POST request
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Construct the alert object
        alert = {
            "severity": data.get("severity"),
            "location": data.get("location"),
            "timestamp": data.get("timestamp"),
            "vehicleType": data.get("vehicleType")
        }

        # Check that required fields are present
        if not alert["severity"] or not alert["location"] or not alert["timestamp"]:
            return jsonify({"error": "Missing required fields"}), 400
        
        # Insert the alert into MongoDB
        # alert_id = alerts_collection.insert_one(alert).inserted_id
        
        # Convert ObjectId to string for JSON serialization
        # alert["_id"] = str(alert_id)

        # Emit the alert to all connected clients via socket.io (broadcasting the event)
        socketio.emit('new_alert', json.dumps(alert))

        # return jsonify({"message": "Alert received", "id": str(alert_id)}), 201
        return jsonify({"message": "Alert received"}), 201
    
    except Exception as e:
        # Log the error and return a 500 error if something goes wrong
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
