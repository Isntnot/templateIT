#!/usr/bin/env python3
from argprs import parser
from tps import getTemplateTps, getTPS
from utils.creation import createFile
from utils.dirmatching import matchDir
from utils.templater import process_templater
import os
from pathlib import Path

CURRENT_DIR = Path(os.getcwd())
MAX_DEEP = 3

# 1. Find the tps file walking up parent directories
target = CURRENT_DIR
tps = []

for _ in range(MAX_DEEP):
    tps = getTPS(target)  # Pass 'target' so it checks the current parent level
    if tps:
        break
    target = target.parent

if not tps:
    raise FileNotFoundError("[TEMPLATEIT] A template.txt was not found in folders up to its parent limit.")

# 2. Get mapping and parse arguments
d2t = getTemplateTps(tps[0])
args = parser.parse_args()
file = Path(args.filename).resolve() # Resolve to ensure absolute path matching

template = None
tps_dir = tps[0].parent  # The directory where the .tps file is located

for d, t in d2t.items():
    # If 'd' is a relative path in the config, anchor it to the .tps file's location
    d_path = Path(d)
    if not d_path.is_absolute():
        d_path = (tps_dir / d_path).resolve()
    else:
      d_path = d_path.resolve()

    if matchDir(d_path, file):
        template = t
        break  # Stop at the first valid match

if not template:
    raise FileNotFoundError(f"[TEMPLATEIT] No matching template directory found for file: {file}")

# 4. Read template and create file
with open(str(template), "r") as f:
    source = f.read()
createFile(args.filename, process_templater(source, file.name))
