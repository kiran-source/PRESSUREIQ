import hashlib
import glob
import os

raw_dir = "SupeRR Selector Season 2 _ Problem Statement _ Data Pack/SupeRR Selector Season 2 _ Data Pack"
files = sorted(glob.glob(os.path.join(raw_dir, "*.csv")))

print(f"Found {len(files)} raw CSV files:")
for f in files:
    h = hashlib.sha256()
    with open(f, "rb") as fp:
        while chunk := fp.read(8192 * 1024):
            h.update(chunk)
    size_mb = os.path.getsize(f) / (1024 * 1024)
    print(f"- {os.path.basename(f)} ({size_mb:.2f} MB): {h.hexdigest()}")
