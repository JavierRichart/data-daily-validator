from pathlib import Path

import pandas as pd

def load_file(file_path: str | Path) -> pd.DataFrame:

    path = Path(file_path)

    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)

    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)

    raise ValueError(f"Formato no compatible: {path.suffix}")