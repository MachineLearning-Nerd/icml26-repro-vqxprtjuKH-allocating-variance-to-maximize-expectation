# Command and environment

- Fixed experiment command: `uv run --frozen python -m reproduction.run_all`
- Environment manager: `uv`
- Python constraint: `>=3.11,<3.13` (`.python-version` selects 3.12)
- Resolved packages: `uv.lock`
- Intended compute: one CPU worker
- Deterministic seed: none required (exact rational proof)
- Primary verifier: `reproduction/claims/claim4_counterexample.py`
- Independent checker: `reproduction/checkers/claim4_checker.py`
- Standalone negative control:
  `uv run --frozen python -m reproduction.claims.claim4_counterexample --negative-control`
  (expected exit code 1)

