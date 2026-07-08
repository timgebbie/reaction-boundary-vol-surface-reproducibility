# Source Freeze

Artefact status: Stage 2 source-freeze record

Frozen source files:

| Frozen file | Source role | SHA-256 |
|---|---|---|
| `CATG-BSMFromAdjointProjection-FMF-v1.8-source-v0.tex` | Theory source | `e36d9916d5389e4ff8eaa03036e0c6f9a95e801f54ef371aa23126a2ff48d61b` |
| `BSMFromAdjointProjection-FMF-v1.8-references-v0.bib` | BibTeX source | `a23204333d8cbb768451d92e23064365495cc5a702431dc7fe87e3507c5fcca8` |
| `Computational-Project-Guide-Bundle-v1.0-rc-source-v0.zip` | Workflow guide bundle | `abc230b0a2868fc0e728a6656c9776bbb632066efa2f7d32596bf003a858a21b` |
| `../archive/reaction-boundary-vol-surface-stage00-revised-v0.zip` | Revised Stage 00 planning checkpoint | `903ab2ac9c9a4a2aceb1270d6377e3971dd370d655daeea29f5bd3c0f27a3e4e` |

Freeze rule:

- Do not edit frozen source files.
- Any source correction must be made as a new versioned source file after
  explicit user approval.
- Computational code should cite source equations and labels rather than
  modifying the paper source.

Active source interpretation:

- Project routing is simulation only.
- Primary computational equation is the main-result closure identified by
  the user as Eq. 18, corresponding in the source to the operational
  result closure.
- Response-function simulations must include both low-z and high-z cases
  from Eq. 22.

