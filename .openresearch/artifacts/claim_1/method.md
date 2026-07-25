# Method — Claim 1

This is the paper's support-and-grid algorithm, not the continuous optimizer
used as `OPT`. Search candidates have at most `ceil(epsilon^-2)` positive
entries and every pre-completion standard deviation is an integer multiple of
`epsilon^3`. Because a generic grid tuple does not exhaust variance one, the
remaining variance is added to a supported coordinate after the grid search;
mean-preserving spread cannot lower an expected convex maximum.

Finite non-negative-mean cases in low- and high-mean-spread regimes are checked
against a rigorous Chernoff log-sum-exp upper bound on `OPT`. For each Chernoff
parameter, convexity in the variance vector means its maximum on the simplex
occurs at a vertex. An adaptive-quadrature checker independently recomputes
every reported PTAS objective.

Scaling uses fixed `epsilon=0.8`, hence fixed support cap two, and unique
deterministic non-negative means through `n=512`. This directly demonstrates
the fixed-epsilon polynomial search rather than equating PTAS with OPT.
