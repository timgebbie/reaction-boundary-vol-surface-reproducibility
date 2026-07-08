# Stage 06 Implementation Notes v1

Artefact status: implementation draft

Implementation target:

Configuration files and reusable helper functions for the two response
regimes, three structural profiles, and projected variance/volatility
surface evaluator.

Files created:

- `config/parameter-ranges-v1.csv`
- `config/profile-definitions-v1.json`
- `functions/__init__.py`
- `functions/response_regimes.py`
- `functions/structural_profiles.py`
- `functions/vol_surface_kernel.py`

Stage 7 dependency update:

- The implementation no longer requires `scipy` for the high-z prefactor.
  It uses the standard-library `math.lgamma`.

No scripts were created.
No figures were generated.
No tables were generated.
No output files were generated.

Implemented theory objects:

- Low-z response case from `eq:F-asymp`.
- High-z response case from `eq:F-asymp`.
- Three structural profiles from the Stage 5 numerical design.
- Projected variance surface using the main-result closure and
  deterministic activity profile.

Expected next stage:

Stage 7 code diagnostics. The first checks should import the modules,
evaluate small grids for all profile/regime combinations, and verify
positivity, finite values, and qualitative response-regime behaviour.
