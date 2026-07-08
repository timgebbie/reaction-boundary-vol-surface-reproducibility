# Release notes: v1.0

Initial reduced reproducibility release candidate for the supplementary simulation materials associated with [arXiv:2607.05011](https://arxiv.org/abs/2607.05011).

## Public-facing release purpose

This release is a quantitative-finance reproducibility object. It reproduces the reaction-boundary volatility-surface simulations used in the supplementary materials and makes the link between the structural model ingredients and the generated surface shapes inspectable.

## Included

- Active reproducibility scripts and helper functions.
- Configuration files for parameter ranges and structural profiles.
- Generated v3 Matplotlib surface and contour figures.
- README presentation image for the combined structural high-z surface/contour pair.
- Generated CSV and LaTeX tables.
- Diagnostic and sensitivity-check outputs.
- Supplementary-materials TeX and PDF.
- Provenance notes, audits, registers, and source-freeze records needed to trace the staged construction.

## Enrichment added during reduction and Stage 5 preparation

- `README.md` refocused around the quantitative-finance purpose.
- Active links to the arXiv paper and the supplementary-materials PDF.
- README figure using the combined structural high-z surface/contour pair.
- Longer README caption explaining the finance point of the key figure.
- `STATUS.md` revised so that the current and future situations are finance-first rather than software-first.
- `DOI-CITATION-LICENSE.md` with concrete placeholders for DOI, release URL, citation, and license information.
- `CITATION.cff` updated with the actual GitHub repository URL.
- `TEST-REPORT-v1.0.md` updated to include the passed private GitHub clean-clone gate and the generated-PDF byte-difference caveat.
- `.gitignore`, `LICENSE`, `scripts/run_all.py`, and `provenance/full-workspace-file-index.csv`.

## Not included from the original staged ZIP

- empty directories;
- Python cache files, if any;
- bulky checkpoint ZIPs;
- the previous computational-project guide ZIP.

The omitted items are not part of the active v1.0 reproducibility route. Their omission is recorded in `REDUCTION-AUDIT.md`.

## Execution gate confirmation

The author confirmed that the reduced v1.0 bundle executed successfully on Windows with Python 3.13.9 using a `venv` under an Anaconda installation. The private GitHub clean-clone test also completed successfully with:

```text
Active v1.0 reproducibility route completed successfully.
```

## Known reproducibility caveat

Regenerated Matplotlib PDF files may differ byte-for-byte from the committed PDFs across machines because of backend metadata, fonts, or rendering details. This does not invalidate the v1.0 reproducibility route. The release claim is scientific and procedural reproducibility of the generated figures, tables, diagnostics, and sensitivity checks, not byte-identical PDF binaries on every system.
