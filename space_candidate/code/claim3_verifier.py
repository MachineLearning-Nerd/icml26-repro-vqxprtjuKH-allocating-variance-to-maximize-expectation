"""Evaluator-visible standalone entrypoint for Claim 3."""

import argparse
import json

from reproduction.checkers.claim3_checker import check_algorithm3
from reproduction.claims.claim3_algorithm3 import (
    verify_algorithm3,
    verify_negative_control,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative-control", action="store_true")
    args = parser.parse_args()
    if args.negative_control:
        control = verify_negative_control()
        print(json.dumps(control, indent=2, sort_keys=True))
        return 1 if control["status"] == "REJECTED_BAD_SUBSTITUTE" else 0
    primary = verify_algorithm3()
    checker = check_algorithm3()
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
            and control["status"] == "REJECTED_BAD_SUBSTITUTE"
        )
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(main())
