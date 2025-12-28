import pandas as pd
from pathlib import Path

input_dir = Path("amfi_downloads")
output_dir = Path("extracted_growth_equity")
output_dir.mkdir(exist_ok=True)

# flexible keywords
START_KEYWORDS = ["growth", "equity", "oriented"]
END_KEYWORDS = ["sub total", "subtotal", "sub-total"]

for file in input_dir.iterdir():
    if file.suffix not in [".xls", ".xlsx"]:
        continue

    print(f"Processing {file.name}")

    # -------- AUTO-DETECT EXCEL FORMAT --------
    try:
        # Try XLSX first (many .xls files are actually xlsx)
        df = pd.read_excel(file, header=None, engine="openpyxl")
    except Exception:
        try:
            # Fallback to true XLS
            df = pd.read_excel(file, header=None, engine="xlrd")
        except Exception as e:
            print(f" Failed to read {file.name}: {e}")
            continue

    df = df.astype(str)

    # -------- FIND START ROW (LOOSE MATCH) --------
    start_idx = None
    for i, row in df.iterrows():
        row_text = " ".join(row).lower()
        if all(k in row_text for k in START_KEYWORDS):
            start_idx = i
            break

    # -------- FIND END ROW (LOOSE MATCH) --------
    end_idx = None
    for i in range(start_idx + 1 if start_idx is not None else 0, len(df)):
        row_text = " ".join(df.iloc[i]).lower()
        if any(k in row_text for k in END_KEYWORDS):
            end_idx = i
            break

    if start_idx is None or end_idx is None:
        print(f" Section not found in {file.name}")
        continue

    # slice section
    section_df = df.loc[start_idx:end_idx].reset_index(drop=True)

    # save
    output_file = output_dir / f"{file.stem}_growth_equity.xlsx"
    section_df.to_excel(output_file, index=False, header=False)

    print(f"Saved → {output_file.name}")

print("\nAll files processed.")
