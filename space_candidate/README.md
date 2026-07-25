---
title: "Repro - Allocating Variance to Maximize Expectation"
emoji: 🎯
colorFrom: yellow
colorTo: red
sdk: static
pinned: false
tags:
 - trackio
 - trackio-logbook
 - open-experiment
 - icml2026-repro
 - paper-vqxprtjuKH
---

# Repro - Allocating Variance to Maximize Expectation

## Current evaluator entrypoint

[Open the current claim-by-claim verification](#/current-verification), then
read the [release audit and score forecast](#/release-audit).

The current evidence verdicts are:

| Claim | Verdict |
| --- | --- |
| 1 | VERIFIED |
| 2 | FALSIFIED as written |
| 3 | VERIFIED under proof assumptions |
| 4 | FALSIFIED as written |
| 5 | VERIFIED |
| 6 | BLOCKED after four routes |

The fixed command is
`uv run --frozen python -m reproduction.run_all`. Raw data, executable
verifiers, independent checker output, controls, assumptions, limitations,
runtime/CPU metadata, and the visibility matrix are linked inline from the
current page. The live judged score remains `5/12` pending reevaluation.

The prior judged content is preserved and labeled **Historical rejected
baseline**. This logbook is published with
[Trackio](https://github.com/gradio-app/trackio).
