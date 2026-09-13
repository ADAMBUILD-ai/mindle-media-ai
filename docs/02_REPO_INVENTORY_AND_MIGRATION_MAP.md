# Repository Inventory and Migration Map

| Source area found locally | Current state | Official destination | Action |
|---|---|---|---|
| `src/media_ai/` | present | `src/media_ai/` | retain and test |
| `tests/` | present | `tests/` | retain and extend |
| PHOTO and VIDEO evidence | not present | `evidence/` | import only from verified package or official history |
| Model Scout registry and artifacts | not present | `evidence/model_scout/` and `model_scout/` | restore from verified evidence package before adapter enablement |
| UI source and approved screenshot | not present | `ui/` and `docs/` | retrieve approved source; do not recreate visual design by inference |
| Real photo and video fixtures | not present | `fixtures/` | PC Track B only with source and license metadata |

## Required official branch flow

`integration` or a task branch -> tests and evidence -> review gate -> `main` only after approval. The current workspace has no remote and no integration branch, so it cannot truthfully claim GitHub integration.
