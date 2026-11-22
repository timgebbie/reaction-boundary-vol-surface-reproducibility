# Version and release policy

The public v1.0.0 tag identifies the July 2026 structural-surface workflow. Its accompanying supplement is v0.1. The November 2026 scientific reference is arXiv:2607.05011v4. The public supplement uses the major and minor numbers of the computational checkpoint it covers. The final component records supplement revisions within that scope. For example, supplement v1.2.1 can extend a proof or algorithm for computational v1.2.0. The historical v0.1 edition retains its original identifier.

## Mainline checkpoints and major milestones

Work proceeds on `main`. Record each checkpoint by its scope, commit and evidence. A patch checkpoint covers preservation or corrections. A minor checkpoint introduces a verified extension. A major version identifies a substantial change in scientific scope or compatibility.

An accepted, reproducible checkpoint may receive an immutable version tag after the authors review its tests, claims and limitations. Reserve GitHub releases for explicitly approved major scientific or reproducibility milestones. A major milestone may occur within a semantic minor version. Record the commit, remote tag and GitHub release as separate facts.

## Evidence and configuration

For changes to numerical defaults, grids, units or response regimes, record the configuration and affected outputs using the existing [configuration policy](config/CONFIGURATION-POLICY.md). For a scientific milestone, identify the exact source revision, parameters, reproduction command, measured results and limitations. Record software, supplement and archive identifiers separately.

At each gate, record the current state, verified evidence, open limitations, next gate and any approval needed. The [baseline audit](docs/audits/baseline-v1.0.0.md) records the first such checkpoint.

When a checkpoint is accepted, update the public README header, source checkout, evidence and release tables, and decision footer as part of recording the decision on main. Verify the rendered source on GitHub against the accepted revision.

Use arXiv records for the paper trail. Record Git revisions, software deposits, supplement revisions and computation inputs separately as artifact provenance.
