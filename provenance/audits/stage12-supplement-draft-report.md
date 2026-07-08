# Stage 12 Supplement Draft Report

Artefact status: Stage 12 completion candidate

## Scope

Created the first standalone supplementary-materials science draft:

`interpretation/supplementary-materials/ReactionBoundaryVolSurface-Supplement-v0.1.tex`

The document is written as a single-column article and contains only scientific
and computational interpretation material. It does not describe the staged
project process.

## Contents

- Short background.
- Reaction-boundary volatility closure.
- Low-z and high-z response-regime approximations.
- Structural simulation profiles for liquidity-only,
  resilience-response-only, and combined structural cases.
- Numerical implementation summary.
- Parameter, response-regime, and profile tables.
- Six paired figure panels using the preferred v3 PDF figures.
- Robustness and limitation notes.

## Build And QA

Command run from `interpretation/supplementary-materials`:

```text
pdflatex -interaction=nonstopmode -halt-on-error ReactionBoundaryVolSurface-Supplement-v0.1.tex
```

The command was run twice to resolve cross-references. The compiled PDF has
8 pages.

Visual QA was performed by rendering the PDF pages to PNG with `pdftoppm` and
reviewing a contact sheet. A first render showed that later section headings
could move ahead of some figure floats. The TeX was revised to add
`placeins` float barriers after each profile block. The refreshed render keeps
the figures with their corresponding profile sections.

Remaining LaTeX messages are small table-width overfull boxes of a few points
and harmless underfull boxes in narrow table columns.

## Current Review Status

Ready for user science review. Main likely review topics:

- whether all six figure pairs should remain in the first supplement draft;
- whether the resilience-response-only low-z diagnostic should remain as a
  main figure or move to an appendix;
- whether the parameter table should be shortened for the paper-facing version;
- whether captions should be made more concise or more explanatory.
