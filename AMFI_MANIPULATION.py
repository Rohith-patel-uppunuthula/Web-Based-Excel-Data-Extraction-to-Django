import pandas as pd
from pathlib import Path

# ==========================
# CONFIG
# ==========================
input_dir = Path("amfi_downloads")
output_dir = Path("extracted_growth_equity")
output_dir.mkdir(exist_ok=True)

START_KEYWORDS = ["growth", "equity", "oriented"]
END_KEYWORDS = ["sub total", "subtotal", "sub-total"]

HEADER_KEYWORDS = [
    "scheme", "schemes",
    "net", "assets",
    "aum",
    "rs.", "₹"
]

# ==========================
# PROCESS FILES
# ==========================
for file in input_dir.iterdir():
    if file.suffix not in [".xls", ".xlsx"]:
        continue

    print(f"\nProcessing {file.name}")

    # --------------------------
    # READ EXCEL (robust)
    # --------------------------
    try:
        df_raw = pd.read_excel(file, header=None, engine="openpyxl")
    except Exception:
        try:
            df_raw = pd.read_excel(file, header=None, engine="xlrd")
        except Exception as e:
            print(f"  ❌ Failed to read file: {e}")
            continue

    df_raw = df_raw.astype(str)

    # --------------------------
    # DETECT HEADER ROW
    # --------------------------
    header_row = None
    for i, row in df_raw.iterrows():
        row_text = " ".join(row).lower()
        if any(k in row_text for k in HEADER_KEYWORDS):
            header_row = i
            break

    if header_row is None:
        print("  ❌ Header row not found")
        continue

    # --------------------------
    # FIX HEADERS
    # --------------------------
    df = df_raw.copy()
    df.columns = df.iloc[header_row]
    df = df.iloc[header_row + 1:].reset_index(drop=True)

    # remove junk columns
    df = df.loc[:, df.columns.notna()]
    df = df.loc[:, ~df.columns.astype(str).str.contains("nan", case=False)]

    df_str = df.astype(str)

    # --------------------------
    # FIND START ROW
    # --------------------------
    start_idx = None
    for i, row in df_str.iterrows():
        if all(k in " ".join(row).lower() for k in START_KEYWORDS):
            start_idx = i
            break

    # --------------------------
    # FIND END ROW
    # --------------------------
    end_idx = None
    for i in range(start_idx + 1 if start_idx is not None else 0, len(df)):
        if any(k in " ".join(df_str.iloc[i]).lower() for k in END_KEYWORDS):
            end_idx = i
            break

    if start_idx is None or end_idx is None:
        print("  ❌ Growth / Equity section not found")
        continue

    # --------------------------
    # SLICE SECTION
    # --------------------------
    section_df = df.iloc[start_idx:end_idx + 1].copy()

    # --------------------------
    # REMOVE CATEGORY HEADER ROWS
    # --------------------------
    numeric_cols = [
        col for col in section_df.columns
        if col not in ["Sr", "Scheme Name"]
    ]

    section_df = section_df.dropna(
        subset=numeric_cols,
        how="all"
    )

    # --------------------------
    # FINAL CLEANUP
    # --------------------------
    section_df = section_df.loc[:, section_df.columns.notna()]
    section_df = section_df.reset_index(drop=True)

    # --------------------------
    # SAVE
    # --------------------------
    output_file = output_dir / f"{file.stem}_growth_equity.xlsx"
    section_df.to_excel(output_file, index=False)

    print(f"  ✅ Saved → {output_file.name}")

print("\n🎯 All files processed successfully.")
