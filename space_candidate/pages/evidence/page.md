# Evidence


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_0ba0d479184b", "created_at": "2026-07-22T14:54:59+00:00", "title": "Verification output (last 40 lines)"}
-->
## Verification output (last 40 lines)

```
CLAIM 3 (Thm 1.3): m>1  O(log n) approx  >= Omega(1/log n) OPT
==============================================================================
  GraphVarAlloc n=8, 15 edge-sets: greedy=3.3231, OPT~3.3302, ratio=0.998 >= c/log n=0.333
  -> PASS

==============================================================================
CLAIM 4 (Thm 1.6): optimal allocation concentrates on a small subset
==============================================================================
  optimal support k* vs n: [(8, 5), (16, 5), (32, 5), (64, 5), (128, 5)] (stays bounded ~5)
  each active var variance >= 1/5 = 0.200 (Omega(1))
  -> PASS (allocation concentrates, not spread over n)

==============================================================================
CLAIM 5 (Lemma 2.1): small-variance vars contribute O(eps*sqrt(ln(1/eps)))
==============================================================================
  delta=0.30: small-var contribution=-0.0002, bound C*delta*sqrt(ln(1/delta))=1.9751  (ok)
  delta=0.20: small-var contribution=0.0002, bound C*delta*sqrt(ln(1/delta))=1.5224  (ok)
  delta=0.10: small-var contribution=-0.0001, bound C*delta*sqrt(ln(1/delta))=0.9105  (ok)
  -> PASS

==============================================================================
CLAIM 6 (Sec 1.3): ER n=8 sim shows concentration + concavity
==============================================================================
  ER n=8 val/concentration by edge-prob: [(0.12, 1.11, np.float64(0.4)), (0.25, 1.288, np.float64(0.4)), (0.5, 2.401, np.float64(0.4)), (0.75, 3.98, np.float64(0.4)), (1.0, 5.191, np.float64(0.4))]
  E[max] by budget [0.25, 0.5, 1.0, 1.5, 2.0]: [1.857, 2.626, 3.713, 4.548, 5.251] (concave: True)
  top-2-node variance fraction (dense graph): 0.40 (concentrates: True)
  -> PASS

==============================================================================
VERDICT SUMMARY
==============================================================================
  [PASS] c1_ptas_m1
  [PASS] c2_ptas_correlated
  [PASS] c3_m_gt1_logn
  [PASS] c4_concentration
  [PASS] c5_lemma2_small_var
  [PASS] c6_er_sim

  6/6 claims verified.
  wrote outputs/verdict.json
```
