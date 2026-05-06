from analyser import FlakeAnalyser
from utils import load_json
import argparse
def main():
    parser = argparse.ArgumentParser(description="flaky test analyser")
    parser.add_argument("input",help="path to json results file")
    parser.add_argument("--csv",help="export report to csv file")
    parser.add_argument("--min-score",type=float,default=0.0,help="filter test")
    args = parser.parse_args()
    runs = load_json(args.input)
    analyser = FlakeAnalyser(runs)
    report = analyser.calculate_flakiness()
    prnt_table(report)


def prnt_table(report):
    print("FLAKINESS REPORT")
    for item in report:
        print(f"{item['test']}")
        print(f"  Score: {item['score']}")
        print(f"  Status: {item['classification']}")
        print(f"  Pattern: {item['patterns']}")
        print(f"  Runs: {item['runs']} | Failures: {item['failures']} | Retries: {item['retries']}")
        print()


if __name__ == "__main__":
    main()