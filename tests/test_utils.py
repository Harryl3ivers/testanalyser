from flakiness_analyser.utils import load_json, load_playwright_report,export_csv
import json
import pytest

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

    runs = load_playwright_report([file])

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

def test_load_invalid_json(tmp_path):
    file = tmp_path / "report.csv"
    file.write_text("this is not valid json")
    with pytest.raises(json.JSONDecodeError):
        load_json(file)


def test_load_multiple_playwright_reports(tmp_path):
    file1 = tmp_path / "run1.json"
    file2 = tmp_path / "run2.json"

    file1.write_text("""
    {
        "tests": [
            {
                "nodeid": "test_login",
                "outcome": "passed",
                "rerun": 0
            }
        ]
    }
    """)

    file2.write_text("""
    {
        "tests": [
            {
                "nodeid": "test_login",
                "outcome": "failed",
                "rerun": 0
            }
        ]
    }
    """)

    runs = load_playwright_report([file1, file2])

    assert len(runs) == 2
    assert runs[0]["results"][0]["status"] == "passed"
    assert runs[1]["results"][0]["status"] == "failed"