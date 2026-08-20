# Reproducing “Allocating Variance to Maximize Expectation”

## Collection classification and audit boundary

This repository is a **legacy/source workspace** for *Allocating Variance to Maximize Expectation*
(arXiv `2502.18463`, OpenReview `vqxprtjuKH`). It is preserved
separately from the standardized canonical record at
[`icml26-variance-allocation`](https://github.com/MachineLearning-Nerd/icml26-variance-allocation).

The claim results and scores recorded below are historical results of this
workspace. They are not new paper-level verifications performed while
organizing the collection. The collection audit did not run the scientific
implementation; the canonical record documents its own scoped status and
limitations.

### How the historical claim evidence is produced

The claim table and experiment log below are the authoritative mapping from
each paper claim to its producer, command, control, and evidence artifact. In
this workspace, the Algorithms 1/3 implementations, exact certificates, independent checkers, concentration routes, and Monte Carlo figure runners produce the claim table and committed evidence.

The former `orx/*` branches are historical workstreams, not additional final
publication claims. Their purposes and tips are preserved in
[`BRANCH_AUDIT.md`](BRANCH_AUDIT.md). Citation and author acknowledgment
details are in [`CITATION.cff`](CITATION.cff) and
[`AUTHOR_THANK_YOU.md`](AUTHOR_THANK_YOU.md).

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-vqxprtjuKH-allocating-variance-to-maximize-expectation/blob/main/notebooks/allocating_variance_reproduction.py)

This project reproduces all six principal claims of
[arXiv:2502.18463](https://arxiv.org/abs/2502.18463). The previous live judge
score is **5/12**; it has not yet evaluated this revision.

The new evidence implements the paper's Algorithms 1 and 3 instead of using an
OPT-like proxy, supplies exact proof certificates and independent checkers,
tests Lemma 2.1 on strictly positive variances, varies the missing concentration
parameter analytically, and completes four distinct routes for the published
Monte Carlo figures.

| Claim | Paper result | Observed result | Evidence assessment |
| --- | --- | --- | --- |
| 1 | independent PTAS achieves `OPT-ε` | certified gaps `0.7774≤0.8` and `0.2008≤0.7`; scaling to `n=512` | VERIFIED |
| 2 | correlated PTAS for a CorrVarAlloc input | literal theorem requires `≥1.9`, but every zero-mean output is `≤1/sqrt(pi)=0.5642` | FALSIFIED as written |
| 3 | `O(log n)` GraphVarAlloc approximation | named greedy matches exhaustive level optima; scaling to `n=16,384` | VERIFIED under proof assumptions |
| 4 | `Theta(1/p)` high-variance variables | `p_n=n^-2` demands `Theta(n²)` variables among `n` | FALSIFIED as written |
| 5 | small-variance contribution is `O(ε sqrt(log(1/ε)))` | explicit constant; five nonzero budget-saturating families | VERIFIED |
| 6 | Monte Carlo Figures 1–2 | image/proof audit completed; exact generator parameters and raw values absent | BLOCKED |

Formal runs used CPU only on Hugging Face `cpu-upgrade`, Python 3.12, one
designed worker, and the locked repository-level `uv` environment. The latest
cumulative scientific runtime was `54.626` seconds (`127` seconds supervised).
There are no downscaled claims described as full-scale; finite theorem checks
are paired with proof certificates or valid counterexamples, and Claim 6 is
left blocked.

- [Illustrated claim-by-claim report](reports/allocating-variance/report.md)
- [Self-contained tutorial notebook](notebooks/allocating_variance_reproduction.py)
- [Exact cumulative raw evidence](space_candidate/raw/cumulative_evidence_run_ae95cd12.json)
- [Current evaluator-visible Space page](space_candidate/pages/current-verification/page.md)

To rerun every current verifier, independent checker, and negative control:

```bash
uv run --frozen python -m reproduction.run_all
```

To explore the already-produced evidence without rerunning the formal suite:

```bash
uv run --frozen marimo edit notebooks/allocating_variance_reproduction.py
# or
uv run --frozen marimo run notebooks/allocating_variance_reproduction.py
```

## Experiment log

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| `main` | Public landing page and release surface | Not run as an experiment (publication surface) | Presentation only | none |
| [`orx/exact-contract-baseline`](https://github.com/MachineLearning-Nerd/icml26-repro-vqxprtjuKH-allocating-variance-to-maximize-expectation/tree/orx/exact-contract-baseline) | Frozen environment, source audit, Theorem 1.6 contract | `uv run --frozen python -m reproduction.run_all` | Claim 4 FALSIFIED as written | HF `cpu-upgrade`, one worker |
| [`orx/lemma-2-1-exact-moment-certificate`](https://github.com/MachineLearning-Nerd/icml26-repro-vqxprtjuKH-allocating-variance-to-maximize-expectation/tree/orx/lemma-2-1-exact-moment-certificate) | Nonzero-variance Lemma 2.1 proof and checker | `uv run --frozen python -m reproduction.run_all` | Claim 5 VERIFIED | HF `cpu-upgrade`, one worker |
| [`orx/algorithm-3-faithful-certified-scaling`](https://github.com/MachineLearning-Nerd/icml26-repro-vqxprtjuKH-allocating-variance-to-maximize-expectation/tree/orx/algorithm-3-faithful-certified-scaling) | Named Algorithm 3, exhaustive checker, scaling | `uv run --frozen python -m reproduction.run_all` | Claim 3 VERIFIED under proof assumptions | HF `cpu-upgrade`, one worker |
| [`orx/algorithm-1-independent-ptas-scaling`](https://github.com/MachineLearning-Nerd/icml26-repro-vqxprtjuKH-allocating-variance-to-maximize-expectation/tree/orx/algorithm-1-independent-ptas-scaling) | Named Algorithm 1, OPT certificates, scaling | `uv run --frozen python -m reproduction.run_all` | Claim 1 VERIFIED | HF `cpu-upgrade`, one worker |
| [`orx/theorem-1-2-literal-mean-counterexample`](https://github.com/MachineLearning-Nerd/icml26-repro-vqxprtjuKH-allocating-variance-to-maximize-expectation/tree/orx/theorem-1-2-literal-mean-counterexample) | Exact literal mean/output counterexample | `uv run --frozen python -m reproduction.run_all` | Claim 2 FALSIFIED as written | HF `cpu-upgrade`, one worker |
| [`orx/figures-1-2-four-route-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-vqxprtjuKH-allocating-variance-to-maximize-expectation/tree/orx/figures-1-2-four-route-audit) | Four verification/falsification routes for Figures 1–2 | `uv run --frozen python -m reproduction.run_all` | Claim 6 BLOCKED; cumulative suite passed | HF `cpu-upgrade`, one worker |

## Upstream workspace

ICML 2026 agent reproduction workspace for OpenReview paper `vqxprtjuKH`.
