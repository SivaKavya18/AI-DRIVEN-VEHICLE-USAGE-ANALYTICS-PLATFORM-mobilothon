from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import joblib
import sklearn
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from flask_caching import Cache
from generate_data import generate_synthetic_data
from insert_db import insert_data_to_db
import time
import threading
import os

print("Database Path:", os.path.abspath('vehicle_data.db'))

app = Flask(__name__)
CORS(app)

cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 300})
DATABASE = 'vehicle_data.db'

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # To return rows as dictionaries
    return conn

# Helper function to fetch fuel efficiency
def fetch_fuel_efficiency():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT speed, maf, rpm, eLoad FROM vehicle_data');
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['speed', 'maf', 'rpm', 'eLoad'])
    loaded_model = joblib.load('ridge_fuel_efficiency_model.joblib')
    fuel_efficinecy = loaded_model.predict(df)
    avg_fuel_efficiency = np.mean(fuel_efficinecy)
    conn.close()
    return avg_fuel_efficiency

# Helper function to fetch gear predictions
def fetch_gear_predictions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vehicle_data ORDER BY timestamp DESC LIMIT 10')
    data = cursor.fetchall()
    gear_predictions = ["Gear " + str(int(d['rpm'] // 1000)) for d in data]  # Simplified logic
    conn.close()
    return gear_predictions

# Helper function to fetch turn alerts
def fetch_turn_alerts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vehicle_data ORDER BY timestamp DESC LIMIT 10')
    data = cursor.fetchall()
    turn_alerts = [{"sharp_turn": d['accData'] > 1.5} for d in data]
    conn.close()
    return turn_alerts

# Helper function to fetch driving patterns
def fetch_driving_patterns():
    conn = get_db_connection()
    cursor = conn.cursor()
    query='''SELECT * FROM vehicle_data WHERE strftime('%Y-%m', timestamp) = strftime('%Y-%m', 'now');'''
    cursor.execute(query)
    rows = cursor.fetchall()
    patterns = [{
        "timestamp": row['timestamp'],
        "gps_speed": row['speed'],
        "rpm": row['rpm'],
    } for row in rows]
    avg_speed = np.mean([row['speed'] for row in rows])
    conn.close()
    return {"avg_speed": avg_speed, "patterns": patterns}

def predict_driving_behaviour():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT accData, rpm, speed, tPos FROM vehicle_data ORDER BY timestamp DESC LIMIT 10');
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['accData', 'rpm','speed', 'tPos'])
    loaded_model = joblib.load('random_forest_model.joblib')
    driving_behaviour = loaded_model.predict(df)
    driving_behaviour=[0 if d ==0 else 1 for d in driving_behaviour]
    conn.close()
    return driving_behaviour

def detect_vehicle_health_issues():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehicle_data WHERE DATE(timestamp) = DATE('now')")
    data = cursor.fetchall()
    
    # Initialize counters
    rpm_anomalies = 0
    battery_anomalies = 0

    # Iterate through each row to check for anomalies
    for row in data:
        if row['rpm'] >= 3000:  # RPM threshold
            rpm_anomalies += 1
        if row['battery_voltage'] < 12.6 or row['battery_voltage'] > 14.7:  # Battery voltage range
            battery_anomalies += 1

    # Total anomalies
    total_anomalies = rpm_anomalies + battery_anomalies
    conn.close()
    return total_anomalies

def fuel_efficiency_trend():
    current_fuel_avg=fetch_fuel_efficiency()
    if current_fuel_avg < 10:  # Assuming 10 km/l as a threshold
        return ("Your average fuel efficiency is low. Consider smoother driving and checking for vehicle issues.")
    else:
        return ("Your fuel efficiency is within a good range.")

def health_issues():
    health_issue_count=detect_vehicle_health_issues()
    if health_issue_count > 0:
        return (f"Your vehicle shows {health_issue_count} potential health issues in recent readings. Please check your RPM levels and battery voltage.")
    else:
        return ("No significant vehicle health issues detected.")
    
def predict_driving_behaviour_overall():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT speed, accData, rpm, tPos FROM vehicle_data ORDER BY timestamp DESC LIMIT 10')
    data = cursor.fetchall()
    
    # Process data for LSTM
    df = pd.DataFrame(data, columns=['speed', 'accData', 'rpm', 'tPos'])    
    # Ensure the sequence length is correct for LSTM input
    if len(df) < 10:
        conn.close()
        return "Not enough data for LSTM prediction"
    
    # Preprocess for LSTM (scaling, reshaping)
    sequence_data = df[['accData', 'rpm', 'speed', 'tPos']].values
    sequence_data = sequence_data[-10:]  # Use the last 10 rows for the LSTM input
    sequence_data = np.expand_dims(sequence_data, axis=0)  # Reshape to (1, 10, features)
    
    # Predict driving behavior sequence with LSTM
    lstm_model = load_model('lstm_model.keras')
    lstm_prediction = lstm_model.predict(sequence_data)
    conn.close()
    driving_behavior = "Aggressive" if lstm_prediction[0, 0] >= 0.5 else "Normal"
    return driving_behavior

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/data')
def get_data():
    # Collect all the data from helper functions
    data = {
        "fuelEfficiency": fetch_fuel_efficiency(),
        "fuelEfficiencyTrend":fuel_efficiency_trend(),
        "gearPredictions": fetch_gear_predictions(),
        "turnAlerts": fetch_turn_alerts(),
        "healthIssues":health_issues(),
        "OverallDrivingBehaviour":predict_driving_behaviour_overall(),
        "drivingBehaviourPredictions":predict_driving_behaviour(),
        "drivingPatterns": fetch_driving_patterns()
    }
    return jsonify(data)

def main_program():
    while True:
        data = generate_synthetic_data()
        insert_data_to_db(data)
        time.sleep(30)

if __name__ == '__main__':
    data_thread = threading.Thread(target=main_program)
    # Start the data generation thread
    data_thread.start()
    app.run(debug=True)
