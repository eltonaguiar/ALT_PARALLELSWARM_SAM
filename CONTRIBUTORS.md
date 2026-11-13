# CONTRIBUTORS — who wrote which folder, on which model

Every agent that adds work to this repo owns **one** folder under `agents/` named
`<model>__<provider>__<harness>` (see `HARNESS.md`). Never edit another agent's folder.

| agent folder | model | provider | harness | worktree(s) | contributed |
|---|---|---|---|---|---|
| `grok-4.6__xai__kilo` | `grok-4.6` | xAI (`xai`) | Kilo | SNC_SAM__WT1 | scaffold harness (`shared/` copied from Discovery pass and retargeted), roster, first SAM research pass |
| `SAM_MODULE__kilo__default` | `kilo` | kilo | Kilo | SNC_DISC__WT1 | SAM module configuration reference (foundational data, baseline metrics, planning, governance, technical implementation, failure patterns, general module framework, quick-start checklist) |

## Adding yourself

1. Pick an id: `<model>__<provider>__<harness>`, lowercase, dots allowed (e.g. `qwen3-30b-a3b__ollama__hermes`).
2. Create `agents/<id>/SNC_SAM__WT<n>/` using the folder contract in `HARNESS.md`.
3. Declare **model + provider** in `00_PREREQ/PREREQ.md`, `01_PLAN/PLAN.md`, `05_FINAL/FINAL_SUMMARY.md`, `06_FILESCOPE/FILESCOPE.md`.
4. Add a row to this table and an entry to `agents.yaml` (`agents:` if the harness dispatches you, `self_runs:` if you drove your own tools).
5. Only commit your own folder (plus this table row and your roster entry).

## Self-driven runs (`agents.yaml → self_runs`)

`orchestrate.py` reads only the `agents:` list. A model that ran under its own native tooling
(no API dispatch) belongs in `self_runs:` so the roster stays truthful without being re-run.