# Limitations and deviations

- The verdict uses standard asymptotic big-O as `epsilon -> 0`, made explicit
  as `epsilon <= exp(-1)`.
- The paper's phrase “for any epsilon in (0,1)” should not be read as a single
  uniform constant up to `epsilon=1`; that literal reading is false because
  the displayed rate tends to zero there.
- The numerical family is independent, while the analytic certificate covers
  arbitrary correlations.
- Numerical integration corroborates and calibrates the proof; it is not the
  basis for the universal verdict.

