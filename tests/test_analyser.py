import pytest
from flakiness_analyser.analyser import FlakeAnalyser
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
    assert report[0]["classification"] == "CONSISTENT_FAILURE"

def test_mixed_results():
    runs = [
         {"results": [{"name": "test1", "status": "passed", "retries": 0}]},
        {"results": [{"name": "test1", "status": "failed", "retries": 1}]}
    ]
    analyser = FlakeAnalyser(runs)
    report = analyser.calculate_flakiness()
    assert report[0]["classification"] == "SUSPICIOUS"

def test_intermittent():
    results = [
        {"status": "passed"},
        {"status": "failed"},
        {"status": "passed"},
    ]
    analyser = FlakeAnalyser([{"results": results}])
    pattern  = analyser.identify_patterns(results)
    assert pattern == "INTERMITTENT"

def test_empty_runs():
    analyser = FlakeAnalyser([])
    report = analyser.calculate_flakiness()
    assert report == []

@pytest.mark.parametrize("runs,expected_classification",[
    ([{"results": [{"name": "test1", "status": "passed", "retries": 0}]}], "STABLE"),
    ([{"results": [{"name": "test1", "status": "failed", "retries": 0}]}], "CONSISTENT_FAILURE"),
    ([
    {"results": [{"name": "test1", "status": "passed", "retries": 0}]},
    {"results": [{"name": "test1", "status": "failed", "retries": 1}]}
], "SUSPICIOUS")
])
def test_flake_classification(runs,expected_classification):
    analyser = FlakeAnalyser(runs)
    report = analyser.calculate_flakiness()
    assert report[0]["classification"] == expected_classification

def test_flaky_test():
    runs = [
        {"results": [{"name": "test1", "status": "passed", "retries": 0}]},
        {"results": [{"name": "test1", "status": "failed", "retries": 0}]},
        {"results": [{"name": "test1", "status": "failed", "retries": 0}]},
    ]

    analyser = FlakeAnalyser(runs)
    report = analyser.calculate_flakiness()

    assert report[0]["classification"] == "FLAKY"


# def test_50_percent_failure():
#     pass