from collections import defaultdict
from models import TestResults
class FlakeAnalyser:
    def __init__(self,runs):
        self.runs = runs
    
   
    
    def test_history(self):
        history = defaultdict(list)
        for run in self.runs:
            for test in run["results"]:
                history[test["name"]].append(test)
        return history
    
    def identify_patterns(self,results):
        statuses = [r["status"]for r in results]
        if all(s == "failed" for s in statuses):
            return "CONSISTENT_FAILURE"
        if all(s == "passed" for s in statuses):
            return "CONSISTENT_PASS"
        return "INTERMITTENT"

    
    def calculate_flakiness(self):
        history = self.test_history()
        report = []
        
        for test_name, results in history.items():
            total = len(results)
            pattern = self.identify_patterns(results)
            failures = sum(1 for r in results if r["status"] == "failed")  
            retries = sum(r["retries"] for r in results)
            failure_percent = failures / total if total else 0
            retry_percent = retries / total if total else 0
            score = (failure_percent * 0.6) + (retry_percent * 0.4)
            classification = (
                "FLAKY" if score > 0.5 else
                "SUSPICIOUS" if score  > 0.2 else                                             
                "STABLE"
            )

            report.append({ "test": test_name,
                "score": round(score, 3),
                "classification": classification,
                "patterns": pattern,
                "runs": total,
                "failures": failures,
                "retries": retries
                })
        return sorted(report,key=self.get_score,reverse=True)
            
    def get_score(self,x):
        return x["score"]





            #                 if score > 0.5:
#     classification = "FLAKY"
# elif score > 0.2:
#     classification = "SUSPICIOUS"
# else:
#     classification = "STABLE"