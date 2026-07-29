# Command and environment — independent Claim 6 replication

Fixed command:

`uv run --frozen python -m reproduction.run_all`

Successful OpenResearch run:
`1da2d5d6-f35e-404d-a38a-77cf5b257b0b`

Git commit:
`dc11c556f7dbf34bc643e60eb3c1e11bce682e88`

Backend: Hugging Face `cpu-upgrade`, image
`ghcr.io/astral-sh/uv:python3.12-bookworm-slim`.

The container reported Python 3.12.12, 64 visible CPUs, and 64 CPUs in its
affinity mask. The implementation deliberately uses one worker. Scientific
runtime was 8.476 seconds; the cumulative six-claim suite took 47.603 seconds
and the supervised run duration was 1 minute 36 seconds.
