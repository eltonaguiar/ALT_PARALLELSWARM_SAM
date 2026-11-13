# Bidirectional gap diff — repo docs vs live sam-guide vs learning protocol

**Agent:** `kilo-sam-deepdive__kilo__cli` · **Date:** 2026-11-13
**Corpora:** our GitHub SAM corpus (`final/*`, `research/servicenow-sam/*`) · live page <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/sam/sam-guide/> (verified identical to repo file, 1,074 lines) · learning protocol repo `eltonaguiar/ServiceNow_Learning` (methodology, checklists, module framework, `data/modules.json`)

Directions:
- **A. Repo → SAM guide page:** we have it, the page does not → add to the SAM page.
- **B. Repo → ServiceNow_Learning protocol:** generic items that apply to any module → add to the learning protocol (with exact target files).
- **C. Page → our repo:** the page has substance we lack → absorb (or explicitly reject).

---

## A. Repo-only items missing from the live SAM guide (add to the page)

| # | Item | Why it matters | Source in repo |
|---|---|---|---|
| A1 | Out-of-box component inventory: 15 scheduled jobs, the install→discovery-model business rule, reconciliation script includes (Yokohama `com.sn_itam_samp` move), flows | The page's "Out-of-Box Features" is a feature list, not an auditable component inventory | DD §2; FINAL_grok §14–§15 |
| A2 | Parameter quick reference (Tier 0/1/2 properties + defaults) and undocumented-property audit recipe | No property guidance exists on the page; these decide go-live trust | DD §7 |
| A3 | License Position report field list; LMR allocation breakdown (Allocated in use / Not allocated in use / Allocated not in use / Nontransferable rights); Rights Needed By | Page has no result-field reference at all | DD §5.1–§5.2 `[S18][S63]` |
| A4 | Normalization statuses, five rule families (Product/Package Map, Pattern, Enhanced Pattern, Wide-net, ML), revert rules, suggestions, matching-job algorithm + manual lock | Page says only "SUMN normalization" without mechanics | DD §4; FINAL_grok §7–§9 |
| A5 | Software-model creation procedure + related lists; PPN resolution scenarios | Page omits how models are actually created/matched | DD §3; FINAL_grok §9 |
| A6 | Usage & reclamation data model: `samp_sw_usage`, Total Usage Time / Last Used Date, CI-retirement deletion, flow timeout 30 days, suite-parent behaviour, SaaS auto-created rules | Reclamation described conceptually only | DD §5.3 `[S61][S22][S34]` |
| A7 | Duplicate/stale hygiene: dedup levels + custom rules, Active flag, REST uninstalled-install delete, exclude-CI flag, Security Update exception | Page mentions duplicates once, no controls | DD §5.5, §8.2–8.3 |
| A8 | CMDB-layer governance cross-reference (IRE identification/data-source/reconciliation/data-refresh; insert gate) | Page ignores IRE entirely | DD §8.4; X1; X2 |
| A9 | Tier split: Foundation `com.snc.sams` vs Professional `com.sn_samp_master_ws` vs SaaS LM `sn_sam_saas_int`; workspace activation hides classic UI; classic-only menu list | Page's plugin tip is wrong/incomplete | DD §1.2, §6.2 |
| A10 | Activity-center alert/notification table with source tables; health-check suites; success portal maturity; renewals calendar; overlapping usage | Page lists dashboards generically | DD §6.3–§6.4 `[S38][S43]` |
| A11 | Content Service opt-in toggles, exclusion flags, product-suggestion consolidation | Absent from page | DD §4.7 `[S16]` |
| A12 | Insert-vs-update decision matrix and duplicate-prevention layers | Absent from page | DD §8.2–8.3 |

---

## B. Generic items to add to the ServiceNow_Learning protocol

These come from our SAM work but apply to **any** module implementation. Suggested targets:

| # | Item | Target file(s) | Rationale |
|---|---|---|---|
| B1 | Implementation gate checklist (pilot/go-no-go, acceptance thresholds, ownership evidence) | new `docs/methodology/module-implementation-protocol.md`; extend `scripts/rapid-learning-checklist.md` | Methodology currently ends at learning a module, not delivering one |
| B2 | Prerequisite/dependency map template (plugin, roles, dependent modules, release pin, content services, irreversible upgrades) | `docs/methodology/module-implementation-protocol.md` | Missing from module framework |
| B3 | RACI/ownership matrix template (data domains × roles) | same | Governance absent fleet-wide |
| B4 | Source-system contract template (frequency, required fields, error handling, fallback) | same | Needed for any integrated module |
| B5 | Test-case catalogue pattern (scenario → expected result → evidence) | same + `scripts/concept-summary-template.md` | Zero test cases exist in SAM corpus |
| B6 | Change-control procedure for configuration that alters results | same | Only `Revert Customizations` named anywhere |
| B7 | Validation/rollback/exception procedures | same | No rollback plan in SAM corpus |
| B8 | Cutover/hypercare/monitoring/runbook/training plan | same | Day-2 operations undocumented |
| B9 | OOB inventory audit recipe (how to enumerate shipped jobs/BRs/flows/ACLs when vendors don't publish them) | `docs/out-of-box/out-of-box-workflows-integrations.md` | Directly reusable; SAM recipe exists in DD §2.8 |
| B10 | Parameter-tiering pattern (must-configure at go-live / tune later / never touch) | `docs/fields/mandatory-vs-critical-fields.md` | Generalises DD §7.2 |
| B11 | Breadcrumb verification rule (confirm against actual UI before documenting; label release) | `docs/navigation/breadcrumbs-cheatsheet.md` | Curriculum breadcrumbs were wrong; encode the lesson |
| B12 | **SAM entry in `data/modules.json`** | `data/modules.json` | Catalog has tsom/csm/fsm/sales-crm/ham/itsm — **no SAM entry**; add tables, roles, breadcrumbs, OOB, critical fields from DD |

---

## C. Page-only items to absorb into our repo (or explicitly reject)

| # | Page item | Status in repo | Action |
|---|---|---|---|
| C1 | CIS-SAM domain weights (~15/25/30/20/10) | Referenced only in curriculum findings | **Absorb** as an exam-alignment appendix (labelled external/unverified) |
| C2 | Compliance-position state vocabulary (incl. "Not counted", Unknown/Unallocated) | Not integrated; DD uses documented Compliant/Not Compliant | **Absorb with correction**: keep documented statuses primary, note page vocabulary as exam framing |
| C3 | Publisher trap detail (MS per-core/virtualization/M365 overlap/downgrade; Oracle core factor/server licensing/LMS/named-user minimums; IBM PVU/sub-capacity ILMT; SAP named-user classes/indirect access; Adobe VIP/shared device; ServiceNow subscription billing) | High-level only (DD §5.4) | **Absorb** as practice guidance, labelled non-normative |
| C4 | Optimization priority order + 60–90 day reclaim window | Mentioned only in curriculum compare | **Absorb** into DD §5.3 as practice guidance |
| C5 | Day-one report definitions (5 reports with table/grouping) | Absent | **Absorb** with corrected table names (`samp_reconciliation_result`, `samp_sw_usage`) |
| C6 | Indicative KPI targets (>95% normalized etc.) | Absent | **Absorb** with "indicative, not vendor SLA" label |
| C7 | SaaS assigned-vs-active seats; dead-connector warning; typical SaaS targets | Nearly absent (1 hit) | **Absorb** as SaaS operating notes |
| C8 | Integration protocol table (SCCM/Intune/Jamf/M365/Adobe/Salesforce/Oracle LMS/ILMT/SAP) | Partial (DD §8.1) | **Absorb** as protocol/mechanism mapping |
| C9 | Memory aids (BAA, LOCS, ARM, Retire Before Delete, Order vs Priority, Coalesce = Match, Log First Then Debug) | Referenced only | **Absorb** into curriculum/exam material, not operational docs |
| C10 | Lab sequence (7 steps) + teach-back | Absent | **Absorb** as a hands-on lab doc (uses corrected names/paths) |
| C11 | Quiz | Referenced only | **Absorb** corrected quiz into exam material |
| C12 | Official resources/videos/courses | Absent | **Absorb** as resource pointers |
| C13 | Data-source taxonomy + quality rules | Partial | **Absorb/merge** into DD §8.1 |
| C14 | Page errors (`cmdb_sam_sw_usage`, `sam_sw_reconciliation_result`, nightly cadence, SUMN, plugin tip, breadcrumbs) | Documented in CURRICULUM_FINDINGS | **Reject** — keep corrections in fleet docs; feed back to page maintainers |

---

## D. Recommended sequence

1. **To the SAM guide maintainers** (highest value): apply corrections (CURRICULUM_FINDINGS §5) then add sections A1–A12.
2. **To ServiceNow_Learning**: add B1–B8 as a new implementation protocol + extend the checklist; add B9–B11 to existing docs; add the SAM entry to `data/modules.json`.
3. **To our GitHub repo**: absorb C1–C13 selectively (exam appendix, practice notes, corrected day-one reports/lab/quiz) — keep official-doc authority and label practice vs documented.

*Evidence-based diff; no external repos modified.*
