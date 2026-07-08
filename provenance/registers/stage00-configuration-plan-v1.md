# Stage 00 Configuration-Control Plan v1

Artefact status: draft computational map

Recommended initial mode:
Standard mode, simulation only.

Escalation trigger:
Move to Complex mode only if stochastic simulation, fragile numerical
integration, expensive computation, or claim-critical numerical output
becomes central. Calibrated data and empirical calibration are out of
scope for this project revision.

Preferred working form:

- Python-first.
- Standalone Python scripts.
- Markdown run notes.
- Overleaf / Overleaf Labs friendly.
- No notebooks unless interactive exploration becomes genuinely useful.

Default project layout for Stage 2:

```text
reaction-boundary-vol-surface/
  README-workspace.txt
  CURRENT-STATUS.txt
  artefact-register.md
  source/
  theory-to-code/
  registers/
  scripts/
  functions/
  config/
  run-notes/
  notebooks/
  data/
  outputs/
  raw-outputs/
  figures/
  tables/
  captions/
  diagnostics/
  audits/
  interpretation/
  final/
  archive/
```

Mandatory infrastructure for Standard mode:

- Source freeze.
- Theory-to-code map.
- Assumption and approximation register.
- Parameter register.
- Dependency map.
- Configuration-control plan.
- Code diagnostics.
- Figure and table provenance register.
- Caption register or caption draft files.
- Reproducibility README.
- Unresolved-issues file.

Optional infrastructure not activated yet:

- Full empirical data lineage register.
- Calibration audit.
- Random-seed register, unless stochastic simulation is selected.
- Environment lockfile, unless package fragility appears.
- Clean-environment rerun.
- Independent rerun.
