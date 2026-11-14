# 01 — PLAN

**Run:** `finalv2` SAM documentation pass
**Timestamp:** 2026-11-14T07:31:00Z
**Methodology:** the six-phase discovery-swarm contract in the run diagram (PREREQ → PLAN → CLARIFY → PHASES → QA → FINAL), plus shared context, self-review, and wrap-up.

---

## Goal

Produce a self-contained, cross-referenced **ServiceNow SAM module** documentation set in `finalv2/`, grounded in official product documentation, that:

1. explains the SAM data pipeline end to end,
2. separates CMDB/IRE governance from SAM software normalization,
3. documents configuration and operations with confidence marks,
4. reconciles conflicts with the repo's v1 final docs and the public SAM guide, and
5. records how the work was verified — including subagent cross-checks.

## Output format

```
finalv2/
  README.md                         # index + executive summary + cheat sheet
  METHODOLOGY.md                    # how the six-phase contract was applied
  CROSS_REFERENCE_MATRIX.md         # claim → official source → v1 → status
  GUIDE_CROSS_REFERENCE.md          # v2 vs public SAM guide, with corrections
  CONFLICT_LOG.md                   # disagreements and resolutions
  SUBAGENT_CROSSCHECK.md            # subagent dispatch + findings
  00_PREREQ/PREREQ.md
  01_PLAN/PLAN.md
  02_CLARIFICATIONS/CLARIFY.md
  03_PHASES/phase1..6.md
  04_QA/QA.md
  05_FINAL/01..08_*.md
  06_FILESCOPE/FILESCOPE.md
```

Every final doc uses **V/C/U/P** status marks. Every disputed claim is either resolved in `CONFLICT_LOG.md` or marked **U**.

## Phases

| Phase | Output | Exit criterion |
|---|---|---|
| 1 | Source inventory | Official SAM + IRE extracts identified; guide fetched |
| 2 | Scope + contract | In/out of scope; record chain; confidence policy |
| 3 | CMDB/IRE layer | Four rule families + insert/update truth table |
| 4 | SAM pipeline | Install → discovery model → normalization → model → reconciliation |
| 5 | Configuration + operations | Plugin/role/table/property/job inventory; runbook |
| 6 | QA + publish | Score against plan; subagent checks; filescope; push |

## Risks

| Risk | Mitigation |
|---|---|
| Mixing Brazil SAM with Australia IRE | Release pin in every doc; conflict log |
| Repeating v1 errors | Re-check v1 claims against official extracts; mark corrections |
| Treating the guide as official | Guide is **C/P**; corrections table |
| Over-claiming instance detail | **U** + verification queries |
| Duplicating v1 wholesale | Cross-reference and correct; v2 is self-contained but not a copy |
| Subagent drift | Give each a narrow checklist and require evidence paths |

## Success criteria

1. A reader can trace any install to a compliance result using the documented chain.
2. The four IRE rule families and their insert/update applicability are correct.
3. The six normalization statuses and revert rules are correct.
4. The three reconciliation tiers and rights algebra are correct.
5. Plugin/role/table/property claims are marked with evidence status.
6. The public guide's conflicting claims are listed with corrections.
7. Subagents return findings, and the findings are incorporated or explicitly rejected with a reason.
8. The folder is self-contained, lint-clean Markdown, and pushed only as `finalv2/**` plus the requested root README addition.

## Verification plan

- **Self-review:** read every final doc against the plan and the official extracts.
- **Subagent round 1:** four parallel cross-checks (pipeline/data model, IRE, licensing/reconciliation, guide delta).
- **Subagent round 2:** one consistency reviewer after revisions.
- **Mechanical:** link check, table check, `markdownlint` if available, no unresolved placeholders.
- **Publish:** commit only the new folder and the requested README section; push; report the commit.

## Non-goals

- No live-instance changes.
- No publisher contract interpretation.
- No container/Kubernetes licensing.
- No re-publication of the private rubric.
