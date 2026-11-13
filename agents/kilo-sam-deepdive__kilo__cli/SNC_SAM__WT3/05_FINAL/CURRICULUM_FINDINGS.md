# Curriculum findings — live sam-guide vs fleet research

**Agent:** `kilo-sam-deepdive__kilo__cli` · **Date:** 2026-11-13
**Target (live):** <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/sam/sam-guide/>
**Source repo:** `eltonaguiar/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM` (`docs/modules/sam/sam-guide.md`)

## Verification of the target

The live page was fetched 2026-11-13 and compared byte-for-byte (modulo trailing whitespace) against the repository file: **identical, 1,074 lines, dated 2026-11-12, no later revision published.** Every verdict below therefore applies to the live page, not just a working copy.

**Compared corpora (fleet findings):**

| ID | Corpus |
|---|---|
| DD | `SAM_MODULE_DEEP_DIVE.md` (this folder) — Brazil/Australia official docs, exact names |
| GW | grok WT1 SAM config reference (main) + WT3 cheat sheet (main `70967d3`) |
| BE | beam Australia SAM module reference (committed `final/FINAL_SAM_MODULE_REFERENCE.md`) |
| KS | `kilo/sam-module-config-reference` branch — CMDB/IRE-layer SAM reference |
| X1 | `ALT_PARALLELSWARM/final/DISCOVERY_INSERT_VS_UPDATE_GUIDE.md` |
| SB | sam-buffy KiloCode pack (rejected) |

---

## 1. Section-by-section verdicts

| # | Live section | Verdict | Finding / correction |
|---|---|---|---|
| 1 | Purpose | AGREE | Two-truths framing (owned vs observed) matches the install→model→entitlement pipeline `[S2][S4]` |
| 2 | SAM vs HAM vs ITAM | AGREE (with caveat) | Core record `alm_license` correct; "`alm_asset` (licenses)" shared-table wording is loose — entitlements live on `alm_license`, assets on `alm_asset` `[S4]` |
| 3 | Where to Find It | **CONFLICT** | Breadcrumbs use `All > Software Asset Management > …`. Actual paths: `Workspaces > Software Asset Workspace` and classic `All > Software asset > …` / `All > Software Asset > …` `[S12][S13][S35]`. Plugin tip wrong: `com.snc.sams` is Foundation, not Pro; Pro is `com.sn_samp_master_ws`/`com.sn_samp_master`/`com.snc.samp`; `com.snc.iam` is not a SAM component `[S1][S60]` |
| 4 | CIS-SAM exam alignment | AGREE (external) | Domain weights ~15/25/30/20/10 are curriculum-side data; DD coverage mapped in §4 below |
| 5 | SAM Lifecycle Diagram | AGREE | Request→Entitle→Discover→Reconcile→Optimize→Renew loop consistent with maturity stages `[S40]` |
| 6 | Three Record Types | **CONFLICT** | Four names right (`cmdb_software_product_model`, `cmdb_sam_sw_discovery_model`, `cmdb_sam_sw_install`, `alm_license`). **Usage table wrong:** `cmdb_sam_sw_usage` → official **`samp_sw_usage`** `[S61]`. **Recon result table wrong:** `sam_sw_reconciliation_result` → `samp_reconciliation_result` parent + three tiers `[S21][S43]` |
| 7 | Software Models & Normalization (SUMN) | **CONFLICT** | "SUMN (Software Usage and Normalization Mapping)" is **not** an official term; docs describe Content Library normalization via named daily jobs and rule families `[S11]`. Workflow itself agrees; "models extend `cmdb_model`" and `normalized_software_model` field are unverified `[GW UNVERIFIED]` |
| 8 | Entitlements | AGREE | Attributes and hygiene rules sound; "one entitlement per contract line" is practice guidance, not doc-verified. Docs add: PPN resolution scenarios, license-type impact (Perpetual+SA, Maintenance linking, Upgrade/Step-up), Microsoft Step-up only, Contractual duration needs dates `[S4][S64]` |
| 9 | Reconciliation — Core Engine | **CONFLICT** | "**default nightly**" is wrong — documented default is **weekly**, on demand available `[S20][S21]`. Steps otherwise align; results persist as three tiers, not a single mutable row `[S21]` |
| 10 | Compliance Positions Explained | PARTIAL | Docs publish exactly two statuses: **Compliant / Not Compliant** `[S18]`. Over/under/unlicensed/not-counted are analytical interpretations; "Unknown" handling (never report as compliant) is correct practice. Fleet adds unlicensed-installs/rights-needed columns as the operational signal `[S18][S63]` |
| 11 | Discovery & Data Sources | AGREE (broad) | Source taxonomy fine. Fleet specifics: base SAM patterns (Citrix XenApp/XenDesktop, VMware vCenter, MS SQL Server, Exchange, Oracle DB); SCCM plugins deprecated Tokyo → Service Graph connector; 3rd-party via `com.snc.samp.ire.datasource.integration` REST; Intune/Jamf are CMDB connectors, not native SAM sources `[S3][S57]` |
| 12 | SaaS License Management | AGREE (concept) | Subscription/consumption metric groups via `sn_sam_saas_int`; SaaS profiles auto-create reclamation rules; assign-seats-not-sign-ins rule is sound `[S1][S22]` |
| 13 | Optimization & Reclamation | AGREE | Priority order and 60–90 day window are good practice (window not a vendor default). Doc facts: reclamation types Total Usage Time / Last Used Date; flow timeout 30 days; suite parents pull components `[S22][S34][S61]` |
| 14 | Publisher-Specific Traps | AGREE | Traps directionally correct; fleet adds exact properties: Oracle `reconlevel`/host affinity; RHEL 3.2 ratio; Windows Server 4.59; SQL 0.25/1.25 ratios; IBM region/ILMT API `[S34]` |
| 15 | Re-usable Code / Metadata | **CURRICULUM-WRONG as OOB** | All four snippets are teaching illustrations using custom fields (`u_normalization_status`, `u_sam_status`, `u_license_metric_notes`) and the wrong recon-result table. Do **not** present as shipped logic; OOB BR behaviour is documented separately `[S2][S3][S60]` |
| 16 | Out-of-Box Features | PARTIAL | Accurate at feature level; missing the actual job/BR inventory (DD §2) and the true OOB roles/plugins list `[S1]` |
| 17 | Key Table Hierarchy | **CONFLICT** | Wrong: `cmdb_sam_sw_usage`, `sam_sw_reconciliation_result`, `license_metric_type` field, `compliance_state`. Correct set in DD §1.4. Guidance to verify via `sys_db_object.list` is appropriate `[S61][S21][S63]` |
| 18 | Integrations | AGREE (broad) | Fleet confirms Discovery, SCCM→Service Graph, SaaS connectors, ILMT, SAP; adds File Signature Normalization and IRE REST integration `[S1][S3][S57]` |
| 19 | Key Fields | **CONFLICT** | Several fields unverifiable/wrong: `normalized_software_model`, `license_metric_type`, `compliance_state`, `entitlement_count`/`install_count`. Verified field sets in DD §3.3/§5.2/§7.3 (Discovery Model, Install, LMR, Suggestion forms) `[S10][S33][S63]` |
| 20 | Goals, Benefits & Key Metrics | AGREE (indicative) | Targets explicitly indicative, not vendor SLAs — keep the label |
| 21 | Common Mistakes | AGREE | "Normalize first, then entitle" nuance: docs say discover **after** entitlements when PPN-driven models are wanted `[S3][S60]`; rest sound |
| 22 | Lab | AGREE | Nav paths need updating to workspace/classic paths above; otherwise a valid sequence |
| 23 | SLAs, Dashboards & Workspaces | **CONFLICT** | "Reconciliation run | nightly" wrong (weekly). Dashboard list generic; vendor-named dashboards in DD §6.3 |
| 24 | Quiz | AGREE (with fixes) | Q2/Q4 answers should cite three tiers and `samp_sw_usage`; otherwise fine |
| 25–27 | Resources / Memory Aids / Related | AGREE | Neutral study aids; no factual claims requiring correction |

---

## 2. Consolidated error register (curriculum → official)

| # | Live curriculum claim | Official / fleet finding | Evidence |
|---|---|---|---|
| E1 | Usage table `cmdb_sam_sw_usage` | **`samp_sw_usage`** (product-level; reclamation types Total Usage Time / Last Used Date) | `[S61]` GW WT3 |
| E2 | Reconciliation result `sam_sw_reconciliation_result` | **`samp_reconciliation_result`** parent; three tiers Product/Model/Metric Results (`samp_license_metric_result`) | `[S21][S43][S63]` |
| E3 | Reconciliation "default nightly" | **Weekly default**, on demand per publisher/group/subgroup | `[S20][S21]` GW WT3 |
| E4 | "SUMN" as product term | Not in official docs; Content Library + named normalize jobs | `[S11]` GW WT3 |
| E5 | Menus need `com.snc.sams` (Pro) + `com.snc.iam` | Foundation `com.snc.sams`; Pro `com.sn_samp_master_ws`/`com.sn_samp_master`/`com.snc.samp`; IAM unrelated | `[S1][S60]` |
| E6 | Sample BR writes `software_model` on install | BR matches discovered publisher+product+version to the **discovery model** | `[S2][S3]` |
| E7 | Breadcrumb root `All > Software Asset Management` | `Workspaces > Software Asset Workspace`; classic `All > Software Asset > …` / `All > Software asset > …` | `[S12][S13][S35]` |
| E8 | `license_metric_type` / `normalized_software_model` / `compliance_state` fields | Not confirmed in official corpus; mark UNVERIFIED or verify on instance | DD §13 |
| E9 | Six compliance-position states incl. "Unknown" | Two published statuses (Compliant / Not Compliant); unlicensed installs/rights needed are the unknown-exposure signals | `[S18][S63]` |
| E10 | Result fields `entitlement_count`/`install_count`/`usage_count` | `Rights owned`, `Rights used`, `Rights available`, allocation breakdown, `Rights needed` | `[S63]` |

**Never import from the sam-buffy pack** (wrong tables `alm_software`/`alm_software_installation`, wrong roles `sam_license_manager`/`sn_sam.admin`, wrong nav parent) — independently rejected by GW WT2 and DD.

---

## 3. What the curriculum gets right (and should keep)

- Two-truths reconciliation framing; ELI5 example.
- Record-type distinctions for the four core records.
- Entitlement hygiene (never overwrite quantity; maintenance ≠ licence; metric mismatch is silent).
- Compliance position semantics incl. "unknown ≠ compliant".
- Optimization priority order and the 60–90 day reclamation window (as practice).
- Publisher trap table (Oracle server-level licensing, IBM PVU/ILMT, SAP named users, MS SQL cores, Adobe VIP).
- Data-source taxonomy and dead-connector warning.
- Day-one report list, indicative KPI targets, lab structure, memory aids.

## 4. CIS-SAM domain map vs fleet coverage

| Domain (weight) | Live section(s) | Fleet coverage | Verdict |
|---|---|---|---|
| 1 Overview (~15%) | 1, 2, 3 | DD §1 mental model/tiers/roles; KS breadcrumbs | Covered; fix breadcrumbs/plugin tip |
| 2 Models/normalization (~25%) | 6, 7 | DD §3–§4 (statuses, five rule families, matching job, revert, suggestions) | Covered; fix usage table + SUMN wording |
| 3 Entitlements/reconciliation (~30%) | 8, 9, 10 | DD §3.4, §5.1–§5.2, §7.2 | Covered; fix cadence + result tables |
| 4 Optimization/reclamation/audit (~20%) | 12, 13, 14 | DD §5.3–§5.5 | Covered; add doc-named rule types and timeout |
| 5 Reporting/dashboards/integration (~10%) | 16, 18, 19, 23 | DD §6 (named dashboards + alert sources), §10 | Covered; replace generic dashboard list with named ones |

## 5. Recommended edits to the live guide (actionable)

1. Replace `cmdb_sam_sw_usage` → `samp_sw_usage` everywhere (sections 6, 7, 17, 19; quiz Q2).
2. Replace `sam_sw_reconciliation_result` → `samp_reconciliation_result` and add the three-tier hierarchy.
3. Change "default nightly" → "weekly default; on demand" (sections 9 and 23).
4. Remove "SUMN" branding or label it as community shorthand; keep Content Library terminology.
5. Fix the plugin tip: Foundation `com.snc.sams`; Professional `com.sn_samp_master_ws` (loads `com.sn_samp_master` + `sn_sam_workspace`).
6. Update breadcrumbs to the real navigation roots (workspace + classic variants).
7. Mark `license_metric_type`, `normalized_software_model`, `compliance_state`, `entitlement_count`/`install_count` as UNVERIFIED or replace with documented field sets.
8. Recategorize sample scripts as "illustrative, not OOB" and fix their table/field references.
9. Add a short pointer to the OOB job/BR inventory (DD §2) and parameter catalog (DD §7).

## 6. Fleet corroboration

Grok WT3 independently reached the same verdicts on E1–E4 (its "Names the exam curriculum got wrong" table). This double-derivation from separate agents against official docs makes the error register high-confidence. No fleet source disagrees with any correction above.

*Compiled 2026-11-13. Live target verified identical to repository `sam-guide.md` at fetch time.*
