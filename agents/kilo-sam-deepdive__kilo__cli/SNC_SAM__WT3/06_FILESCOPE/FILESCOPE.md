# FILESCOPE — SNC_SAM__WT3

**Branch:** `docs/sam-module-deep-dive` (from `origin/main` 2baf209)
**Isolation:** dedicated clone at `/tmp/kilo/samdeepdive`; the shared checkout used by other agents was not modified.

## Files created by this worktree

```
research/servicenow-sam/
  README.md
  SAM_MODULE_DEEP_DIVE.md          # canonical guide (1,048 lines)
  CURRICULUM_COMPARE.md            # round-2 curriculum/community diff
  sources/                         # 61 mirrored source files
    *.txt                          # Brazil ITAM corpus (copied verbatim from grok WT1 research/raw/)
    _australia/*.txt               # beam Australia abstracts
    IMPLEMENTATION_SUCCESS.md      # community digest (corroboration only)
    CONFIG_INVENTORY_AUSTRALIA.md  # Australia inventory

agents/kilo-sam-deepdive__kilo__cli/
  AGENT_CARD.md
  SNC_SAM__WT3/
    00_PREREQ/PREREQ.md
    01_PLAN/PLAN.md
    02_CLARIFICATIONS/CLARIFY.md
    03_PHASES/phase1_corpus_lock.md
    03_PHASES/phase2_scope_mapping.md
    03_PHASES/phase3_theme_extraction.md
    03_PHASES/phase4_synthesis.md
    03_PHASES/phase5_qa.md
    03_PHASES/phase6_final.md
    03_PHASES/phase7_round2_curriculum.md
    04_QA/QA.md
    05_FINAL/SAM_MODULE_DEEP_DIVE.md   # identical copy of canonical guide
    05_FINAL/CURRICULUM_COMPARE.md      # identical copy of round-2 compare
    05_FINAL/FINAL_SUMMARY.md
    06_FILESCOPE/FILESCOPE.md

plans/kilo-sam-deepdive__kilo__cli__WT3/PLAN.md   # mirror of the plan
```

## Files intentionally NOT touched

| File | Why |
|---|---|
| `INDEX.md` | shared fleet index; other agents edit it |
| `CONTRIBUTORS.md` | shared fleet roster |
| `agents.yaml` | already modified in the working checkout by another agent |
| `final/*`, `agents/grok-4.6__xai__kilo/*`, `agents/beam__kilo__cli/*`, `agents/SAM_MODULE__kilo__default/*`, `agents/sam-research/*`, `docs/replication/*`, `updates/*` | other agents' corpus/work |

## Provenance note

Source `.txt` files under `research/servicenow-sam/sources/` are unmodified copies of research already committed in this repository by `grok-4.6__xai__kilo` (Brazil khub fetch) and `beam__kilo__cli` (Australia abstracts), plus two committed digests. They are duplicated here so the consolidated guide is self-contained, mirroring how `ALT_PARALLELSWARM/research/servicenow-discovery/sources/` stores its corpus.
