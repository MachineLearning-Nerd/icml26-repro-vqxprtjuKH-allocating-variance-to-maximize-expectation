# Method

The primary route independently derives an `Lq` moment certificate. It gives
the explicit dimension-free bound

`E max(0,max_i Y_i) <= e sqrt(2) epsilon sqrt(log(1/epsilon))`

for `epsilon <= exp(-1)`, including arbitrary correlations.

The numerical stress family is deliberately non-vacuous: for every tested
`epsilon`, it has `m=1/epsilon^2` independent variables, each with variance
exactly `epsilon^2`, so every variance is nonzero and the total variance is
exactly one. Adaptive quadrature evaluates

`epsilon * integral_0^infinity [1-Phi(z)^m] dz`.

An independent 512-node Gauss-Legendre calculation on `[0,12]` must agree
within `2e-10`. The negative control removes the total-variance budget and
uses a super-polynomial number of equal-variance variables; it is rejected
because the uncontrolled `sqrt(log m)` factor returns.

