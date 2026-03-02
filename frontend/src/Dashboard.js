import { useState, useEffect } from "react";
import axios from "axios";
import KPICards from "./KPICards";
import MapView from "./MapView";
import ChartView from "./ChartView";

export default function Dashboard() {
  const [students, setStudents] = useState(300);
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get(`http://127.0.0.1:8000/dashboard?students=${students}`)
      .then(res => setData(res.data));
  }, [students]);

  if (!data) return <div>Loading...</div>;

  return (
    <div style={{ padding: 20 }}>
      <h1>🎯 Smart Campus Command Center</h1>

      <input
        type="range"
        min="100"
        max="600"
        value={students}
        onChange={e => setStudents(e.target.value)}
      />
      <p>Students: {students}</p>

      <KPICards data={data} />
      <MapView zones={data.zones} />
      <ChartView trend={data.trend} />
    </div>
  );
}