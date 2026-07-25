# Method — Claim 1

This is the paper's support-and-grid algorithm, not the continuous optimizer
used as `OPT`. Search candidates have at most `ceil(epsilon^-2)` positive
entries and every pre-completion standard deviation is an integer multiple of
`epsilon^3`. Because a generic grid tuple does not exhaust variance one, the
remaining variance is added to a supported coordinate after the grid search;
mean-preserving spread cannot lower an expected convex maximum.

One nonzero-mean case is checked against a rigorous Chernoff log-sum-exp upper
bound on `OPT`; for each Chernoff parameter, convexity in the variance vector
makes its maximum on the simplex occur at a vertex. A separate canonical
zero-mean case uses the pointwise positive-part energy bound
`max_i X_i <= sqrt(sum_i (X_i^+)^2)`, which yields `OPT<=1/sqrt(2)` by Jensen
and Gaussian symmetry. An adaptive-quadrature checker independently recomputes
every reported PTAS objective.

Scaling uses fixed `epsilon=0.8`, hence fixed support cap two, and unique
deterministic non-negative means through `n=512`. This directly demonstrates
the fixed-epsilon polynomial search rather than equating PTAS with OPT.
