"""Independent CSV checker for the Figure 1 digitization."""

from __future__ import annotations

import csv
from pathlib import Path


RAW = Path(".openresearch/artifacts/claim_6/raw_digitized_payoff.csv")


def check_digitized_payoff() -> dict[str, object]:
    series: dict[str, list[float]] = {}
    with RAW.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            series.setdefault(row["series"], []).append(float(row["pixel_y"]))
    rows: list[dict[str, object]] = []
    passed = True
    for name, values in series.items():
        second = [
            values[index + 2] - 2 * values[index + 1] + values[index]
            for index in range(len(values) - 2)
        ]
        expected = (
            all(value >= 0.0 for value in second)
            if name == "independent"
            else min(second) == -3.0
        )
        passed &= expected
        rows.append(
            {
                "series": name,
                "pixel_y": values,
                "pixel_second_differences": second,
                "passed": expected,
            }
        )
    return {
        "checker": "independent CSV parse and finite differences",
        "passed": passed and set(series) == {"independent", "negative"},
        "rows": rows,
    }
