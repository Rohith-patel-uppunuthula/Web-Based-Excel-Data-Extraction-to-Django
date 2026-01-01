function YearSelector({ year, setYear }) {
  const startYear = 2020;
  const currentYear = new Date().getFullYear();

  const years = [];
  for (let y = startYear; y <= currentYear; y++) {
    years.push(y.toString());
  }

  return (
    <select value={year} onChange={(e) => setYear(e.target.value)}>
      <option value="">Select Year</option>
      {years.map((y) => (
        <option key={y} value={y}>
          {y}
        </option>
      ))}
    </select>
  );
}

export default YearSelector;
