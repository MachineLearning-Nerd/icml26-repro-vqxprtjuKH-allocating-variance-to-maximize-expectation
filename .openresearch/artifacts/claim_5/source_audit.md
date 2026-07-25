# Claim 5 source audit

The source and hash are the same explicit-User-Agent retrieval recorded for
Claim 4. Lemma 2.1 is at `#S2.Thmtheorem1`; its proof begins in Section 2.1.

Exact assumptions:

- any `epsilon in (0,1)`;
- any positive number of zero-mean jointly Gaussian variables;
- every marginal variance lies in `[0,epsilon^2]`;
- the sum of marginal variances is at most one;
- no independence assumption.

The conclusion uses big-O. The only mathematically coherent reading is
asymptotic as `epsilon -> 0`; a uniform bound on all of `(0,1)` cannot use
`sqrt(log(1/epsilon))`, which vanishes as `epsilon -> 1`. The verifier therefore
states and checks the explicit range `epsilon <= exp(-1)`.

