# Structural-surface baseline replay, 22 November 2026

**Current.** v1.0.1 is a documentation and preservation checkpoint on `main`. The published v1.0.0 tag resolves to commit `ee37d994b72b64395560de1126531bb259c1f794`. The pre-checkpoint tip of `main` was `42ca2702baf7e8d2f54971a239c188e019f41125`. The two intervening commits changed only the README.

## Verified evidence

In separate clean checkouts of those two commits, run `python scripts/run_all.py` from each repository root. Replay environment: Linux, Python 3.12.14, NumPy 2.3.5, Matplotlib 3.11.0, Pillow 13.0.0 and ReportLab 4.4.9.

| Output | Result |
|---|---|
| Stage 7 diagnostics | 42 verified on each revision, zero failures |
| Stage 9 sensitivity checks | 19 verified on each revision, zero failures |
| Six structural surfaces | Generated tables, captions, diagnostic reports and sensitivity summaries agreed between replays. All 12 surface and contour PNGs agreed pixel-for-pixel between replays. |
| Comparison with tagged CSVs | All parsed diagnostic and parameter-table entries matched. Five floating-point cells in the sensitivity summary differed, with maximum absolute difference of 4.45 × 10⁻¹⁶ (rounded up). |
| Comparison with tagged PNGs | Eleven matched in RGB. The resilience/response-only low-z surface differed at 428 of 1,618,408 pixels. |
| Supplement v0.1 | Two LaTeX passes with the tagged figure assets produced nine pages. The SHA-256 of layout-extracted text agreed with the tagged PDF. |
| Frozen TeX and bibliography | Both SHA-256 values matched the historical source-freeze record. Its TeX source is FMF v1.8. The extension uses arXiv:2607.05011v4. |

To rebuild the supplement with a configured pdfLaTeX installation, start at the repository root in a fresh checkout of the tag. The nested working directory resolves the figure paths in the archived TeX.

```sh
mkdir -p supplementary-materials/build
cd supplementary-materials/build
pdflatex -halt-on-error ../ReactionBoundaryVolSurface-Supplement-v0.1.tex
pdflatex -halt-on-error ../ReactionBoundaryVolSurface-Supplement-v0.1.tex
```

## Archive and integrity

The historical `FILE-MANIFEST-SHA256.csv` describes staged files. For each listed path we compared its digest with the raw blob returned by `git show v1.0.0:<path>`. Of 132 rows, 98 matched directly and six more matched after LF-to-CRLF conversion. Another 27 had different digests. One listed file, `LOCAL-EXECUTION-GATE-v1.0.md`, is absent from the tag. These differences already exist at the release commit. Use the tag to identify the Git baseline and retain the CSV as historical provenance.

The registered software DOI is `10.25375/uct.32936867`. ZivaHub version 1 lists the staged ZIP, `ReactionBoundaryVolSurface-Reproducibility-v1.0-stage5.zip`. The [current source map](../../reproducibility-manifest.md) locates the reduced Git workflow.

**Open limitations.** Pixel and CSV comparisons bound the observed replay differences. The high-z figures show unconditional stationary response morphology. A state-conditioned high-z pricing coefficient and the proposed collective-root dynamics require separate evidence.

**Next gate.** At v1.1.0, compare the exact finite-cutoff coefficient in v4 Appendix A, Eq. (47), with an independent time-domain calculation. Evaluate the zero-cutoff crossover and its two asymptotes separately. Keep the structural-surface entry point available.

**Approval needed.** The preservation checkpoint was accepted for mainline implementation. Tagging and publication require explicit approval at a designated major milestone.
