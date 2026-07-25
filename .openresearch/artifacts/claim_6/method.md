# Four verification routes — Claim 6

1. **Source completeness.** Download the exact hashed arXiv bundle and inspect
   every member. This establishes which reproduction inputs are actually
   public.
2. **Image-data extraction.** Recover the independent and negative-correlation
   Figure 1 curves from exact Matplotlib RGB pixels. Check second differences,
   and inspect the dominant horizontal allocation levels for `p=0.25` and
   `p=1` in Figure 2.
3. **Independent proof route.** Reconstruct the max inequality used in the
   independent concavity proof and check 2,401 integer sanity cases. This
   supports the independent theorem but cannot supply missing correlated
   simulation settings.
4. **Dedicated falsification route.** Search the digitized negative-correlation
   curve for a concavity violation. Its final pixel second difference is
   `-3`, but that is comparable to line width. Without raw values and
   uncertainty it is not a valid counterexample.

The final result is `BLOCKED`, not `PASS`: the paper image is observable, but
the Monte Carlo experiment that generated it is not fully specified.
