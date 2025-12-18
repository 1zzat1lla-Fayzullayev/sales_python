import csv
import os

def read_data(filename):
    path = os.path.join("database", filename)

    if not os.path.exists(path):
        return []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)
