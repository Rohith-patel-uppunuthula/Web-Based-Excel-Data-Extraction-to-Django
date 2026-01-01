import pandas as pd
from market_data.models import AmfiMonthlyData

EXCEL_PATH = "data/amnov2025repo_growth_equity.xlsx"
MONTH = "November 2025"

def run():
    df = pd.read_excel(EXCEL_PATH)

    print("Columns:", list(df.columns))

    for _, row in df.iterrows():
        scheme = str(row.iloc[1]).strip()   # Scheme Name
        net_inflow_val = row.iloc[6]        # Net Inflow column

        # 🚫 Skip section headers / totals / junk rows
        if (
            "Sub Total" in scheme
             or "Growth/Equity Oriented Schemes" in scheme
             or pd.isna(net_inflow_val)
        ):
            continue

        AmfiMonthlyData.objects.update_or_create(
            month=MONTH,
            scheme_category=scheme,
            defaults={
                "net_inflow": float(net_inflow_val)
            }
        )

    print("✅ AMFI data loaded into DB successfully")
