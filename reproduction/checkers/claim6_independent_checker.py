"""Independent pseudo-random checker for the Claim 6 Sobol replication."""

from __future__ import annotations

import math

import numpy as np

from reproduction.claims.claim6_independent_replication import (
    ACTIVE_VARIANCE_THRESHOLD,
    BERNOULLI_WEIGHTS,
    FIXED_WEIGHTS,
    N,
    P_VALUES,
)


CHECKER_SAMPLES = 32768
CHECKER_SEED = 184632502


def _base(regime: str, rng: np.random.Generator) -> np.ndarray:
    dimension = N if regime == "independent" else N // 2
    latent = rng.standard_normal((CHECKER_SAMPLES, dimension))
    if regime == "independent":
        return latent
    expanded = np.empty((CHECKER_SAMPLES, N), dtype=float)
    expanded[:, 0::2] = latent
    expanded[:, 1::2] = (
        latent if regime == "positive_block" else -latent
    )
    return expanded


def _draws(
    base: np.ndarray,
    variance: np.ndarray,
    design: str,
    p_index: int,
) -> np.ndarray:
    ordered = np.sort(base * np.sqrt(variance)[None, :], axis=1)
    fixed = ordered @ FIXED_WEIGHTS.T
    if design == "fixed_cardinality":
        return fixed[:, p_index]
    return fixed @ BERNOULLI_WEIGHTS[p_index]


def _estimate(values: np.ndarray) -> tuple[float, float]:
    return float(values.mean()), float(values.std(ddof=1) / math.sqrt(len(values)))


def check_independent_replication(
    primary: dict[str, object],
) -> dict[str, object]:
    rng = np.random.default_rng(CHECKER_SEED)
    bases = {
        regime: _base(regime, rng)
        for regime in ("independent", "positive_block", "negative_block")
    }
    grouped: dict[tuple[str, str], list[np.ndarray]] = {}
    reproduction_rows: list[dict[str, object]] = []
    passed = True
    for row in primary["population_rows"]:
        regime = str(row["regime"])
        design = str(row["design"])
        p_index = int(row["k"]) - 1
        variance = np.asarray(row["variance"], dtype=float)
        draws = _draws(bases[regime], variance, design, p_index)
        mean, standard_error = _estimate(draws)
        reference = float(row["validation_objective"])
        reference_se = float(row["validation_standard_error"])
        tolerance = 7.0 * math.sqrt(
            standard_error**2 + reference_se**2
        ) + 0.003
        row_passed = (
            abs(variance.sum() - 1.0) <= 1e-9
            and np.all(variance >= 0.0)
            and abs(mean - reference) <= tolerance
        )
        passed &= row_passed
        reproduction_rows.append(
            {
                "design": design,
                "regime": regime,
                "p": float(P_VALUES[p_index]),
                "pseudo_random_objective": mean,
                "standard_error": standard_error,
                "sobol_reference": reference,
                "absolute_difference": abs(mean - reference),
                "tolerance": tolerance,
                "passed": bool(row_passed),
            }
        )
        grouped.setdefault((design, regime), []).append(draws)

    concavity_rows: list[dict[str, object]] = []
    for (design, regime), series in grouped.items():
        if len(series) != N:
            passed = False
            continue
        for index in range(N - 2):
            second = series[index + 2] - 2.0 * series[index + 1] + series[index]
            mean, standard_error = _estimate(second)
            violation = mean - 4.0 * standard_error > 0.0
            passed &= not violation
            concavity_rows.append(
                {
                    "design": design,
                    "regime": regime,
                    "center_p": float(P_VALUES[index + 1]),
                    "second_difference": mean,
                    "standard_error": standard_error,
                    "significant_violation": bool(violation),
                }
            )

    concentration_rows: list[dict[str, object]] = []
    for design in ("fixed_cardinality", "bernoulli_conditioned_nonempty"):
        for regime in ("independent", "positive_block", "negative_block"):
            rows = [
                row
                for row in primary["population_rows"]
                if row["design"] == design and row["regime"] == regime
            ]
            low = np.asarray(rows[1]["variance"], dtype=float)
            high = np.asarray(rows[-1]["variance"], dtype=float)
            low_effective = float(1.0 / np.sum(low**2))
            high_effective = float(1.0 / np.sum(high**2))
            increased = high_effective < low_effective - 0.15
            passed &= increased
            concentration_rows.append(
                {
                    "design": design,
                    "regime": regime,
                    "low_effective_support": low_effective,
                    "high_effective_support": high_effective,
                    "low_active_count": int(
                        np.count_nonzero(low >= ACTIVE_VARIANCE_THRESHOLD)
                    ),
                    "high_active_count": int(
                        np.count_nonzero(high >= ACTIVE_VARIANCE_THRESHOLD)
                    ),
                    "concentration_increased": bool(increased),
                }
            )

    return {
        "checker": (
            "independent NumPy pseudo-random replication of every reported "
            "allocation, curve, uncertainty comparison, and concentration test"
        ),
        "samples": CHECKER_SAMPLES,
        "seed": CHECKER_SEED,
        "passed": bool(passed),
        "reproduction_rows": reproduction_rows,
        "concavity_rows": concavity_rows,
        "concentration_rows": concentration_rows,
    }
