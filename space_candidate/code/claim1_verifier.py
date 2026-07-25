"""Evaluator-visible standalone Claim 1 verifier."""

from reproduction.checkers.claim1_checker import check_algorithm1
from reproduction.claims.claim1_algorithm1 import (
    verify_algorithm1,
    verify_negative_control,
)


def main() -> int:
    primary = verify_algorithm1()
    checker = check_algorithm1()
    control = verify_negative_control()
    print({"primary": primary, "checker": checker, "control": control})
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
