import json
import csv
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    print("DEBUG FILE:", file_path)
    print("DEBUG CONTENT:", repr(content))

    return json.loads(content)