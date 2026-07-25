# Command and environment — Claim 1

Fixed command: `uv run --frozen python -m reproduction.run_all`.

The repository-level `.venv`, Python 3.12, `pyproject.toml`, and `uv.lock` are
inherited unchanged. Formal execution uses Hugging Face `cpu-upgrade` and the
locked uv Python image. The implementation has exactly one designed worker.
