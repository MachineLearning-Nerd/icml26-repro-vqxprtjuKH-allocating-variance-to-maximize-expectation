# Command and environment

- Fixed command: `uv run --frozen python -m reproduction.run_all`
- Primary: `reproduction/claims/claim5_lemma21.py`
- Independent checker: `reproduction/checkers/claim5_checker.py`
- Negative control:
  `uv run --frozen python -m reproduction.claims.claim5_lemma21 --negative-control`
  (expected exit code 1)
- Random seeds: none; all calculations are deterministic
- Worker count: one
- Locked environment: repository `uv.lock`

