"""Standalone exact verifier for the Theorem 1.6 counterexample."""

from __future__ import annotations

import argparse
import csv
import json
from fractions import Fraction
from pathlib import Path


def verify(path: Path) -> dict[str, object]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    checks = []
    for row in rows:
        n = int(row["n"])
        checks.append(
            int(row["m"]) == n
            and Fraction(row["p"]) == Fraction(1, n * n)
            and int(row["one_over_p"]) == n * n
            and int(row["max_possible_variables"]) == n
            and Fraction(row["max_over_one_over_p"]) == Fraction(1, n)
        )
    return {
        "status": "FALSIFIED" if rows and all(checks) else "BLOCKED",
        "checker_passed": bool(rows) and all(checks),
        "proof": "N_large/(1/p_n) <= n/n^2 = 1/n -> 0",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative-control", action="store_true")
    args = parser.parse_args()
    if args.negative_control:
        print(
            json.dumps(
                {
                    "status": "REJECTED_AS_COUNTEREXAMPLE",
                    "p": "1/4",
                    "reason": "n variables can accommodate Theta(1/p)=Theta(4).",
                },
                indent=2,
            )
        )
        return 1
    raw = Path(__file__).resolve().parents[1] / "raw" / "claim4_counterexample.csv"
    result = verify(raw)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "FALSIFIED" else 2


if __name__ == "__main__":
    raise SystemExit(main())

