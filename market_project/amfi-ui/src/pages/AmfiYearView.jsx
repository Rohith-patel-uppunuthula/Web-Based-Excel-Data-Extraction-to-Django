import { useEffect, useState } from "react";
import { fetchYearPivot } from "../api/amfi";

// 🔹 Month formatter (DB stays YYYY-MM, UI shows human format)
function formatMonth(month) {
  const [year, m] = month.split("-");
  const names = [
    "Jan","Feb","Mar","Apr","May","Jun",
    "Jul","Aug","Sep","Oct","Nov","Dec"
  ];
  return `${names[Number(m) - 1]} ${year}`;
}

export default function AmfiYearView() {
  const [year, setYear] = useState("2025");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);

    fetchYearPivot(year)
      .then((res) => {
        console.log("API DATA:", res); // debugging
        setData(res);
      })
      .catch((err) => {
        console.error("API ERROR:", err);
        setData(null);
      })
      .finally(() => setLoading(false));
  }, [year]);

  if (loading) {
    return <p style={{ padding: 20 }}>Loading…</p>;
  }

  if (!data) {
    return <p style={{ padding: 20 }}>No data available</p>;
  }

  const { months, categories, matrix } = data;

  return (
    <div style={{ padding: 20 }}>
      <h2>AMFI Category-wise Monthly Values</h2>

      <label>
        Select Year:&nbsp;
        <select value={year} onChange={(e) => setYear(e.target.value)}>
          <option value="2025">2025</option>
          <option value="2024">2024</option>
          <option value="2023">2023</option>
        </select>
      </label>

      <div style={{ overflowX: "auto", marginTop: 20 }}>
        <table border="1" cellPadding="6" cellSpacing="0">
          <thead>
            <tr>
              <th>Month</th>
              {categories.map((cat) => (
                <th key={cat}>{cat}</th>
              ))}
            </tr>
          </thead>

          <tbody>
            {months.map((month) => (
              <tr key={month}>
                <td><strong>{formatMonth(month)}</strong></td>

                {categories.map((cat) => {
                  const value = matrix[month]?.[cat];

                  return (
                    <td
                      key={cat}
                      style={{
                        color: value < 0 ? "red" : "green",
                        textAlign: "right",
                      }}
                    >
                      {value !== undefined ? value.toFixed(2) : "-"}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
