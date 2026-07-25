# Current verification

This page supersedes the historical verifier at revision
`f16e54bdef639f2be75cb380594c9371871a3cc4`. The historical pages remain
reachable below under the exact navigation label **Historical rejected
baseline**.

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
- [Exact claim contract](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/contracts/claim4_contract.json)

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

## Visibility matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | pending | pending | pending | pending | pending | pending | pending | BLOCKED |
| 2 | pending | pending | pending | pending | pending | pending | pending | BLOCKED |
| 3 | pending | pending | pending | pending | pending | pending | pending | BLOCKED |
| 4 | this page | yes | yes | yes | yes | yes | yes | FALSIFIED |
| 5 | pending | pending | pending | pending | pending | pending | pending | BLOCKED |
| 6 | pending | pending | pending | pending | pending | pending | pending | BLOCKED |

