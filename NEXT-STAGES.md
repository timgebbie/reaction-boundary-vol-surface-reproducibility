# Next stages after private GitHub clean-clone gate

> Historical July 2026 preparation record. The public v1.0.0 release and the subsequent preservation checkpoint are documented in the [baseline audit](docs/audits/baseline-v1.0.0.md).

The private GitHub clean-clone test has passed. The project can now move toward the public v1.0.0 release and the ZivaHub/Figshare DOI deposit.

## Stage 5: Public-facing release preparation

Before making the repository public:

1. confirm the final license choices with all authors;
2. confirm the README figure and caption;
3. update `CITATION.cff` if the release date or title changes;
4. leave the DOI placeholders in place until ZivaHub/Figshare assigns the DOI;
5. tag the release as `v1.0.0` only after the public-facing README, status file, citation file, and license notes are final.

Recommended tag command from the repository root:

```bash
git tag v1.0.0
git push origin v1.0.0
```

Then create the GitHub release from the `v1.0.0` tag.

## Stage 6: ZivaHub/Figshare DOI and arXiv update

Deposit the public GitHub release archive and supplementary-materials PDF on ZivaHub/Figshare.

Use these placeholders until the deposit is live:

```text
ZivaHub/Figshare DOI: [TO BE ADDED: 10.xxxx/xxxxx]
ZivaHub/Figshare landing page: [TO BE ADDED: https://...]
GitHub release: https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility/releases/tag/v1.0.0
Associated arXiv paper: https://arxiv.org/abs/2607.05011
Supplementary PDF: supplementary-materials/ReactionBoundaryVolSurface-Supplement-v0.1.pdf
```

Suggested arXiv code-availability statement:

```text
Code and supplementary materials. The Python code, configuration files,
diagnostics, generated figures, and supplementary materials used to reproduce
the reaction-boundary volatility-surface simulations are available at
https://doi.org/[TO-BE-ADDED]. The public development repository is available at
https://github.com/timgebbie/reaction-boundary-vol-surface-reproducibility.
```

## Finance-first future situation

Future versions should first be framed as quantitative-finance extensions, for example empirical comparison with option-implied local-volatility surfaces, calibration from order-flow or limit-order-book data, market-state interpretation of high-z and low-z regimes, long-memory response analysis, and no-arbitrage projection or regularisation. Software improvements should support those aims rather than define the project.
