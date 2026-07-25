# Claims


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_ddd8b6e53f1f", "created_at": "2026-07-22T14:54:58+00:00", "title": "Claims to reproduce"}
-->
## Claims to reproduce

1. For the independent Gaussian variance allocation problem, the paper gives a PTAS achieving E[max_i X_i] ≥ OPT - ε in polynomial time (Theorem 1.1, Section 1.2).
2. For correlated Gaussian variables, a PTAS with the same additive ε guarantee is established (Theorem 1.2, Section 1.2).
3. For the GraphVarAlloc problem with multiple constraint sets (general m>1), the paper gives an O(log n) multiplicative approximation guaranteeing Ω(1/log n)·OPT (Theorem 1.3, Section 1.2).
4. Theorem 1.6 proves that in the optimal allocation, only Θ(1/p) variables receive variance Ω(p), i.e., the allocation concentrates on a shrinking subset as the constraint parameter p grows (Theorem 1.6, Section 1.3).
5. Lemma 2.1 bounds the contribution of small-variance variables by O(ε√ln(1/ε)), which is used to limit the number of high-variance variables to O(1/ε²) and underlies the PTAS construction (Lemma 2.1, Section 2.1).
6. Monte Carlo simulations on Erdős–Rényi random graphs with n=8 nodes and edge probabilities p ranging from 1/8 to 8/8 are used to illustrate the concentration and concavity results across independent, positively, and negatively correlated settings (Figures 1-2, Section 1.3).
