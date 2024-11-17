# AI-DRIVEN-VEHICLE-USAGE-ANALYTICS-PLATFORM 
Managing vehicles can be challenging due to unpredictable driving behavior that increases accident risk, inefficient fuel usage that leads to higher operational costs, and a lack of real-time alerts for unsafe driving conditions. Additionally, vehicles often lack proactive maintenance insights, resulting in unexpected breakdowns and increased repair costs. Addressing these issues requires a comprehensive solution that monitors, analyzes, and provides actionable feedback on driving and vehicle health.​The objective of this project is to develop a real-time monitoring system that improves driving behavior, enhances fuel efficiency, and predicts potential vehicle health issues.

## FEATURES
**Driving Behavior Analysis:** Uses Random forest ML model to detect "Normal" vs. "Aggressive" driving instantaneously and LSTM model to predict the overall driving behaviour based on past readings.​<br/>
**Fuel Efficiency Monitoring:** Provides real-time and trend-based insights on fuel consumption and predicts fuel efficiency using ridge regression model.<br/>
**Gear Predictions:** Simplified gear predictions based on vehicle data.​<br/>
**Turn Alerts:** Detection of sharp turns using accelerometer data.​<br/>
**Vehicle Health Monitoring:** Identifies potential issues (based on battery, RPM anomalies).

## GETTING STARTED
#### DEPENDENCIES
* Python 3.x
* pip
* virtualenv

#### Step 1: Clone the Repository
```bash
git clone https://github.com/SivaKavya18/AI-DRIVEN-VEHICLE-USAGE-ANALYTICS-PLATFORM-mobilothon.git
```

#### Step 2: Set Up Virtual Environment (Optional but recommended)
```bash
python3 -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Running the Application
```bash
python3 app.py
```
Open your browser and navigate to http://127.0.0.1:5000/.

## Database Design
SQLite is used to store the readings of the vehicle.
To create or use rules.db:
```sql
sqlite3 vehicle_data.db
```
Table info:
sqlite> PRAGMA table_info(vehicle_data);
0|id|INTEGER|0||1 <br/>
1|speed|REAL|0||0 <br/>
2|rpm|REAL|0||0 <br/>
3|accData|REAL|0||0 <br/>
4|timestamp|TEXT|0||0 <br/>
5|battery_voltage|REAL|0||0 <br/>
6|tpos|REAL|0||0 <br/>
7|maf|REAL|0||0 <br/>
8|eload|REAL|0||0 <br/>
9|ctemp|REAL|0||0 <br/>

## CONTRIBUTORS:
[Siva Kavya](https://github.com/SivaKavya18)<br/>
[Venkata Shravya](https://github.com/KvShravya)
