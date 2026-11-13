# PLAN — SNC_SAM__WT1 (deepseek-flash · deepseek · Kilo)

**Agent:** `deepseek-flash__deepseek__kilo`
**Model:** `deepseek/deepseek-flash` · **Provider:** DeepSeek · **Harness:** Kilo CLI
**Date:** 2026-11-13
**Release pin:** ServiceNow docs **Brazil** ITAM map (`PMOYmdGTPDs40EbYh10h4g`), pages *Updated Sep 10 2026* unless noted. Australia-family corroboration used only where Brazil is silent, and is labelled.
**Task:** apply the `ALT_PARALLELSWARM` CMDB/Discovery phased pattern to **Software Asset Management (SAM)**, at equal depth, covering every SAM configuration option, discovery rule, and licence/CI insertion-and-update rule.

---

## 0. Goal and non-goals

**Goal.** A single, evidence-anchored SAM module reference that an implementer can run from, with:

1. out-of-box scripts/jobs enumerated (purpose → target table/field → customise vs leave → risk);
2. maintenance runbooks for **adding a software model** and **normalising a software model**, listing every table and field touched;
3. the high-probability recurring work (licence position, compliance, reclamation, true-up) with exact tables/fields;
4. named workspaces, dashboards, reports;
5. a parameter inventory split into *must-consider* and *full per-screen*;
6. exact ServiceNow table/field names, with an explicit confidence marker where the docs publish only a label;
7. a second-round comparison against the learning curriculum, plus a gap list.

**Non-goal.** Re-documenting raw Discovery/IRE internals (MID Server, Shazzam, IRE rule families). Those live in `ALT_PARALLELSWARM`. SAM only reuses them where software data crosses the boundary (`cmdb_sam_sw_install`, file-based discovery, IRE third-party insert).

---

## 1. Output format

Every deliverable is Markdown in the repo's standard contract:

```
agents/deepseek-flash__deepseek__kilo/
  AGENT_CARD.md
  SNC_SAM__WT1/
    00_PREREQ/PREREQ.md
    01_PLAN/PLAN.md                # this file
    02_CLARIFICATIONS/CLARIFY.md
    03_PHASES/phaseN_*.md
    04_QA/QA.md
    05_FINAL/SAM_MODULE_REFERENCE.md     # the deep reference
    05_FINAL/ROUND2_GAP_ANALYSIS.md      # curriculum compare + missed items
    05_FINAL/FINAL_SUMMARY.md
    06_FILESCOPE/FILESCOPE.md
    research/README.md
plans/deepseek-flash__deepseek__kilo__WT1/{PLAN.md,STATUS.md}   # mirror
final/FINAL_deepseek-flash__deepseek__kilo.md                   # merged fleet compilation
README.MD                                                       # appended section
```

**Confidence legend used in every table** (mirrors the reference repo's evidence discipline):

| Mark | Meaning |
|---|---|
| **V** | table/field/value printed verbatim on the Brazil docs page cited |
| **C** | corroborated by a sibling Australia-family page or by `ALT_PARALLELSWARM` |
| **U** | the docs publish only the UI label; internal column/table is **unverified** — read `sys_dictionary` / `sys_db_object` on the instance before scripting |

Never invent a column to fill a gap. A `U` is a finding, not a failure.

---

## 2. Phases

| # | Phase | Output | Exit check |
|---|---|---|---|
| 0 | **Prereq** | `00_PREREQ/PREREQ.md` | Can read the repo, GitHub, and the existing Brazil corpus; no live instance (so all claims are documentary) |
| 1 | **Corpus inventory** | `research/README.md` | Every Brazil SAM page already fetched by the fleet is indexed by local file + `[S<n>]`; duplication avoided |
| 2 | **Plan + contract** | `01_PLAN/PLAN.md`, folder skeleton | Folder matches `ALT_PARALLELSWARM`; conflict-free agent id chosen |
| 3 | **Table/field contract + insert/update** | reference §2, §4 | Every record type has a table, a key, and an insert-vs-update decision row |
| 4 | **Normalisation deep dive** | reference §5, §6 | All normalisation statuses, transitions, revert rules, suggestions, pattern/wide-net/ML, model↔vendor, listed |
| 5 | **Reconciliation / position / true-up / reclamation** | reference §7–§9 | Rights algebra and every remediation option tied to a field |
| 6 | **OOB scripts + maintenance runbooks** | reference §3, §10, §11 | Jobs/BRs/flows/UI actions enumerated; add-model and normalise-model runbooks list every table/field |
| 7 | **Workspaces, dashboards, reporting** | reference §12 | Every named workspace/report/widget has a source table |
| 8 | **Integrations** | reference §13 | Each feed has plugin id, direction, target table, and uninstall behaviour |
| 9 | **Parameter inventory** | reference §14 | Must-consider list separated from per-screen list; defaults and blast radius given |
| 10 | **QA / verification** | `04_QA/QA.md` | Every `V` has a local source; every `U` is explicitly listed |
| 11 | **Round 2 — curriculum + gap** | `05_FINAL/ROUND2_GAP_ANALYSIS.md` | CIS-SAM domains, conflicts, missed platform/SAM items, reporting and combination checks answered |
| 12 | **Final merge + publish** | `final/…`, `README.MD`, push | Folder pushed; README appended with separator, agent id, timestamp, fleet compilation |

---

## 3. Critical items — coverage requirements (the "combinations" bar)

For each item the plan requires an explicit matrix, not prose:

1. **Normalisation status** — all values × manual-normalise allowed × revert allowed × suggestion behaviour × auto-accept.
2. **Normalisation rule family** — Product/Package Map × Pattern × Enhanced Pattern × Wide-net × ML × manual; scope and when each wins.
3. **Dedup** — Exact × Major × Any × stale threshold × source reliability × completeness × version tiebreak.
4. **Insert/update** — install × discovery model × software model × entitlement × catalog item × allocation; what can block each.
5. **Rights** — owned/used/available × allocated-in-use / not-allocated-in-use / allocated-not-in-use / not-allocated / allocations-needed × remediation option.
6. **Licence type** — Perpetual × +SA × +Maintenance × Subscription × Upgrade × Step-up × Subscription Step-up × Add-on × From SA × Enterprise agreements.
7. **Product type** — Child × Driver × Licensable × Not Licensable × Patch × Unknown × reconciliation participation.
8. **PPN import** — blank/provided × standard/MLS × auto-create on/off.
9. **Scope controls** — exclude-CI × published-products × content-service exclusion × Security-Update skip × dedup Active=false.
10. **Recon grouping** — None × Company × Cost Center × Country × Department × Region, and group ≠ subgroup.

If a combination is undocumented, the reference says so and gives the instance query to settle it.

---

## 4. Risks

| Risk | Mitigation |
|---|---|
| Confusing **software model** with **discovery model** — the #1 SAM error | §2 record-type table, §6 model-vs-vendor, explicit "cannot be created manually" |
| Treating legacy/community table names (`alm_software`, `samp_sw_entitlement`, `cmdb_sam_sw_usage`, `sam_sw_reconciliation_result`) as real | Rejected in §2 and Round-2 §4; only `alm_license`, `cmdb_sam_sw_*`, `samp_*` verified forms used |
| Overlaying the unnamed install→discovery-model business rule | "Leave untouched" rule in §3; extension points listed |
| Assuming reconciliation is nightly | Brazil docs say **weekly default + on demand**; recorded as a conflict |
| Publishing flattened parameter lists | Must-consider first, full list second, each with blast radius |
| Release drift (Brazil vs Australia/Zurich) | Pin stated in every header; Australia-only facts marked **C** |

---

## 5. Success criteria

- [ ] Folder contract identical in shape to `ALT_PARALLELSWARM`.
- [ ] Every requested ordering (OOB scripts → add model → normalise model → high-probability items → workspaces/reporting → parameter inventory) is a numbered section.
- [ ] Every table/field carries a confidence mark; no fabricated columns.
- [ ] Reporting, integrations, normalisation-status fields, model-vs-vendor, and option combinations each have a dedicated matrix.
- [ ] Round-2 curriculum compare names agreements, conflicts, and curriculum-only vs docs-only items.
- [ ] `README.MD` append uses `--------------`, agent identity, ISO timestamp, and merges **all** fleet SAM work.
- [ ] Pushed to `eltonaguiar/ALT_PARALLELSWARM_SAM` inside a unique folder; no other agent's files touched.

---

## 6. Effort / sequencing

Single self-driven run. Phase 1 is cheap because the fleet already fetched the Brazil corpus; the cost is synthesis and the matrices. Order matters: table contract (3) before normalisation (4) before reconciliation (5), because rights algebra is meaningless until the record types are fixed. OOB scripts (6) come after reconciliation so each job can be tied to the field it writes.
