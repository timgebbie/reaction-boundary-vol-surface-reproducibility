# Stage 00 Table Plan v1

Artefact status: draft computational map

No tables have been generated.

Default table policy:

- Final or candidate tables should be typeset as standalone LaTeX files.
- Each table should also have a raw flat file, preferably CSV for numerical
  values.
- Markdown is acceptable for planning registers, but CSV is preferred for
  machine-readable numerical tables.
- Standalone LaTeX table files should include comments listing required
  packages and comments indicating text that may be cut and pasted into the
  target paper.

| Table ID | Concept | Preferred raw format | LaTeX output | Status |
|---|---|---|---|---|
| T1 | Simulation parameter ranges and baseline values | CSV | Standalone `.tex` | Mandatory first table |
| T2 | Response-regime cases from Eq. 22 | CSV | Standalone `.tex` | Mandatory |
| T3 | Figure/surface configuration table | CSV | Standalone `.tex` | Optional |
| T4 | Diagnostic summary by script | CSV | Standalone `.tex` | Deferred |

No table should be promoted to paper-ready until its generating script,
configuration file, and diagnostics are recorded.
