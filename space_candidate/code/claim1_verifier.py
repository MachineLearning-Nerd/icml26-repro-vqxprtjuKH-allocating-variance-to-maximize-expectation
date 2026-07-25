"""Evaluator-visible standalone Claim 1 verifier."""

import argparse
import json

from reproduction.checkers.claim1_checker import check_algorithm1
from reproduction.claims.claim1_algorithm1 import (
    verify_algorithm1,
    verify_negative_control,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative-control", action="store_true")
    args = parser.parse_args()
    if args.negative_control:
        control = verify_negative_control()
        print(json.dumps(control, indent=2, sort_keys=True))
        return 1 if control["status"] == "REJECTED_NOT_ALGORITHM_1" else 0
    primary = verify_algorithm1()
    checker = check_algorithm1()
    control = verify_negative_control()
    print(
        json.dumps(
            {"primary": primary, "checker": checker, "control": control},
            indent=2,
            sort_keys=True,
        )
    )
    return (
        0
        if (
            primary["status"] == "VERIFIED"
            and checker["passed"]
            and control["status"] == "REJECTED_NOT_ALGORITHM_1"
        )
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(main())
