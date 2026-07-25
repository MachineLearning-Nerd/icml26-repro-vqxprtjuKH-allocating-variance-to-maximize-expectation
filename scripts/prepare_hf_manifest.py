"""Create the exact text-only Space upload allowlist and SHA-256 manifest."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


TEXT_SUFFIXES = {".csv", ".json", ".lock", ".md", ".py", ".toml", ".txt"}
ALWAYS_TEXT = {".python-version", "HF_UPLOAD_ALLOWLIST.txt", "SHA256SUMS.txt"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("judged", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("source_output", type=Path)
    args = parser.parse_args()
    judged_files = {
        str(path.relative_to(args.judged)): digest(path)
        for path in args.judged.rglob("*")
        if path.is_file() and ".git" not in path.parts
    }
    candidate_text = {
        str(path.relative_to(args.candidate)): path
        for path in args.candidate.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and (path.suffix in TEXT_SUFFIXES or path.name in ALWAYS_TEXT)
    }
    changed = sorted(
        relative
        for relative, path in candidate_text.items()
        if judged_files.get(relative) != digest(path)
    )
    for generated in ("HF_UPLOAD_ALLOWLIST.txt", "SHA256SUMS.txt"):
        if generated not in changed:
            changed.append(generated)
    changed.sort()

    allowlist_path = args.source_output / "HF_UPLOAD_ALLOWLIST.txt"
    manifest_path = args.source_output / "SHA256SUMS.txt"
    allowlist_path.write_text("\n".join(changed) + "\n", encoding="utf-8")

    hash_rows: list[str] = []
    for relative in changed:
        if relative == "SHA256SUMS.txt":
            continue
        source = (
            allowlist_path
            if relative == "HF_UPLOAD_ALLOWLIST.txt"
            else args.candidate / relative
        )
        if not source.is_file():
            raise SystemExit(f"allowlisted source is absent: {relative}")
        source.read_text(encoding="utf-8")
        hash_rows.append(f"{digest(source)}  {relative}")
    manifest_path.write_text("\n".join(hash_rows) + "\n", encoding="utf-8")
    print(f"text_upload_paths={len(changed)}")
    print(f"hashed_paths={len(hash_rows)}")


if __name__ == "__main__":
    main()
