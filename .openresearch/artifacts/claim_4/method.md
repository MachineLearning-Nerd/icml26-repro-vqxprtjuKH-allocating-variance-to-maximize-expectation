# Method

This route tests the exact quantifiers before performing stochastic
optimization. Choose the allowed asymptotic sequence

`m_n = n`, `p_n = 1/n^2`.

Every instance has exactly `n` Gaussian variables, so every subset of variables
(including those receiving variance at least any threshold) has cardinality at
most `n`. The theorem's lower `Theta(1/p_n)` requirement would require at least
`c/p_n = c n^2` variables for some constant `c>0` and all sufficiently large
`n`. For `n>1/c`, `c n^2 > n`, a contradiction. Equivalently,

`N_large / (1/p_n) <= n/n^2 = 1/n -> 0`,

so `N_large` cannot be `Omega(1/p_n)`.

The independent checker parses the raw CSV using exact rational arithmetic.
The negative control fixes `p=1/4`; then `1/p=4`, and the cardinality cap no
longer contradicts a constant-size support. The route correctly rejects that
control as a counterexample.

