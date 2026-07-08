# Stage 5 public-facing refinement summary

Stage 5 refined the user-facing release materials without changing the scientific code path.

## Changes made

- Added a GitHub-renderable README figure: `figures/readme-combined-structural-high-z-pair-v1.png`.
- Refocused `README.md` around the quantitative-finance purpose of the bundle.
- Added active links to the arXiv paper and the supplementary-materials PDF.
- Added a longer caption for the combined structural high-z surface/contour pair.
- Revised `STATUS.md` so that the current and future situations are finance-first rather than software-first.
- Added `DOI-CITATION-LICENSE.md` with concrete placeholders for DOI, GitHub release, repository citation, arXiv statement, and license wording.
- Updated `CITATION.cff` with the actual GitHub repository URL.
- Updated `TEST-REPORT-v1.0.md` to include the private GitHub clean-clone gate and the Matplotlib PDF byte-difference caveat.
- Updated `NEXT-STAGES.md` and `RELEASE-NOTES-v1.0.md` for the public v1.0.0 release route.

## Not changed

- No Python source code was changed.
- No mathematical model functions were changed.
- No parameter configuration files were changed.
- No original standalone generated surface or contour figures were replaced.
- No supplementary-materials PDF or TeX source was changed.

## Release status

The project has passed:

- local author execution gate;
- private GitHub upload gate;
- private GitHub clean-clone execution gate.

The next actions are to commit these Stage 5 documentation/presentation refinements to the private GitHub repository, confirm licensing with all authors, tag `v1.0.0`, create the public GitHub release, and then deposit the release package on ZivaHub/Figshare for the DOI.
