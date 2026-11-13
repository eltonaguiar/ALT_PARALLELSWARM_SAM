# Fleet index — SNC_SAM_RESEARCH

Each agent ran in its own git worktree and wrote only inside its own folder,
so every branch merges without conflict. Cards below are generated from the run data.

| agent folder | model | provider | browse | internal check | private rubric | card |
|---|---|---|---|---|---|---|
| [`agents/deepseek-v4-flash__deepseek__hermes`](agents/deepseek-v4-flash__deepseek__hermes/AGENT_CARD.md) | `deepseek-v4-flash` | deepseek | yes | 8/8 | 4/4 mentioned · 2/4 quality | [card](agents/deepseek-v4-flash__deepseek__hermes/AGENT_CARD.md) |
| [`agents/deepseek-v4.1-flash-fast__freebuff__buffy`](agents/deepseek-v4.1-flash-fast__freebuff__buffy/AGENT_CARD.md) | `deepseek-v4.1-flash-fast` | freebuff | no | ?/? | ?/4 mentioned · ?/4 quality | [card](agents/deepseek-v4.1-flash-fast__freebuff__buffy/AGENT_CARD.md) |
| [`agents/SAM_MODULE__kilo__default`](agents/SAM_MODULE__kilo__default/AGENT_CARD.md) | `kilo` | kilo | yes | 7/7 | 4/4 mentioned · 4/4 quality | [card](agents/SAM_MODULE__kilo__default/AGENT_CARD.md) |
| [`agents/openrouter-free__openrouter__kilo`](agents/openrouter-free__openrouter__kilo/AGENT_CARD.md) | `openrouter-free` | openrouter | yes | ?/? | ?/4 mentioned · ?/4 quality | [card](agents/openrouter-free__openrouter__kilo/AGENT_CARD.md) |
| [`agents/particle-1__openrouter__alt-swarm`](agents/particle-1__openrouter__alt-swarm/AGENT_CARD.md) | `particle-1` | openrouter | no | ?/? | ?/4 mentioned · ?/4 quality | [card](agents/particle-1__openrouter__alt-swarm/AGENT_CARD.md) |

## Folder contract (every agent)

```
agents/<model>__<provider>__<harness>/
  AGENT_CARD.md                 # this summary: model, worktree, goal, format, files
  SNC_SAM__WT<n>/
    00_PREREQ/PREREQ.md         # can I browse? playwright? context?
    01_PLAN/PLAN.md             # goal, format, phases, risks, success criteria
    02_CLARIFICATIONS/CLARIFY.md
    03_PHASES/phaseN_*.md       # heartbeat per phase
    04_QA/QA.md
    05_FINAL/SAM_CONFIG_REFERENCE.md
    05_FINAL/FINAL_SUMMARY.md
    06_FILESCOPE/FILESCOPE.md
    research/                   # raw search→digest transcripts
```

## Grading

Private rubrics live **outside** this repo (`~/.alt_parallelswarm_private/`). `shared/judge.py` refuses to score if the rubric is inside the tree, and no rubric term appears in any agent prompt. See `HARNESS.md` → Grading.