# Release audit and score forecast

Previous live judged score: `5/12`

Conservative projected score range after the proposed change: **7–10/12**

Best-supported possible new score: **10/12 (forecast, not a judge result)**

The live evaluator has not scored this candidate. No score increase is claimed.

## Claim forecast

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| 1 | 1 | 2 | MEDIUM | VERIFIED | The named Algorithm 1, rigorous finite OPT upper certificates, independent quadrature, scaling through `n=512`, and a rejected OPT-like control all pass. Remaining risk: the proof writes `O(epsilon)` and needs the standard internal-accuracy calibration. |
| 2 | 1 | 2 | MEDIUM | FALSIFIED | The exact literal mean/output counterexample has a rational checker and repaired-zero-mean control. Remaining risk: an evaluator may impose the likely intended zero-mean input restriction instead of the printed quantifiers. |
| 3 | 1 | 2 | MEDIUM | VERIFIED | The named Algorithm 3, exhaustive level optimization, independent quadrature, sparse scaling through `n=16384`, and a rejected fixed-order control pass. Remaining risk: the proof uses nonnegative means and explicit-input-size conventions. |
| 4 | 0 | 2 | MEDIUM | FALSIFIED | The sequence `m_n=n`, `p_n=n^-2` satisfies the printed unrestricted asymptotic domain and gives an exact cardinality contradiction. Remaining risk: the evaluator may read `p` as implicitly fixed. |
| 5 | 1 | 2 | HIGH | VERIFIED | An explicit universal moment certificate covers arbitrary correlation, five strictly positive budget-saturating families, independent quadrature, and a rejected assumption-violating control. |
| 6 | 1 | 0 | LOW | BLOCKED | Exactly four routes are complete. The image and proof can be audited, but omitted `m`, seeds, Monte Carlo count, optimizer, stopping rule, raw values, and uncertainty prevent exact regeneration or valid falsification. |

Current total score: **5/12**.

Conservative projected total score range: **7–10/12**.

Best-supported possible total score: **10/12**, as a forecast only.

Claims 1, 2, 3, 4, and 5 materially changed since the previous judge result.
Claim 6 changed from a toy proxy to an honestly documented **BLOCKED** result.

## Low-confidence four-route record

Claim 6 is the only LOW-confidence claim. Its required routes were:

1. source-bundle completeness: 19 members, six rendered PNGs, no script or raw
   numeric data;
2. exact-RGB image digitization: independent pixel second differences
   `[142,41,7.5,12,9,9]`, and Figure 2 changes from one allocation level at
   `p=0.25` to two at `p=1`;
3. independent proof reconstruction: Lemma B.3 was derived exactly and checked
   on 2,401 sanity cases;
4. dedicated falsification: the negative curve's final `-3`-pixel second
   difference is comparable to line width and is not a valid raw-data
   counterexample.

The fourth route did not establish falsification. Claim 6 therefore remains
BLOCKED. Author simulation code/configuration and raw per-seed outputs would
unblock it.

## Evaluator-blind traversal

The exact judged revision was downloaded into a fresh directory. A separate
candidate tree was assembled, then reviewed only from `README.md`,
`logbook.json`, and `pages/index.md`.

Pass 1 exposed two defects in the automated traversal itself: its URL parser
truncated `.csv`/`.json` paths at the letter `s`, and its static nonzero-exit
detector missed multiline returns in the Claim 1 and Claim 3 wrappers. The
candidate files were present; the audit correctly remained failed until the
review logic was fixed.

Pass 2 opened the canonical current page, all six verifiers, all six
independent checker sources, all contracts, raw tables, checker/control
outputs, environment files, methods, limitations, and the cumulative JSON.
Every visibility cell passed and no followed path was missing. The only
conclusion that remained unverifiable was the deliberately BLOCKED exact
Monte Carlo regeneration for Claim 6.

- [Pass 1 raw traversal record](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/raw/evaluator_blind_pass1.json)
- [Pass 2 raw traversal record, including every file opened](https://huggingface.co/spaces/DineshAI/vqxprtjuKH/blob/main/raw/evaluator_blind_pass2.json)

## Visibility matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Current verification | yes | yes | yes | yes | yes | yes | VERIFIED |
| 2 | Current verification | yes | yes | yes | yes | yes | yes | FALSIFIED |
| 3 | Current verification | yes | yes | yes | yes | yes | yes | VERIFIED |
| 4 | Current verification | yes | yes | yes | yes | yes | yes | FALSIFIED |
| 5 | Current verification | yes | yes | yes | yes | yes | yes | VERIFIED |
| 6 | Current verification | yes | yes | yes | yes | yes | yes | BLOCKED |

## Preservation and publication action

Every content hash from judged revision
`f16e54bdef639f2be75cb380594c9371871a3cc4` appears in the candidate.
Unchanged evidence remains at its original path. The three navigation files
that changed are additionally preserved byte-for-byte under
`historical_judged/`.

After all gates pass, the exact action is a text-only commit to the existing
Space `DineshAI/vqxprtjuKH`; no second Space will be created. The published
text paths will then be mirrored to GitHub `main`, followed by a fresh download,
hash verification, and canonical-entrypoint traversal. The paper will remain
marked awaiting judge.
