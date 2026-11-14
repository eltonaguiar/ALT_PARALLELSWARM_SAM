# 04 — QA

**Scored against:** [`../01_PLAN/PLAN.md`](../01_PLAN/PLAN.md)
**Not scored against:** the private rubric (not read).
**Date:** 2026-11-14.

---

## 1. Scorecard

| Dimension | Weight | Score | Notes |
|---|---|---|---|
| **Coverage** — the plan's required topics are present | 20 | 19 | Module guide, IRE, pipeline, normalization/dedup, entitlements/reconciliation, config, operations, sources. Publisher-specific depth is intentionally summarized. |
| **Accuracy** — official claims match the extracts | 30 | 27 | Round 1 found no fabricated mechanisms; 1 release fact, 1 guide attribution, 1 matching mechanism, and 1 usage-granularity issue were corrected. Residual **U** items are labeled. |
| **Evidence** — claims trace to a source and status | 15 | 14 | Cross-reference matrix + source notes. A few **U** items rely on absence of evidence, which is stated. |
| **Consistency** — docs agree with each other | 15 | 14 | Round 2 found mark/mapping conflicts; all blockers fixed. |
| **Operability** — a team can execute the runbook | 10 | 9 | Pre-flight, gates, troubleshooting, rollback, audit chain. No live instance, so execution is untested. |
| **Guide cross-reference** — guide claims audited | 10 | 9 | 21 numbered items + G-22–G-31; C-10 correctly marked not-a-correction; C-19 correctly partial. |
| **Total** | 100 | **92** | Pass for a documentary reference; conditional for production change. |

---

## 2. Plan success criteria

| # | Criterion | Result |
|---|---|---|
| 1 | Trace any install to a compliance result | **Met** — record chain + three tiers |
| 2 | Four IRE rule families + insert/update applicability | **Met** — truth table + first-writer exception |
| 3 | Six normalization statuses + revert rules | **Met** |
| 4 | Three reconciliation tiers + rights algebra | **Met** |
| 5 | Plugin/role/table/property evidence marks | **Met** — with **U** where instance-dependent |
| 6 | Guide conflicts listed with corrections | **Met** — 21 + 10 additional |
| 7 | Subagent findings incorporated or rejected | **Met** — `SUBAGENT_CROSSCHECK.md` |
| 8 | Self-contained, lint-clean, published only as planned | **Met** (see filescope) |

---

## 3. Defects found by subagents and fixed

| # | Defect | Fix |
|---|---|---|
| 1 | Software-model matching described with the v1 Display Name strategy | Replaced with the official `SAM – Discovery Model to Software Model matching` job semantics; v1 strategy marked **C/U** |
| 2 | Classic UI support date said Australia | Corrected to Brazil + master-plugin lockout |
| 3 | Runtime diagram conflated normalization status with model association | Rewrote the branch |
| 4 | Usage drawn as install-level | Corrected to product-level; removed the install edge |
| 5 | Retired/stolen CI row contradicted the install-deletion behavior | Reworded; exclude-CI scoped to leased/out-of-scope |
| 6 | Overview widget dependency named the wrong job | Corrected to normalize + `SAM - Daily Job`; added CDS job |
| 7 | `New` status described as manually eligible | Corrected; reconciliation gate is `Licensable` |
| 8 | Dedup primary selection attributed to IRE | Corrected to SAM dedup logic |
| 9 | Intune/Jamf marked V | Marked **U** for the Brazil SAM pages |
| 10 | Guide C-10 attributed an OOB claim the guide did not make | Rewritten as not-a-correction |
| 11 | Guide C-19 said the table lacked records | Reframed as a heading rename |
| 12 | GUIDE ↔ CONFLICT correction IDs collided | Rebuilt both mapping tables |
| 13 | IRE "four families" marked V | Framing **C**; each family **V** |
| 14 | IRE property defaults attributed to a secondary matrix | Re-labeled **V**, cited the official properties page |
| 15 | IRE first-writer exception missing | Added |
| 16 | `installed_on` API column marked V | Marked **U** |
| 17 | `samp_reconciliation_result` marked C in one file and V in others | Standardized to **V**; the "no single analysis table" claim remains **C** |
| 18 | Suggestion table name plural/singular inconsistent | Standardized: singular **V**, plural label **C**, exact table **U** |
| 19 | Step-up conflict marked inconsistently | Standardized **C/U** |
| 20 | Missing `com.sn_itam_samp`, `samp_sw_resource_value`, cost-ratio properties, CDS/spend jobs | Added |
| 21 | `SUBAGENT_CROSSCHECK` cited `05 §9` for classic UI | Corrected to `01 §9` |
| 22 | Round 2 truncated session ID | Corrected |

---

## 4. UNVERIFIED items (kept as U, not filed as gaps)

| # | Item | Why unverified | Verification |
|---|---|---|---|
| U1 | Exact data-refresh definition table/field names | Not exposed in the fetched IRE pages | CI Class Manager → Reconciliation Rules → Add |
| U2 | Exact API columns (`normalization_status`, `software_model`, `license_metric`, `installed_on`) | Docs expose labels, not columns | `sys_dictionary.list` |
| U3 | Software Model Results table name | Not documented in Brazil | `sys_db_object` / result record |
| U4 | Publisher-specific rules (Oracle core factors, IBM PVU, SAP indirect access, Microsoft virtualization) | Contract/pack-specific | Publisher agreement + pack docs |
| U5 | Exact reconciliation schedule/time zone | Weekly default documented; hour is configuration | `sysauto_script` |
| U6 | Job cadences for jobs other than the five official ones | Not published | `sysauto_script` |
| U7 | Foundation vs Professional plugin containment in your release | Release-dependent | `sys_plugins` |
| U8 | Static vs dynamic IRE in your instance | Instance configuration | `glide.identification_engine.dynamic_ire_enabled` |
| U9 | Intune/Jamf Service Graph support in Brazil SAM pages | Not in the fetched pages | Connector docs / instance |
| U10 | `samp_vmware_license_key`, `samp_oracle_options`, `cmdb_ci_spkg` table names | v1/secondary only | `sys_db_object` |
| U11 | `samp_entitlement` / `cmdb_sam_entitlement` | Not documented for Brazil; do not use | `sys_db_object` (migration only) |
| U12 | Whether your instance has manual model-matching overrides | Instance data | `Automatically matched` field |

---

## 5. Round 2 verdict

**First pass: fail.** The reviewer found two missing artifacts (`04_QA/QA.md`, `06_FILESCOPE/FILESCOPE.md`), wrong GUIDE↔LOG mappings, five confidence-mark conflicts, one overstated subagent record, and a link checked from the wrong directory. All were fixed:

- **Missing artifacts:** created.
- **Mapping:** both tables rebuilt (C-01..C-23).
- **Marks:** `samp_reconciliation_result` → **V**; suggestion table → **V/C/U** consistently; IRE defaults → **V**; IRE roles → **V**; step-up → **C/U**.
- **Subagent record:** section references corrected; round 2 ID recorded; role additions made true.
- **v1 links:** `../final/` paths verified against the repo (the reviewer checked from `/tmp`, where they cannot resolve). The published `finalv2/` sits beside `final/`.
- **Minor:** trap wording, cheat-sheet link claim, top-correction plugin set, phase status/timestamps.

**Final status: pass for publication as a documentary reference.** It is **not** a substitute for instance-level verification before a production change.

---

## 6. Residual risks

| Risk | Severity | Mitigation |
|---|---|---|
| Release drift (Brazil → later) | Medium | Release pin + **U** marks; re-verify plugins/properties |
| Publisher rules summarized | Medium | Contract-specific; do not quote as product rules |
| No live instance | High for execution | Run the pre-flight and gates in sub-production |
| Guide remains wrong in its main body | Medium | High-risk corrections should be applied to the guide itself |
| Private rubric unknown | Low | Scored against the public plan; the user can grade independently |
| v1 docs remain in the repo with old claims | Low | This set cross-references and corrects them; v1 is not edited |

---

## 7. Publication gate

| Check | Status |
|---|---|
| All planned docs exist | Yes |
| Relative links resolve in repo layout | Yes |
| No TODO/TBD placeholders | Yes |
| Cross-reference matrix present | Yes |
| Conflict log present | Yes |
| Guide delta present | Yes |
| Subagent record present | Yes |
| Filescope present | Yes |
| Only `finalv2/**` + requested README section | Yes (see filescope) |
| No secrets or credentials | Yes |
