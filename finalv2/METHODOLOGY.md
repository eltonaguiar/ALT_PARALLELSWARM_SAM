# Methodology — how this run followed the Discovery swarm contract

This document maps the run diagram's six phases and three collaboration rules to the artifacts in `finalv2/`. It exists so the process is inspectable, not just the output.

---

## 1. The six phases

| # | Diagram phase | What it asks | Artifact |
|---|---|---|---|
| 00 | **PREREQ** | Can I browse, run Playwright, and hold the context? If not, ask another agent before writing. | [`00_PREREQ/PREREQ.md`](00_PREREQ/PREREQ.md) |
| 01 | **PLAN** | Goal, output format, phases, risks, success criteria. Mirrored under `plans/` so it is not buried. | [`01_PLAN/PLAN.md`](01_PLAN/PLAN.md) |
| 02 | **CLARIFY** | What is blocked, or what must be solved in another worktree before this one continues. | [`02_CLARIFICATIONS/CLARIFY.md`](02_CLARIFICATIONS/CLARIFY.md) |
| 03 | **PHASES** | A markdown file drops the moment a phase starts. Progress is a file, not a status claim. | [`03_PHASES/`](03_PHASES/) |
| 04 | **QA** | Score the draft against the plan. Mark what is UNVERIFIED instead of filing the gap. | [`04_QA/QA.md`](04_QA/QA.md) |
| 05 | **FINAL** | The reference, whether the goal was met, and a filescope naming the branch. | [`05_FINAL/`](05_FINAL/) + [`06_FILESCOPE/FILESCOPE.md`](06_FILESCOPE/FILESCOPE.md) |

The phase files are dated and evidence-based. They are not a narrative of good intentions.

---

## 2. Where the work collaborated

The diagram names three collaboration surfaces. This run used them as follows:

### Shared context

The **lead** (this pass) fetched the public SAM guide and read the official ServiceNow extracts. Peers that cannot browse would receive the snippets. In this run, the "peers" are the cross-check subagents; they receive exact paths and a narrow checklist rather than a full re-crawl.

- Guide: fetched and cross-referenced in [`GUIDE_CROSS_REFERENCE.md`](GUIDE_CROSS_REFERENCE.md).
- Official SAM extracts: `agents/grok-4.6__xai__kilo/SNC_SAM__WT1/research/raw/`.
- Official IRE extracts: `/home/eaguiar2015/ALT_PARALLELSWARM/research/servicenow-discovery/sources/`.

### Self-review

Inside the worktree, the draft is reviewed and fixed before QA. **The self-review does not see the private rubric.** The private rubric was not read in this pass; QA scores against the public plan.

### Wrap-up

The author reads every relevant folder (v1 `final/`, the agents' finals, the guide, the official extracts), de-duplicates, and keeps the claim that matches current docs. Disagreements stay in [`CONFLICT_LOG.md`](CONFLICT_LOG.md) — they are not averaged away.

---

## 3. What the merge had to keep

The diagram's section 03 is itself about CMDB/IRE, and it is a useful checklist for the merge:

| Merge rule | How it was applied |
|---|---|
| **Identification Rules** — Does this CI already exist? | The v2 record chain starts with CI identity; duplicate CIs are treated as a compliance risk before normalization. |
| **Reconciliation Rules** — Which source may update this field? | Every conflicting claim was resolved by an explicit authority order: official page > v1 > guide > practice. |
| **Data Refresh Rules** — Has the higher-priority source gone stale? | Older v1 claims (Australia) were re-checked against Brazil; stale claims were corrected or marked **U**. |
| **IRE Data Source Rules** — May this source insert this class? | New claims were admitted only if an official page supported them; otherwise they were marked **U** or **P**. |
| **Order: identify first. Match, then reconcile and data refresh. No match, then the data source rule gates the insert.** | Applied to both the IRE documentation and the document merge: identify the claim, match it to a source, reconcile conflicts, and only then allow a new claim to be inserted. |

This is also why the IRE document is included: the methodology's own merge rules are IRE rules, and the SAM module depends on the CI identity layer.

---

## 4. Subagent cross-checks

The user asked for subagents to cross-check the work. The dispatch is recorded in [`SUBAGENT_CROSSCHECK.md`](SUBAGENT_CROSSCHECK.md):

- **Round 1 (four parallel):** data model/pipeline, IRE, licensing/reconciliation, guide delta.
- **Round 2 (one):** final consistency and link check.

Each subagent received:

1. exact file paths,
2. a narrow checklist,
3. an instruction to return **verified / corrected / unverified** findings with evidence, and
4. a no-edit constraint.

Findings were incorporated or explicitly rejected with a reason in `SUBAGENT_CROSSCHECK.md`.

---

## 5. Confidence discipline

Every claim is marked:

| Mark | Meaning |
|---|---|
| **V** | Directly stated in an official page read for this pass |
| **C** | Corroborated by a second independent source |
| **U** | Unverified / instance-dependent / release-dependent |
| **P** | Recommended practice |

The marks are not decoration. They determine what a reader may safely copy into a production change.

---

## 6. What "done" means

The run is done when:

1. the final docs are self-contained and linked,
2. the cross-reference matrix covers the material claims,
3. the conflict log records every material disagreement,
4. the guide corrections are listed,
5. the subagent findings are incorporated or rejected with reasons,
6. the QA score is honest about gaps, and
7. the filescope names exactly what was published.
