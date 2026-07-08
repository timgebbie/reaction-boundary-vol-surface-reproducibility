# Test report: v1.0

## Active route

The active v1.0 route is:

```bash
python scripts/run_all.py
```

which runs:

```bash
python scripts/03_run_diagnostics.py
python scripts/01_make_tables.py
python scripts/05_generate_matplotlib_figures_v3.py
python scripts/06_run_sensitivity_checks.py
```

## Gate 1: author local execution gate

Passed.

Author test environment:

```text
Platform: Windows
Python: 3.13.9
Environment: venv under Anaconda installation
```

Confirmed outputs:

```text
Stage 7 diagnostics
Stage 8 table generation
Matplotlib v3 figure generation
Stage 9 sensitivity checks
```

Final status:

```text
Active v1.0 reproducibility route completed successfully.
```

## Gate 2: private GitHub clean-clone gate

Passed.

The private repository was cloned into a fresh test directory, dependencies were installed into a fresh virtual environment, and:

```bash
python scripts/run_all.py
```

completed successfully.

Final status:

```text
Active v1.0 reproducibility route completed successfully.
```

## Expected diagnostics

The original staged workspace recorded:

```text
Stage 7 diagnostics: 42 checks, 0 failures
Stage 9 sensitivity checks: 19 checks, 0 failures
```

## Note on generated PDF files

After the clean-clone test, Git reported regenerated Matplotlib PDF figures as modified. This is a harmless generated-output difference and not a failed reproducibility gate. Matplotlib PDF output can differ byte-for-byte across systems because of backend metadata, font embedding, and local rendering details.

The v1.0 claim is that the active route regenerates the intended scientific figures, tables, diagnostics, and sensitivity checks. It is not a claim that generated PDF binaries are byte-identical across every local environment.
