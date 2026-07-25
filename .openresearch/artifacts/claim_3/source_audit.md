# Source audit — Claim 3

Source: ar5iv HTML for arXiv 2502.18463, retrieved 2026-07-25 with an
explicit OpenResearch browser user-agent. Recorded HTML SHA-256:
`12fdb660f2782fdacabf98f8e9b8950438d15b77517c0548677ed30d16b7d9ef`.

Theorem 1.3 says that, given a GraphVarAlloc input, an algorithm polynomial in
`n` returns a variance vector whose objective is `Omega(1/log n) OPT`.
Appendix B.2 gives Algorithm 3:

1. remove singleton sets;
2. for every integer `k=0,...,floor(log2 n)`, greedily select
   `min(4^k,n)` variables;
3. give every selected variable variance `4^-k`;
4. return the level having the largest original objective.

The proof cites Lemma 2.6 (power-of-four rounding), Lemma 2.1 (small-variance
tail), Lemma 2.7 (submodularity), Lemma B.1, and the Nemhauser greedy theorem.
Its mean-removal step explicitly uses non-negative means, although that
restriction is not repeated in Theorem 1.3. The executable evidence tests the
zero-mean domain exactly and calls out this scope issue rather than hiding it.

The explicit-set representation also makes runtime polynomial in input size
`n + sum_j |S_j|`; a literal bound polynomial only in `n` needs the conventional
assumption that the explicit set list has polynomial length.
