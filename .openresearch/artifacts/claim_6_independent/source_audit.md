# Source audit — independent Claim 6 replication

The arXiv v1 source bundle has SHA-256
`459cf66ee46d8c78ca931343dbf1d13729d3e4ce62ab1179c93aa34212b7f2af`.
Its 19 members include the rendered figure PNGs but no Python, R, Julia,
notebook, CSV, JSON, NumPy, or other simulation artifact. The paper and source
omit `m`, graph and Gaussian seeds, Monte Carlo count, optimizer, stopping
rule, raw values, and uncertainty. GitHub searches by paper id, OpenReview id,
title, and authors found no author implementation; arXiv lists one version and
no associated code.

The paper itself leaves a model ambiguity. Section 1.3 defines
`p=|S_j|/n`, and Theorem 1.5 averages over every fixed-size `k` subset. The
figure captions instead call the instance Erdős–Rényi, corresponding to
independent Bernoulli membership. The replication therefore tests both:

1. all fixed-cardinality `k`-subsets at `p=k/8`; and
2. Bernoulli membership at `p=k/8`, conditioned on nonempty sets because
   `max` over an empty set is undefined.

Exact published-pixel regeneration remains `BLOCKED`. The independent
qualitative claim is evaluated without inventing a hidden author configuration.
