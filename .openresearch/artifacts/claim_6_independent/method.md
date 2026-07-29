# Method — independent Claim 6 replication

For `n=8`, the mean maximum over all size-`k` subsets is computed from each
Gaussian draw's sorted coordinates using the exact combinatorial weight

`P(x_(r) is the subset maximum) = C(r,k-1) / C(8,k)`.

The Bernoulli-population objective is the exact mixture of those eight
fixed-cardinality objectives under the conditional binomial size law. This
removes the paper's omitted `m` from the population reference.

For every one of 48 cases (two set models, three dependence regimes, eight
`p` values), SLSQP optimizes the variance simplex. It starts from the best
symmetry-reduced equal-support allocation and the uniform allocation, uses
4,096 scrambled-Sobol common-random-number draws, `ftol=1e-10`, and at most
180 iterations. A disjoint 32,768-draw Sobol scramble supplies values and
standard errors.

The exact covariance restriction in Figure 1 is reproduced: the positive
case has identical latent normals within each fixed pair, and the negative
case uses opposite signs within each fixed pair. All means are zero.

Controls:

- ordinary finite-`m=8192` Monte Carlo at seeds `101`, `202`, and `303` for
  every case must agree with the population reference;
- an independent NumPy pseudo-random checker uses 32,768 samples and seed
  `184632502`;
- a uniform-at-`p=1` substitute and an artificial nonconcave curve must be
  rejected.
