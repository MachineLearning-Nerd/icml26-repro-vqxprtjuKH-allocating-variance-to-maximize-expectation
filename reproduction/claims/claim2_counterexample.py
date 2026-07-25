"""Exact counterexample to the literal quantifiers of Theorem 1.2."""

from __future__ import annotations

import math
from fractions import Fraction


MEAN_1 = Fraction(2, 1)
MEAN_2 = Fraction(0, 1)
EPSILON = Fraction(1, 10)


def verify_counterexample() -> dict[str, object]:
    # CorrVarAlloc as defined permits mu=(2,0).  The feasible covariance
    # diag(0,1) makes X1=2 deterministically, hence OPT >= 2.
    input_opt_lower = MEAN_1
    required_output_lower = input_opt_lower - EPSILON

    # The theorem explicitly evaluates the returned vector as N(0,Sigmahat).
    # For every two-dimensional zero-mean covariance with trace one,
    # E max(Y1,Y2) = E|Y1-Y2|/2 <= 1/sqrt(pi).
    zero_mean_output_upper = 1.0 / math.sqrt(math.pi)
    contradicted = zero_mean_output_upper < float(required_output_lower)
    return {
        "claim": "Theorem 1.2 exact literal mean/output quantifiers",
        "status": "FALSIFIED" if contradicted else "BLOCKED",
        "input": {
            "n": 2,
            "means": [str(MEAN_1), str(MEAN_2)],
            "epsilon": str(EPSILON),
            "feasible_covariance": [["0", "0"], ["0", "1"]],
            "trace": "1",
            "positive_semidefinite": True,
        },
        "input_opt_lower_bound": str(input_opt_lower),
        "required_theorem_output_lower_bound": str(required_output_lower),
        "literal_output_distribution": "N(0,Sigma_hat)",
        "universal_zero_mean_output_upper_bound": zero_mean_output_upper,
        "proof": [
            "E max(Y1,Y2) = E|Y1-Y2|/2 for zero means.",
            "Var(Y1-Y2)=1-2*Sigma12 under trace(Sigma)=1.",
            "PSD gives Sigma12 >= -sqrt(v*(1-v)), v=Sigma11.",
            "v*(1-v)<=1/4, so Var(Y1-Y2)<=2.",
            "Therefore E max(Y1,Y2)<=1/sqrt(pi)<1<19/10.",
            "But feasible input covariance diag(0,1) has X1=2 pointwise, so OPT>=2.",
        ],
        "scope": (
            "This falsifies Theorem 1.2 as written. It does not falsify a "
            "repaired theorem whose CorrVarAlloc input is explicitly zero-mean."
        ),
    }


def verify_negative_control() -> dict[str, object]:
    optimum = 1.0 / math.sqrt(math.pi)
    repaired_requirement = optimum - float(EPSILON)
    attainable = optimum
    return {
        "control": "repair the theorem by requiring input means mu=(0,0)",
        "exact_zero_mean_optimum": optimum,
        "required_output_for_epsilon": repaired_requirement,
        "attained_by": "Sigma=[[1/2,-1/2],[-1/2,1/2]]",
        "attainable_output": attainable,
        "status": (
            "REJECTED_AS_COUNTEREXAMPLE"
            if attainable >= repaired_requirement
            else "UNEXPECTED"
        ),
    }
