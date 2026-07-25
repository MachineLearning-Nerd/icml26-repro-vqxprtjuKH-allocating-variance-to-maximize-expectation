"""Independent checker for the Theorem 1.6 counterexample certificate."""

from __future__ import annotations

import csv
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / ".openresearch" / "artifacts" / "claim_4" / "raw_counterexample.csv"


def check_raw_certificate() -> dict[str, object]:
    with RAW.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    checks: list[bool] = []
    for row in rows:
        n = int(row["n"])
        m = int(row["m"])
        p = Fraction(row["p"])
        inv_p = int(row["one_over_p"])
        cap = int(row["max_possible_variables"])
        ratio = Fraction(row["max_over_one_over_p"])
        checks.extend(
            (
                m == n,
                p == Fraction(1, n * n),
                inv_p == n * n,
                cap == n,
                ratio == Fraction(1, n),
            )
        )

    ns = [int(row["n"]) for row in rows]
    ratios = [Fraction(row["max_over_one_over_p"]) for row in rows]
    monotone_to_zero = all(a > b for a, b in zip(ratios, ratios[1:]))
    doubled = all(b == 2 * a for a, b in zip(ns, ns[1:]))
    passed = bool(rows) and all(checks) and monotone_to_zero and doubled
    return {
        "checker": "independent CSV rational-arithmetic checker",
        "passed": passed,
        "row_count": len(rows),
        "last_ratio": str(ratios[-1]) if ratios else None,
        "reason": "N_large/(1/p_n) <= n/n^2 = 1/n tends to zero.",
    }

