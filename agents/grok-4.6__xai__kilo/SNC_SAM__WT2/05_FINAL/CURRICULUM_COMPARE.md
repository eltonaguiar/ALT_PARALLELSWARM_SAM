# Curriculum compare — SAM WT1 vs learning guides

**Agent:** `grok-4.6__xai__kilo` · **Round:** SNC_SAM__WT2 · **Date:** 2026-11-13

Compared:
| ID | Corpus | URL / path |
|---|---|---|
| WT1 | Brazil-pinned SAM config reference | `agents/grok-4.6__xai__kilo/SNC_SAM__WT1/05_FINAL/SAM_CONFIG_REFERENCE.md` |
| LG | Learning curriculum SAM guide (opencode, 2026-11-12, CIS-SAM mapped) | https://github.com/eltonaguiar/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/blob/main/docs/modules/sam/sam-guide.md |
| SB | sam-buffy KiloCode pack (2026-11-04) | `/home/eaguiar2015/sam-buffy/KiloCode/` |
| DOC | Official Brazil/Australia product docs | WT1 `research/raw/` + S38 |

Discovery-pass analog: deepseek-flash QA terminology audit vs cmdb-guide / discovery-guide.

---

## 1. CIS-SAM domain coverage (LG blueprint vs WT1)

Weights are **from LG only** (Now Learning blueprint not fetched).

| CIS-SAM domain (LG) | ~weight | WT1 coverage | Verdict |
|---|---|---|---|
| 1 Overview & fundamentals | 15% | §1 mental model, Foundation vs Pro vs SaaS, roles | **AGREE** — WT1 stronger on plugin IDs |
| 2 Data integrity: models, normalization, Content Library | 25% | §7–9, §8 rule families, Content Service | **AGREE** — WT1 names Product/Package/Pattern/Wide-net/ML; LG calls this **SUMN** (not in official properties pages) |
| 3 Entitlements, licenses, reconciliation | 30% | §11–12, insert-vs-update table | **AGREE** on `alm_license`; **CONFLICT** recon cadence |
| 4 Optimization, reclamation, audit | 20% | §13, §20 Path to Value | **AGREE** directionally; WT1 has named reclamation rule types from DOC |
| 5 Reporting, dashboards, ops integration | 10% | §5 workspace, §18 verification, Success portal | **PARTIAL** — LG has exam-style KPI table; WT1 has Success portal widgets |

**Curriculum-only (not in WT1, worth a WT3):** `cmdb_sam_sw_usage`, reconciliation-result table name, publisher-trap core-factor/PVU/SAP named-user, CIS-SAM lab steps, Ask-a-Ranger video list.

**Docs-only (not in LG):** four catalog/discovery paths, `com.snc.samp.manage.published.products`, exclude-CI flag, unnamed install BR, `SAM – Discovery Model to Software Model matching`, 3rd-party IRE property, Foundation `com.snc.sams` vs Pro `com.sn_samp_master_ws`.

---

## 2. Record types — AGREE with LG, REJECT SB

LG “three record types you must never confuse” (actually six rows) vs WT1 four matching layers:

| Record | LG table | WT1 / DOC | Verdict |
|---|---|---|---|
| Software model | `cmdb_software_product_model` | same | **AGREE** |
| Discovery model | `cmdb_sam_sw_discovery_model` | same | **AGREE** |
| Installation | `cmdb_sam_sw_install` | same | **AGREE** |
| Entitlement | `alm_license` | same | **AGREE** |
| Usage | `cmdb_sam_sw_usage` | not in WT1 | **CURRICULUM-ONLY** — verify on instance |
| Recon result | `sam_sw_reconciliation_result` | not named in DOC pages we fetched | **UNVERIFIED** table name |
| Catalog item | (LG almost silent) | Product Catalog publish/link §10A | **DOCS-ONLY** — LG collapses this into “request/procure” |

**SB is wrong and must not be merged:**

| SB claim | Official |
|---|---|
| Core tables `alm_software`, `alm_software_installation` | **CURRICULUM-WRONG** — those are not SAM Pro install/model tables |
| Roles `sam_license_manager`, `sn_sam.admin` | **CURRICULUM-WRONG** — DOC: `sam_admin`, `sam_user`, `sam_developer`, `sam_integrator` |
| Nav `SAM → Hardware Asset Management` | **CURRICULUM-WRONG** — HAM is a sibling module |
| Foundation data = asset categories/states as SAM go-live | Mixes HAM `alm_asset` onboarding with SAM |

LG already warns: *verify table names in your release*. WT1 + DOC win on names.

---

## 3. Conflicts to keep explicit

| Topic | LG | WT1 / DOC | Keep |
|---|---|---|---|
| Reconciliation schedule | “default **nightly**” | Properties page: **weekly** run of recon grouping; also on-demand | **DOC weekly** as default; nightly is UNVERIFIED |
| Plugin for menus | `com.snc.sams` **and** `com.snc.iam` | Foundation `com.snc.sams`; Pro `com.sn_samp_master_ws` / `com.snc.samp`; IAM not in SAM components article | **DOC split**; do not say Foundation plugin = Pro |
| Normalization product name | **SUMN** | Content Library + daily `SAM - Normalize discovery models using content library rules` | **DOC names**; SUMN is LG jargon |
| Install → model link | sample BR uses `current.software_model` on install | DOC BR matches **publisher+product+version** to **discovery model** | **DOC**; LG sample BR is teaching code, not OOB |
| Recon default | nightly job walks every model | weekly + `com.snc.samp.recon.group` | **DOC** |
| Breadcrumbs | `All > Software Asset Management > SAM Workspace` | `Workspaces > Software Asset Workspace` / `All → Software asset → Software Asset Workspace` | both exist; Brazil prefers Workspace |
| Auto-create models | not emphasized | `automaticsmrcreation` off in Crawl (Office Hours + DOC) | **WT1** |
| Catalog vs discovery | lifecycle “Request and Procure” then entitle then discover | four **separate** paths A–D | **WT1** — LG under-specifies catalog publish |

---

## 4. Where LG is stronger (absorb later, don’t overwrite WT1)

- CIS-SAM domain map + quiz + lab (entitle 1, recon, then raise qty)
- Compliance positions including **Unknown ≠ compliant**
- Publisher traps (Oracle core factor, IBM PVU+ILMT, SAP named user, MS SQL cores)
- “Never overwrite entitlement quantity; create true-up”
- Maintenance ≠ license
- Suite roll-up as #1 over-count
- 60–90 day reclaim window (DOC does not give that number; LG/community)
- Usage table and last-used as reclamation evidence
- Shared `ast_contract` / `alm_asset` hierarchy with HAM

---

## 5. Module-implementation checklist (LG 10 questions vs WT1)

LG module framework asks: table, role, 5 fields, BRs, UI policies, ACLs, flows, related tables, OOB reports, integrations.

| Question | WT1 | Gap |
|---|---|---|
| Primary tables | yes | — |
| Roles | yes (`sam_*`) | SB roles discarded |
| Important fields | install + model + entitlement | usage + recon-result fields thin |
| BRs on insert/update | unnamed install→DMAP BR | **sys_ids / UI policies still instance-only** |
| UI policies | UNVERIFIED | still UNVERIFIED |
| ACLs | not listed | gap |
| Flows | reclamation timeout, request workflow pointed at | names thin |
| Related tables | yes | add `cmdb_sam_sw_usage`, `ast_contract` |
| OOB reports | Success portal / license position | LG day-one report list useful |
| Integrations | Discovery, SCCM/SGC, ILMT, SaaS, IRE 3rd-party | Intune/Jamf as SGC not native SAM |

---

## 6. Corrections we will **not** take from SB or LG sample code

1. Do not teach `alm_software` / `alm_software_installation`.
2. Do not teach `sam_license_manager` / `sn_sam.admin` as SAM Pro roles.
3. Do not ship LG sample BRs that write `u_normalization_status` on install as if they were OOB.
4. Do not change recon default from weekly to nightly without an instance check.
5. Do not equate Product Catalog publish with software-model creation.

---

## 7. Recommended WT1 follow-ups (not done this round)

- Add `cmdb_sam_sw_usage` section if the table exists on Brazil.
- Verify `sam_sw_reconciliation_result` vs license position / `samp_license_metric_result`.
- Map CIS-SAM quiz items to WT1 section numbers in a cheat sheet.
- Pull HAM guide only for shared `alm_asset` / catalog publish (already §10A).
