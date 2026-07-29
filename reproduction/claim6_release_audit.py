"""Claim 6 additive release checks executed by the fixed cumulative command."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "space_candidate"
PROTECTED_MANIFEST = (
    ROOT / ".openresearch" / "protected_space_8fee0d82_manifest.sha256"
)
PROTECTED_EXCEPTIONS = {
    "HF_UPLOAD_ALLOWLIST.txt": "protected_10_12/HF_UPLOAD_ALLOWLIST.txt",
    "SHA256SUMS.txt": "protected_10_12/SHA256SUMS.txt",
    "logbook.json": "protected_10_12/logbook.json",
    "reproduction/run_all.py": "protected_10_12/reproduction_run_all.py",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def manifest_rows() -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    manifest = ROOT / ".openresearch" / "judged_space_manifest.sha256"
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        expected, relative = line.split(maxsplit=1)
        rows.append((expected, relative))
    return rows


def all_candidate_hashes() -> set[str]:
    return {
        sha256(path)
        for path in CANDIDATE.rglob("*")
        if path.is_file()
    }


def protected_manifest_rows() -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for line in PROTECTED_MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        expected, relative = line.split(maxsplit=1)
        rows.append((expected, relative))
    return rows


def syntax_checks() -> dict[str, bool]:
    results: dict[str, bool] = {}
    sources = sorted((CANDIDATE / "code").glob("*.py"))
    sources.extend(sorted((ROOT / "reproduction").rglob("*.py")))
    for source in sources:
        compile(source.read_text(encoding="utf-8"), str(source), "exec")
        results[str(source.relative_to(ROOT))] = True
    return results


def required_evidence_checks() -> dict[str, bool]:
    checks: dict[str, bool] = {}
    for claim in range(1, 7):
        artifact = ROOT / ".openresearch" / "artifacts" / f"claim_{claim}"
        for name in (
            "claim_contract.json",
            "source_audit.md",
            "method.md",
            "command_environment.md",
            "EVAL.md",
            "limitations.md",
            "latest_output.json",
        ):
            path = artifact / name
            checks[f"claim_{claim}/{name}"] = path.is_file() and path.stat().st_size > 0
        checks[f"claim_{claim}/raw"] = any(
            path.is_file() and path.stat().st_size > 0
            for path in artifact.glob("raw*")
        ) or (artifact / "proof_certificate.json").is_file()
        checks[f"claim_{claim}/space_contract"] = (
            CANDIDATE / "contracts" / f"claim{claim}_contract.json"
        ).is_file()
        checks[f"claim_{claim}/space_output"] = (
            CANDIDATE / "raw" / f"claim{claim}_checker_control_output.json"
        ).is_file()
        checks[f"claim_{claim}/space_verifier"] = (
            CANDIDATE / "code" / f"claim{claim}_verifier.py"
        ).is_file()
    return checks


def secret_scan() -> list[str]:
    patterns = (
        re.compile(r"hf_[A-Za-z0-9]{20,}"),
        re.compile(r"AKIA[0-9A-Z]{16}"),
        re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    )
    findings: list[str] = []
    suffixes = {".md", ".json", ".csv", ".py", ".toml", ".lock", ".txt", ".svg"}
    roots = [CANDIDATE, ROOT / "reproduction", ROOT / ".openresearch" / "artifacts"]
    for scan_root in roots:
        for path in scan_root.rglob("*"):
            if not path.is_file() or path.suffix not in suffixes:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if any(pattern.search(text) for pattern in patterns):
                findings.append(str(path.relative_to(ROOT)))
    return findings


def upload_source(relative: str) -> Path:
    if relative == "artifacts/run_metadata.json":
        return ROOT / ".openresearch" / "run_metadata.json"
    if relative.startswith("artifacts/"):
        return ROOT / ".openresearch" / relative
    if relative.startswith("reproduction/") or relative in {
        ".python-version",
        "pyproject.toml",
        "uv.lock",
    }:
        return ROOT / relative
    return CANDIDATE / relative


def protected_preservation_checks() -> dict[str, object]:
    exact_paths: dict[str, bool] = {}
    archived_exceptions: dict[str, bool] = {}
    for expected, relative in protected_manifest_rows():
        if relative in PROTECTED_EXCEPTIONS:
            archived = CANDIDATE / PROTECTED_EXCEPTIONS[relative]
            archived_exceptions[relative] = (
                archived.is_file() and sha256(archived) == expected
            )
            continue
        source = upload_source(relative)
        exact_paths[relative] = source.is_file() and sha256(source) == expected

    archived_logbook = json.loads(
        (CANDIDATE / "protected_10_12" / "logbook.json").read_text(
            encoding="utf-8"
        )
    )
    live_logbook = json.loads(
        (CANDIDATE / "logbook.json").read_text(encoding="utf-8")
    )
    protected_children = archived_logbook["root"]["children"]
    live_children = live_logbook["root"]["children"]
    old_navigation_preserved = all(
        child in live_children for child in protected_children
    )
    claim_paths = [
        relative
        for _, relative in protected_manifest_rows()
        if (
            relative.startswith("artifacts/claim_")
            or relative.startswith("code/claim")
            or relative.startswith("contracts/claim")
            or relative.startswith("raw/claim")
            or relative == "pages/current-verification/page.md"
        )
    ]
    protected_claim_paths_unchanged = all(
        exact_paths.get(relative, False) for relative in claim_paths
    )
    return {
        "passed": (
            all(exact_paths.values())
            and all(archived_exceptions.values())
            and old_navigation_preserved
            and protected_claim_paths_unchanged
        ),
        "manifest_entries": len(exact_paths) + len(archived_exceptions),
        "exact_original_paths": sum(exact_paths.values()),
        "exact_original_path_failures": [
            path for path, passed in exact_paths.items() if not passed
        ],
        "authorized_additive_navigation_exceptions": sorted(
            PROTECTED_EXCEPTIONS
        ),
        "archived_exception_hashes": archived_exceptions,
        "old_navigation_preserved": old_navigation_preserved,
        "protected_claim_paths_unchanged": protected_claim_paths_unchanged,
    }


def upload_manifest_checks() -> dict[str, object]:
    allowlist_path = CANDIDATE / "HF_UPLOAD_ALLOWLIST.txt"
    manifest_path = CANDIDATE / "SHA256SUMS.txt"
    allowed = allowlist_path.read_text(encoding="utf-8").splitlines()
    manifest: dict[str, str] = {}
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split(maxsplit=1)
        manifest[relative] = expected
    missing: list[str] = []
    mismatched: list[str] = []
    non_text: list[str] = []
    for relative in allowed:
        if relative == "SHA256SUMS.txt":
            continue
        source = upload_source(relative)
        if not source.is_file():
            missing.append(relative)
            continue
        try:
            source.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            non_text.append(relative)
        if manifest.get(relative) != sha256(source):
            mismatched.append(relative)
    return {
        "passed": (
            bool(allowed)
            and len(allowed) == len(set(allowed))
            and allowed == sorted(allowed)
            and "HF_UPLOAD_ALLOWLIST.txt" in allowed
            and "SHA256SUMS.txt" in allowed
            and set(manifest) == set(allowed) - {"SHA256SUMS.txt"}
            and not missing
            and not mismatched
            and not non_text
        ),
        "allowlisted_paths": len(allowed),
        "hashed_paths": len(manifest),
        "missing": missing,
        "hash_mismatches": mismatched,
        "non_text": non_text,
    }


def audit_release_candidate() -> dict[str, object]:
    logbook = json.loads(
        (CANDIDATE / "logbook.json").read_text(encoding="utf-8")
    )
    children = logbook["root"]["children"]
    current_page = (
        CANDIDATE / "pages" / "current-verification" / "page.md"
    ).read_text(encoding="utf-8")
    claim6_page = (
        CANDIDATE
        / "pages"
        / "claim-6-independent-replication"
        / "page.md"
    ).read_text(encoding="utf-8")
    expected_status = {
        1: "VERIFIED",
        2: "FALSIFIED",
        3: "VERIFIED",
        4: "FALSIFIED",
        5: "VERIFIED",
        6: "BLOCKED",
    }
    status_checks = {
        f"claim_{claim}": (
            f"| {claim} | this page | yes | yes | yes | yes | yes | yes | {status} |"
            in current_page
        )
        for claim, status in expected_status.items()
    }
    output_checks: dict[str, bool] = {}
    expected_controls = {
        1: "REJECTED_NOT_ALGORITHM_1",
        2: "REJECTED_AS_COUNTEREXAMPLE",
        3: "REJECTED_BAD_SUBSTITUTE",
        4: "REJECTED_AS_COUNTEREXAMPLE",
        5: "REJECTED_INVALID_ASSUMPTIONS",
        6: "REJECTED_NONCONCAVE_SERIES",
    }
    for claim, expected_control in expected_controls.items():
        payload = json.loads(
            (
                CANDIDATE
                / "raw"
                / f"claim{claim}_checker_control_output.json"
            ).read_text(encoding="utf-8")
        )
        output_checks[f"claim_{claim}_status"] = (
            payload["status"] == expected_status[claim]
        )
        output_checks[f"claim_{claim}_checker"] = bool(
            payload["independent_checker"]["passed"]
        )
        output_checks[f"claim_{claim}_control"] = (
            payload["negative_control"]["status"] == expected_control
        )
    claim6_output = json.loads(
        (
            CANDIDATE / "raw" / "claim6_independent_output.json"
        ).read_text(encoding="utf-8")
    )
    output_checks["claim_6_independent_status"] = (
        claim6_output["status"] == "VERIFIED"
    )
    output_checks["claim_6_independent_checker"] = bool(
        claim6_output["independent_checker"]["passed"]
    )
    output_checks["claim_6_independent_control"] = (
        claim6_output["negative_control"]["status"]
        == "REJECTED_INVALID_SUBSTITUTE"
    )
    preservation = protected_preservation_checks()
    required = required_evidence_checks()
    target_artifact = (
        ROOT / ".openresearch" / "artifacts" / "claim_6_independent"
    )
    target_required = {
        name: (target_artifact / name).is_file()
        and (target_artifact / name).stat().st_size > 0
        for name in (
            "claim_contract.json",
            "source_audit.md",
            "method.md",
            "command_environment.md",
            "EVAL.md",
            "limitations.md",
            "latest_output.json",
            "raw_population.csv",
            "raw_concavity.csv",
            "raw_finite_m.csv",
        )
    }
    target_required.update(
        {
            "space_page": (
                CANDIDATE
                / "pages"
                / "claim-6-independent-replication"
                / "page.md"
            ).is_file(),
            "space_verifier": (
                CANDIDATE / "code" / "claim6_independent_verifier.py"
            ).is_file(),
            "space_contract": (
                CANDIDATE / "contracts" / "claim6_independent_contract.json"
            ).is_file(),
        }
    )
    syntax = syntax_checks()
    secrets = secret_scan()
    upload_manifest = upload_manifest_checks()
    checks = {
        "space_id_exact": logbook["space_id"] == "DineshAI/vqxprtjuKH",
        "claim_6_independent_page_first": (
            children[0]["slug"] == "claim-6-independent-replication"
            and children[0]["file"]
            == "pages/claim-6-independent-replication/page.md"
        ),
        "protected_current_verification_still_reachable": any(
            child["slug"] == "current-verification"
            and child["file"] == "pages/current-verification/page.md"
            for child in children
        ),
        "historical_pages_labeled": all(
            child["title"].startswith("Historical rejected baseline")
            for child in children
            if child["slug"]
            not in {
                "claim-6-independent-replication",
                "current-verification",
                "release-audit",
            }
        ),
        "fixed_command_visible": (
            "uv run --frozen python -m reproduction.run_all" in current_page
        ),
        "pinned_environment_visible": (
            "pyproject.toml" in current_page and "uv.lock" in current_page
        ),
        "raw_cumulative_visible": "cumulative_evidence_run_ae95cd12.json" in current_page,
        "no_pending_cells": "| pending |" not in current_page,
        "live_score_not_overclaimed": "remains `5/12`" in current_page,
        "claim_6_exact_scope_visible": (
            "VERIFIED as an independent qualitative replication" in claim6_page
            and "exact unpublished author run remains **BLOCKED**" in claim6_page
        ),
        "claim_6_raw_evidence_visible": all(
            token in claim6_page
            for token in (
                "claim6_independent_population.csv",
                "claim6_independent_concavity.csv",
                "claim6_independent_finite_m.csv",
                "claim6_independent_output.json",
            )
        ),
        "all_status_rows_complete": all(status_checks.values()),
        "all_output_checks_pass": all(output_checks.values()),
        "all_required_evidence_present": all(required.values()),
        "all_target_evidence_present": all(target_required.values()),
        "all_python_sources_compile": all(syntax.values()),
        "protected_10_12_preservation_gate": bool(preservation["passed"]),
        "secret_scan_clean": not secrets,
        "upload_allowlist_and_manifest_valid": bool(upload_manifest["passed"]),
    }
    return {
        "passed": all(checks.values()),
        "checks": checks,
        "visibility_status_rows": status_checks,
        "checker_control_outputs": output_checks,
        "required_evidence": required,
        "target_required_evidence": target_required,
        "protected_10_12_preservation": preservation,
        "secret_findings": secrets,
        "compiled_sources": len(syntax),
        "upload_manifest": upload_manifest,
    }
