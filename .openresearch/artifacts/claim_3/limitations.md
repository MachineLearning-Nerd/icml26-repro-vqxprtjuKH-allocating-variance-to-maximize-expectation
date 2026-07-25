# Limitations and deviations — Claim 3

- The implementation covers the zero-mean core exactly. The paper's proof
  reduces non-negative means to this core, but Theorem 1.3 does not restate
  that sign assumption.
- Runtime is polynomial in the explicit input length. A literal
  polynomial-in-`n` statement requires `m` and the total set incidence length
  to be polynomial in `n`.
- Large scaling instances corroborate runtime and feasibility; they are not by
  themselves proof of a universal approximation theorem.
- The proof certificate depends on the cited analytic lemmas and the classical
  Nemhauser submodular-greedy theorem; the executable checks their concrete
  consequences rather than formalizing all real analysis in a proof assistant.
