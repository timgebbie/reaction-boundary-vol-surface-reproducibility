# Release notes: v1.0

Initial reduced reproducibility release candidate.

## Included

- Active reproducibility scripts and helper functions.
- Configuration files.
- Generated v3 Matplotlib figures.
- Generated tables.
- Diagnostic and sensitivity-check outputs.
- Supplementary-materials TeX and PDF.
- Provenance notes, audits, registers, and source-freeze records needed to trace the staged construction.

## Enrichment added during reduction

- `README.md` with current/future situation sections.
- `STATUS.md` with the current situation, future situation, and no-content-loss control statement.
- `REDUCTION-AUDIT.md` explaining the reduction boundary.
- `CITATION.cff` draft.
- `.gitignore`.
- `LICENSE` draft.
- `scripts/run_all.py` convenience wrapper.
- `provenance/full-workspace-file-index.csv`.

## Not included from the original staged ZIP

- empty directories;
- Python cache files, if any;
- bulky checkpoint ZIPs;
- the previous computational-project guide ZIP.

The omitted items are not part of the active v1.0 reproducibility route. Their omission is recorded in `REDUCTION-AUDIT.md`.
