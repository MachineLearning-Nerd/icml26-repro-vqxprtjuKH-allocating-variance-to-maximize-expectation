"""Run every accepted claim verifier, checker, and negative control."""

from __future__ import annotations

import json
import os
import platform
import time

from reproduction.checkers.claim4_checker import check_raw_certificate
from reproduction.checkers.claim5_checker import check_nonzero_family
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
    passed = (
        claim4["status"] == "FALSIFIED"
        and bool(checker4["passed"])
        and control_rejected
        and claim5["status"] == "VERIFIED"
        and bool(checker5["passed"])
        and control5_rejected
    )
    result = {
        "schema": "openresearch.claim-suite.v1",
        "git_sha": os.environ.get("ORX_GIT_SHA", "reported-by-orx-run-metadata"),
        "seed": None,
        "compute": cpu_metadata(),
        "claims": {
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
