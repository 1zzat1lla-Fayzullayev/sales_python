import json
import os

def read_data(filename):
    path = os.path.join("database", filename)

    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
