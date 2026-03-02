export default function KPICards({ data }) {
  return (
    <div style={{ display: "flex", gap: 20 }}>
      <div>🚦 Congestion: {data.congestion.toFixed(2)}</div>
      <div>⚡ Energy: {data.energy_usage}</div>
      <div>💧 Water: {data.water_usage}</div>
    </div>
  );
}