"""Independent numerical checker for Algorithm 1 outputs."""

from __future__ import annotations

import math

import numpy as np
from scipy.integrate import quad
from scipy.special import ndtr

from reproduction.claims.claim1_algorithm1 import algorithm1, deterministic_means


def independent_expected_max(
    means: np.ndarray,
    support: tuple[int, ...],
    sigmas: tuple[float, ...],
) -> float:
    support_set = set(support)
    baseline = max(
        float(means[index])
        for index in range(len(means))
        if index not in support_set
    )
    selected_means = means[np.asarray(support, dtype=int)]
    selected_sigmas = np.asarray(sigmas, dtype=float)
    upper = float(np.max(selected_means + 12.0 * selected_sigmas))

    def survival(x: float) -> float:
        return float(
            1.0
            - np.prod(ndtr((x - selected_means) / selected_sigmas))
        )

    integral, error = quad(
        survival,
        baseline,
        upper,
        epsabs=2e-12,
        epsrel=2e-12,
        limit=200,
    )
    return baseline + float(integral)


def check_algorithm1() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    passed = True
    for epsilon in (0.8, 0.7):
        means = deterministic_means(6)
        result = algorithm1(means, epsilon)
        best = result["best"]
        independent = independent_expected_max(
            means,
            tuple(best["support"]),
            tuple(best["completed_standard_deviations"]),
        )
        difference = abs(independent - float(best["objective"]))
        grid_valid = all(
            abs(sigma / (epsilon**3) - round(sigma / (epsilon**3)))
            <= 2e-12
            for sigma in best["grid_standard_deviations"]
        )
        row_passed = (
            difference <= 2e-8
            and grid_valid
            and len(best["support"]) <= math.ceil(epsilon**-2)
            and abs(float(result["variance_sum"]) - 1.0) <= 2e-14
        )
        passed &= row_passed
        rows.append(
            {
                "epsilon": epsilon,
                "support": list(best["support"]),
                "implementation_objective": best["objective"],
                "adaptive_quadrature_objective": independent,
                "absolute_difference": difference,
                "grid_tuple_valid": grid_valid,
                "passed": row_passed,
            }
        )
    return {
        "checker": "adaptive quadrature independent of the 48-node search objective",
        "passed": passed,
        "rows": rows,
        "tail_audit": "upper integration limit is max(mu_i+12 sigma_i)",
    }
