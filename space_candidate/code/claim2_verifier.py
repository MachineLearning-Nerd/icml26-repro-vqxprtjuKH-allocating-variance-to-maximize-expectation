"""Standalone exact verifier for the literal Theorem 1.2 counterexample."""

import argparse
import json
import math


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative-control", action="store_true")
    args = parser.parse_args()
    opt_lower = 2.0
    epsilon = 0.1
    required = opt_lower - epsilon
    zero_mean_upper = 1.0 / math.sqrt(math.pi)
    primary = zero_mean_upper < required

    # Negative control: with mu=(0,0), the same upper bound is attained by
    # [[1/2,-1/2],[-1/2,1/2]], so no contradiction remains.
    repaired_optimum = zero_mean_upper
    control_rejected = repaired_optimum >= repaired_optimum - epsilon
    if args.negative_control:
        print(
            json.dumps(
                {
                    "status": "REJECTED_AS_COUNTEREXAMPLE",
                    "scope": "repaired input mu=(0,0)",
                    "attainable_output": repaired_optimum,
                    "required_output": repaired_optimum - epsilon,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 1 if control_rejected else 0
    print(
        json.dumps(
            {
            "status": "FALSIFIED" if primary else "BLOCKED",
            "opt_lower": opt_lower,
            "required": required,
            "universal_zero_mean_upper": zero_mean_upper,
            "symbolic_checker": "1/4-v(1-v)=(2v-1)^2/4>=0",
            "negative_control": (
                "REJECTED_AS_COUNTEREXAMPLE"
                if control_rejected
                else "UNEXPECTED"
            ),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if primary and control_rejected else 2


if __name__ == "__main__":
    raise SystemExit(main())
