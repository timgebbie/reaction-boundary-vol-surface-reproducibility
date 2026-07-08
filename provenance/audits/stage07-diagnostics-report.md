# Stage 7 Code Diagnostics And Numerical Verification

Artefact status: Stage 7 diagnostic report

Completed:

- Created `scripts/03_run_diagnostics.py`.
- Created `run-notes/stage07-diagnostics-run-note-v1.md`.
- Ran the diagnostics command:

```bash
python scripts/03_run_diagnostics.py
```

- Generated diagnostic outputs:
  - `diagnostics/stage07-diagnostics-v1.csv`
  - `diagnostics/stage07-diagnostics-v1.md`

Diagnostic result:

- Total checks: 42.
- Verified checks: 42.
- Failed checks: 0.

Important checks passed:

- Low-z response is positive and finite.
- High-z response is positive and finite.
- Low-z response branch is independent of `z`.
- High-z response decreases with `z` for the baseline `0 < gamma < 1`.
- All profile/regime components are positive and finite.
- All variance and volatility surfaces are positive and finite.
- Surface array shape is `(96, 121)` for all profile/regime combinations.
- Homogeneous baseline is state-flat.
- Resilience-only profile has no leading-order low-z state effect and has a
  high-z state effect.

Implementation adjustment made during diagnostics:

- The first diagnostic run exposed that `scipy` was unavailable in the
  runtime environment.
- The high-z prefactor implementation was revised to use the
  standard-library `math.lgamma` instead of `scipy.special.gammaln`.
- Syntax compilation passed after the adjustment.

Not completed:

- No figures generated.
- No paper tables generated.
- No captions generated.
- No interpretation written.

Current diagnostic status:

Verified with the current Stage 7 checks. The code is ready for controlled
Stage 8 table/figure generation.

Recommended next stage:

Stage 8: figure, table, and caption generation with provenance.

