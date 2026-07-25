# Current verification

This page supersedes the historical verifier at revision
`f16e54bdef639f2be75cb380594c9371871a3cc4`. The historical pages remain
reachable below under the exact navigation label **Historical rejected
baseline**.

## Reproduction contract and cumulative result

The exact paper source was retrieved on `2026-07-25` from
`https://ar5iv.labs.arxiv.org/html/2502.18463` with an explicit browser
User-Agent; its SHA-256 is
`12fdb660f2782fdacabf98f8e9b8950438d15b77517c0548677ed30d16b7d9ef`.
The arXiv source bundle SHA-256 is
`459cf66ee46d8c78ca931343dbf1d13729d3e4ce62ab1179c93aa34212b7f2af`.
The exact theorem anchors, assumptions, and quantifiers are in each linked
claim contract and source audit.

Every experiment node inherited the same command:

`uv run --frozen python -m reproduction.run_all`

The pinned environment is Python 3.12 with
[pyproject.toml](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/pyproject.toml)
and [uv.lock](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/uv.lock).
The latest cumulative run is OpenResearch run
`ae95cd12-130e-47cc-8d9c-7f2b745649aa` at Git commit
`1ddb02136c7ab95f14dfb8b199072bc6a2775385`. It used Hugging Face
`cpu-upgrade`: 64 logical CPUs were visible and in the affinity mask, while
the implementation deliberately used one worker. Scientific runtime was
`54.625654894975014` seconds and supervised wall time was `127` seconds.
All checks are deterministic (`seed=null`).

- [Complete raw cumulative JSON](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/raw/cumulative_evidence_run_ae95cd12.json)
- [Cumulative verifier and nonzero exit contract](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/reproduction/run_all.py)
- [Pinned implementation package](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/tree/main/reproduction)

## Claim 6 — Figures 1–2

**Exact reproduction verdict: BLOCKED after four routes.**

The source bundle contains the rendered figures, but no simulation code or raw
data. The paper specifies `n=8`, `p=1/8,...,1`, and ±1 correlation inside 2x2
blocks, while omitting `m`, seeds, Monte Carlo sample count, optimizer,
stopping rule, raw values, and uncertainty. Those choices materially determine
the displayed allocations.

Four different routes were completed:

1. the exact hashed arXiv bundle was inspected member by member;
2. Figure 1 was digitized from exact RGB pixels, and Figure 2 visibly changes
   from one uniform level at `p=0.25` to two allocation levels at `p=1`;
3. the max inequality underlying the independent concavity proof was
   reconstructed and checked;
4. a falsification attempt found a `-3`-pixel final second difference in the
   negative-correlation curve, but this is comparable to line width and is not
   a valid numerical counterexample without raw values.

The independent displayed curve has pixel second differences
`[142, 41, 7.5, 12, 9, 9]`, consistent with concavity. This is evidence about
the image, not an independently regenerated Monte Carlo experiment.

- [Digitized raw CSV](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/raw/claim6_digitized_payoff.csv)
- [Four-route verifier](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/code/claim6_verifier.py)
- [Primary four-route implementation](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/reproduction/claims/claim6_figure_audit.py)
- [Independent checker source](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/reproduction/checkers/claim6_checker.py)
- [Checker and control output](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/raw/claim6_checker_control_output.json)
- [Exact claim contract](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/contracts/claim6_contract.json)
- [Source audit, method, environment, and limitations](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/tree/main/artifacts/claim_6)

## Claim 2 — Theorem 1.2

**Exact reproduction verdict: FALSIFIED as written. Live judge: pending.**

CorrVarAlloc is defined with supplied means `mu`, but Theorem 1.2 evaluates its
promised output under `N(0,Sigma_hat)`. Choose `n=2`, `mu=(2,0)`, and
`epsilon=1/10`. The feasible covariance `diag(0,1)` makes the first input
variable deterministically two, so `OPT>=2`.

For every literal zero-mean output with trace one,

`E max(Y1,Y2)=E|Y1-Y2|/2 <= 1/sqrt(pi) < 1`,

because PSD and `v(1-v)<=1/4` imply
`Var(Y1-Y2)<=2`. The promised inequality would require at least
`OPT-epsilon>=19/10`, which is impossible.

This falsifies the theorem's published quantifiers. It does **not** falsify a
repaired theorem restricted to zero-mean input; that repair is the negative
control and removes the contradiction.

| n | mu | epsilon | input OPT lower | required output | zero-mean output upper |
| ---: | --- | ---: | ---: | ---: | ---: |
| 2 | (2,0) | 1/10 | 2 | 19/10 | 1/sqrt(pi) |

- [Raw certificate](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/raw/claim2_counterexample.csv)
- [Executable verifier](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/code/claim2_verifier.py)
- [Primary counterexample implementation](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/reproduction/claims/claim2_counterexample.py)
- [Independent checker source](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/reproduction/checkers/claim2_checker.py)
- [Checker and control output](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/raw/claim2_checker_control_output.json)
- [Exact claim contract](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/contracts/claim2_contract.json)
- [Source audit, method, environment, and limitations](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/tree/main/artifacts/claim_2)

## Claim 1 — Theorem 1.1 and Algorithm 1

**Exact reproduction verdict: VERIFIED. Live judge: pending.**

The candidate now runs the paper's distinct PTAS: it enumerates supports of at
most `ceil(epsilon^-2)` variables and every budget-feasible tuple on the
`epsilon^3` standard-deviation grid. It does not use the continuous reference
optimizer as both “PTAS” and “OPT”.

For a nonzero-mean case, a Chernoff log-sum-exp certificate gives a rigorous
upper bound on `OPT`. A separate canonical zero-mean case uses the independent
positive-part energy certificate `OPT<=1/sqrt(2)`. The candidate must be within
`epsilon` of the applicable upper bound. Adaptive quadrature independently
recomputes the displayed objective. Fixed-epsilon polynomial scaling uses
unique means through `n=512`.
An equal-variance OPT-like substitute is rejected because it violates both the
support cap and the specified grid.

The paper's proof states `O(epsilon)` loss; the exact theorem uses the standard
PTAS reparameterization to a smaller internal accuracy. The candidate exposes
that calibration and its hidden-constant limitation.

| case | n | epsilon | candidates | PTAS objective | rigorous OPT upper | certified gap |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| nonzero mean | 6 | 0.8 | 21 | 0.703109846980 | 1.480519860791 | 0.777410013811 |
| zero mean | 6 | 0.7 | 152 | 0.506279250318 | 0.707106781187 | 0.200827530868 |

At fixed `epsilon=0.8`, candidate counts were `528`, `2,080`, `8,256`,
`32,896`, and `131,328` for `n=32,64,128,256,512`; measured runtimes were
`0.0399`, `0.1890`, `0.9747`, `5.8420`, and `38.8984` seconds. The independent
adaptive-quadrature discrepancies were at most `1.07e-14`.

- [Raw cases and scaling CSV](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/raw/claim1_algorithm1.csv)
- [Executable verifier](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/code/claim1_verifier.py)
- [Algorithm 1 implementation](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/reproduction/claims/claim1_algorithm1.py)
- [Independent checker](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/reproduction/checkers/claim1_checker.py)
- [Checker and control output](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/raw/claim1_checker_control_output.json)
- [Exact claim contract](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/contracts/claim1_contract.json)
- [Source audit, method, environment, and limitations](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/tree/main/artifacts/claim_1)

## Claim 3 — Theorem 1.3 and Algorithm 3

**Exact reproduction verdict: VERIFIED under the proof assumptions. Live
judge: pending.**

The current candidate implements the paper's named Algorithm 3: it tries every
integer `k=0,...,floor(log2 n)`, greedily selects `min(4^k,n)` variables using
the exact current GraphVarAlloc objective marginal, assigns selected variance
`4^-k`, and returns the best level. It does not substitute brute-force OPT for
the approximation algorithm.

The verifier combines the Appendix B.2 proof obligations with exhaustive
same-level subset optimization on an eight-variable hypergraph, an independent
384-node quadrature checker, sparse scaling through `n=16384`, and a star
negative control. The control replaces greedy marginals with fixed index order
and must fall below `1-1/e`.

Scope audit: the executable core uses zero means, exactly the core reached by
the paper's proof. That proof invokes non-negative means even though Theorem
1.3 does not repeat the sign restriction. Runtime is polynomial in the explicit
input length; “polynomial in n” also requires a polynomial-length set list.

| n | set count m | best k | selected | objective | runtime (s) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 64 | 192 | 3 | 64 | 15.7973083393 | 0.00748 |
| 256 | 768 | 4 | 256 | 31.5946166787 | 0.04275 |
| 1,024 | 3,072 | 5 | 1,024 | 63.1892333573 | 0.24739 |
| 4,096 | 12,288 | 6 | 4,096 | 126.3784667147 | 1.08508 |
| 16,384 | 49,152 | 7 | 16,384 | 252.7569334294 | 6.02690 |

On the complete eight-variable domain, every level matched exhaustive
same-level optimization and the independent 384-node quadrature checker
within `1.99e-13`. The fixed-order star control achieved only
`0.007874` of the correct greedy objective, below `1-1/e`, and was rejected.

- [Raw exhaustive, scaling, and control CSV](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/raw/claim3_algorithm3.csv)
- [Executable verifier](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/code/claim3_verifier.py)
- [Algorithm 3 implementation](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/reproduction/claims/claim3_algorithm3.py)
- [Independent checker](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/reproduction/checkers/claim3_checker.py)
- [Checker and control output](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/raw/claim3_checker_control_output.json)
- [Exact claim contract](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/contracts/claim3_contract.json)
- [Source audit, method, environment, and limitations](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/tree/main/artifacts/claim_3)

## Claim 4 — Theorem 1.6

**Exact reproduction verdict: FALSIFIED as written. Live judge: pending.**

The theorem states that for random GraphVarAlloc instances as `n,m -> infinity`
there are `Theta(1/p)` variables receiving variance `Omega(p)`. It does not
restrict how the Erdős–Rényi edge probability `p` may scale with `n`.

Choose `m_n=n` and `p_n=1/n^2`. These satisfy the stated random-instance model,
but `Theta(1/p_n)=Theta(n^2)` variables cannot exist among only `n` variables:

`N_large / (1/p_n) <= n/n^2 = 1/n -> 0`.

This is a counterexample to the unrestricted-`p` theorem. It does **not**
falsify a repaired version assuming fixed `p`.

### Assumption audit and raw certificate

| n | m | p | 1/p | maximum possible variables | cap / (1/p) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | 8 | 1/64 | 64 | 8 | 1/8 |
| 16 | 16 | 1/256 | 256 | 16 | 1/16 |
| 32 | 32 | 1/1024 | 1024 | 32 | 1/32 |
| 64 | 64 | 1/4096 | 4096 | 64 | 1/64 |
| 128 | 128 | 1/16384 | 16384 | 128 | 1/128 |
| 256 | 256 | 1/65536 | 65536 | 256 | 1/256 |
| 512 | 512 | 1/262144 | 262144 | 512 | 1/512 |
| 1024 | 1024 | 1/1048576 | 1048576 | 1024 | 1/1024 |

- [Download raw CSV](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/raw/claim4_counterexample.csv)
- [Executable verifier](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/code/claim4_verifier.py)
- [Primary counterexample implementation](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/reproduction/claims/claim4_counterexample.py)
- [Independent checker source](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/reproduction/checkers/claim4_checker.py)
- [Checker and control output](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/raw/claim4_checker_control_output.json)
- [Exact claim contract](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/contracts/claim4_contract.json)
- [Source audit, method, environment, and limitations](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/tree/main/artifacts/claim_4)

Run: `python code/claim4_verifier.py`

Independent checker: exact rational arithmetic re-parses every row and verifies
`p=1/n^2`, `1/p=n^2`, and the ratio `1/n`. It reports `passed=true`.

Negative control: `python code/claim4_verifier.py --negative-control` uses fixed
`p=1/4`. It exits 1 with `REJECTED_AS_COUNTEREXAMPLE`, because the cap `n` is
compatible with `Theta(1/p)=Theta(4)`.

Compute: deterministic one-worker CPU proof; no random seed; runtime is reported
by the fixed OpenResearch command
`uv run --frozen python -m reproduction.run_all`. The pinned environment is
`pyproject.toml` plus `uv.lock` in the linked GitHub revision.

## Claim 5 — Lemma 2.1

**Exact reproduction verdict: VERIFIED under the standard
`epsilon -> 0` big-O reading. Live judge: pending.**

For `M=max(0,max_i Y_i)`, `v_i=Sigma_ii`, and
`q=2 log(1/epsilon)>=2`, the independent proof certificate checks

`M^q <= sum_i (Y_i^+)^q`,

`sum_i v_i^(q/2) <= epsilon^(q-2) sum_i v_i <= epsilon^(q-2)`,

and the Gaussian moment bound
`E[(Z_+)^q] <= q^(q/2)`. Therefore

`E[M] <= sqrt(q) epsilon^(1-2/q)
      = e sqrt(2) epsilon sqrt(log(1/epsilon))`

for `epsilon<=exp(-1)`. This argument uses only Gaussian marginal moments, so
it permits every correlation allowed by the lemma.

The stress family is non-vacuous: `m=1/epsilon^2` independent variables each
have variance exactly `epsilon^2`; all variances are positive and their sum is
one. Adaptive quadrature is independently checked by 256-node Gauss-Legendre
integration.

- [Raw nonzero cases](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/raw/claim5_nonzero_cases.csv)
- [Executable verifier](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/code/claim5_verifier.py)
- [Primary proof-certificate implementation](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/reproduction/claims/claim5_lemma21.py)
- [Independent checker source](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/reproduction/checkers/claim5_checker.py)
- [Checker and control output](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/raw/claim5_checker_control_output.json)
- [Exact claim contract](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/contracts/claim5_contract.json)
- [Source audit, method, environment, and limitations](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/tree/main/artifacts/claim_5)

Negative control: removing `sum_i Sigma_ii<=1` restores the uncontrolled
`sqrt(log m)` factor. The control exits 1 as
`REJECTED_INVALID_ASSUMPTIONS`.

## Visibility matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | this page | yes | yes | yes | yes | yes | yes | VERIFIED |
| 2 | this page | yes | yes | yes | yes | yes | yes | FALSIFIED |
| 3 | this page | yes | yes | yes | yes | yes | yes | VERIFIED |
| 4 | this page | yes | yes | yes | yes | yes | yes | FALSIFIED |
| 5 | this page | yes | yes | yes | yes | yes | yes | VERIFIED |
| 6 | this page | yes | yes | yes | yes | yes | yes | BLOCKED |

`VERIFIED` and `FALSIFIED` are scientific evidence verdicts, not live judge
points. The live judged score remains `5/12` until the evaluator records a new
revision.
