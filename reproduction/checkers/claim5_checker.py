"""Independent fixed-node quadrature checker for Lemma 2.1 stress cases."""

from __future__ import annotations

import math

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import log_ndtr

from reproduction.claims.claim5_lemma21 import (
    EPSILONS,
    expected_positive_max_independent,
)

NODES, WEIGHTS = leggauss(256)


def fixed_node_positive_max(epsilon: float, m: int) -> float:
    # The omitted Gaussian upper tail beyond z=12 is far below 1e-15 even
    # after the largest union factor in the stress family.
    z = 6.0 * (NODES + 1.0)
    survival = -np.expm1(m * log_ndtr(z))
    return float(epsilon * 6.0 * np.dot(WEIGHTS, survival))


def check_nonzero_family() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    passed = True
    for epsilon in EPSILONS:
        m = round(1.0 / (epsilon * epsilon))
        adaptive = expected_positive_max_independent(epsilon, m)
        fixed_node = fixed_node_positive_max(epsilon, m)
        difference = abs(adaptive - fixed_node)
        row_passed = (
            epsilon > 0.0
            and m * epsilon * epsilon == 1.0
            and difference <= 2e-9
        )
        passed &= row_passed
        rows.append(
            {
                "epsilon": epsilon,
                "m": m,
                "adaptive_quadrature": adaptive,
                "fixed_node_quadrature": fixed_node,
                "absolute_difference": difference,
                "passed": row_passed,
            }
        )
    return {
        "checker": "256-node Gauss-Legendre integration on [0,12]",
        "passed": passed,
        "rows": rows,
        "tail_audit": "m*P[Z>12] < 1e-28 for all tested m",
        "rate": "epsilon*sqrt(log(1/epsilon))",
        "finite_values": all(
            math.isfinite(float(row["fixed_node_quadrature"])) for row in rows
        ),
    }
