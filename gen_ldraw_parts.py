import csv
import os

ldraw_path = '/usr/share/ldraw'

count = 0
with open('parts.csv') as parts:
    for row in csv.DictReader(parts):
        exists = os.path.exists(f"{ldraw_path}/parts/{row['part_num']}.dat")
        if exists:
            print(row)
            count += 1

print(count)
        