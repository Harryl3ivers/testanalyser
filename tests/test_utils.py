from flakiness_analyser.utils import load_json, load_playwright_report,export_csv
import json

def test_load_json(tmp_path):
    file = tmp_path / "results.json"
    file.write_text('{"test": "example"}')
    result = load_json(file)
    assert result["test"] == "example"

def test_load_playwright_report(tmp_path):
    file = tmp_path / "results.json"
    file.write_text(
         """
        {
            "tests": [
                {
                    "nodeid": "test_login",
                    "outcome": "passed",
                    "rerun": 0
                }
            ]
        }
        """

    )
    runs = load_playwright_report(file)
    assert len(runs) == 1
    assert runs[0]["results"][0]["name"] == "test_login"
    assert runs[0]["results"][0]["status"] == "passed"

def test_export_csv(tmp_path):
    file = tmp_path / "report.csv"
    report= [
        {
              "test": "test_login",
            "score": 0.5,
            "classification": "FLAKY",
            "patterns": "INTERMITTENT",
            "runs": 3,
            "failures": 2,
            "retries": 0
        }
    ]
    export_csv(report,file)
    content = file.read_text()
    assert "test_login" in content
    assert "FLAKY" in content