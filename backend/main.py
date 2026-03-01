from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import asyncio
import random
import time
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

app = FastAPI()

# ===============================
# 🔹 CORS CONFIG
# ===============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# 🔹 LOAD HISTORICAL DATA
# ===============================
df = pd.read_csv("data/smart_campus_ai_complete_dataset_800_rows.csv")

df["time_index"] = np.arange(len(df))

X = df[["time_index"]]
y = df["traffic_percentage"]

model = LinearRegression()
model.fit(X, y)


# ===============================
# 🔹 MODEL PERFORMANCE METRICS
# ===============================

y_pred = model.predict(X)

r2 = r2_score(y, y_pred)
mae = mean_absolute_error(y, y_pred)

model_accuracy = round(r2 * 100, 2)
model_mae = round(mae, 2)


# ===============================
# 🔹 AI TRAFFIC PREDICTION
# ===============================
def predict_next(minutes_ahead=10):
    future_index = df["time_index"].iloc[-1] + minutes_ahead
    prediction = model.predict([[future_index]])
    return int(max(0, min(100, prediction[0])))

# 🔹 WASTE LEVEL PREDICTION MODEL
# ===============================

# Create synthetic historical waste data from dataset
df["waste_level"] = (df["traffic_percentage"] * 0.6 +
                     np.random.randint(10, 30, len(df)))

waste_features = df[["time_index", "traffic_percentage"]]
waste_target = df["waste_level"]

waste_model = RandomForestRegressor(n_estimators=50)
waste_model.fit(waste_features, waste_target)


def predict_waste(time_index, traffic):
    prediction = waste_model.predict([[time_index, traffic]])
    return int(max(0, min(100, prediction[0])))


# ===============================
# 🔹 WATER ANOMALY DETECTION
# ===============================

df["water_usage"] = (df["traffic_percentage"] * 0.5 +
                     np.random.randint(20, 40, len(df)))

avg_water_usage = df["water_usage"].mean()

def detect_water_anomaly(current_water):
    if current_water > avg_water_usage * 1.5:
        return "Leakage Suspected"
    return "Normal"


# ===============================
# 🔹 PREDICTIVE ROUTING ENGINE
# ===============================

def calculate_priority_score(waste, traffic):
    return (waste * 0.7) + (traffic * 0.3)


def optimize_route(zones):
    for zone in zones:
        zone["priority_score"] = calculate_priority_score(
            zone["waste_level"],
            zone["traffic"]
        )

    # Sort descending by priority
    optimized = sorted(zones, key=lambda x: x["priority_score"], reverse=True)

    return optimized

# ===============================
# 🔹 SMART RISK ENGINE
# ===============================
def calculate_risk(traffic, pollution, energy):
    return int((traffic * 0.4) + (pollution * 0.3) + (energy * 0.3))

# ===============================
# 🔹 IoT SENSOR SIMULATION
# ===============================
def simulate_iot():
    return {
        "gate_sensor": random.randint(20, 100),
        "parking_sensor": random.randint(10, 100),
        "water_level_sensor": random.randint(40, 95),
        "waste_bin_level": random.randint(10, 100),
        "lab_equipment_health": random.randint(60, 100)
    }

# ===============================
# 🔹 SPACE UTILIZATION
# ===============================
def space_utilization():
    return {
        "library_usage": random.randint(30, 100),
        "lab_usage": random.randint(20, 95),
        "classroom_occupancy": random.randint(40, 100)
    }

# ===============================
# 🔹 PREDICTIVE MAINTENANCE
# ===============================
def predictive_maintenance():
    health_score = random.randint(50, 100)
    status = "OK" if health_score > 70 else "Maintenance Required"
    return {
        "equipment_health_score": health_score,
        "maintenance_status": status
    }

# ===============================
# 🔹 DIGITAL TWIN ZONES
# ===============================
def generate_zones(current_time_index):
    base_coords = [
        {"name": "Tech Park", "lat": 28.6139, "lng": 77.2090},
        {"name": "Industrial Area", "lat": 28.6200, "lng": 77.2150},
        {"name": "Residential Zone", "lat": 28.6100, "lng": 77.2000},
        {"name": "University Block", "lat": 28.6150, "lng": 77.2050},
    ]

    zones = []

    for zone in base_coords:
        traffic = random.randint(30, 95)
        waste_level = predict_waste(current_time_index, traffic)

        zones.append({
            "name": zone["name"],
            "lat": zone["lat"],
            "lng": zone["lng"],
            "traffic": traffic,
            "waste_level": waste_level
        })

    optimized = optimize_route(zones)

    return optimized

# ===============================
# 🔹 ADVANCED UTILITIES
# ===============================
def maintenance_score(lab_equip, hvac_health):
    score = (lab_equip * 0.6) + ((100 - hvac_health) * 0.4)
    return int(min(100, score))


def waste_priority(waste_level):
    if waste_level > 80:
        return "High Priority Pickup"
    elif waste_level > 50:
        return "Medium Priority"
    else:
        return "Low"


def shuttle_recommendation(traffic, transport):
    if traffic > 75 and transport > 70:
        return "Increase Shuttle Frequency"
    elif traffic < 40:
        return "Reduce Shuttle Frequency"
    else:
        return "Normal Operation"

# ===============================
# 🔹 DASHBOARD API
# ===============================
@app.get("/dashboard")
def dashboard():

    traffic = predict_next(1) + random.randint(-5, 5)
    traffic = max(0, min(100, traffic))

    pollution = int(traffic * 0.8)
    energy = int(traffic * 0.7)

    transport = random.randint(30, 95)
    emergency = random.randint(0, 2)

    risk = calculate_risk(traffic, pollution, energy)

    return {
        "timestamp": time.time(),
        "traffic": traffic,
        "pollution": pollution,
        "energy": energy,
        "transport": transport,
        "emergency": emergency,
        "risk": risk,
        "prediction_10min": predict_next(10),
        "prediction_30min": predict_next(30),
        "zones": generate_zones(),
        "iot": simulate_iot(),
        "space": space_utilization(),
        "maintenance": predictive_maintenance(),
        "model_accuracy": model_accuracy,
"model_mae": model_mae,
"library_usage": random.randint(40, 95),
"lab_usage": random.randint(30, 90),
"classroom_occupancy": random.randint(35, 100),
"model_metrics": {
    "r2_score": round(r2, 4),
    "mae": round(mae, 2)
}
    }

# ===============================
# 🔹 DOWNLOAD HISTORY
# ===============================
@app.get("/download-history")
def download_history():
    return df.to_dict(orient="records")

# ===============================
# 🔹 WEBSOCKET REAL-TIME STREAM
# ===============================
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    current_time_index = df["time_index"].iloc[-1]

    while True:

        traffic = predict_next(1) + random.randint(-5, 5)
        traffic = max(0, min(100, traffic))

        pollution = int(traffic * 0.8)
        energy = int(traffic * 0.7)
        emergency = random.randint(0, 2)

        water_usage = random.randint(40, 120)
        water_status = detect_water_anomaly(water_usage)

        # Generate optimized waste route
        zones = generate_zones(current_time_index)

        data = {
            "traffic": traffic,
            "pollution": pollution,
            "energy": energy,
            "emergency": emergency,
            "risk": calculate_risk(traffic, pollution, energy),
            "water_usage": water_usage,
            "water_status": water_status,
            "optimized_waste_route": zones,
            "prediction_10min": predict_next(10),
            "prediction_30min": predict_next(30),
            "model_accuracy": model_accuracy,
             "model_mae": model_mae,
              "model_metrics": {
        "r2_score": round(r2, 4),
        "mae": round(mae, 2)
              },
               "iot": simulate_iot(),
               "space": space_utilization(),
                "maintenance": predictive_maintenance()

        }

        await websocket.send_json(data)
        await asyncio.sleep(5)

        current_time_index += 1