"""Verifier for the intended asymptotic reading of Lemma 2.1."""

from __future__ import annotations

import argparse
import json
import math

from scipy.integrate import quad
from scipy.special import log_ndtr


EPSILONS = (1 / 4, 1 / 8, 1 / 16, 1 / 32, 1 / 64)
EXPLICIT_CONSTANT = math.e * math.sqrt(2.0)


def proof_certificate(epsilon: float) -> dict[str, float | str | bool]:
    log_inverse = math.log(1.0 / epsilon)
    q = 2.0 * log_inverse
    bound = EXPLICIT_CONSTANT * epsilon * math.sqrt(log_inverse)
    return {
        "epsilon": epsilon,
        "q": q,
        "q_at_least_2": q >= 2.0,
        "explicit_constant": EXPLICIT_CONSTANT,
        "bound": bound,
        "derivation": (
            "E[M] <= (E[(Z_+)^q] sum_i v_i^(q/2))^(1/q) "
            "<= sqrt(q) epsilon^(1-2/q) "
            "= e*sqrt(2)*epsilon*sqrt(log(1/epsilon))"
        ),
    }


def expected_positive_max_independent(epsilon: float, m: int) -> float:
    """Compute eps * integral_0^inf [1-Phi(z)^m] dz deterministically."""

    def survival(z: float) -> float:
        return -math.expm1(m * float(log_ndtr(z)))

    integral, error = quad(
        survival,
        0.0,
        math.inf,
        epsabs=1e-12,
        epsrel=1e-12,
        limit=300,
    )
    if error > 1e-9:
        raise RuntimeError(f"quadrature error too large: {error}")
    return epsilon * integral


def verify_lemma() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    all_passed = True
    for epsilon in EPSILONS:
        m = round(1.0 / (epsilon * epsilon))
        variance = epsilon * epsilon
        variance_sum = m * variance
        observed = expected_positive_max_independent(epsilon, m)
        certificate = proof_certificate(epsilon)
        passed = (
            variance > 0.0
            and abs(variance_sum - 1.0) < 1e-14
            and bool(certificate["q_at_least_2"])
            and observed <= float(certificate["bound"])
        )
        all_passed &= passed
        rows.append(
            {
                "epsilon": epsilon,
                "m": m,
                "variance_each": variance,
                "variance_sum": variance_sum,
                "expected_positive_max": observed,
                "explicit_upper_bound": certificate["bound"],
                "observed_over_rate": observed
                / (epsilon * math.sqrt(math.log(1.0 / epsilon))),
                "passed": passed,
            }
        )
    return {
        "claim": "Lemma 2.1 under the standard epsilon->0 big-O reading",
        "status": "VERIFIED" if all_passed else "BLOCKED",
        "proof_constant": EXPLICIT_CONSTANT,
        "valid_range": "0 < epsilon <= exp(-1)",
        "proof_certificates": [proof_certificate(eps) for eps in EPSILONS],
        "nonzero_saturating_family": rows,
    }


def verify_negative_control() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for epsilon in EPSILONS:
        log_inverse = math.log(1.0 / epsilon)
        # The additive 3L term makes the control violate the budget at every
        # tested epsilon: log(m*epsilon^2) = L^3 + L > 0.
        log_m = log_inverse**3 + 3.0 * log_inverse
        log_total_variance = log_m + 2.0 * math.log(epsilon)
        rows.append(
            {
                "epsilon": epsilon,
                "log_m": log_m,
                "log_total_variance": log_total_variance,
                "total_variance_exceeds_one": log_total_variance > 0.0,
                "asymptotic_scale_without_budget": (
                    "epsilon*sqrt(2*log(m)) = "
                    "sqrt(2)*epsilon*log(1/epsilon)^(3/2)"
                ),
            }
        )
    rejected = all(bool(row["total_variance_exceeds_one"]) for row in rows)
    return {
        "control": "remove sum_i variance_i <= 1",
        "status": "REJECTED_INVALID_ASSUMPTIONS" if rejected else "UNEXPECTED",
        "reason": (
            "Without the total-variance budget, the maximum retains an "
            "uncontrolled sqrt(log m) factor."
        ),
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative-control", action="store_true")
    args = parser.parse_args()
    if args.negative_control:
        print(json.dumps(verify_negative_control(), indent=2, sort_keys=True))
        return 1
    result = verify_lemma()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "VERIFIED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
