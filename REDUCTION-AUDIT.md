# Reduction audit

Version prepared: v1.0
Date prepared: 2026-07-08

## Purpose

This file documents the reduction of the full staged workspace into the GitHub-ready reproducibility bundle.

The reduction is controlled, not silent. The original uploaded ZIP remains the complete staged workspace record. This v1.0 bundle preserves the active reproducibility core and selected provenance material, while omitting empty folders and bulky checkpoint artefacts that are not part of the public reproducibility route.

## No-content-loss principle

The active reproducibility core was copied into the reduced bundle without intentional scientific or computational alteration. Enrichment was added through new documentation, citation metadata, a Git ignore file, release notes, and a convenience run-all script.

The full staged workspace file index is recorded at:

```text
provenance/full-workspace-file-index.csv
```

## Counts from the staged workspace

- Original files mapped as included: 116
- Original files mapped as excluded: 2

Exclusion does not mean deletion from the project history. It means the file is not required for the reduced GitHub-ready v1.0 release.

## Active v1.0 route

```bash
python scripts/03_run_diagnostics.py
python scripts/01_make_tables.py
python scripts/05_generate_matplotlib_figures_v3.py
python scripts/06_run_sensitivity_checks.py
```

The optional wrapper is:

```bash
python scripts/run_all.py
```

## Material deliberately retained for provenance

- Stage audits.
- Registers.
- Run notes.
- Theory-to-code maps.
- Source-freeze records.
- Legacy v1/v2 figure-generation scripts, stored under `provenance/legacy-scripts/` and marked as inactive.

## Material deliberately omitted from the reduced release

- Empty workspace folders.
- Bulky checkpoint ZIPs.
- The earlier computational-project guide ZIP, which is not part of this reproducibility object.

## Future enrichment

Future versions may add packaging, tests, CI, notebooks, locked environments, and empirical calibration examples. Those changes should be treated as new release increments rather than retroactive changes to v1.0.
