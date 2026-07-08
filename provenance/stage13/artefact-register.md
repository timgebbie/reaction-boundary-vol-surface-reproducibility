# Artefact Register

Artefact status: Stage 2 configuration-control register

| Artefact | Path | Status | Notes |
|---|---|---|---|
| Workspace README | `README-workspace.txt` | Current | Stage 2 workspace overview |
| Current status | `CURRENT-STATUS.txt` | Current | Active project state |
| Source freeze note | `source/SOURCE-FREEZE.md` | Current | Hashes and source filenames |
| Theory source | `source/CATG-BSMFromAdjointProjection-FMF-v1.8-source-v0.tex` | Frozen source | Do not edit |
| BibTeX source | `source/BSMFromAdjointProjection-FMF-v1.8-references-v0.bib` | Frozen source | Do not edit |
| Guide bundle | `source/Computational-Project-Guide-Bundle-v1.0-rc-source-v0.zip` | Frozen source | Do not edit |
| Stage 00 checkpoint | `archive/reaction-boundary-vol-surface-stage00-revised-v0.zip` | Archived planning input | Revised simulation-only checkpoint |
| Configuration policy | `config/CONFIGURATION-POLICY.md` | Current | No parameter defaults accepted yet |
| Data instructions | `data/DATA-INSTRUCTIONS.txt` | Current | Simulation-only, no empirical data |
| Run-note placeholder | `run-notes/README-run-notes.md` | Current | No run commands yet |
| Stage 2 report | `audits/stage02-source-freeze-report.md` | Current | Stage 2 completion record |
| Stage 00 theory-to-code map | `theory-to-code/stage00-theory-to-code-map-v1.tex` | Carried forward | Revised simulation-only map |
| Stage 00 computational map | `registers/stage00-computational-project-map-v1.tex` | Carried forward | Revised simulation-only map |
| Stage 00 parameter register | `registers/stage00-parameter-register-v1.tex` | Carried forward | Revised simulation-only register |
| Stage 00 figure plan | `registers/stage00-figure-plan-v1.md` | Carried forward | Includes both Eq. 22 cases |
| Stage 00 table plan | `registers/stage00-table-plan-v1.md` | Carried forward | Parameter and response-regime tables |
| Stage 00 configuration plan | `registers/stage00-configuration-plan-v1.md` | Carried forward | Standard simulation-only mode |
| Stage 00 data plan | `registers/stage00-data-plan-v1.md` | Carried forward | Simulation only |
| Stage 00 stage sequence | `registers/stage00-stage-sequence-v1.tex` | Carried forward | Next stage sequence |
| Revision note | `registers/revision-note-v2.md` | Carried forward | User revisions applied |
| Stage 00 unresolved issues | `registers/unresolved-issues-stage00.md` | Carried forward | Open issues for Stage 3+ |
| Stage 3 theory-to-code map | `theory-to-code/stage03-theory-to-code-map-v1.tex` | Current | Full source-label map |
| Stage 3 assumption register | `registers/stage03-assumption-approximation-register-v1.md` | Current | Assumptions and approximations |
| Stage 3 parameter source map | `registers/stage03-parameter-source-map-v1.md` | Current | Parameter roles, no defaults |
| Stage 3 response-regime map | `registers/stage03-response-regime-map-v1.md` | Current | Low-z and high-z cases |
| Stage 3 surface questions | `registers/stage03-surface-design-questions-v1.md` | Current | Open design questions |
| Stage 3 report | `audits/stage03-theory-to-code-map-report.md` | Current | Stage 3 completion candidate |
| Stage 4 stock-dependence strategy | `registers/stage04-stock-dependence-strategy-v1.md` | Current | Refactored simulation profiles |
| Stage 4 modelling audit | `audits/stage04-modelling-audit-report.md` | Current | Stage 4 completion candidate |
| Stage 5 numerical design | `config/stage05-numerical-design-v1.md` | Current | Algorithm and surface design |
| Stage 5 parameter-range design | `registers/stage05-parameter-range-design-v1.md` | Current | Dimensionless baseline ranges |
| Stage 5 profile formulas | `registers/stage05-profile-formulas-v1.md` | Current | Three structural profiles |
| Stage 5 output design | `registers/stage05-output-design-v1.md` | Current | Tables and figures planned |
| Stage 5 script plan | `run-notes/stage05-script-plan-v1.md` | Current | Planned implementation order |
| Stage 5 diagnostic plan | `diagnostics/stage05-diagnostic-plan-v1.md` | Current | Checks to implement later |
| Stage 5 report | `audits/stage05-numerical-design-report.md` | Current | Stage 5 completion candidate |
| Parameter ranges config | `config/parameter-ranges-v1.csv` | Implementation draft | Baseline ranges |
| Profile definitions config | `config/profile-definitions-v1.json` | Implementation draft | Grid, baselines, profiles |
| Response-regime helpers | `functions/response_regimes.py` | Implementation draft | Low-z and high-z functions |
| Structural-profile helpers | `functions/structural_profiles.py` | Implementation draft | Profile components |
| Volatility-kernel helpers | `functions/vol_surface_kernel.py` | Implementation draft | Projected variance and volatility |
| Stage 6 implementation notes | `run-notes/stage06-implementation-notes-v1.md` | Current | Files and implementation scope |
| Stage 6 report | `audits/stage06-implementation-report.md` | Current | Stage 6 completion candidate |
| Stage 7 diagnostics script | `scripts/03_run_diagnostics.py` | Current | Diagnostic runner |
| Stage 7 run note | `run-notes/stage07-diagnostics-run-note-v1.md` | Current | Diagnostic command |
| Stage 7 diagnostic CSV | `diagnostics/stage07-diagnostics-v1.csv` | Diagnostic output | 42 checks, all verified |
| Stage 7 diagnostic Markdown | `diagnostics/stage07-diagnostics-v1.md` | Diagnostic output | Human-readable diagnostic report |
| Stage 7 report | `audits/stage07-diagnostics-report.md` | Current | Stage 7 completion candidate |
| Table generation script | `scripts/01_make_tables.py` | Current | Generates CSV and standalone LaTeX tables |
| Surface generation script | `scripts/02_generate_surfaces.py` | Current | Generates PDF figures, raw outputs, captions, provenance |
| Stage 8 run note | `run-notes/stage08-generation-run-note-v1.md` | Current | Table and figure commands |
| Parameter table | `tables/parameter-ranges-v1.tex` | Table draft | Standalone LaTeX table |
| Response-regime table | `tables/response-regimes-v1.tex` | Table draft | Standalone LaTeX table |
| Profile-definition table | `tables/profile-definitions-v1.tex` | Table draft | Standalone LaTeX table |
| Superseded v1/v2 generated artefacts | earlier Stage 8 checkpoint bundles | Pruned from active workspace | Preserved in earlier checkpoints |
| Figure-table manifest | `figure-table-manifest.md` | Current | Tables and preferred v3 figures |
| Figure-table provenance | `figure-table-provenance-register.csv` | Current | Preferred v3 figure provenance |
| Stage 8 report | `audits/stage08-generation-report.md` | Current | Stage 8 completion candidate |
| Refined v2 figure script | `scripts/04_generate_refined_figures_v2.py` | Superseded script | Kept for provenance; generated v2 artefacts pruned |
| Refined v2 run note | `run-notes/stage08-refined-figures-v2-run-note.md` | Superseded note | Kept for provenance |
| Matplotlib v3 figure script | `scripts/05_generate_matplotlib_figures_v3.py` | Preferred current | Boxed 3D surfaces and contour-line figures |
| Matplotlib v3 run note | `run-notes/stage08-matplotlib-figures-v3-run-note.md` | Current | v3 figure command and dependency note |
| Matplotlib v3 requirements | `config/requirements-figures-v3.txt` | Current | Figure-generation dependency note |
| Matplotlib v3 manifest | `figure-table-manifest-v3-addendum.md` | Current | Preferred refined figure manifest |
| Matplotlib v3 figures | `figures/mpl-*-v3.pdf`, `figures/mpl-*-v3.png` | Preferred figure drafts | Separate surface and contour files |
| Matplotlib v3 captions | `captions/caption-mpl-*-v3.md` | Caption drafts | Captions for preferred figure family |
| Stage 8 v3 refinement report | `audits/stage08-v3-refinement-report.md` | Current | Controlled Stage 8 refinement |
| Stage 9 sensitivity script | `scripts/06_run_sensitivity_checks.py` | Current | Sensitivity and edge-case checks |
| Stage 9 run note | `run-notes/stage09-sensitivity-run-note-v1.md` | Current | Sensitivity command |
| Stage 9 diagnostics | `diagnostics/stage09-sensitivity-checks-v1.md` | Diagnostic output | 19 checks, no failures |
| Stage 9 summary | `outputs/stage09-sensitivity-summary-v1.csv` | Generated output | Sensitivity summary |
| Stage 9 report | `audits/stage09-sensitivity-report.md` | Current | Stage 9 completion candidate |
| Build README | `README-build.txt` | Current | Reproducibility build notes |
| Figure README | `README-figures.txt` | Current | Figure usage and LaTeX notes |
| Requirements | `requirements.txt` | Current | Python dependency record |
| Reproducibility manifest | `reproducibility-manifest.md` | Current | Active source/config/script/output map |
| Stage 10 report | `audits/stage10-reproducibility-report.md` | Current | Stage 10 completion candidate |
| Supplement plan | `interpretation/supplementary-materials/supplement-plan-v1.md` | Current | Proposed structure and phases |
| Supplement TeX outline | `interpretation/supplementary-materials/ReactionBoundaryVolSurface-Supplement-v0.1-outline.tex` | Draft outline | Science-only standalone TeX outline |
| Stage 11 report | `audits/stage11-user-review-report.md` | Current | User review gate |
| Supplement TeX draft | `interpretation/supplementary-materials/ReactionBoundaryVolSurface-Supplement-v0.1.tex` | Current draft | First full science-only supplement draft |
| Supplement PDF draft | `interpretation/supplementary-materials/ReactionBoundaryVolSurface-Supplement-v0.1.pdf` | Compiled draft | 9-page local compile for visual review |
| Stage 12 report | `audits/stage12-supplement-draft-report.md` | Current | Supplement draft and visual QA record |
| Local-volatility interpretation note | `interpretation/local-volatility-interpretation-note-v1.md` | Current | Critical interpretation of mechanism surfaces versus calibrated local volatility |
| Stage 13 report | `audits/stage13-local-vol-interpretation-report.md` | Current | Supplement enrichment and interpretation record |

Interpretation artefacts now include a first standalone supplement draft.
Tables, preferred v3 figures, captions, diagnostics, and provenance exist as
drafts. Superseded v1/v2 generated artefacts were pruned from the active
workspace.
