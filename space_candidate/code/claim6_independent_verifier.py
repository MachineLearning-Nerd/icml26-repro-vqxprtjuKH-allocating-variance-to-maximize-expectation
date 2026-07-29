"""Standalone evaluator-visible verifier for independent Claim 6 evidence."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative-control", action="store_true")
    args = parser.parse_args()
    if args.negative_control:
        artificial = [0.10, 0.28, 0.41, 0.64, 0.82, 1.02, 1.20, 1.45]
        second = [
            artificial[i + 2] - 2 * artificial[i + 1] + artificial[i]
            for i in range(len(artificial) - 2)
        ]
        rejected = any(value > 0.0 for value in second)
        print(
            json.dumps(
                {
                    "status": (
                        "REJECTED_INVALID_SUBSTITUTE"
                        if rejected
                        else "UNEXPECTED"
                    ),
                    "second_differences": second,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 1 if rejected else 0

    payload = json.loads(
        (ROOT / "raw" / "claim6_independent_output.json").read_text(
            encoding="utf-8"
        )
    )
    with (
        ROOT / "raw" / "claim6_independent_population.csv"
    ).open(newline="", encoding="utf-8") as handle:
        population = list(csv.DictReader(handle))
    with (
        ROOT / "raw" / "claim6_independent_concavity.csv"
    ).open(newline="", encoding="utf-8") as handle:
        concavity = list(csv.DictReader(handle))
    with (
        ROOT / "raw" / "claim6_independent_finite_m.csv"
    ).open(newline="", encoding="utf-8") as handle:
        finite = list(csv.DictReader(handle))

    passed = (
        payload["status"] == "VERIFIED"
        and payload["primary"]["status"] == "VERIFIED"
        and payload["independent_checker"]["passed"] is True
        and payload["negative_control"]["status"]
        == "REJECTED_INVALID_SUBSTITUTE"
        and len(population) == 48
        and len(concavity) == 36
        and len(finite) == 144
        and all(
            row["consistent_with_concavity"] == "true" for row in concavity
        )
        and all(row["agrees_with_population"] == "true" for row in finite)
    )
    print(
        json.dumps(
            {
                "status": "VERIFIED" if passed else "BLOCKED",
                "population_rows": len(population),
                "concavity_rows": len(concavity),
                "finite_m_rows": len(finite),
                "checker_passed": payload["independent_checker"]["passed"],
                "exact_published_plot_regeneration": "BLOCKED",
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
