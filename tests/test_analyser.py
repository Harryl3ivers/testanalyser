import pytest
from analyser import FlakeAnalyser
def test_all_passed():
    runs = [
        {"results": [{"name": "test1", "status": "passed", "retries": 0}]}
    ]
    analyser = FlakeAnalyser(runs)
    report = analyser.calculate_flakiness()
    assert report[0]["score"] == 0
    assert report[0]["classification"] == "STABLE"

def test_all_failed():
    runs = [
        {"results": [{"name": "test1", "status": "failed", "retries": 0}]}
    ]
    analyser = FlakeAnalyser(runs)
    report = analyser.calculate_flakiness()
    assert report[0]["classification"] == "FLAKY"

def test_mixed_results():
    runs = [
         {"results": [{"name": "test1", "status": "passed", "retries": 0}]},
        {"results": [{"name": "test1", "status": "failed", "retries": 1}]}
    ]
    analyser = FlakeAnalyser(runs)
    report = analyser.calculate_flakiness()
    assert report[0]["classification"] in ["SUSPICIOUS","FLAKY"]

def test_intermittent():
    results = [
        {"status": "passed"},
        {"status": "failed"},
        {"status": "passed"},
    ]
    analyser = FlakeAnalyser()
    pattern  = analyser.identify_patterns(results)
    assert pattern == "INTERMITTENT"

def test_empty_runs():
    analyser = FlakeAnalyser([])
    report = analyser.calculate_flakiness()
    assert report == []