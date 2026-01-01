import { useState } from "react";
import YearSelector from "./components/YearSelector";

function App() {
  const [year, setYear] = useState("");

  return (
    <div style={{ padding: "20px" }}>
      <h1>AMFI Dashboard</h1>

      <YearSelector year={year} setYear={setYear} />

      {year && (
        <p style={{ marginTop: "10px" }}>
          Showing data for year: <strong>{year}</strong>
        </p>
      )}
    </div>
  );
}

export default App;
