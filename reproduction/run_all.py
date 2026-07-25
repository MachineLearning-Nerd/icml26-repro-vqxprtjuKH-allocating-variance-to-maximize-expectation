"""Run every accepted claim verifier, checker, and negative control."""

from __future__ import annotations

import json
import os
import platform
import time

from reproduction.checkers.claim4_checker import check_raw_certificate
from reproduction.checkers.claim5_checker import check_nonzero_family
from reproduction.checkers.claim3_checker import check_algorithm3
from reproduction.checkers.claim1_checker import check_algorithm1
from reproduction.checkers.claim2_checker import check_counterexample as check_claim2
from reproduction.checkers.claim6_checker import check_digitized_payoff
from reproduction.claims.claim1_algorithm1 import (
    verify_algorithm1,
    verify_negative_control as verify_algorithm1_negative_control,
)
from reproduction.claims.claim2_counterexample import (
    verify_counterexample as verify_claim2_counterexample,
    verify_negative_control as verify_claim2_negative_control,
)
from reproduction.claims.claim6_figure_audit import (
    verify_figure_claim,
    verify_negative_control as verify_figure_negative_control,
)
from reproduction.claims.claim3_algorithm3 import (
    verify_algorithm3,
    verify_negative_control as verify_algorithm3_negative_control,
)
from reproduction.claims.claim4_counterexample import (
    verify_counterexample,
    verify_negative_control,
)
from reproduction.claims.claim5_lemma21 import (
    verify_lemma,
    verify_negative_control as verify_lemma_negative_control,
)


def cpu_metadata() -> dict[str, object]:
    affinity = None
    if hasattr(os, "sched_getaffinity"):
        affinity = len(os.sched_getaffinity(0))
    return {
        "platform": platform.platform(),
        "python": platform.python_version(),
        "visible_logical_cpus": os.cpu_count(),
        "affinity_cpus": affinity,
        "designed_worker_count": 1,
    }


def main() -> int:
    started = time.perf_counter()
    claim4 = verify_counterexample()
    checker4 = check_raw_certificate()
    control4 = verify_negative_control()
    control_rejected = control4["status"] == "REJECTED_AS_COUNTEREXAMPLE"
    claim5 = verify_lemma()
    checker5 = check_nonzero_family()
    control5 = verify_lemma_negative_control()
    control5_rejected = control5["status"] == "REJECTED_INVALID_ASSUMPTIONS"
    claim3 = verify_algorithm3()
    checker3 = check_algorithm3()
    control3 = verify_algorithm3_negative_control()
    control3_rejected = control3["status"] == "REJECTED_BAD_SUBSTITUTE"
    claim1 = verify_algorithm1()
    checker1 = check_algorithm1()
    control1 = verify_algorithm1_negative_control()
    control1_rejected = control1["status"] == "REJECTED_NOT_ALGORITHM_1"
    claim2 = verify_claim2_counterexample()
    checker2 = check_claim2()
    control2 = verify_claim2_negative_control()
    control2_rejected = control2["status"] == "REJECTED_AS_COUNTEREXAMPLE"
    claim6 = verify_figure_claim()
    checker6 = check_digitized_payoff()
    control6 = verify_figure_negative_control()
    control6_rejected = control6["status"] == "REJECTED_NONCONCAVE_SERIES"
    passed = (
        claim4["status"] == "FALSIFIED"
        and bool(checker4["passed"])
        and control_rejected
        and claim5["status"] == "VERIFIED"
        and bool(checker5["passed"])
        and control5_rejected
        and claim3["status"] == "VERIFIED"
        and bool(checker3["passed"])
        and control3_rejected
        and claim1["status"] == "VERIFIED"
        and bool(checker1["passed"])
        and control1_rejected
        and claim2["status"] == "FALSIFIED"
        and bool(checker2["passed"])
        and control2_rejected
        and claim6["status"] == "BLOCKED"
        and bool(claim6["all_four_routes_complete"])
        and bool(checker6["passed"])
        and control6_rejected
    )
    result = {
        "schema": "openresearch.claim-suite.v1",
        "git_sha": os.environ.get("ORX_GIT_SHA", "reported-by-orx-run-metadata"),
        "seed": None,
        "compute": cpu_metadata(),
        "claims": {
            "claim_6": {
                "status": claim6["status"],
                "primary": claim6,
                "independent_checker": checker6,
                "negative_control": control6,
            },
            "claim_2": {
                "status": claim2["status"],
                "primary": claim2,
                "independent_checker": checker2,
                "negative_control": control2,
            },
            "claim_1": {
                "status": claim1["status"],
                "primary": claim1,
                "independent_checker": checker1,
                "negative_control": control1,
            },
            "claim_3": {
                "status": claim3["status"],
                "primary": claim3,
                "independent_checker": checker3,
                "negative_control": control3,
            },
            "claim_4": {
                "status": claim4["status"],
                "primary": claim4,
                "independent_checker": checker4,
                "negative_control": control4,
            },
            "claim_5": {
                "status": claim5["status"],
                "primary": claim5,
                "independent_checker": checker5,
                "negative_control": control5,
            },
        },
        "suite_passed": passed,
        "runtime_seconds": time.perf_counter() - started,
    }
    print("=== OPENRESEARCH_EVIDENCE_JSON_BEGIN ===")
    print(json.dumps(result, indent=2, sort_keys=True))
    print("=== OPENRESEARCH_EVIDENCE_JSON_END ===")
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
