"""Evaluator-visible standalone entrypoint for Claim 3."""

from reproduction.checkers.claim3_checker import check_algorithm3
from reproduction.claims.claim3_algorithm3 import (
    verify_algorithm3,
    verify_negative_control,
)


def main() -> int:
    primary = verify_algorithm3()
    checker = check_algorithm3()
    control = verify_negative_control()
    print({"primary": primary, "checker": checker, "control": control})
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
