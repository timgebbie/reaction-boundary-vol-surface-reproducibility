# Stage 05 Diagnostic Plan v1

Artefact status: numerical design, no implementation

Diagnostics to implement after code exists:

| Diagnostic | Purpose | Expected status |
|---|---|---|
| positivity check | ensure `L`, `A_eff`, `z`, `alpha`, variance, and volatility are positive | mandatory |
| finite-value check | catch `nan`, `inf`, overflow, or gamma endpoint failure | mandatory |
| low-z branch check | confirm low-z response does not depend on `z` for fixed `gamma` | mandatory |
| high-z monotonicity check | confirm high-z response decreases with `z` when `0 < gamma < 1` | mandatory |
| homogeneous baseline check | with all profiles constant, surface is state-flat | mandatory |
| liquidity-only isolation check | only `L(m)` changes state shape | mandatory |
| resilience-only isolation check | low-z state effect is absent or weak; high-z state effect appears | mandatory |
| output provenance check | every figure and table has a generating script and config | mandatory |

Acceptance labels:

- verified;
- verified with caveat;
- runs but not verified;
- exploratory only;
- failed check.

