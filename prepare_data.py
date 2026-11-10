"""Week 3: read the UCI file, check it, and save a balanced sample as data/urls.csv.

Run once:  python prepare_data.py
"""
import sys
from pathlib import Path
from urllib.parse import urlsplit

import pandas as pd

from settings import RANDOM_STATE, SAMPLE_PER_CLASS
from urlfeatures import check_url

RAW = Path("data/raw/PhiUSIIL_Phishing_URL_Dataset.csv")
OUT = Path("data/urls.csv")


def stop(message):
    print("ERROR:", message)
    sys.exit(1)


if not RAW.exists():
    stop(f"Missing file: {RAW}. Copy the CSV into data/raw (see PUT_UCI_FILE_HERE.txt).")

header = pd.read_csv(RAW, nrows=0).columns.tolist()
for col in ("URL", "label"):
    if col not in header:
        stop(f"The column {col} was not found. Columns in the file: {header[:12]} ... Is this the PhiUSIIL file?")
df = pd.read_csv(RAW, usecols=["URL", "label"])
print("Rows read:", len(df))
if df["label"].isin([0, 1]).sum() != len(df):
    stop("The label column has values other than 0 and 1.")

# In this dataset label 1 = legitimate and label 0 = phishing. We store the opposite
# (is_phishing = 1 for phishing) because phishing is the class we want to catch.
df["is_phishing"] = (df["label"] == 0).astype(int)
df = df.drop(columns="label").dropna().drop_duplicates(subset="URL")
df["URL"] = df["URL"].astype(str).str.strip()

# keep only the addresses the website would also accept
ok = df["URL"].map(lambda u: check_url(u)[1] is None)
print(f"Removed {int((~ok).sum())} addresses that do not pass the website's address check.")
df = df[ok]

take = []
for value, name in ((1, "phishing"), (0, "legitimate")):
    part = df[df["is_phishing"] == value]
    n = min(SAMPLE_PER_CLASS, len(part))
    print(f"{name}: {len(part)} available, {n} taken")
    take.append(part.sample(n=n, random_state=RANDOM_STATE))
out = pd.concat(take).sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)
out = out.rename(columns={"URL": "url"})
out["host"] = out["url"].map(lambda u: (urlsplit(u).hostname or "").lower())

OUT.parent.mkdir(exist_ok=True)
out.to_csv(OUT, index=False)
print(f"Saved {len(out)} URLs to {OUT}")
print("Different hosts:", out["host"].nunique())
print()
print("Check that the labels make sense (read them, do NOT open them):")
for value, name in ((1, "PHISHING"), (0, "LEGITIMATE")):
    print(f"--- 5 {name} examples")
    for u in out[out["is_phishing"] == value]["url"].head(5):
        print("   ", u[:100])
