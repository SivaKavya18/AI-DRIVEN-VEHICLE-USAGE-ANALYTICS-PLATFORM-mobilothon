import sqlite3

DATABASE = 'vehicle_data.db'

def insert_data_to_db(data):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # SQL query to insert data into the vehicle_data table
    cursor.execute('''
        INSERT INTO vehicle_data (speed, rpm, accData, timestamp, battery_voltage, tpos, maf, eload, ctemp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['speed'], data['rpm'], data['accData'], data['timestamp'], 
          data['battery_voltage'], data['tpos'], data['maf'], data['eload'], data['ctemp']))
    
    conn.commit()
    conn.close()