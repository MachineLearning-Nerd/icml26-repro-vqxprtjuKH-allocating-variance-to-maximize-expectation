# Evaluation — Claim 3

Verdict: **VERIFIED under the paper proof's assumptions**.

The named Algorithm 3 implementation, independent 384-node quadrature,
exhaustive same-level checks, proof-obligation checks, sparse scaling through
`n=16384`, star negative control, and cumulative regression all passed at
commit `1ddb02136c7ab95f14dfb8b199072bc6a2775385` (run
`ae95cd12-130e-47cc-8d9c-7f2b745649aa`).

The proof uses nonnegative means, while the executable instances use the
zero-mean subdomain. Polynomial runtime is measured in the explicit input
length; the stated shorthand “polynomial in n” also needs a polynomial-size
set list. The live judge has not evaluated this evidence.
