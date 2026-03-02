import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
} from "chart.js";

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement);

export default function ChartView({ trend }) {
  const data = {
    labels: trend.map((_, i) => i),
    datasets: [{
      label: "Predicted Congestion",
      data: trend
    }]
  };

  return <Line data={data} />;
}