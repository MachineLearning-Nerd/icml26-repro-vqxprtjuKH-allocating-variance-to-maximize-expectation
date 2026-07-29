# Evaluation — independent Claim 6 replication

Verdict: **VERIFIED as an independent qualitative replication.**

Exact regeneration of the authors' unpublished plotting run remains
**BLOCKED**.

All declared gates passed:

- 48/48 optimizers converged and satisfied the variance simplex;
- 36/36 second-difference tests showed no four-standard-error concavity
  violation across both set models and all three dependence regimes;
- 6/6 concentration comparisons showed smaller effective support from
  `p=2/8` to `p=1`;
- 144/144 finite-`m` multi-seed estimates agreed with the population
  reference;
- the independent 32,768-sample pseudo-random checker passed;
- the uniform/nonconcave substitute was rejected.

The largest candidate positive second difference was `0.003723 ± 0.001564`
for fixed-cardinality negative block correlation at center `p=0.75`; its
four-standard-error lower endpoint is `-0.002532`, so it is not a significant
violation. The independent checker likewise found no significant violation.

Fixed-cardinality effective supports changed as follows:

| Regime | p=0.25 | p=1 |
| --- | ---: | ---: |
| independent | 7.999 | 4.104 |
| positive block | 5.124 | 3.996 |
| negative block | 8.000 | 2.019 |

The Bernoulli-conditioned model independently passed the same concentration
gate.
