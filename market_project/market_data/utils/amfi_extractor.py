import pandas as pd
from pathlib import Path

START_KEYWORDS = ["growth", "equity", "oriented"]
END_KEYWORDS = ["sub total", "subtotal", "sub-total"]
HEADER_KEYWORDS = ["scheme", "schemes", "net", "assets", "aum", "rs.", "₹"]

def extract_growth_equity(input_dir: Path, output_dir: Path):
    output_dir.mkdir(exist_ok=True)

    for file in input_dir.iterdir():
        if file.suffix not in [".xls", ".xlsx"]:
            continue

        output_file = output_dir / f"{file.stem}_growth_equity.xlsx"
        if output_file.exists():
            continue  # already processed

        try:
            df_raw = pd.read_excel(file, header=None)
        except Exception:
            continue

        df_raw = df_raw.astype(str)

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

        start_idx = None
        for i, row in df_str.iterrows():
            if all(k in " ".join(row).lower() for k in START_KEYWORDS):
                start_idx = i
                break

        end_idx = None
        for i in range(start_idx + 1 if start_idx else 0, len(df)):
            if any(k in " ".join(df_str.iloc[i]).lower() for k in END_KEYWORDS):
                end_idx = i
                break

        if start_idx is None or end_idx is None:
            continue

        section_df = df.iloc[start_idx:end_idx].copy()
        section_df = section_df.dropna(how="all").reset_index(drop=True)
        section_df.to_excel(output_file, index=False)
