# Limitations and deviations — Claim 1

- The paper writes `k=1/epsilon^2`; the executable uses the conservative
  integer ceiling.
- The paper does not say how a coarse standard-deviation grid satisfies the
  equality variance constraint. We enumerate budget-feasible grid points and
  complete leftover variance afterward, explicitly recording both vectors.
- The proof text gives `O(epsilon)` rather than its hidden constant. The exact
  universal theorem uses standard internal-accuracy reparameterization; finite
  displayed cases additionally have direct rigorous upper-bound certificates.
- Scaling uses a coarse fixed epsilon so the named exhaustive algorithm is
  computationally observable at hundreds of variables. It is not presented as
  a small-epsilon practical algorithm.
