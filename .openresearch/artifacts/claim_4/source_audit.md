# Claim 4 source audit

Source retrieved from `https://ar5iv.labs.arxiv.org/html/2502.18463` on
2026-07-25T04:48:47Z with an explicit `OpenResearch-Reproduction/1.0`
User-Agent. The retrieved HTML SHA-256 is
`12fdb660f2782fdacabf98f8e9b8950438d15b77517c0548677ed30d16b7d9ef`.

Anchors:

- problem model: `#S1.SS1`;
- concentration discussion: `#S1.SS3`;
- theorem statement: `#S1.Thmtheorem6`;
- random-graph proof: `#A2.SS1`.

The theorem uses an Erdős–Rényi incidence model: each variable belongs to each
set independently with probability `p`; the Gaussians are independent,
zero-mean, and have total variance budget one. It states the result as
`n,m -> infinity` but does not say that `p` is fixed, bounded below, or that
`np -> infinity`.

The source text contains the phrase “with probability p > 1-delta”. Because
`p` already denotes edge probability, the contract adopts the only coherent
reading, “with probability > 1-delta”. The counterexample remains valid under
that charitable correction.

