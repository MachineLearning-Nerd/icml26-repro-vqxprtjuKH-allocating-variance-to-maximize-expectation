"""Exact quantifier counterexample for Theorem 1.6 as written.

The theorem does not constrain how the Erdős–Rényi edge probability p may
depend on n.  Along p_n = n^-2, Theta(1/p_n) = Theta(n^2) variables cannot
exist in an instance with only n variables.  This is a cardinality
contradiction and does not depend on numerical optimization.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction


def counterexample_rows() -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    for n in (8, 16, 32, 64, 128, 256, 512, 1024):
        p = Fraction(1, n * n)
        inverse_p = 1 / p
        rows.append(
            {
                "n": n,
                "m": n,
                "p": f"1/{n * n}",
                "one_over_p": int(inverse_p),
                "max_possible_variables": n,
                "max_over_one_over_p": f"1/{n}",
            }
        )
    return rows


def fixed_p_control_rows() -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    p = Fraction(1, 4)
    for n in (8, 16, 32, 64, 128, 256, 512, 1024):
        rows.append(
            {
                "n": n,
                "m": n,
                "p": "1/4",
                "one_over_p": 4,
                "max_possible_variables": n,
                "max_over_one_over_p": f"{n}/4",
            }
        )
    return rows


def verify_counterexample() -> dict[str, object]:
    rows = counterexample_rows()
    exact_identities = all(
        row["one_over_p"] == row["n"] ** 2
        and row["max_possible_variables"] == row["n"]
        and row["max_over_one_over_p"] == f"1/{row['n']}"
        for row in rows
    )
    # The proof obligation for a Theta(1/p) lower bound is: there exists a
    # constant c>0 for which N_large >= c/p eventually.  But N_large <= n,
    # and with p=n^-2, n/(1/p)=1/n -> 0.  Hence every c>0 is contradicted for
    # n>1/c.
    symbolic_limit = "lim_{n->infinity} n/(1/p_n) = lim 1/n = 0"
    return {
        "claim": "Theorem 1.6 exact unrestricted-p quantifier",
        "status": "FALSIFIED" if exact_identities else "BLOCKED",
        "assumption_audit": {
            "n_to_infinity": True,
            "m_to_infinity": True,
            "m_sequence": "m_n=n",
            "erdos_renyi_probability": "p_n=n^-2 in (0,1)",
            "number_of_variables": "n",
        },
        "proof": {
            "demanded_scale": "Theta(1/p_n)=Theta(n^2)",
            "absolute_cardinality_cap": "N_large <= n",
            "ratio": "N_large/(1/p_n) <= 1/n -> 0",
            "symbolic_limit": symbolic_limit,
        },
        "rows": rows,
    }


def verify_negative_control() -> dict[str, object]:
    rows = fixed_p_control_rows()
    # For fixed p=1/4, 1/p=4 and the cap n does not contradict a constant
    # number of large-variance variables.  This route must therefore reject
    # the purported counterexample.
    rejected = all(row["max_possible_variables"] >= row["one_over_p"] for row in rows)
    return {
        "control": "fixed p=1/4",
        "status": "REJECTED_AS_COUNTEREXAMPLE" if rejected else "UNEXPECTED",
        "reason": "The cardinality cap n is compatible with Theta(1/p)=Theta(4).",
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative-control", action="store_true")
    args = parser.parse_args()
    if args.negative_control:
        result = verify_negative_control()
        print(json.dumps(result, indent=2, sort_keys=True))
        # A negative-control invocation intentionally exits nonzero because it
        # is not a valid falsification.
        return 1
    result = verify_counterexample()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "FALSIFIED" else 2


if __name__ == "__main__":
    raise SystemExit(main())

