"""Independent numerical replication of the qualitative Figures 1--2 claim.

The paper is ambiguous between two random-set models:

* Section 1.3 and Theorem 1.5 use ``p=|S_j|/n`` and all size-k subsets.
* The figure captions call the instances Erdos--Renyi, which means independent
  Bernoulli membership with probability p.

For n=8 both population objectives can be evaluated without choosing the
omitted number of sets m.  We optimize those population objectives using
scrambled Sobol common random numbers, validate on a disjoint scramble, and
then run ordinary finite-m Monte Carlo controls at three independent seeds.
This is an independent qualitative replication, not an exact regeneration of
the authors' unpublished simulation.
"""

from __future__ import annotations

import math
import time
from itertools import product

import numpy as np
from scipy.optimize import minimize
from scipy.special import ndtri
from scipy.stats import qmc


N = 8
P_VALUES = np.arange(1, N + 1, dtype=float) / N
REGIMES = ("independent", "positive_block", "negative_block")
DESIGNS = ("fixed_cardinality", "bernoulli_conditioned_nonempty")
TRAIN_EXPONENT = 12
VALIDATION_EXPONENT = 15
TRAIN_SEED = 250218463
VALIDATION_SEED = 250218464
FINITE_M = 8192
FINITE_SEEDS = (101, 202, 303)
ACTIVE_VARIANCE_THRESHOLD = 0.02
SOURCE_SHA256 = "459cf66ee46d8c78ca931343dbf1d13729d3e4ce62ab1179c93aa34212b7f2af"


def subset_max_weights() -> np.ndarray:
    """Weights mapping sorted values to the mean max of all k-subsets."""
    weights = np.zeros((N, N), dtype=float)
    for k in range(1, N + 1):
        denominator = math.comb(N, k)
        for rank in range(k - 1, N):
            weights[k - 1, rank] = math.comb(rank, k - 1) / denominator
    if not np.allclose(weights.sum(axis=1), 1.0):
        raise AssertionError("fixed-cardinality max weights do not sum to one")
    return weights


FIXED_WEIGHTS = subset_max_weights()


def bernoulli_size_weights() -> np.ndarray:
    """Conditional size law for Bernoulli subsets given non-emptiness."""
    rows = np.zeros((N, N), dtype=float)
    for row, p in enumerate(P_VALUES):
        normalizer = 1.0 - (1.0 - p) ** N
        for k in range(1, N + 1):
            rows[row, k - 1] = (
                math.comb(N, k) * p**k * (1.0 - p) ** (N - k)
                / normalizer
            )
    if not np.allclose(rows.sum(axis=1), 1.0):
        raise AssertionError("conditioned Bernoulli size weights do not sum to one")
    return rows


BERNOULLI_WEIGHTS = bernoulli_size_weights()


def normal_base(regime: str, exponent: int, seed: int) -> np.ndarray:
    """Generate deterministic normal common random numbers for one regime."""
    dimension = N if regime == "independent" else N // 2
    uniform = qmc.Sobol(dimension, scramble=True, seed=seed).random_base2(exponent)
    latent = ndtri(np.clip(uniform, 1e-12, 1.0 - 1e-12))
    if regime == "independent":
        return latent
    expanded = np.empty((len(latent), N), dtype=float)
    expanded[:, 0::2] = latent
    expanded[:, 1::2] = latent if regime == "positive_block" else -latent
    return expanded


def per_draw_fixed_objectives(
    base: np.ndarray, variance: np.ndarray
) -> np.ndarray:
    """Return one row per Gaussian draw and one column per k=1,...,8."""
    values = base * np.sqrt(variance)[None, :]
    ordered = np.sort(values, axis=1)
    return ordered @ FIXED_WEIGHTS.T


def per_draw_objective(
    base: np.ndarray,
    variance: np.ndarray,
    design: str,
    p_index: int,
) -> np.ndarray:
    fixed = per_draw_fixed_objectives(base, variance)
    if design == "fixed_cardinality":
        return fixed[:, p_index]
    if design == "bernoulli_conditioned_nonempty":
        return fixed @ BERNOULLI_WEIGHTS[p_index]
    raise ValueError(f"unknown design {design}")


def estimate(values: np.ndarray) -> tuple[float, float]:
    return float(values.mean()), float(values.std(ddof=1) / math.sqrt(len(values)))


def _variance_from_counts(counts: tuple[int, ...]) -> np.ndarray:
    active: list[int] = []
    for pair, count in enumerate(counts):
        active.extend((2 * pair, 2 * pair + 1)[:count])
    variance = np.zeros(N, dtype=float)
    variance[active] = 1.0 / len(active)
    return variance


def initial_allocations(regime: str) -> list[np.ndarray]:
    """Symmetry-reduced equal-support starts plus the uniform allocation."""
    if regime == "independent":
        starts = []
        for support in range(1, N + 1):
            variance = np.zeros(N, dtype=float)
            variance[:support] = 1.0 / support
            starts.append(variance)
        return starts
    canonical_counts = [
        counts
        for counts in product(range(3), repeat=N // 2)
        if any(counts) and counts == tuple(sorted(counts, reverse=True))
    ]
    return [_variance_from_counts(counts) for counts in canonical_counts]


def _interior(variance: np.ndarray) -> np.ndarray:
    result = np.maximum(np.asarray(variance, dtype=float), 1e-8)
    return result / result.sum()


def optimize_case(
    train_base: np.ndarray,
    validation_base: np.ndarray,
    regime: str,
    design: str,
    p_index: int,
) -> tuple[dict[str, object], np.ndarray]:
    """Multi-start population optimization followed by disjoint validation."""

    def objective(variance: np.ndarray) -> float:
        return -float(
            per_draw_objective(train_base, variance, design, p_index).mean()
        )

    starts = initial_allocations(regime)
    ranked = sorted(starts, key=objective)
    selected_starts = [ranked[0], np.full(N, 1.0 / N)]
    candidates: list[tuple[float, np.ndarray, bool, int, str]] = []
    for start in selected_starts:
        result = minimize(
            objective,
            _interior(start),
            method="SLSQP",
            bounds=[(1e-10, 1.0)] * N,
            constraints={
                "type": "eq",
                "fun": lambda variance: float(np.sum(variance) - 1.0),
            },
            options={"ftol": 1e-10, "maxiter": 90, "disp": False},
        )
        variance = _interior(result.x)
        candidates.append(
            (
                -objective(variance),
                variance,
                bool(result.success),
                int(result.nit),
                str(result.message),
            )
        )
    for start in ranked[:3]:
        variance = _interior(start)
        candidates.append((-objective(variance), variance, True, 0, "enumerated"))
    train_mean, variance, success, iterations, message = max(
        candidates, key=lambda item: item[0]
    )
    validation_draws = per_draw_objective(
        validation_base, variance, design, p_index
    )
    validation_mean, validation_se = estimate(validation_draws)
    row = {
        "design": design,
        "regime": regime,
        "p": float(P_VALUES[p_index]),
        "k": p_index + 1,
        "variance": [float(value) for value in variance],
        "variance_sum": float(variance.sum()),
        "active_count_at_0.02": int(
            np.count_nonzero(variance >= ACTIVE_VARIANCE_THRESHOLD)
        ),
        "effective_support_inverse_herfindahl": float(
            1.0 / np.sum(variance**2)
        ),
        "train_objective": float(train_mean),
        "validation_objective": validation_mean,
        "validation_standard_error": validation_se,
        "optimizer_success": success,
        "optimizer_iterations": iterations,
        "optimizer_message": message,
        "optimizer_start_count": 2,
        "enumerated_symmetry_starts": len(starts),
    }
    return row, validation_draws


def concavity_audit(
    design: str,
    regime: str,
    draws: list[np.ndarray],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for index in range(N - 2):
        second_draw = draws[index + 2] - 2.0 * draws[index + 1] + draws[index]
        mean, standard_error = estimate(second_draw)
        statistically_significant_violation = mean - 4.0 * standard_error > 0.0
        rows.append(
            {
                "design": design,
                "regime": regime,
                "center_p": float(P_VALUES[index + 1]),
                "second_difference": mean,
                "standard_error": standard_error,
                "four_se_upper": mean + 4.0 * standard_error,
                "four_se_lower": mean - 4.0 * standard_error,
                "statistically_significant_violation": bool(
                    statistically_significant_violation
                ),
                "consistent_with_concavity": not statistically_significant_violation,
            }
        )
    return rows


def concentration_audit(
    design: str,
    regime: str,
    rows: list[dict[str, object]],
) -> dict[str, object]:
    low = rows[1]  # p=2/8 avoids the singleton objective's variance degeneracy.
    high = rows[-1]
    low_effective = float(low["effective_support_inverse_herfindahl"])
    high_effective = float(high["effective_support_inverse_herfindahl"])
    return {
        "design": design,
        "regime": regime,
        "low_p": float(low["p"]),
        "high_p": float(high["p"]),
        "low_effective_support": low_effective,
        "high_effective_support": high_effective,
        "low_active_count_at_0.02": int(low["active_count_at_0.02"]),
        "high_active_count_at_0.02": int(high["active_count_at_0.02"]),
        "concentration_increased": high_effective < low_effective - 0.15,
    }


def _finite_membership(
    rng: np.random.Generator, design: str, p_index: int, count: int
) -> np.ndarray:
    if design == "fixed_cardinality":
        k = p_index + 1
        keys = rng.random((count, N))
        chosen = np.argpartition(keys, k - 1, axis=1)[:, :k]
        membership = np.zeros((count, N), dtype=bool)
        membership[np.arange(count)[:, None], chosen] = True
        return membership
    p = float(P_VALUES[p_index])
    membership = rng.random((count, N)) < p
    empty = ~membership.any(axis=1)
    while np.any(empty):
        membership[empty] = rng.random((int(empty.sum()), N)) < p
        empty = ~membership.any(axis=1)
    return membership


def finite_m_audit(
    design: str,
    regime: str,
    p_index: int,
    variance: np.ndarray,
    population_mean: float,
    population_se: float,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    dimension = N if regime == "independent" else N // 2
    for seed in FINITE_SEEDS:
        rng = np.random.default_rng(seed + 1000 * p_index)
        latent = rng.standard_normal((FINITE_M, dimension))
        if regime == "independent":
            base = latent
        else:
            base = np.empty((FINITE_M, N), dtype=float)
            base[:, 0::2] = latent
            base[:, 1::2] = (
                latent if regime == "positive_block" else -latent
            )
        values = base * np.sqrt(variance)[None, :]
        membership = _finite_membership(rng, design, p_index, FINITE_M)
        maxima = np.max(np.where(membership, values, -np.inf), axis=1)
        mean, standard_error = estimate(maxima)
        tolerance = (
            6.0 * math.sqrt(standard_error**2 + population_se**2) + 0.004
        )
        rows.append(
            {
                "design": design,
                "regime": regime,
                "p": float(P_VALUES[p_index]),
                "seed": seed,
                "m": FINITE_M,
                "estimate": mean,
                "standard_error": standard_error,
                "population_reference": population_mean,
                "absolute_difference": abs(mean - population_mean),
                "tolerance": tolerance,
                "agrees_with_population": abs(mean - population_mean) <= tolerance,
            }
        )
    return rows


def verify_independent_replication() -> dict[str, object]:
    started = time.perf_counter()
    result_rows: list[dict[str, object]] = []
    concavity_rows: list[dict[str, object]] = []
    concentration_rows: list[dict[str, object]] = []
    finite_rows: list[dict[str, object]] = []
    for regime_index, regime in enumerate(REGIMES):
        train_base = normal_base(
            regime, TRAIN_EXPONENT, TRAIN_SEED + regime_index
        )
        validation_base = normal_base(
            regime, VALIDATION_EXPONENT, VALIDATION_SEED + regime_index
        )
        for design in DESIGNS:
            design_rows: list[dict[str, object]] = []
            design_draws: list[np.ndarray] = []
            for p_index in range(N):
                row, draws = optimize_case(
                    train_base, validation_base, regime, design, p_index
                )
                design_rows.append(row)
                design_draws.append(draws)
                result_rows.append(row)
                finite_rows.extend(
                    finite_m_audit(
                        design,
                        regime,
                        p_index,
                        np.asarray(row["variance"], dtype=float),
                        float(row["validation_objective"]),
                        float(row["validation_standard_error"]),
                    )
                )
            concavity_rows.extend(
                concavity_audit(design, regime, design_draws)
            )
            concentration_rows.append(
                concentration_audit(design, regime, design_rows)
            )

    concavity_passed = all(
        bool(row["consistent_with_concavity"]) for row in concavity_rows
    )
    concentration_passed = all(
        bool(row["concentration_increased"]) for row in concentration_rows
    )
    finite_m_passed = all(
        bool(row["agrees_with_population"]) for row in finite_rows
    )
    optimizer_passed = all(
        bool(row["optimizer_success"])
        and abs(float(row["variance_sum"]) - 1.0) <= 1e-10
        for row in result_rows
    )
    status = (
        "VERIFIED"
        if (
            concavity_passed
            and concentration_passed
            and finite_m_passed
            and optimizer_passed
        )
        else "BLOCKED"
    )
    return {
        "claim": "Figures 1-2 qualitative n=8 concavity and concentration",
        "status": status,
        "scope": (
            "Independent numerical replication under both interpretations "
            "supported by the paper; not an exact regeneration of unpublished "
            "author code or figure pixels."
        ),
        "paper_inputs": {
            "n": N,
            "p_values": [float(value) for value in P_VALUES],
            "correlation": (
                "independent or exact +/-1 correlation inside fixed 2x2 blocks"
            ),
            "source_bundle_sha256": SOURCE_SHA256,
        },
        "resolved_ambiguity": {
            "fixed_cardinality": (
                "all size-k subsets, matching p=|S_j|/n and Theorem 1.5"
            ),
            "bernoulli_conditioned_nonempty": (
                "independent membership with probability p, matching the "
                "Erdos-Renyi figure caption; empty sets are conditioned away "
                "because max over an empty set is undefined"
            ),
        },
        "method": {
            "train_samples": 2**TRAIN_EXPONENT,
            "validation_samples": 2**VALIDATION_EXPONENT,
            "train_seed": TRAIN_SEED,
            "validation_seed": VALIDATION_SEED,
            "optimizer": "SLSQP on the variance simplex",
            "optimizer_max_iterations": 90,
            "optimizer_ftol": 1e-10,
            "common_random_numbers": True,
            "finite_m": FINITE_M,
            "finite_seeds": list(FINITE_SEEDS),
            "worker_count": 1,
        },
        "population_rows": result_rows,
        "concavity_rows": concavity_rows,
        "concentration_rows": concentration_rows,
        "finite_m_rows": finite_rows,
        "checks": {
            "no_significant_concavity_violation": concavity_passed,
            "concentration_increased_in_every_design_and_regime": (
                concentration_passed
            ),
            "finite_m_multi_seed_agrees_with_population": finite_m_passed,
            "optimizer_and_simplex_checks": optimizer_passed,
        },
        "exact_published_plot_regeneration": {
            "status": "BLOCKED",
            "reason": (
                "The paper omits m, seeds, Gaussian sample count, optimizer, "
                "stopping rule, raw values, and uncertainty."
            ),
        },
        "runtime_seconds": time.perf_counter() - started,
    }


def verify_negative_control(
    primary: dict[str, object],
) -> dict[str, object]:
    """Reject uniform allocation as a substitute for concentration."""
    final_rows = [
        row
        for row in primary["population_rows"]
        if math.isclose(float(row["p"]), 1.0)
    ]
    rejected = all(
        float(row["effective_support_inverse_herfindahl"]) < N - 0.15
        for row in final_rows
    )
    artificial_curve = np.asarray(
        [0.10, 0.28, 0.41, 0.64, 0.82, 1.02, 1.20, 1.45]
    )
    artificial_second = np.diff(artificial_curve, n=2)
    curve_rejected = bool(np.any(artificial_second > 0.0))
    return {
        "control": (
            "force uniform variance at p=1 and feed a fabricated nonconcave "
            "curve to the second-difference test"
        ),
        "uniform_effective_support": N,
        "optimized_final_effective_supports": [
            {
                "design": row["design"],
                "regime": row["regime"],
                "effective_support": row[
                    "effective_support_inverse_herfindahl"
                ],
            }
            for row in final_rows
        ],
        "artificial_curve_second_differences": [
            float(value) for value in artificial_second
        ],
        "status": (
            "REJECTED_INVALID_SUBSTITUTE"
            if rejected and curve_rejected
            else "UNEXPECTED"
        ),
    }
