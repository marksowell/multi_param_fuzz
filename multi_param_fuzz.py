# multi_param_fuzz.py

import requests
from urllib.parse import quote
import sys

TARGET = input("Target URL (without query string): ").strip()
PARAM_FILE = input("Path to params.txt: ").strip()
VALUE = input("Value to use (default: z>k): ").strip() or "z>k"

mode = input("How many params per request? (number or 'all'): ").strip()

with open(PARAM_FILE) as f:
    params = [line.strip() for line in f if line.strip()]

if mode.lower() == "all":
    group_size = len(params)
else:
    try:
        group_size = int(mode)
    except ValueError:
        print("Invalid input.")
        sys.exit(1)

print(f"\nSending {len(params)} params total, {group_size} per request\n")

for i in range(0, len(params), group_size):
    batch = params[i:i+group_size]
    query = "&".join(f"{p}={quote(VALUE)}" for p in batch)
    url = f"{TARGET}?{query}"

    print(f"[+] Sending batch {i//group_size + 1}")
    r = requests.get(url, timeout=10)
    print(f"    Status: {r.status_code} | Length: {len(r.text)}")