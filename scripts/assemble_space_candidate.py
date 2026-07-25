"""Assemble the exact additive Hugging Face Space candidate for audit."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".csv", ".json", ".lock", ".md", ".py", ".toml", ".txt"}


def copy_tree(source: Path, destination: Path, *, text_only: bool = False) -> None:
    for path in sorted(source.rglob("*")):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if text_only and path.suffix not in TEXT_SUFFIXES:
            continue
        target = destination / path.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--judged-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() and any(args.output.iterdir()):
        raise SystemExit("output must be an existing empty directory or absent")
    args.output.mkdir(parents=True, exist_ok=True)

    copy_tree(args.judged_root, args.output)
    copy_tree(ROOT / "space_candidate", args.output)
    copy_tree(ROOT / "reproduction", args.output / "reproduction", text_only=True)
    copy_tree(
        ROOT / ".openresearch" / "artifacts",
        args.output / "artifacts",
        text_only=True,
    )
    for filename in (".python-version", "pyproject.toml", "uv.lock"):
        shutil.copy2(ROOT / filename, args.output / filename)
    shutil.copy2(
        ROOT / ".openresearch" / "run_metadata.json",
        args.output / "artifacts" / "run_metadata.json",
    )


if __name__ == "__main__":
    main()
