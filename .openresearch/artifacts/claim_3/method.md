# Method — Claim 3

The implementation follows Algorithm 3 literally after the paper's zero-mean
reduction. For equal selected variance, each set contribution is a
one-dimensional Gaussian order-statistic integral. Greedy gains are updated
only for sets incident to the newly selected variable, but the chosen variable
is exactly the global maximum current marginal with deterministic tie-breaking.

The primary verifier:

- checks all variance budgets at every dyadic level;
- exhaustively enumerates every same-cardinality subset on an eight-variable
  hypergraph and checks the `1-1/e` greedy guarantee;
- runs deterministic sparse mixed graph/hypergraph instances through
  `n=16384`;
- checks a star instance where the exact first greedy choice is known.

The independent checker uses a 384-node Gauss-Legendre integration table and
fresh exhaustive enumeration. The negative control replaces marginal greedy
selection by fixed index order on a star whose center has the last index. It
must be rejected below the `1-1/e` level guarantee.
