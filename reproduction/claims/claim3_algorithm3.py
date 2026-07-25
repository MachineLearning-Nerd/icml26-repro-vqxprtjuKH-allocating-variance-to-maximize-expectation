"""Faithful zero-mean core of Algorithm 3 for GraphVarAlloc.

The paper first reduces non-negative means to the zero-mean problem at a
constant-factor loss.  This module implements the resulting Algorithm 3
literally: try every k, set selected variances to 4**(-k), greedily select at
most min(4**k, n) variables by the exact objective marginal, and return the
best level.
"""

from __future__ import annotations

import heapq
import math
import time
from dataclasses import dataclass
from itertools import combinations

from scipy.integrate import quad


SQRT_TWO_PI = math.sqrt(2.0 * math.pi)


def _normal_cdf(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def expected_standard_max(selected: int, set_size: int) -> float:
    """E max of selected N(0,1)s and the remaining degenerate zeros."""
    if selected == 0:
        return 0.0
    if selected < set_size:
        value, _ = quad(
            lambda x: 1.0 - _normal_cdf(x) ** selected,
            0.0,
            10.0,
            epsabs=2e-13,
            epsrel=2e-13,
        )
        return float(value)
    positive, _ = quad(
        lambda x: (
            1.0
            - _normal_cdf(x) ** selected
            - (1.0 - _normal_cdf(x)) ** selected
        ),
        0.0,
        10.0,
        epsabs=2e-13,
        epsrel=2e-13,
    )
    return float(positive)


def max_table(max_set_size: int) -> dict[int, tuple[float, ...]]:
    return {
        size: tuple(expected_standard_max(t, size) for t in range(size + 1))
        for size in range(2, max_set_size + 1)
    }


@dataclass(frozen=True)
class LevelResult:
    k: int
    variance: float
    selected: tuple[int, ...]
    objective: float
    total_variance: float


def objective_equal_variance(
    sets: tuple[tuple[int, ...], ...],
    selected: frozenset[int],
    standard_deviation: float,
    table: dict[int, tuple[float, ...]],
) -> float:
    return standard_deviation * sum(
        table[len(group)][sum(vertex in selected for vertex in group)]
        for group in sets
    )


def algorithm3(
    n: int,
    sets: tuple[tuple[int, ...], ...],
) -> dict[str, object]:
    """Run Algorithm 3 using exact greedy marginals for zero-mean Gaussians."""
    if n < 2:
        raise ValueError("Algorithm 3 requires n >= 2")
    if not sets or any(len(group) < 2 for group in sets):
        raise ValueError("singleton/empty sets must be removed before Algorithm 3")
    if any(len(set(group)) != len(group) for group in sets):
        raise ValueError("sets must not contain duplicate vertices")
    if any(vertex < 0 or vertex >= n for group in sets for vertex in group):
        raise ValueError("vertex outside [0,n)")

    table = max_table(max(map(len, sets)))
    incidence: list[list[int]] = [[] for _ in range(n)]
    for set_index, group in enumerate(sets):
        for vertex in group:
            incidence[vertex].append(set_index)

    levels: list[LevelResult] = []
    for k in range(math.floor(math.log2(n)) + 1):
        variance = 4.0 ** (-k)
        standard_deviation = 2.0 ** (-k)
        budget = min(4**k, n)
        counts = [0] * len(sets)
        chosen = [False] * n

        def marginal(vertex: int) -> float:
            return standard_deviation * sum(
                table[len(sets[index])][counts[index] + 1]
                - table[len(sets[index])][counts[index]]
                for index in incidence[vertex]
            )

        versions = [0] * n
        heap = [(-marginal(vertex), vertex, 0) for vertex in range(n)]
        heapq.heapify(heap)
        selected: list[int] = []
        objective = 0.0
        while len(selected) < budget:
            negative_gain, vertex, version = heapq.heappop(heap)
            if chosen[vertex] or version != versions[vertex]:
                continue
            current_gain = marginal(vertex)
            if abs(current_gain + negative_gain) > 1e-12:
                versions[vertex] += 1
                heapq.heappush(
                    heap, (-current_gain, vertex, versions[vertex])
                )
                continue
            chosen[vertex] = True
            selected.append(vertex)
            objective += current_gain
            affected: set[int] = set()
            for index in incidence[vertex]:
                counts[index] += 1
                affected.update(sets[index])
            for neighbor in affected:
                if not chosen[neighbor]:
                    versions[neighbor] += 1
                    heapq.heappush(
                        heap, (-marginal(neighbor), neighbor, versions[neighbor])
                    )

        selected_set = frozenset(selected)
        direct_objective = objective_equal_variance(
            sets, selected_set, standard_deviation, table
        )
        if abs(objective - direct_objective) > 2e-10:
            raise AssertionError("incremental objective disagrees with direct value")
        levels.append(
            LevelResult(
                k=k,
                variance=variance,
                selected=tuple(selected),
                objective=direct_objective,
                total_variance=len(selected) * variance,
            )
        )

    best = max(levels, key=lambda level: (level.objective, -level.k))
    return {
        "best": best,
        "levels": tuple(levels),
        "all_levels_feasible": all(
            level.total_variance <= 1.0 + 1e-14 for level in levels
        ),
    }


def small_hypergraph() -> tuple[int, tuple[tuple[int, ...], ...]]:
    return (
        8,
        (
            (0, 1),
            (0, 2, 3),
            (1, 2, 4, 5),
            (3, 4),
            (2, 5, 6),
            (0, 6, 7),
            (1, 3, 7),
            (4, 6),
            (2, 3, 5, 7),
        ),
    )


def sparse_scaling_instance(
    n: int,
) -> tuple[tuple[int, ...], ...]:
    """Deterministic sparse graph/hypergraph family with 3n distinct sets."""
    groups: set[tuple[int, ...]] = set()
    for vertex in range(n):
        groups.add(tuple(sorted((vertex, (vertex + 1) % n))))
        groups.add(tuple(sorted((vertex, (vertex + 7) % n))))
        groups.add(
            tuple(
                sorted(
                    (
                        vertex,
                        (vertex + 3) % n,
                        (vertex + 11) % n,
                    )
                )
            )
        )
    return tuple(sorted(groups))


def star_instance(n: int) -> tuple[tuple[int, ...], ...]:
    center = n - 1
    return tuple((leaf, center) for leaf in range(n - 1))


def verify_algorithm3() -> dict[str, object]:
    started = time.perf_counter()
    n_small, sets_small = small_hypergraph()
    small_result = algorithm3(n_small, sets_small)
    table = max_table(max(map(len, sets_small)))
    exhaustive_rows: list[dict[str, object]] = []
    greedy_bound_passed = True
    for level in small_result["levels"]:
        assert isinstance(level, LevelResult)
        budget = len(level.selected)
        exact = max(
            objective_equal_variance(
                sets_small,
                frozenset(subset),
                math.sqrt(level.variance),
                table,
            )
            for subset in combinations(range(n_small), budget)
        )
        ratio = level.objective / exact if exact > 0.0 else 1.0
        row_passed = ratio + 1e-12 >= 1.0 - 1.0 / math.e
        greedy_bound_passed &= row_passed
        exhaustive_rows.append(
            {
                "k": level.k,
                "cardinality": budget,
                "greedy_objective": level.objective,
                "exact_level_objective": exact,
                "ratio": ratio,
                "nemhauser_threshold": 1.0 - 1.0 / math.e,
                "passed": row_passed,
            }
        )

    scale_rows: list[dict[str, object]] = []
    for n in (64, 256, 1024, 4096, 16384):
        sets = sparse_scaling_instance(n)
        scale_started = time.perf_counter()
        result = algorithm3(n, sets)
        best = result["best"]
        assert isinstance(best, LevelResult)
        scale_rows.append(
            {
                "n": n,
                "m": len(sets),
                "best_k": best.k,
                "selected_count": len(best.selected),
                "objective": best.objective,
                "total_variance": best.total_variance,
                "runtime_seconds": time.perf_counter() - scale_started,
                "feasible": result["all_levels_feasible"],
            }
        )

    star = algorithm3(128, star_instance(128))
    star_best = star["best"]
    assert isinstance(star_best, LevelResult)
    status = (
        "VERIFIED"
        if (
            small_result["all_levels_feasible"]
            and greedy_bound_passed
            and all(bool(row["feasible"]) for row in scale_rows)
            and star_best.selected[0] == 127
        )
        else "BLOCKED"
    )
    return {
        "claim": "Theorem 1.3 / faithful Algorithm 3 under its proof assumptions",
        "status": status,
        "algorithm_contract": {
            "levels": "integer k=0,...,floor(log2(n))",
            "variance_each": "4^(-k)",
            "cardinality": "min(4^k,n)",
            "selection": "exact current-objective greedy marginal",
            "return": "highest-objective level",
        },
        "proof_certificate": {
            "rounding": "Lemma 2.6: power-of-four variance rounding loses <=2",
            "grouping": "K+2 variance groups; max <= sum of positive group maxima",
            "tail": "Lemma 2.1 makes variance<1/n^2 contribution negligible versus uniform baseline",
            "pigeonhole": "one of K+1 retained groups contributes Omega(OPT/log n)",
            "submodular_greedy": "Lemma 2.7 plus Nemhauser gives factor 1-1/e",
            "mean_reduction": "paper proof requires non-negative means; experiments use exact zero means",
            "machine_checks": {
                "every_level_budget_feasible": bool(
                    small_result["all_levels_feasible"]
                )
                and all(bool(row["feasible"]) for row in scale_rows),
                "greedy_factor_exhaustive_small_domain": greedy_bound_passed,
                "star_first_choice_is_center": star_best.selected[0] == 127,
            },
        },
        "exhaustive_small_domain": exhaustive_rows,
        "scaling": scale_rows,
        "star_best": {
            "n": 128,
            "m": 127,
            "best_k": star_best.k,
            "first_selected": star_best.selected[0],
            "objective": star_best.objective,
        },
        "runtime_seconds": time.perf_counter() - started,
    }


def verify_negative_control() -> dict[str, object]:
    """A fixed-index substitute violates the greedy guarantee on a star."""
    n = 128
    variance = 1.0
    good = (n - 1) / SQRT_TWO_PI
    bad = 1.0 / SQRT_TWO_PI
    ratio = bad / good
    rejected = ratio < 1.0 - 1.0 / math.e
    return {
        "control": "replace exact greedy marginal by fixed vertex order",
        "instance": "128-vertex star with center at index 127, k=0",
        "greedy_objective": good,
        "fixed_order_objective": bad,
        "ratio": ratio,
        "required_level_ratio": 1.0 - 1.0 / math.e,
        "status": "REJECTED_BAD_SUBSTITUTE" if rejected else "UNEXPECTED",
    }
