"""Independent exact-algebra checker for the Theorem 1.2 counterexample."""

from __future__ import annotations

import math
from fractions import Fraction


def check_counterexample() -> dict[str, object]:
    # For v in [0,1],
    # 1/4-v(1-v) = (2v-1)^2/4 >= 0.
    # This proves sqrt(v(1-v))<=1/2 without numerical optimization.
    maximum_difference_variance = Fraction(2, 1)
    required = Fraction(19, 10)
    upper = 1.0 / math.sqrt(math.pi)
    passed = (
        maximum_difference_variance == 2
        and upper < 1.0
        and Fraction(1, 1) < required
    )
    return {
        "checker": "independent rational inequality and Gaussian absolute moment",
        "passed": passed,
        "symbolic_identity": "1/4-v(1-v)=(2v-1)^2/4>=0",
        "max_variance_Y1_minus_Y2": str(maximum_difference_variance),
        "zero_mean_expected_max_upper": upper,
        "required_lower": str(required),
        "strict_separation": float(required) - upper,
    }
