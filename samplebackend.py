from flask import Flask, render_template
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get the MongoDB connection string from the environment variable
mongo_uri = os.getenv('DB')
client = MongoClient(mongo_uri)

# Select your database and collection
db = client['sensor_database']  # Replace with your database name
collection = db['sensor_data']  # Replace with your collection name

@app.route('/')
def dashboard():
    # Fetch the latest sensor data from MongoDB
    latest_data = collection.find_one(sort=[('_id', -1)])  # Assuming you're storing documents with timestamps or IDs
    
    # If data is found, otherwise provide some default values
    if latest_data:
        data = {
            'soil_moisture': latest_data.get('soil_moisture', 'N/A'),
            'temperature': latest_data.get('temperature', 'N/A'),
            'humidity': latest_data.get('humidity', 'N/A')
        }

        # Alerts based on the fetched data
        alerts = []
        if data['soil_moisture'] < 30:
            alerts.append("Soil moisture is too low! Water the plants.")
        else:
            alerts.append("Soil moisture is adequate.")
        
        if data['temperature'] > 30:
            alerts.append("Temperature is too high! Cooling needed.")
        elif data['temperature'] < 10:
            alerts.append("Temperature is too low! Heating needed.")
        else:
            alerts.append("Temperature is within the optimal range.")
        
        if data['humidity'] > 60:
            alerts.append("Humidity is too high!")
        elif data['humidity'] < 30:
            alerts.append("Humidity is too low!")
        else:
            alerts.append("Humidity levels are normal.")
    else:
        data = {
            'soil_moisture': 'N/A',
            'temperature': 'N/A',
            'humidity': 'N/A'
        }
        alerts = ["No data available from the sensors."]

    return render_template('index.html', data=data, alerts=alerts)

if __name__ == '__main__':
    app.run(debug=True)
