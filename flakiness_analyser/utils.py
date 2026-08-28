import json
import csv
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    print("DEBUG FILE:", file_path)
    print("DEBUG CONTENT:", repr(content))

    return json.loads(content)

def load_playwright_report(file_paths):
    runs = []

    for filepath in file_paths:
        data = load_json(filepath)

        results = []

        for test in data.get("tests", []):
            results.append({
                "name": test["nodeid"],
                "status": test["outcome"],
                "retries": test.get("rerun")
            })

        runs.append({"results": results})

    return runs
                 

def export_csv(report,filename):
    keys = ["test", "score", "classification", "patterns", "runs", "failures", "retries"]
    with open(filename,"w",newline="") as f:
        writer = csv.DictWriter(f,fieldnames=keys)
        writer.writeheader()
        for item in report:
            writer.writerow(item)