import sys
import os
sys.path.insert(0, os.path.abspath("."))
import subprocess
import time
import urllib.request
import re

print("Testing direct streamlit output...")
res = subprocess.run([
    sys.executable, "-m", "streamlit", "version"
], capture_output=True, text=True)
print("Streamlit version:", res.stdout.strip())

# Check app.py compilation and import
import src.dashboard.app as app
print("src.dashboard.app successfully imported without errors!")
