# Stage 10 Reproducibility Package

Artefact status: Stage 10 completion candidate

Completed:

- Added `README-build.txt`.
- Added `README-figures.txt`.
- Added `requirements.txt`.
- Added `reproducibility-manifest.md`.
- Preserved source freeze records and active theory-to-code maps.
- Preserved active configuration files.
- Preserved scripts needed to regenerate diagnostics, tables, preferred v3
  figures, and sensitivity checks.
- Preserved preferred v3 figures in PDF and PNG formats.
- Preserved standalone LaTeX/CSV tables.
- Preserved caption drafts and provenance records.
- Reran the active reproduction command sequence successfully:
  diagnostics, tables, preferred v3 figures, and sensitivity checks.

Package policy:

- Exclude `.deps/` from checkpoint bundles.
- Exclude Python cache directories.
- Keep dependency installation instructions instead of vendoring local
  packages.

Recommended next stage:

Stage 11: user review gate.
