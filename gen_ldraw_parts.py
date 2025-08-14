"""Generate a list of all Rebrickable parts with ldraw models"""

import csv
import os

ldraw_path = "ldraw"

count = 0
with open("parts.csv") as parts:
    for row in csv.DictReader(parts):
        exists = os.path.exists(f"{ldraw_path}/parts/{row['part_num']}.dat")
        if exists:
            print(row["part_num"])
