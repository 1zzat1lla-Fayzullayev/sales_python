import os
import csv

def read_data(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "..", "database", filename)

    path = os.path.abspath(path)

    if not os.path.exists(path):
        return []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)
