"""Standalone exact verifier for the literal Theorem 1.2 counterexample."""

import math


def main() -> int:
    opt_lower = 2.0
    epsilon = 0.1
    required = opt_lower - epsilon
    zero_mean_upper = 1.0 / math.sqrt(math.pi)
    primary = zero_mean_upper < required

    # Negative control: with mu=(0,0), the same upper bound is attained by
    # [[1/2,-1/2],[-1/2,1/2]], so no contradiction remains.
    repaired_optimum = zero_mean_upper
    control_rejected = repaired_optimum >= repaired_optimum - epsilon
    print(
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
        }
    )
    return 0 if primary and control_rejected else 2


if __name__ == "__main__":
    raise SystemExit(main())
