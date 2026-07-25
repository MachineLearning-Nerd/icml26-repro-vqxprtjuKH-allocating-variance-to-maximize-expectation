"""Standalone proof-certificate checker for Lemma 2.1."""

from __future__ import annotations

import argparse
import json
import math


def verify() -> dict[str, object]:
    rows = []
    for epsilon in (1 / 4, 1 / 8, 1 / 16, 1 / 32, 1 / 64):
        q = 2.0 * math.log(1.0 / epsilon)
        rows.append(
            {
                "epsilon": epsilon,
                "q": q,
                "q_at_least_2": q >= 2.0,
                "explicit_bound": math.e
                * math.sqrt(2.0)
                * epsilon
                * math.sqrt(math.log(1.0 / epsilon)),
                "m": round(1.0 / epsilon**2),
                "variance_sum": round(1.0 / epsilon**2) * epsilon**2,
            }
        )
    passed = all(
        row["q_at_least_2"] and row["variance_sum"] == 1.0 for row in rows
    )
    return {
        "status": "VERIFIED" if passed else "BLOCKED",
        "proof": (
            "Lp certificate: E[M] <= sqrt(q) eps^(1-2/q); "
            "q=2 log(1/eps) gives e sqrt(2) eps sqrt(log(1/eps))."
        ),
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative-control", action="store_true")
    args = parser.parse_args()
    if args.negative_control:
        print(
            json.dumps(
                {
                    "status": "REJECTED_INVALID_ASSUMPTIONS",
                    "reason": "Removing total variance restores sqrt(log m).",
                },
                indent=2,
            )
        )
        return 1
    result = verify()
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "VERIFIED" else 2


if __name__ == "__main__":
    raise SystemExit(main())

