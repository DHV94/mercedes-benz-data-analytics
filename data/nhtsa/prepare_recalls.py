"""Prepare the real NHTSA recall file for the bronze layer.

Input : data/nhtsa/raw/FLAT_RCL_POST_2010.zip  (public NHTSA flat file, tab separated, all makes)
Output: data/nhtsa/prepared/mb_recalls_2021_2025.csv  (only what the project needs)

What it does (and nothing more - the cleaning is dbt's job):
  - keeps Mercedes-Benz / Mercedes-Maybach VEHICLE recalls (RCLTYPECD = 'V')
  - keeps model years 2021-2025, the same years as the sales data
  - keeps 9 columns and writes them as a comma separated CSV with a header, text as it comes

Run from the repo root:  python data/nhtsa/prepare_recalls.py
"""
import csv
import io
import zipfile
from pathlib import Path

SRC = Path("data/nhtsa/raw/FLAT_RCL_POST_2010.zip")
OUT = Path("data/nhtsa/prepared/mb_recalls_2021_2025.csv")
YEARS = {"2021", "2022", "2023", "2024", "2025"}

# Field numbers come from data/nhtsa/raw/RCL.txt (position - 1)
COLUMNS = {
    "record_id": 0,
    "campno": 1,
    "maketxt": 2,
    "modeltxt": 3,
    "yeartxt": 4,
    "compname": 6,
    "potaff": 11,
    "rcdate": 15,
}


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    kept = 0
    with zipfile.ZipFile(SRC) as z, z.open(z.namelist()[0]) as raw, OUT.open("w", newline="", encoding="utf-8") as out:
        writer = csv.writer(out)
        writer.writerow(COLUMNS.keys())
        for line in io.TextIOWrapper(raw, encoding="latin-1"):
            p = line.rstrip("\n").split("\t")
            if len(p) < 17:
                continue
            if p[2].upper().startswith("MERCEDES") and p[10] == "V" and p[4] in YEARS:
                writer.writerow([p[i].strip() for i in COLUMNS.values()])
                kept += 1
    print(f"{kept} rows written to {OUT}")


if __name__ == "__main__":
    main()
