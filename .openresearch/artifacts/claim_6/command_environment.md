# Command and environment — Claim 6

Fixed command: `uv run --frozen python -m reproduction.run_all`.

The verifier uses one CPU worker, the locked repository `.venv`, Python 3.12,
Pillow, and NumPy. It downloads only the public arXiv source with an explicit
user-agent and refuses a source bundle whose SHA-256 differs from the audited
hash.
