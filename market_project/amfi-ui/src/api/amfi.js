export async function fetchYearPivot(year) {
  const res = await fetch(
    `http://127.0.0.1:8000/api/amfi/year-summary/?year=${year}`
  );

  if (!res.ok) {
    const text = await res.text();
    console.error("Backend error:", text);
    throw new Error("Failed to fetch AMFI data");
  }

  return res.json();
}
