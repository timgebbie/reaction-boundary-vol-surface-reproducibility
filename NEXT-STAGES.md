# Next stages after reduced v1.0 preparation

This file records the staged route from the reduced v1.0 bundle to a public DOI-bearing reproducibility object.

## Stage 1 completed here: reduced v1.0 bundle

Completed:

- reduced the full staged workspace to `ReactionBoundaryVolSurface-Reproducibility-v1.0`;
- preserved the active reproducibility core;
- retained selected provenance material;
- added README, STATUS, citation metadata, license draft, audit notes, and test report;
- tested the reduced bundle in a clean copy.

## Stage 2: local author test

On the author's machine, unpack the v1.0 bundle and run:

```bash
python -m venv .venv
```

Activate the environment.

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the active route:

```bash
python scripts/run_all.py
```

If necessary, run the scripts separately:

```bash
python scripts/03_run_diagnostics.py
python scripts/01_make_tables.py
python scripts/05_generate_matplotlib_figures_v3.py
python scripts/06_run_sensitivity_checks.py
```

## Stage 3: private GitHub repository

Create a private repository named:

```text
reaction-boundary-vol-surface-reproducibility
```

Then, from inside the reduced v1.0 folder:

```bash
git init
git add .
git commit -m "Initial v1.0 reproducibility bundle for arXiv 2607.05011"
git branch -M main
git remote add origin <PRIVATE-GITHUB-URL>
git push -u origin main
```

## Stage 4: clean-clone test

Clone the private repository into a fresh local directory and rerun the active route. This is the practical reproducibility gate.

```bash
git clone <PRIVATE-GITHUB-URL>
cd reaction-boundary-vol-surface-reproducibility
python -m venv .venv
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python scripts/run_all.py
```

## Stage 5: public release

After the clean-clone test passes:

```bash
git tag v1.0.0
git push origin v1.0.0
```

Then make the GitHub repository public and create a GitHub release from tag `v1.0.0`.

## Stage 6: ZivaHub/Figshare DOI and arXiv update

Deposit the GitHub release archive and supplementary PDF on ZivaHub/Figshare.

Suggested deposit title:

> Supplementary materials and reproducibility code for “Reaction-boundary variance and adjoint-consistent local-volatility projection”

Suggested description:

> This deposit contains the v1.0 reproducibility bundle for the supplementary simulation materials associated with arXiv:2607.05011. It includes Python scripts, configuration files, generated figures, tables, diagnostics, sensitivity checks, and the supplementary-materials PDF and TeX source.

After the DOI is assigned, update:

- `README.md`;
- `CITATION.cff`;
- the arXiv paper's code/data availability statement;
- the Papers with Code / arXiv code link, if used.

Suggested arXiv wording:

> Code and supplementary materials. The Python code, configuration files, diagnostics, generated figures, and supplementary materials used to reproduce the reaction-boundary volatility-surface simulations are available at [ZivaHub DOI]. The public development repository is available at [GitHub URL].
