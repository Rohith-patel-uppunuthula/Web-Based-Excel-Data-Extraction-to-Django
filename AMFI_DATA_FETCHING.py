import requests
from pathlib import Path

BASE_URL = "https://portal.amfiindia.com/spages"
YEAR = 2025
MONTHS = [
    "jan","feb","mar","apr","may","jun",
    "jul","aug","sep","oct","nov","dec"
]

DOWNLOAD_DIR = Path("amfi_downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

for month in MONTHS:
    filename = f"am{month}{YEAR}repo.xls"
    url = f"{BASE_URL}/{filename}"
    file_path = DOWNLOAD_DIR / filename

    print(f"Checking {filename}...")

    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200 and r.content:
            with open(file_path, "wb") as f:
                f.write(r.content)
            print(f" Downloaded: {filename}")
        else:
            print(f" Not available: {filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

print("Done.")
