# PLAN — SNC_SAM__WT3 (ServiceNow SAM module deep dive)

**Agent:** `kilo-sam-deepdive__kilo__cli`
**Model:** Kilo (inherited) · **Provider:** current-turn provider · **Harness:** Kilo CLI
**Goal owner:** this worktree. **Deliverable lives in** `research/servicenow-sam/SAM_MODULE_DEEP_DIVE.md` (canonical copy also at `05_FINAL/`).
**Mirror:** `plans/kilo-sam-deepdive__kilo__cli__WT3/PLAN.md`
**Isolation:** all work happens on branch `docs/sam-module-deep-dive` from `origin/main`, in a dedicated clone at `/tmp/kilo/samdeepdive`. No shared fleet file (`INDEX.md`, `CONTRIBUTORS.md`, `agents.yaml`) is edited, so other agents' uncommitted work in the main checkout cannot collide.

## Context

The reference swarm `eltonaguiar/ALT_PARALLELSWARM` documented the CMDB/Discovery module as a single end-to-end guide (`research/servicenow-discovery/DISCOVERY_END_TO_END_GUIDE.md`): moving parts → zero-to-first-success order → per-phase mechanism → full property catalog → troubleshooting → runbook → source index → gaps. This plan applies the **same phases, folder contract and depth** to `eltonaguiar/alt_parallelswarm_SAM`, documenting the SAM module with emphasis on the components every org hits — not a flat screen-parameter dump.

Existing SAM work in this repo (grok WT1 config reference, beam Australia reference, SAM_MODULE replication, grok WT2 curriculum compare) is treated as **corpus**, not overwritten. This worktree adds an independent, deeper pass organized around six operational themes in the order the user specified.

## Goal

An exhaustive, exact-name reference for ServiceNow **Software Asset Management (SAM)** covering:

1. **Out-of-box scripts** — enumerate shipped scheduled jobs, the documented business rule(s), reconciliation script includes, flows/workflows and plugin payloads; purpose, table/field target, customize-vs-leave guidance, customization risks.
2. **Maintenance — add a new software model** — step-by-step procedure listing every table and field touched, prerequisites, roles, PPN/software-model resolution scenarios.
3. **Maintenance — normalize a software model** — normalization rule families, matching job, manual/pattern paths, revert rules, normalization suggestions, then reconciliation and reclassification steps.
4. **High-probability items** — license position, compliance, reclamation, true-up, duplicate/stale hygiene — each with its exact tables/fields.
5. **Key workspaces & dashboards** — named workspace views, classic menus that remain, dashboards and reports SAM teams use daily, with source tables.
6. **Parameter inventory** — must-consider properties prioritized above the full per-screen parameter list, covering both.

Supporting sections reach parity with the CMDB guide: mental model/data model, Discovery→SAM insert-vs-update rules, order of operations, verification/health, anti-patterns/troubleshooting, source index, gaps.

## Output format

`research/servicenow-sam/SAM_MODULE_DEEP_DIVE.md`, numbered sections:

```
0   Provenance, method, release pin
1   Mental model and moving parts (short)
2   Out-of-box scripts (THEME 1)
3   Maintenance — add a new software model (THEME 2)
4   Maintenance — normalize a software model (THEME 3)
5   High-probability items (THEME 4)
6   Key workspaces & dashboards (THEME 5)
7   Parameter inventory (THEME 6)
8   Discovery feed and insert/update rules (SAM analog of IRE)
9   Order of operations (setup A / runtime B)
10  Verification, health and observability
11  Anti-patterns and troubleshooting
12  Source index
13  Gaps & UNVERIFIED
```

Every non-obvious claim carries `[S<n>]` → §12. No invented property names, table names or UI paths. Exact names are quoted from the fetched corpus.

## Phases (heartbeat written in `03_PHASES/` when the phase starts)

| phase | what | exit condition |
|---|---|---|
| 1 | capability gate + corpus lock | `00_PREREQ/PREREQ.md` PASS; all cited sources present locally |
| 2 | scope mapping: OOB component inventory | every named SAM job/BR/plugin/flow in the corpus enumerated |
| 3 | deep-dive extraction for the six themes | each theme has a draft section with exact tables/fields |
| 4 | synthesis into the guide | all 14 top-level sections present and cross-referenced |
| 5 | QA against success criteria below | `04_QA/QA.md` scored; name spot-checks pass |
| 6 | final: consolidate to `research/servicenow-sam/`, filescope, commit + push branch | branch `docs/sam-module-deep-dive` pushed with only this worktree's files |
| 7 | round 2: curriculum comparison vs `sam-guide.md` + community packs | `05_FINAL/CURRICULUM_COMPARE.md` committed |

## Success criteria (mirrors the CMDB swarm SC list)

| # | Criterion | Measurement |
|---|---|---|
| SC1 | OOB scripts enumerated extensively | §2 lists every documented SAM scheduled job, the install→discovery-model BR, recon script includes, flows; each row has purpose/table/field/customize?/risk |
| SC2 | Add-software-model procedure | §3 step-by-step with every table + field touched, roles, PPN scenarios |
| SC3 | Normalize procedure | §4 covers four rule families + ML, matching job, manual/pattern/revert, suggestions, reconciliation + reclassification steps |
| SC4 | High-probability items | §5 maps license position / compliance / reclamation / true-up / stale hygiene to exact tables and fields |
| SC5 | Workspaces & dashboards | §6 names workspace views, remaining classic menus, dashboards/reports with source tables and navigation paths |
| SC6 | Parameter inventory | §7 separates must-consider (prioritized) from the full per-screen parameter list; exact property names + defaults |
| SC7 | Traceability | every non-obvious claim has `[S<n>]`; no fabricated names |
| SC8 | Exact-name fidelity | spot-check property/table/field strings against fetched text before commit |
| SC9 | Honest limitations | §13 lists UNVERIFIED items + no-instance caveat |
| SC10 | Structural parity | same phase/folder contract and section density as `DISCOVERY_END_TO_END_GUIDE.md` |

## Risks

| risk | mitigation |
|---|---|
| Release drift (Brazil pin vs Australia/Yokohama/Xanadu) | pin Brazil primary; label Australia/Yokohama variants explicitly; flag version-gated values |
| Foundation (`com.snc.sams`) vs Professional (`com.sn_samp_master_ws`) vs SaaS LM split | name the product tier on every control |
| OOB business-rule sys_ids, UI policies, ACLs are not published | quote component lists; mark sys_id-level claims UNVERIFIED; give the audit query instead |
| Reconciliation script includes reorganized in Yokohama | call out the customization-migration risk explicitly (§2.4) |
| Community learning packs contain wrong table/role names | official docs win; pack errors recorded in §13 and round-2 compare, never merged as fact |
| Login-gated Now Create / Success Checklist content | tagged UNVERIFIED |
| Property spelling drift in docs (`samp_normalization_suggestion(s)`, `ml.overrride_ml_model_version`) | quote both spellings instead of picking one |

## Scope exclusions (named, not silent)

- Full publisher-pack licensing arithmetic beyond documented metrics (Oracle core factor, IBM PVU math, SAP named-user detail) — referenced, not derived.
- Horizontal-pattern authoring for Discovery (covered by the sibling CMDB guide); only the SAM-specific patterns/sources are listed.
- HAM-only configuration except where it shares `cmdb_ci_hardware`, catalog publish or contracts.
- Live instance verification (no entitled instance available) — every instance-behaviour claim is documented, not executed.

## Round 2 (after documentation is pushed)

Diff this guide against:
1. The learning curriculum `ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/sam/sam-guide.md` (CIS-SAM mapped).
2. The `sam-buffy/KiloCode` community pack (2026-11-04) — treated as untrusted; conflicts resolved to official docs.
3. Official Brazil/Australia product docs already cited here.

Mark AGREE / CONFLICT / CURRICULUM-ONLY / DOCS-ONLY / CURRICULUM-WRONG. Deliverable: `05_FINAL/CURRICULUM_COMPARE.md`.
