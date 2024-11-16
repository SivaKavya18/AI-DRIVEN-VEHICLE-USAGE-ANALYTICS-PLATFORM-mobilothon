import random
from datetime import datetime
import time

# Function to generate synthetic vehicle data
def generate_synthetic_data():
    return {
        "speed": random.uniform(0, 120),  # Speed in km/h
        "rpm": random.uniform(500, 3000),  # Engine RPM
        "accData": random.uniform(0, 2),  # Acceleration data
        "battery_voltage": random.uniform(11, 15),  # Battery voltage
        "tpos": random.uniform(0, 100),  # Throttle position (%)
        "maf": random.uniform(0, 40),  # Mass Air Flow (g/s)
        "eload": random.uniform(0, 100),  # Engine load (%)
        "ctemp": random.uniform(-20, 100),  # Coolant temperature (°C)
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp
    }
