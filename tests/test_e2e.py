from flakiness_analyser.utils import load_playwright_report, export_csv
from flakiness_analyser.analyser import FlakeAnalyser
def test_full_pipeline(tmp_path):
    file1 =tmp_path/ "run1.json"
    file2 =tmp_path/ "run2.json"
    file3 = tmp_path/ "run3.json"
    output = tmp_path / "report.csv"

    file1.write_text(""" { "tests": [ { "nodeid": "test_login", "outcome": "passed", "rerun": 0 } ] } """)
    file2.write_text(""" { "tests": [ { "nodeid": "test_login", "outcome": "failed", "rerun": 0 } ] } """) 
    file3.write_text(""" { "tests": [ { "nodeid": "test_login", "outcome": "passed", "rerun": 0 } ] } """)
    runs = load_playwright_report([file1,file2,file3])
    analyser =FlakeAnalyser(runs)
    report = analyser.calculate_flakiness()
    export_csv(report,output)

    content = output.read_text() 
    assert "test_login" in content 
    assert "INTERMITTENT" in content 
    assert len(runs) == 3
   



    