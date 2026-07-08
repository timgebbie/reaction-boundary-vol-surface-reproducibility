# Supplement Plan v1

Artefact status: Stage 11 user-review plan

## Proposed File Name

Recommended standalone TeX filename:

`ReactionBoundaryVolSurface-Supplement-v0.1.tex`

Rationale:

- Short enough for Overleaf and zip bundles.
- Specific to the computational supplement rather than the main paper.
- Versioned independently from the theory paper.
- Can later be promoted to `v1.0` when accepted as an appendix or
  supplementary-materials file.

## Scientific Purpose

Create a standalone, single-column supplementary-materials document that
explains how the reaction-boundary volatility surfaces were generated from
the theoretical closure. The document should be suitable for later editing
into either:

- an appendix to the target paper; or
- a supplementary-materials note with additional figures.

The supplement should contain only scientific and computational content.
It should not mention workflow stages, project-management details, or chat
history.

## Proposed Structure

1. Title
2. Short Background
3. Reaction-Boundary Volatility Closure
4. Response-Regime Approximations
5. Structural Simulation Profiles
6. Numerical Implementation
7. Parameter Choices
8. Simulated Surfaces
9. Robustness Checks
10. Limitations And Interpretation

## Figure Layout

Use single-column text, but place each surface/contour pair as left and
right subfigures:

- left: boxed 3D surface view;
- right: black contour-line projection;
- caption: rich enough to stand alone.

Preferred figures:

- `figures/mpl-surface3d-*-v3.pdf`
- `figures/mpl-contour-lines-*-v3.pdf`

PNG copies remain fallback assets.

## Drafting Phases

### Phase A: Outline And Source Selection

- Confirm the supplement filename.
- Confirm whether all six profile/regime pairs should be included.
- Confirm whether the supplement should focus on the combined structural
  case first and treat liquidity/resilience cases as diagnostics.
- Confirm table selection.

### Phase B: First Science Draft

- Write the standalone TeX file.
- Include concise background and equations.
- Include parameter and response-regime tables.
- Include the preferred figures as subfigures.
- Write captions from the current caption drafts, but improve them for
  scientific clarity.

### Phase C: Technical Review

- Check that every equation maps to the frozen theory source.
- Check every figure path.
- Check captions do not overclaim.
- Check the supplement is self-contained enough to read without the
  workflow bundle.

### Phase D: Compile And Visual QA

- Compile the TeX file if LaTeX is available.
- If not available locally, prepare it for Overleaf.
- Check figure placement, table widths, captions, and page breaks.

### Phase E: Revision Candidate

- Incorporate user edits.
- Save `ReactionBoundaryVolSurface-Supplement-v0.2.tex`.
- Package the supplement draft into the next checkpoint bundle.

## Open Review Questions

1. Should the first supplement include all six figure pairs, or only the
   three most informative pairs?
2. Should the low-z and high-z response regimes be grouped by profile, or
   should profiles be grouped by response regime?
3. Should the parameter tables be included in the supplement body or moved
   to a short final appendix within the supplement?
4. Should the figures use PDF only in the TeX source, or should PNG
   alternatives be noted in comments?

