# Version and release policy

The public v1.0.0 tag identifies the July 2026 structural-surface workflow. Its accompanying supplement is v0.1. The November 2026 scientific reference is arXiv:2607.05011v4. The EFT companion has its own version history, as will the expanded Reaction Boundary supplement.

## Mainline checkpoints and major milestones

Work proceeds on `main`. Record each checkpoint by its scope, commit and evidence. A patch checkpoint covers preservation or corrections. A minor checkpoint introduces a verified extension. A major version identifies a substantial change in scientific scope or compatibility.

Only a major **milestone** designated by the authors is eligible for a tag and a GitHub release. The semantic version number alone does not designate a milestone. Intermediate gates, including the v1.0.1 preservation checkpoint, are recorded by commit. Before publication, present the proposed claims, actual tests and remaining limitations for explicit approval. Preserve published tags and release assets.

## Evidence and configuration

For changes to numerical defaults, grids, units or response regimes, record the configuration and affected outputs using the existing [configuration policy](config/CONFIGURATION-POLICY.md). For a scientific milestone, identify the exact source revision, parameters, reproduction command, measured results and limitations. Record software, supplement and archive identifiers separately.

At each gate, record the current state, verified evidence, open limitations, next gate and any approval needed. The [baseline audit](docs/audits/baseline-v1.0.0.md) records the first such checkpoint.
