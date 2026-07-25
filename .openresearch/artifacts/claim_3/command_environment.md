# Command and environment — Claim 3

Fixed command inherited from the frozen baseline:

`uv run --frozen python -m reproduction.run_all`

Environment: repository `.venv`, Python 3.12, `pyproject.toml`, and `uv.lock`.
Formal execution uses Hugging Face `cpu-upgrade` with image
`ghcr.io/astral-sh/uv:python3.12-bookworm-slim`. The implementation has one
designed worker and does not parallelize across the allocated CPUs.
