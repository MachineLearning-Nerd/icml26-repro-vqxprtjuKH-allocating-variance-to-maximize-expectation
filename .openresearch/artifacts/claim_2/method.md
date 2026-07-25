# Method — Claim 2

Take `n=2`, `mu=(2,0)`, and `epsilon=1/10`. The covariance `diag(0,1)` is PSD
with trace one, and the first input variable is deterministically two.
Therefore the input `OPT>=2`.

For any literal theorem output `Y~N(0,Sigma_hat)` with trace one,

`E max(Y1,Y2) = E|Y1-Y2|/2`.

Writing `v=Sigma_11`, PSD implies
`Sigma_12>=-sqrt(v(1-v))`. Since `v(1-v)<=1/4`,
`Var(Y1-Y2)<=2`, so the Gaussian absolute-moment formula gives
`E max(Y1,Y2)<=1/sqrt(pi)<1`. The theorem would require at least
`OPT-epsilon>=19/10`, a strict contradiction.

The independent checker reconstructs the variance bound from the exact identity
`1/4-v(1-v)=(2v-1)^2/4`.
