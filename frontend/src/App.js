import React, { useEffect, useState } from "react";
import {
  MapContainer,
  TileLayer,
  Circle,
  Marker,
  Popup,
  useMap,
} from "react-leaflet";
import { Line } from "react-chartjs-2";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet.heat";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
} from "chart.js";

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement);

function HeatmapLayer({ zones }) {
  const map = useMap();

  useEffect(() => {
    if (!zones) return;

    const heatPoints = zones.map((z) => [z.lat, z.lng, z.risk / 100]);
    const heatLayer = L.heatLayer(heatPoints, {
      radius: 40,
      blur: 25,
    });

    heatLayer.addTo(map);
    return () => map.removeLayer(heatLayer);
  }, [zones, map]);

  return null;
}

function App() {
  const [data, setData] = useState(null);
  const [trafficHistory, setTrafficHistory] = useState([]);
  const [pollutionHistory, setPollutionHistory] = useState([]);

  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/ws");

    ws.onmessage = (event) => {
      const json = JSON.parse(event.data);
      setData(json);

      setTrafficHistory((prev) => [...prev.slice(-19), json.traffic]);
      setPollutionHistory((prev) => [...prev.slice(-19), json.pollution]);

  
    };

    return () => ws.close();
  }, []);

  if (!data) return <h2>Connecting to Smart Campus AI...</h2>;

  const trafficChart = {
    labels: trafficHistory.map((_, i) => i),
    datasets: [
      {
        label: "Traffic Trend",
        data: trafficHistory,
        borderColor: "cyan",
      },
    ],
  };

  const pollutionChart = {
    labels: pollutionHistory.map((_, i) => i),
    datasets: [
      {
        label: "Pollution Trend",
        data: pollutionHistory,
        borderColor: "orange",
      },
    ],
  };

  return (
    <div style={{ background: "#0f172a", color: "white", padding: "20px" }}>
      <h1>🏙 AI Smart Campus Digital Twin</h1>

      {/* ================= DASHBOARD CARDS ================= */}
      <div style={{ display: "flex", flexWrap: "wrap", gap: "15px" }}>
        <Card title="🚦 Traffic" value={data.traffic + "%"} />
        <Card title="🌫 Pollution" value={data.pollution} />
        <Card title="💡 Energy" value={data.energy + "%"} />
        <Card title="🚌 Transport Load" value={data.transport + "%"} />
        <Card title="⚠ Risk Score" value={data.risk + "%"} />
        <Card title="🔮 10 Min Prediction" value={data.prediction_10min + "%"} />
        <Card title="🔮 30 Min Prediction" value={data.prediction_30min + "%"} />
      </div>

      {/* ================= IoT SENSORS ================= */}
      <h2 style={{ marginTop: "30px" }}>🛰 IoT Sensors</h2>
      <div style={{ display: "flex", gap: "15px", flexWrap: "wrap" }}>
        <Card title="🚪 Gate Sensor" value={data?.iot?.gate_sensor} />
        <Card title="🅿 Parking Sensor" value={data?.iot?.parking_sensor} />
        <Card title="💧 Water Level" value={data?.iot?.water_level_sensor} />
        <Card title="🗑 Waste Level" value={data?.iot?.waste_bin_level} />
        <Card title="🧪 Lab Equipment Health" value={data?.iot?.lab_equipment_health} />
      </div>

      {/* ================= SPACE UTILIZATION ================= */}
      <h2 style={{ marginTop: "30px" }}>🏫 Space Utilization</h2>
      <div style={{ display: "flex", gap: "15px", flexWrap: "wrap" }}>
   <Card title="Library Usage" value={`${data.space?.library_usage || 0}%`} />
<Card title="Lab Usage" value={`${data.space?.lab_usage || 0}%`} />
<Card title="Classroom Occupancy" value={`${data.space?.classroom_occupancy || 0}%`} />
      </div>

      {/* ================= MAINTENANCE ================= */}
      <h2 style={{ marginTop: "30px" }}>🔧 Predictive Maintenance</h2>
      <div style={{ display: "flex", gap: "15px" }}>
        <Card title="Equipment Health" value={data?.maintenance?.equipment_health_score} />
        <Card title="Status" value={data?.maintenance?.maintenance_status} />
      </div>

      {/* ================= CHARTS ================= */}
      <h2 style={{ marginTop: "30px" }}>📈 Live Traffic Analytics</h2>
      <Line data={trafficChart} />

      <h2 style={{ marginTop: "30px" }}>🌫 Pollution Trend</h2>
      <Line data={pollutionChart} />



      <h3>Model Accuracy</h3>
<p>R² Score: {data.model_metrics?.r2_score}</p>
<p>MAE: {data.model_metrics?.mae}</p>

      {/* ================= DOWNLOAD BUTTON ================= */}
      <button
        style={{ marginTop: "20px", padding: "10px" }}
        onClick={() =>
          window.open("http://127.0.0.1:8000/download-history")
        }
      >
        📊 Download Historical Data
      </button>

      {/* ================= MAP ================= */}
      <MapContainer
        center={[28.6139, 77.2090]}
        zoom={13}
        style={{ height: "500px", marginTop: "30px" }}
      >
        <TileLayer
          attribution="&copy; OpenStreetMap contributors"
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {data.zones && <HeatmapLayer zones={data.zones} />}

        {data.zones &&
          data.zones.map((zone, index) => (
            <Circle
              key={index}
              center={[zone.lat, zone.lng]}
              radius={zone.risk * 10}
              pathOptions={{
                color:
                  zone.risk > 70
                    ? "red"
                    : zone.risk > 40
                    ? "orange"
                    : "green",
              }}
            />
          ))}

        {data.zones &&
          data.zones.map((zone, index) => (
            <Marker key={index} position={[zone.lat, zone.lng]}>
              <Popup>
                <b>{zone.name}</b>
                <br />
                Risk Level: {zone.risk}%
              </Popup>
            </Marker>
          ))}
      </MapContainer>
    </div>
  );
}

function Card({ title, value }) {
  return (
    <div
      style={{
        background: "#1e293b",
        padding: "15px",
        borderRadius: "10px",
        minWidth: "160px",
      }}
    >
      <h4>{title}</h4>
      <h2>{value}</h2>
    </div>
  );
}

export default App;