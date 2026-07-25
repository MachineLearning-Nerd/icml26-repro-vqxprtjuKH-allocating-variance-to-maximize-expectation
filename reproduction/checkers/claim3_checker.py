"""Independent checker for the Algorithm 3 evidence."""

from __future__ import annotations

import math
from itertools import combinations

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import ndtr

from reproduction.claims.claim3_algorithm3 import (
    LevelResult,
    algorithm3,
    small_hypergraph,
)


NODES, WEIGHTS = leggauss(384)


def independent_table(max_size: int) -> dict[int, tuple[float, ...]]:
    x = 6.0 * (NODES + 1.0)
    phi = ndtr(x)
    table: dict[int, tuple[float, ...]] = {}
    for size in range(2, max_size + 1):
        values = [0.0]
        for selected in range(1, size + 1):
            integrand = 1.0 - phi**selected
            if selected == size:
                integrand -= (1.0 - phi) ** selected
            values.append(float(6.0 * np.dot(WEIGHTS, integrand)))
        table[size] = tuple(values)
    return table


def independent_objective(
    sets: tuple[tuple[int, ...], ...],
    selected: frozenset[int],
    sigma: float,
    table: dict[int, tuple[float, ...]],
) -> float:
    return sigma * sum(
        table[len(group)][len(selected.intersection(group))] for group in sets
    )


def check_algorithm3() -> dict[str, object]:
    n, sets = small_hypergraph()
    result = algorithm3(n, sets)
    table = independent_table(max(map(len, sets)))
    rows: list[dict[str, object]] = []
    passed = True
    for level in result["levels"]:
        assert isinstance(level, LevelResult)
        sigma = math.sqrt(level.variance)
        prefix: frozenset[int] = frozenset()
        greedy_steps_valid = True
        for chosen in level.selected:
            before = independent_objective(sets, prefix, sigma, table)
            gains = {
                candidate: independent_objective(
                    sets, prefix.union((candidate,)), sigma, table
                )
                - before
                for candidate in range(n)
                if candidate not in prefix
            }
            best_gain = max(gains.values())
            best_vertex = min(
                candidate
                for candidate, gain in gains.items()
                if abs(gain - best_gain) <= 2e-10
            )
            greedy_steps_valid &= (
                abs(gains[chosen] - best_gain) <= 2e-10
                and chosen == best_vertex
            )
            prefix = prefix.union((chosen,))
        independent_value = independent_objective(
            sets, frozenset(level.selected), sigma, table
        )
        exact = max(
            independent_objective(sets, frozenset(subset), sigma, table)
            for subset in combinations(range(n), len(level.selected))
        )
        ratio = independent_value / exact if exact > 0 else 1.0
        row_passed = (
            abs(independent_value - level.objective) <= 2e-10
            and ratio + 1e-12 >= 1.0 - 1.0 / math.e
            and level.total_variance <= 1.0 + 1e-14
            and greedy_steps_valid
        )
        passed &= row_passed
        rows.append(
            {
                "k": level.k,
                "selected": list(level.selected),
                "implementation_objective": level.objective,
                "independent_objective": independent_value,
                "absolute_difference": abs(
                    independent_value - level.objective
                ),
                "independent_level_optimum": exact,
                "greedy_ratio": ratio,
                "every_greedy_step_independently_maximal": greedy_steps_valid,
                "passed": row_passed,
            }
        )
    return {
        "checker": "384-node Gauss-Legendre table plus exhaustive subsets",
        "passed": passed,
        "rows": rows,
        "tail_audit": "all integrals truncated at z=12; omitted Gaussian tail <1e-32",
    }
