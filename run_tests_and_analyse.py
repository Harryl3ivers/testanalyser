import subprocess
from flakiness_analyser.analyser import FlakeAnalyser
from flakiness_analyser.utils import load_playwright_report, export_csv

ECOMMERCE_PYTEST = r"../testanalyser/venv/Scripts/pytest.exe"

report_files = []

for i in range(3):
    filename = f"reports/run{i+1}.json"
    report_files.append(filename)

    subprocess.run([
        ECOMMERCE_PYTEST,
        "../testanalyser/tests",
        "--json-report",
        f"--json-report-file={filename}"
    ])


runs = load_playwright_report(report_files)

analyser = FlakeAnalyser(runs)

report = analyser.calculate_flakiness()

print("\n=== FLAKINESS REPORT ===\n")

for item in report:
    print(f"{item['test']}")
    print(f"  Score: {item['score']}")
    print(f"  Status: {item['classification']}")
    print(f"  Pattern: {item['patterns']}")
    print(f"  Runs: {item['runs']} | Failures: {item['failures']} | Retries: {item['retries']}")
    print()

export_csv(report, "reports/flake_report.csv")

print("Flakiness report exported to reports/flake_report.csv")