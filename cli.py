from flakiness_analyser.analyser import FlakeAnalyser
from flakiness_analyser.utils import load_json,export_csv,load_playwright_report
import argparse
def main():
    parser = argparse.ArgumentParser(description="flaky test analyser")
    parser.add_argument("input",help="path to json results file")
    parser.add_argument("--csv",help="export report to csv file")
    parser.add_argument("--playwright",help="convert playwright report")
    parser.add_argument("--min-score",type=float,default=0.0,help="filter test")
    args = parser.parse_args()
    if args.playwright:
        runs = load_playwright_report(args.input)
    else:
        runs = load_json(args.input)
    analyser = FlakeAnalyser(runs)
    report = analyser.calculate_flakiness()
    prnt_table(report)
    if args.csv:
        export_csv(report,args.csv)
        print(f"\nReport exported to {args.csv}")


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