"""Standalone visibility verifier for the four-route Claim 6 audit."""

import argparse
import csv
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative-control", action="store_true")
    args = parser.parse_args()
    if args.negative_control:
        pixel_y = [1000.0, 800.0, 650.0, 530.0, 400.0]
        second = [
            pixel_y[index + 2] - 2 * pixel_y[index + 1] + pixel_y[index]
            for index in range(len(pixel_y) - 2)
        ]
        rejected = any(value < 0 for value in second)
        print(
            json.dumps(
                {
                    "status": (
                        "REJECTED_NONCONCAVE_SERIES"
                        if rejected
                        else "UNEXPECTED"
                    ),
                    "pixel_y": pixel_y,
                    "second_differences": second,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 1 if rejected else 0
    raw = Path(__file__).resolve().parents[1] / "raw" / "claim6_digitized_payoff.csv"
    with raw.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    series = {}
    for row in rows:
        series.setdefault(row["series"], []).append(float(row["pixel_y"]))
    second = {
        name: [
            values[i + 2] - 2 * values[i + 1] + values[i]
            for i in range(len(values) - 2)
        ]
        for name, values in series.items()
    }
    passed = (
        all(value >= 0 for value in second["independent"])
        and min(second["negative"]) == -3.0
    )
    print(
        json.dumps(
            {
            "status": "BLOCKED",
            "checker_passed": passed,
            "routes_complete": 4,
            "pixel_second_differences": second,
            "blocker": (
                "m, seeds, sample count, optimizer, stopping rule, raw values "
                "and uncertainty are not public"
            ),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
