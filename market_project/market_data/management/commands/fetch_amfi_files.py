import requests
import pandas as pd
from pathlib import Path
from django.core.management.base import BaseCommand
from datetime import datetime
from market_data.models import AmfiMonthlyData

# =========================
# CONFIG
# =========================
BASE_URL = "https://portal.amfiindia.com/spages"

DOWNLOAD_DIR = Path("amfi_downloads")
EXTRACTED_DIR = Path("extracted_growth_equity")

MONTHS = [
    "jan", "feb", "mar", "apr", "may", "jun",
    "jul", "aug", "sep", "oct", "nov", "dec"
]

START_KEYWORDS = ["growth", "equity", "oriented"]
END_KEYWORDS = ["sub total", "subtotal", "sub-total"]
HEADER_KEYWORDS = ["scheme", "net", "assets", "aum", "rs.", "₹"]


class Command(BaseCommand):
    help = "AMFI full pipeline: download → extract → store in DB"

    def handle(self, *args, **options):
        DOWNLOAD_DIR.mkdir(exist_ok=True)
        EXTRACTED_DIR.mkdir(exist_ok=True)

        current_year = datetime.now().year

        for year in range(current_year, current_year - 5, -1):
            for month in MONTHS:
                filename = f"am{month}{year}repo.xls"
                file_path = DOWNLOAD_DIR / filename
                url = f"{BASE_URL}/{filename}"

                # ---------------- DOWNLOAD ----------------
                if not file_path.exists():
                    try:
                        r = requests.get(url, timeout=30)
                        if r.status_code == 200 and r.content:
                            with open(file_path, "wb") as f:
                                f.write(r.content)
                        else:
                            continue
                    except requests.exceptions.RequestException:
                        continue

                # ---------------- READ EXCEL ----------------
                try:
                    df_raw = pd.read_excel(file_path, header=None)
                except Exception:
                    continue

                df_raw = df_raw.astype(str)

                # ---------------- FIND HEADER ----------------
                header_row = None
                for i, row in df_raw.iterrows():
                    if any(k in " ".join(row).lower() for k in HEADER_KEYWORDS):
                        header_row = i
                        break

                if header_row is None:
                    continue

                df = df_raw.copy()
                df.columns = df.iloc[header_row]
                df = df.iloc[header_row + 1:].reset_index(drop=True)
                df = df.loc[:, df.columns.notna()]
                df_str = df.astype(str)

                # ---------------- FIND SECTION ----------------
                start_idx, end_idx = None, None

                for i, row in df_str.iterrows():
                    if all(k in " ".join(row).lower() for k in START_KEYWORDS):
                        start_idx = i
                        break

                if start_idx is not None:
                    for i in range(start_idx + 1, len(df_str)):
                        if any(k in " ".join(df_str.iloc[i]).lower() for k in END_KEYWORDS):
                            end_idx = i
                            break

                if start_idx is None or end_idx is None:
                    continue

                section_df = df.iloc[start_idx:end_idx].copy()
                section_df = section_df.dropna(how="all").reset_index(drop=True)

                # ---------------- STORE INTO DB ----------------
                month_label = f"{month.capitalize()} {year}"

                for _, row in section_df.iterrows():
                    scheme = str(row.iloc[1]).strip()
                    net_inflow = row.iloc[6]

                    if (
                        "sub total" in scheme.lower()
                        or "growth/equity" in scheme.lower()
                        or pd.isna(net_inflow)
                    ):
                        continue

                    try:
                        net_inflow = float(net_inflow)
                    except ValueError:
                        continue

                    AmfiMonthlyData.objects.update_or_create(
                        month=month_label,
                        scheme_category=scheme,
                        defaults={"net_inflow": net_inflow},
                    )

        self.stdout.write(self.style.SUCCESS("🎯 AMFI DOWNLOAD → DB PIPELINE COMPLETE"))
