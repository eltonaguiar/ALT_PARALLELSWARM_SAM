# Curriculum compare — SAM deep dive vs learning guides

**Agent:** `kilo-sam-deepdive__kilo__cli` · **Round:** SNC_SAM__WT3 round 2 · **Date:** 2026-11-13
**Subject:** `SAM_MODULE_DEEP_DIVE.md` (this folder)
**Verdicts:** AGREE · CONFLICT · CURRICULUM-ONLY · DOCS-ONLY · CURRICULUM-WRONG

| ID | Corpus | Path |
|---|---|---|
| DD | This deep dive (Brazil/Australia product docs, exact names) | `research/servicenow-sam/SAM_MODULE_DEEP_DIVE.md` |
| LG | Learning curriculum SAM guide (opencode, 2026-11-12, CIS-SAM mapped) | `ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/sam/sam-guide.md` |
| SB | sam-buffy KiloCode community pack (2026-11-04) — **untrusted** | `/home/eaguiar2015/sam-buffy/KiloCode/` |

---

## 1. CIS-SAM domain coverage (LG blueprint vs DD)

Weights are from LG only (Now Learning blueprint not fetched).

| CIS-SAM domain (LG) | ~weight | DD coverage | Verdict |
|---|---|---|---|
| 1 Overview & fundamentals | 15% | §1 mental model, pipeline, product tiers, roles | **AGREE** — DD stronger on plugin IDs and Foundation/Pro split |
| 2 Data integrity: models, normalization, Content Library | 25% | §4 statuses, five rule families, suggestions, pattern/custom rules; §3 model creation | **AGREE** — DD names Product/Package Map, Pattern, Enhanced Pattern, Wide-net, ML; LG calls this **SUMN**, a term absent from official pages |
| 3 Entitlements, licenses, reconciliation | 30% | §3.4 PPN scenarios; §5.1–5.2 license position + three-tier results; §7.2 parameters | **AGREE** on `alm_license`; **CONFLICT** on recon cadence (LG nightly vs DD/docs weekly) |
| 4 Optimization, reclamation, audit | 20% | §5.3–5.5 reclamation, true-up, duplicate/stale hygiene | **AGREE** directionally — DD has named rule types, tables and the 30-day flow timeout; LG adds 60–90 day reclaim window guidance |
| 5 Reporting, dashboards, ops integration | 10% | §6 workspace views, eight named dashboards/reports with source tables; §10 health/alerts | **PARTIAL** — LG has exam-style KPI/target table; DD has vendor-named widgets and alert sources |

**Curriculum-only topics worth absorbing in a later revision (not overwriting documented facts):** the CIS-SAM domain/weight map itself; the compliance-position state diagram including **Not counted**; SaaS-LM assigned-vs-active seat flow; day-one report definitions; SLA-style targets; the lab sequence; memory aids (BAA/LOCS/ARM).

---

## 2. Record types — AGREE with LG, reject LG naming errors

| Record | LG table | DD / official | Verdict |
|---|---|---|---|
| Software Model | `cmdb_software_product_model` | same | **AGREE** |
| Discovery Model | `cmdb_sam_sw_discovery_model` | same | **AGREE** |
| Installation | `cmdb_sam_sw_install` | same | **AGREE** |
| Entitlement | `alm_license` | same | **AGREE** |
| Usage | `cmdb_sam_sw_usage` | **`samp_sw_usage`** (product-level; reclamation types Total Usage Time / Last Used Date) `[S61]` | **CONFLICT → DD/DOCS win** — LG table name is wrong (round-3 correction) |
| Reconciliation Result | `sam_sw_reconciliation_result` | **`samp_reconciliation_result`** (Activity center source `[S43]`) | **CONFLICT → DD/DOCS win**; LG name is wrong |
| Removal candidate | (not named by LG) | `samp_sw_reclamation_candidate` | **DOCS-ONLY** |
| Product results / metric results | (not named by LG) | `samp_product_result`, `samp_license_metric_result` | **DOCS-ONLY** |

LG's own footer warns *"verify table names…"* — its `sam_sw_reconciliation_result` is exactly the kind of drift to catch.

---

## 3. Conflicts resolved to official docs

| Topic | LG | DD / official docs | Keep |
|---|---|---|---|
| Reconciliation schedule | "scheduled job (**default nightly**)" | "**Reconciliation runs weekly or on demand**" (weekly default; on demand per publisher/group/subgroup) | **DD/DOCS weekly**; LG nightly is wrong |
| Menu plugins | "`com.snc.sams` (Foundation/**Pro**) and ITAM plugin `com.snc.iam`" | Foundation `com.snc.sams`; Professional `com.sn_samp_master_ws` / `com.sn_samp_master` / `com.snc.samp`; `com.snc.iam` is not a SAM component | **DD/DOCS split** — never equate Foundation plugin with Pro |
| Normalization brand | "**SUMN** (Software Usage and Normalization Mapping)" | Content Library normalization; daily job `SAM - Normalize discovery models using content library rules` | **DD/DOCS names**; SUMN not found in official pages |
| Install → model link | sample BR writes `current.software_model` on the install | BR matches **discovered publisher + product + version** against the **discovery model** | **DD/DOCS** — LG sample is teaching code, not OOB |
| Recon result table | `sam_sw_reconciliation_result` | `samp_reconciliation_result` | **DD/DOCS** |
| Software model base | "models extend `cmdb_model`"; field `license_metric_type` | Not confirmed in fetched corpus | **UNVERIFIED** — LG instructs to verify; DD does not assert |
| Navigation parent | `All > Software Asset Management > …` | `Workspaces > Software Asset Workspace` / `All > Software asset > …`; classic docs use `All > Software Asset > …` | **Both exist** — DD lists exact paths per screen |
| Reconciliation inputs | entitlement qty + installs + usage evidence | entitlement + normalized installs/discovery models; usage for reclamation/SaaS | **AGREE** (usage is a reclamation signal, not the primary numerator on-prem) |

---

## 4. Where LG is stronger (absorb later, do not overwrite DD)

1. **CIS-SAM domain map + weights** — gives exam-oriented prioritisation.
2. **Compliance-position vocabulary** — `Not counted` state; explicit "Unknown ≠ compliant" (DD §5.1 carries the operational rule; LG adds the state diagram).
3. **Publisher trap table** — Oracle core-factor/server licensing, IBM PVU sub-capacity/ILMT, SAP named-user classes, MS SQL cores/virtualization, Adobe VIP, ServiceNow subscription billing. DD §5.4 references these; LG is more concrete.
4. **Entitlement hygiene** — one entitlement per contract line; maintenance ≠ licence; never overwrite quantity; metric mismatch is silent.
5. **Optimization priority order** and the 60–90 day reclamation inactivity window.
6. **SaaS assigned-seats vs active-users** distinction and dead-connector warning.
7. **Day-one reports** — expiring entitlements, under-licensed models, unmatched discovery models, no-usage installs, over-licensing cost.
8. **Indicative KPI targets** — clearly labelled indicative, not vendor SLAs.

---

## 5. What DD has that no curriculum covers

- Full OOB component inventory (jobs J1–J15, the documented business rule, reconciliation script includes, flows) with customize-vs-leave guidance.
- Step-by-step add-software-model procedure with every table/field touched and PPN resolution scenarios.
- Complete normalize/reclassify loop (statuses, rule families, revert rules, suggestions, manual matching lock).
- Exact License Position field list and multi-report behaviour.
- Three-tier reconciliation result structure and related lists.
- Workspace view list, classic-only menus, eight named dashboards/reports with source tables, activity-center alert sources.
- Prioritized parameter inventory plus full per-screen parameter list (properties A–O).
- Duplicate/stale hygiene controls (dedup levels, Active flag, uninstall REST delete, exclude-CI flag).
- Honest UNVERIFIED list and the community-pack error register.

---

## 6. Corrections we will NOT take from LG sample code or SB

1. Do not teach `sam_sw_reconciliation_result`, `sam_license_manager`, `sn_sam.admin`, `alm_software`, `alm_software_installation`.
2. Do not present LG's sample BR/scheduled-job/client-script snippets as OOB objects; they are teaching illustrations with custom fields (`u_normalization_status`, `u_sam_status`, `u_license_metric_notes`, `compliance_state`).
3. Do not change the reconciliation default from weekly to nightly.
4. Do not adopt "SUMN" as an official product term; keep Content Library + job names.
5. Do not collapse catalog publish vs software-model creation vs discovery linking — DD keeps them separate.
6. Do not teach LG's `cmdb_sam_sw_usage` — the official table is **`samp_sw_usage`** `[S61]`. Do not treat LG's `cmdb_model` extension claim as fact without an instance check.

**SB remains worse than LG** and must not be merged at all: it teaches `alm_software` / `alm_software_installation` as core tables, roles `sam_license_manager` / `sn_sam.admin`, and places SAM under Hardware Asset Management navigation. None of those appear in official docs.

---

## 7. Recommended follow-ups (not done this round)

1. Add a short "exam alignment" appendix mapping DD sections to CIS-SAM domains, citing LG weights as external context.
2. Absorb LG's optimization priority list and 60–90 day reclaim window as operational guidance in §5.3, clearly labelled as practice guidance rather than vendor-documented defaults.
3. ~~Verify `cmdb_sam_sw_usage`~~ — resolved in round 3: official table is `samp_sw_usage` `[S61]`. Still verify on an entitled instance: `samp_reconciliation_result` spelling and whether usage feeds participate in on-prem reconciliation numerators.
4. Reconcile LG's "Not counted" compliance state with the documented Compliant/Not Compliant pair — likely an exam simplification of exclusion reporting.

*Compare only; no factual changes were made to the deep dive based on the community pack.*
