from flakiness_analyser.utils import load_playwright_report, export_csv
from flakiness_analyser.analyser import FlakeAnalyser
def test_full_pipeline(tmp_path):
    input_file = tmp_path / "results.json"
    output_file = tmp_path / "report.csv"
    input_file.write_text(
          """
    {
        "runs": [
            {
                "tests": [
                    {
                        "nodeid": "test_login",
                        "outcome": "passed",
                        "rerun": 0
                    }
                ]
            },
            {
                "tests": [
                    {
                        "nodeid": "test_login",
                        "outcome": "failed",
                        "rerun": 0
                    }
                ]
            },
            {
                "tests": [
                    {
                        "nodeid": "test_login",
                        "outcome": "passed",
                        "rerun": 0
                    }
                ]
            }
        ]
    }
    """
    )
    runs = load_playwright_report(input_file)
    analyser = FlakeAnalyser(runs)
    report = analyser.calculate_flakiness()
    
    export_csv(report,output_file)
    content = output_file.read_text()
    assert "test_login" in content
    assert len(runs) == 3
    assert report[0]["runs"] == 3 
    assert report[0]["failures"] == 1
# come back ot this test



    