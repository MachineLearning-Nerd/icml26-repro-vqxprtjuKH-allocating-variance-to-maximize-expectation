# Source audit — Claim 1

Theorem 1.1 assumes `mu_i >= 0`, fixed `epsilon>0`, independent Gaussians, and
total variance one. It promises a polynomial-in-`n` allocation with expected
maximum at least `OPT-epsilon`.

Algorithm 1 in Appendix A.1 sets `k=1/epsilon^2`, guesses the supported
variables, enumerates standard deviations that are integer multiples of
`epsilon^3`, evaluates the independent Gaussian maximum, and returns the best.
The prose proves `O(epsilon)` loss; the exact theorem tolerance therefore uses
the standard PTAS reparameterization to a sufficiently small internal accuracy.

Source and hash are the same as the campaign source audit. The arXiv source
bundle was additionally retrieved on 2026-07-25 with an explicit user-agent;
its SHA-256 is
`459cf66ee46d8c78ca931343dbf1d13729d3e4ce62ab1179c93aa34212b7f2af`.
