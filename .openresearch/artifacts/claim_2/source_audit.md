# Source audit — Claim 2

The CorrVarAlloc definition gives means `mu_1,...,mu_n` as input and optimizes
the expectation under `N(mu,Sigma)`. Theorem 1.2 then says “Given an input to
CorrVarAlloc” but evaluates the promised output as
`(X_1,...,X_n) ~ N(0,Sigma_hat)`.

Those are different quantified problems. The counterexample uses the literal
published text. It does not assert that the likely intended zero-mean theorem
is false.

Paper HTML retrieval and hash are recorded in the campaign source audit.
The arXiv source bundle independently confirms the wording; source-tar SHA-256:
`459cf66ee46d8c78ca931343dbf1d13729d3e4ce62ab1179c93aa34212b7f2af`.
