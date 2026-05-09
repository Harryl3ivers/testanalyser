import subprocess
from flakiness_analyser.analyser import FlakeAnalyser
from flakiness_analyser.utils import load_json, load_playwright_report,export_csv

ECOMMERCE_PYTEST = r"../ecommerce app/venv/Scripts/pytest.exe"

subprocess.run([
     ECOMMERCE_PYTEST,
    "../ecommerce app/tests",
    "--json-report",
    "--json-report-file=reports/test_results.json"
])
runs = load_playwright_report("reports/test_results.json")
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

# Step 5: Export CSV
export_csv(report, "reports/flake_report.csv")
print("Flakiness report exported to reports/flake_report.csv")