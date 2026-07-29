"""Blind, canonical-entrypoint traversal of an assembled Space candidate."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote


SPACE_LINK = re.compile(
    r"https://huggingface\.co/spaces/DineshAI/vqxprtjuKH/"
    r"(?:blob|tree)/main/([^\s)]+)"
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.candidate.resolve()
    opened: list[str] = []
    missing: list[str] = []

    def open_text(relative: str) -> str:
        normalized = unquote(relative).split("#", 1)[0]
        path = root / normalized
        if path.is_dir():
            texts: list[str] = []
            for child in sorted(path.rglob("*")):
                if child.is_file():
                    try:
                        texts.append(child.read_text(encoding="utf-8"))
                        opened.append(str(child.relative_to(root)))
                    except UnicodeDecodeError:
                        continue
            return "\n".join(texts)
        if not path.is_file():
            missing.append(normalized)
            return ""
        opened.append(normalized)
        return path.read_text(encoding="utf-8")

    readme = open_text("README.md")
    logbook_text = open_text("logbook.json")
    index = open_text("pages/index.md")
    logbook = json.loads(logbook_text)
    children = logbook["root"]["children"]
    navigation = {child["slug"]: child["file"] for child in children}
    claim6_path = navigation.get("claim-6-independent-replication")
    claim6_page = open_text(claim6_path) if claim6_path else ""
    current_path = navigation.get("current-verification")
    current = open_text(current_path) if current_path else ""
    release_path = navigation.get("release-audit")
    release_page = open_text(release_path) if release_path else ""

    followed: set[str] = set()
    for text in (readme, index, claim6_page, current, release_page):
        for relative in SPACE_LINK.findall(text):
            normalized = unquote(relative)
            if normalized not in followed:
                open_text(normalized)
                followed.add(normalized)

    claim_checks: dict[str, dict[str, bool]] = {}
    expected = {
        1: "VERIFIED",
        2: "FALSIFIED",
        3: "VERIFIED",
        4: "FALSIFIED",
        5: "VERIFIED",
        6: "VERIFIED",
    }
    for claim, verdict in expected.items():
        independent_target = claim == 6
        output_path = (
            "raw/claim6_independent_output.json"
            if independent_target
            else f"raw/claim{claim}_checker_control_output.json"
        )
        output = json.loads(open_text(output_path))
        bundle = root / "artifacts" / (
            "claim_6_independent" if independent_target else f"claim_{claim}"
        )
        raw_prefix = (
            "claim6_independent_" if independent_target else f"claim{claim}_"
        )
        raw_candidates = list((root / "raw").glob(f"{raw_prefix}*"))
        source_candidates = (
            [
                root / "code" / "claim6_independent_verifier.py",
                root
                / "reproduction"
                / "claims"
                / "claim6_independent_replication.py",
                root
                / "reproduction"
                / "checkers"
                / "claim6_independent_checker.py",
            ]
            if independent_target
            else [
                root / "code" / f"claim{claim}_verifier.py",
                root / "reproduction" / "checkers" / f"claim{claim}_checker.py",
            ]
        )
        canonical_page = claim6_page if independent_target else current
        contract_name = (
            "claim6_independent_contract.json"
            if independent_target
            else f"claim{claim}_contract.json"
        )
        verifier_name = (
            "claim6_independent_verifier.py"
            if independent_target
            else f"claim{claim}_verifier.py"
        )
        claim_checks[f"claim_{claim}"] = {
            "canonical_page": f"Claim {claim} " in canonical_page,
            "code_visible": all(path.is_file() for path in source_candidates),
            "data_inline": (
                (
                    "48/48 optimizers converged" in claim6_page
                    and "36/36 concavity tests" in claim6_page
                    and "144/144 finite-`m` estimates" in claim6_page
                )
                if independent_target
                else (
                    f"| {claim} | this page | yes | yes | yes | yes | yes | yes | {verdict} |"
                    in current
                )
            ),
            "raw_link": bool(raw_candidates)
            and f"raw/{raw_prefix}" in canonical_page,
            "checker": bool(output["independent_checker"]["passed"]),
            "control": output["negative_control"]["status"].startswith("REJECTED"),
            "exact_claim_tested": (
                (root / "contracts" / contract_name).is_file()
                and (bundle / "source_audit.md").is_file()
            ),
            "reviewer_verdict": output["status"] == verdict,
            "method_visible": (bundle / "method.md").is_file(),
            "limitations_visible": (bundle / "limitations.md").is_file(),
            "environment_visible": (bundle / "command_environment.md").is_file(),
            "verifier_nonzero_contract": (
                "raise SystemExit(main())"
                in (root / "code" / verifier_name).read_text(
                    encoding="utf-8"
                )
                and "else 2"
                in (root / "code" / verifier_name).read_text(encoding="utf-8")
            ),
        }
    visibility_complete = all(
        all(checks.values()) for checks in claim_checks.values()
    )
    checks = {
        "readme_points_to_current": "#/current-verification" in readme,
        "claim6_page_first": bool(children)
        and children[0]["slug"] == "claim-6-independent-replication",
        "claim6_page_opened": claim6_path in opened,
        "current_page_opened": current_path in opened,
        "fixed_command_visible": "uv run --frozen python -m reproduction.run_all" in current,
        "pinned_environment_reachable": (
            (root / "pyproject.toml").is_file() and (root / "uv.lock").is_file()
        ),
        "raw_cumulative_reachable": (
            root / "raw" / "cumulative_evidence_run_ae95cd12.json"
        ).is_file(),
        "run_metadata_reachable": (root / "raw" / "run_metadata.json").is_file(),
        "visibility_matrix_complete": visibility_complete,
        "historical_current_separation": all(
            child["title"].startswith("Historical rejected baseline")
            for child in children
            if child["slug"]
            not in {
                "claim-6-independent-replication",
                "current-verification",
                "release-audit",
            }
        ),
        "no_missing_followed_links": not missing,
    }
    result = {
        "passed": all(checks.values()),
        "checks": checks,
        "claim_checks": claim_checks,
        "files_opened": list(dict.fromkeys(opened)),
        "missing_paths": sorted(set(missing)),
        "unverifiable_conclusions": [
            "Claim 6 is independently numerically reproduced; exact regeneration of the unpublished author plotting run remains BLOCKED because the paper omits required configuration and raw values."
        ],
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    print(rendered)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0 if result["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
