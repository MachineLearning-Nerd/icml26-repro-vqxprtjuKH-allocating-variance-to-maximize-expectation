# Claim 6 — independent numerical replication

## Verdict

**VERIFIED as an independent qualitative replication.**

The exact unpublished author run remains **BLOCKED**; this page does not claim
pixel-for-pixel regeneration.

## Exact claim and source ambiguity

Figures 1–2 and Section 1.3 state that `n=8`, `p=1/8,...,8/8`
Erdős–Rényi simulations illustrate concavity of optimal value and increasing
concentration under independent, exact positive-block, and exact
negative-block Gaussian dependence.

The paper simultaneously uses two descriptions:

1. `p=|S_j|/n` and every fixed-size `k` subset in Theorem 1.5;
2. Bernoulli Erdős–Rényi membership in the figure caption.

We tested both. The Bernoulli model is conditioned on a nonempty set because
the paper does not define `max` over an empty set.

## Reproducible method

For `n=8`, the population mean maximum over all size-`k` subsets is computed
from sorted Gaussian coordinates with exact combinatorial weights. The
Bernoulli population is the exact conditional-binomial mixture of these eight
objectives. Thus the paper's omitted `m` is not guessed in the population
reference.

Each of 48 cases (two set models × three dependence regimes × eight `p`
values) is optimized on the variance simplex with:

- 4,096 scrambled-Sobol common-random-number training draws;
- a disjoint 32,768-draw Sobol validation scramble;
- SLSQP, `ftol=1e-10`, at most 180 iterations;
- symmetry-reduced equal-support and uniform starts;
- exact `+1` or `-1` correlation inside fixed 2×2 blocks.

Ordinary finite-`m=8192` Monte Carlo at seeds `101`, `202`, and `303` checks
all 48 cases. A separate NumPy pseudo-random implementation uses 32,768
samples and seed `184632502`.

Fixed command:

`uv run --frozen python -m reproduction.run_all`

Successful run:
`1da2d5d6-f35e-404d-a38a-77cf5b257b0b` at Git commit
`dc11c556f7dbf34bc643e60eb3c1e11bce682e88`.

## Results

- 48/48 optimizers converged and satisfied the simplex.
- 36/36 concavity tests had no four-standard-error violation.
- 6/6 concentration comparisons passed.
- 144/144 finite-`m` estimates agreed with the population reference.
- The independent checker passed.
- The uniform/nonconcave substitute was rejected.

| Regime, fixed-cardinality model | Effective support at p=0.25 | Effective support at p=1 |
| --- | ---: | ---: |
| independent | 7.999 | 4.104 |
| positive block | 5.124 | 3.996 |
| negative block | 8.000 | 2.019 |

The Bernoulli-conditioned model independently passed the same concentration
gate. The largest candidate positive second difference was
`0.003723 ± 0.001564` for fixed-cardinality negative block correlation at
center `p=0.75`; its four-standard-error lower endpoint is `-0.002532`, so it
is not a significant violation. The independent checker also found no
significant violation.

## Evidence and executable checks

- [Raw 48-row population table](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/raw/claim6_independent_population.csv)
- [Raw 36-row concavity table](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/raw/claim6_independent_concavity.csv)
- [Raw 144-row finite-m table](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/raw/claim6_independent_finite_m.csv)
- [Primary, checker, and control JSON](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/raw/claim6_independent_output.json)
- [Complete cumulative run JSON](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/raw/cumulative_evidence_run_1da2d5d6.json)
- [Run and seed metadata](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/raw/run_metadata_claim6.json)
- [Standalone verifier](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/code/claim6_independent_verifier.py)
- [Primary implementation](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/reproduction/claims/claim6_independent_replication.py)
- [Independent checker](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/reproduction/checkers/claim6_independent_checker.py)
- [Exact contract](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/contracts/claim6_independent_contract.json)
- [Method, source audit, limitations, and evaluation](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/tree/main/artifacts/claim_6_independent)
- [Protected 10/12 manifest](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/protected_10_12/MANIFEST.sha256)

## Scope and preservation

The source bundle still has no simulation code or raw data and omits `m`,
seeds, sample count, optimizer, stopping rule, values, and uncertainty.
Therefore the exact historical plotting run is not identified.

This release is additive. The protected 10/12 current-verification page,
Claims 1–5 pages, artifacts, executable verifiers, raw results, verdict text,
and old navigation paths remain present. The exact protected logbook is
archived under `protected_10_12/logbook.json`; the live logbook only adds this
target page ahead of the old entries.
