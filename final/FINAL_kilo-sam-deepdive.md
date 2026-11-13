# FINAL — ServiceNow SAM Module Deep Dive

**Compiled by:** `kilo-sam-deepdive__kilo__cli` · **Branch:** `docs/sam-module-deep-dive`
**Date:** 2026-11-13 · **Release pin:** Brazil ITAM map, corroborated by Australia pages
**Contents:** the full operational deep dive (sections 0–13) followed by final thoughts and proposed additions to the live CIS-SAM curriculum page (sections 14–15).
**Companions:** `research/servicenow-sam/{SAM_MODULE_DEEP_DIVE.md, CURRICULUM_COMPARE.md, CURRICULUM_FINDINGS.md, FINAL_FEEDBACK.md}` and the agent folder `agents/kilo-sam-deepdive__kilo__cli/SNC_SAM__WT3/`.

---

# ServiceNow Software Asset Management (SAM) — Module Deep Dive & Configuration Reference

Agent: `kilo-sam-deepdive__kilo__cli` · Model Kilo (inherited) · Provider current-turn · Harness **Kilo CLI**
Date: 2026-11-13 · Release pin: **Brazil** ITAM map (pages updated Mar/Sep/Oct/Nov 2026), corroborated by **Australia** pages where labelled.
Evidence policy: every non-obvious claim carries `[S<n>]` → §12 source index. Exact table names, field names, property names and defaults are quoted from the fetched corpus, not from memory. No entitled instance was available; instance behaviour is **documented, not executed** — verify on your own instance before changing anything.

Scope: the SAM module (Professional / Foundation / SaaS LM) — shipped executable components, maintenance procedures for software models, the recurring license concerns every org hits, the workspaces and dashboards SAM teams live in, and a prioritized parameter inventory. The sibling CMDB/Discovery guide covers horizontal Discovery mechanics (Shazzam, classifiers, IRE identifiers/reconciliation); this guide covers the **SAM-side contract** that sits on top of it.

Structure mirrors `ALT_PARALLELSWARM/research/servicenow-discovery/DISCOVERY_END_TO_END_GUIDE.md`: mechanisms first, catalog second, troubleshooting/runbook last. The six operational themes requested are §§2–7 in the specified order.

---

## 0. Provenance & method

- **Corpus:** 58 Brazil ITAM article abstracts retained locally in `agents/grok-4.6__xai__kilo/SNC_SAM__WT1/research/raw/` (`[S1]`–`[S55]`), the Australia abstract set in `agents/beam__kilo__cli/SNC_SAM__WT1/research/` (`[S58]`), two committed consolidated references (`[S59]`, `[S60]`), and a community Path-to-Value digest kept strictly as corroboration (`[S56]`).
- **Method:** articles were fetched through the ServiceNow docs khub content API by the earlier swarm and are stored as stripped text; this worktree re-read every cited file and transcribed names verbatim. Nothing here is invented. Where the docs print two spellings, both are printed.
- **Known duplicate spellings preserved:** `samp_normalization_suggestion` (record-type article `[S14]`) vs `samp_normalization_suggestions` (Activity center alert source `[S43]`); `com.snc.samp.manage.published.product` (application property `[S32]`) vs `com.snc.samp.manage.published.products` (system property `[S30][S34]`); `com.snc.samp.ml.overrride_ml_model_version` with three r's `[S16]`.
- **Non-official names rejected:** `samp_discovered_model`, `samp_sw_entitlement`, `alm_software`, `alm_software_installation`, `sam_license_manager`, `sn_sam.admin`, and any `glide.cmdb.sam.*` family are **not** official SAM names — see §13.

---

## 1. Mental model and moving parts

### 1.1 The pipeline

```
Discovery / SCCM / Service Graph connector / SaaS integration / file signatures
        │ writes
        ▼
Software Installation   cmdb_sam_sw_install                       [S2][S3]
        │ business rule matches Publisher + Display Name + Version  [S2][S3]
        ▼
Software Discovery Model cmdb_sam_sw_discovery_model               [S2][S10]
        │ normalized vs SAM Content Library                        [S11]
        ▼
Software Model          cmdb_software_product_model               [S4][S9]
        │ entitled by                                              [S4]
        ▼
Software Entitlement    alm_license  →  rights / allocations      [S4][S27]
        │ reconciled weekly/on-demand                              [S20]
        ▼
License position · compliance results · removal candidates · true-up cost
```

| Thing | What it is | What it is not |
|---|---|---|
| Software **installation** | One discovered copy on one CI (`Installed on` = hardware CI) `[S33]` | A license; a catalog item |
| Software **discovery model** | De-duplicated *discovered string* (Publisher + Display Name + Version). **Cannot be created manually.** `[S2][S10]` | A purchasable model |
| Software **model** | Profile of purchased/available software (publisher, version criteria, discovery map) `[S4][S5]` | A catalog item until you publish it `[S49]` |
| Software **entitlement** | Rights purchased, linked to a software model `[S4]` | An install |
| Software **catalog item** | Requestable item in the Product Catalog `[S47][S48][S49]` | Automatic result of discovery |

### 1.2 Product tiers (name the tier on every control)

| Tier | Plugin | Notes |
|---|---|---|
| **Professional** (Brazil/Australia) | `com.sn_samp_master_ws` loads `com.sn_samp_master` + Workspace store app `sn_sam_workspace` in one step `[S1]` | Core plugin `com.snc.samp` is activated by ServiceNow personnel and may not appear in the plugin list `[S60]` |
| **Professional** (pre-Brazil) | `com.sn_samp_master` loads `com.snc.samp` + all publisher packs + `com.sn_samp_workbench` `[S1]` | Upgrading from `com.snc.software_asset_management` is **irreversible** `[S53]` |
| **Foundation / Basic** (ITSM) | `com.snc.sams` `[S57]` | Normalization statuses are only **Manually Normalized** and **New** — no Content Library auto-normalization `[S60]` |
| **SaaS License Management** | `sn_sam_saas_int` (Store; requires `com.snc.samp`) `[S1]` | Creates **subscriptions**, not classic installs |

### 1.3 Roles

| Role | Use | Contains `[S1]` |
|---|---|---|
| `sam_admin` | Full admin: import entitlements, reclamation rules, run reconciliation, custom products, pattern rules, Content Service setup | `sam_user`, `sam_spend_import`, `asset`, `model_manager`, `contract_manager` |
| `sam_user` | All features except admin | `pa_viewer`, `cmdb_read`, `report_user`, `sn_remote_dir_sync.reader` |
| `sam_developer` | Writes scripts on the platform (trained admins only) | `sam_admin` |
| `sam_integrator` | SaaS integration profiles | `sam_user`, `connection_admin`, `flow_operator` |
| `sam_spend_import` | Financial transaction import (Spend Detection) | `pa_viewer` |

Classic Software Model creation needs `sam_user` **or** `model_manager` `[S5]`; workspace normalization needs `sam_admin` or `sam_user` `[S13]`; custom products and pattern rules need `sam_admin` `[S6][S15]`; deleting installs needs `sam_developer` `[S23]`.

### 1.4 Tables you will touch

| Table | Label | Role |
|---|---|---|
| `cmdb_sam_sw_install` | Software Installation | Primary Discovery output; source of truth for current software data `[S1][S33]` |
| `cmdb_sam_sw_discovery_model` | Software Discovery Model | Match key Publisher + Display Name + Version; normalized values + status `[S2][S10]` |
| `cmdb_software_product_model` | Software Model | Purchased profile connected to entitlements `[S4]` |
| `alm_license` | Software Entitlement | Rights purchased; allocations reference it `[S4][S27]` |
| `samp_license_metric_result` | License Metric Results | Rights owned/used + allocation breakdown `[S21][S28][S63]` |
| `samp_sw_usage` | Software Usage | Product-level usage evidence for reclamation rules (Total Usage Time / Last Used Date); manual creation allowed; retiring or stealing the CI deletes related installs `[S61]` |
| `samp_product_result` | Product Results | Per-product compliance, true-up, over-license, savings `[S21][S43]` |
| `samp_reconciliation_result` | Reconciliation Result | Parent of the three result tiers `[S43]` |
| `samp_sw_reclamation_candidate` | Removal Candidate | Reclaim candidates with justification `[S43]` |
| `samp_normalization_suggestion` | Normalization Suggestion | Accept/reject predictions `[S14]` |
| `sam_sw_dedup_rule` | Custom Deduplication Rules | Product-level version-matching override `[S26]` |
| `samp_sw_downgrade_model` / `samp_downgrade_model` | Downgrade Rights | Deleted with the software model `[S4]` |
| `sam_sw_product_lifecycle` / `sam_custom_sw_product_lifecycle` | Product Lifecycle / Custom Product Lifecycle | Lifecycle reporting `[S5]` |
| `samp_sw_resource_value` | Resource Value | Custom metric 1:1 consumption math `[S28]` |
| `samp_job_log` / `samp_entitlement_import` / `samp_bulk_import` | Job Result / Import Error / Import | Operations monitoring `[S43]` |
| `cmdb_ci_hardware` | Hardware | Optional boolean column to exclude devices `[S29]` |
| `samp_vmware_license_key` / `samp_vmware_license_key_usage` | VMWare License Key / Usage | Populated by Discovery from Kingston `[S58]` |
| `samp_oracle_options` | Oracle Options | `Considered for licensing` eligibility `[S59]` |

Tables **not** used by SAM Pro: `cmdb_ci_spkg` (legacy pre-SAM packages; migrated by script) `[S58]`; `samp_discovered_model` / `samp_sw_entitlement` are **wrong names** `[S60]`.
---
## 2. Out-of-box scripts — the shipped executable components

ServiceNow does not publish a single "SAM scripts" reference page. The shipped logic is described across three article families: the plugin component list (`[S1]`), job references inside procedure articles (`[S3]`–`[S45]`), and the reconciliation upgrade note (`[S20]`). This section enumerates every shipped component the corpus names, with its type, trigger, table/field target, customization guidance and risk. Objects the docs do **not** enumerate (business-rule sys_ids, UI policies, ACLs) are covered by audit recipe in §2.8 rather than guessed.

### 2.1 How to find them on an instance

| What | Where | Filter |
|---|---|---|
| Scheduled jobs | `All > Scheduled jobs` | condition builder: **Name starts with SAM** `[S1]` |
| Roles & plugins | `All > System Applications > All Available Applications` / Plugins list | plugin ids in `[S1]`; core `com.snc.samp` may be hidden `[S60]` |
| Reconciliation script includes | Scope `com.sn_itam_samp` (Yokohama+) | `[S20]` |
| Flows / workflows | Flow Designer → All; classic Workflow → All | names not published — UNVERIFIED |
| Business rules / UI policies / ACLs | System Definition → Business Rules / System UI → UI Policies / System Security → Access Control (ACL) | not enumerated by docs — audit recipe §2.8 |

### 2.2 Master inventory — scheduled jobs

Columns: component · trigger/schedule · table(s) · fields written or read · customize? · risk if touched.

| # | Component | Type | Trigger / schedule | Table(s) | Fields written / read | Customize? | Risk |
|---|---|---|---|---|---|---|---|
| J1 | `SAM - Normalize discovery models using content library rules` | Scheduled job | Daily `[S11][S17]` | `cmdb_sam_sw_discovery_model`, `samp_normalization_suggestion` | Writes normalized Publisher, Product, Version, Edition (+ Platform/Language); sets Normalization status and Normalization date `[S11][S14]` | **Leave** — extend with pattern rules/custom products | Overlays or disables manual normalizations; auto-accept property then copies suggestion values `[S14]` |
| J2 | `SAM - Discovery Model Normalization job` | Scheduled job | Daily `[S11][S17]` | Dashboard trend charts (read-only over `cmdb_sam_sw_discovery_model`) | Reads normalization statuses | **Leave** | None material; dashboards go stale if disabled |
| J3 | `SAM - Daily Job` | Scheduled job | Daily `[S17][S43]` | Overview/normalization widgets prerequisite | Read | **Leave** | Widgets not populated until this and J1 have run `[S17]` |
| J4 | `SAM - Central Data Service Download Status` | Scheduled job | Daily `[S17]` | Content download related list | Current count, Expected count, Last updated on, Next action | **Leave** | Breaks CDS content-update monitoring |
| J5 | `SAM - Trigger Full Scan` | Scheduled job (health) | Weekly on content-service KPI categories `[S38]` | Health Check dashboard / scan findings | Health score, findings, recommendations | **Leave** (configure KPI categories instead) | Health checks stop refreshing; misconfigurations surface late |
| J6 | `SAM – Discovery Model to Software Model matching` | Scheduled job | Frequency not stated `[S9]` | `cmdb_sam_sw_discovery_model`, `cmdb_software_product_model` | Sets **Software model** reference on the discovery model; respects `Automatically matched = false` as a manual lock `[S9]` | **Leave** — influence via software-model version criteria and manual match | Overlaying overrides manual matches; duplicate software models appear if criteria are too loose |
| J7 | `SAM- Create downgrades/upgrades for a software entitlement` | Scheduled job | Weekly `[S60]` | `samp_sw_downgrade_model`, `samp_downgrade_model` | Downgrade rights records | **Leave** | Deleting a software model cascades to these tables `[S4]` |
| J8 | `Download software content: Downgrade Rights` | Scheduled job | Weekly `[S60]` | Content tables | Downgrade-right content | **Leave** | Stale downgrade rights after upgrades |
| J9 | `SAM - Deduplicate Install Table` | Scheduled job | Frequency not stated `[S24]` | `cmdb_sam_sw_install` | Sets **Active** = true/false; IBM special case prefers ServiceNow Discovery rows `[S24]` | **Leave** — configure `sam_sw_dedup_rule` for version-level policy `[S26]` | Wrong level inflates/deflates license counts; duplicates consume rights |
| J10 | `SAM — Adjust Installs for excluded CIs` | Scheduled job | Runs after the exclude flag changes `[S29]` | `cmdb_ci_hardware` (flag column named by property) → excludes installs from SAM | Exclude flag evaluation | **Leave** — set the property/column correctly | If the property names the wrong column, exclusion silently does nothing (or excludes everything) |
| J11 | `SAM - Label Spend Transactions` | Scheduled job | Frequency not stated `[S34]` | Spend transactions | Labels; attempts capped by `samp.spend_prediction_service.max_label_attempts` = 3 | **Leave** (Spend Detection scope) | Transaction labelling stalls after 3 attempts |
| J12 | Weekly reconciliation (job name not published) | Scheduled job | **Weekly default**; on demand per publisher/group/subgroup `[S20][S21]` | Creates `samp_reconciliation_result` → `samp_product_result`, software model results, `samp_license_metric_result`, removal candidates | Compliance status, rights owned/used, unlicensed installs, true-up cost, potential savings `[S18][S21]` | **Leave** — tune properties and custom metrics | Acting on first-run results as a purchase order is the classic anti-pattern `[S56]` |
| J13 | Entitlement import | Import Set / bulk import | On demand `[S4]` | `alm_license`, `samp_entitlement_import`, `samp_bulk_import`, `samp_sw_product_definition` | Creates entitlements, resolves PPNs/software models | Use provided templates; do **not** rewrite resolution logic | PPN errors (`PPN and SM not found`, `Multiple software models found…`) block rows `[S4]` |
| J14 | Migration: `Migrate Basic Software Asset Management software installations` | One-time migration script | Manual, post-upgrade | `cmdb_ci_spkg` → `cmdb_sam_sw_install` | Copies installs | Run once, verify counts, then retire | Re-running can duplicate installs; Foundation→Pro upgrade is irreversible `[S53]` |
| J15 | Content update downloads (CDS) | Scheduled/CDS jobs | Recurring | Content tables + `samp_ws_activity_center_items` alerts | Discovery models, lifecycles, PPNs/maps, processor names, exception rules, file signatures `[S16]` | **Leave** | Opting out degrades normalization hit ratios `[S16]` |

### 2.3 Documented business rule — the SAM double-write

The corpus names one shipped business rule explicitly (its sys_id and exact name are **not published**):

> When software install records are written to `cmdb_sam_sw_install`, a business rule verifies whether the unique combination of **discovered publisher, discovered product, and discovered version** exists in the Discovery Model table. If so, the reference to the discovery model is set on the install. If not, a new record is created in the Discovery Model table and that reference is set on the install. `[S2][S3]`

| Aspect | Behaviour |
|---|---|
| Trigger | Insert/update of `cmdb_sam_sw_install` (Discovery or SCCM writes) `[S3]` |
| Match key | Discovered publisher + discovered product + discovered version against `cmdb_sam_sw_discovery_model` `[S2]` |
| Insert path | No matching discovery model → create one, then point the install at it `[S2][S3]` |
| Update path | Matching discovery model → set `Discovery model` reference; install row updated `[S2]` |
| Exceptions | Names containing `Security Update` never create a discovery model `[S2]`; discovery models cannot be created manually `[S2]` |
| Customize? | **Never overlay.** This is the single highest-risk OOB object in SAM `[S60]` |
| Risk | Overlaying changes duplicate behaviour and breaks normalization matching; customization review is required on upgrade because the BR moves with the store app |

### 2.4 Reconciliation script includes (customization danger zone)

From Yokohama onward, **all reconciliation script includes moved from the family release into the SAM store application `com.sn_itam_samp`** (auto-activated with `com.sn_samp_master` or `com.snc.sams`) `[S20]`.

| Rule | Detail |
|---|---|
| If you customized reconciliation script includes pre-Yokohama | You **must move the customizations** to the new script includes on upgrade; old ones are deprecated `[S20]` |
| If you did not customize | Nothing to do; activation is automatic `[S20]` |
| Tuning lever today | Properties (`com.snc.samp.*`) and **custom license metrics**, not include edits `[S34][S28]` |
| Risk | Forked calculation logic drifts from publisher pack updates; upgrade path is manual and easy to miss |

### 2.5 Flows, workflows and request automation

The docs name reclamation/request flows but do not publish flow names or sys_ids (**UNVERIFIED**). What is documented:

| Flow | Trigger | Tables / effects | Source |
|---|---|---|---|
| Reclamation flow | Reclamation candidate lifecycle | Moves toward reclaim; error timeout property `sam_reclamation_flow_error_timeout` default **30 days** → Closed canceled `[S34]`; suite parents pull component usage automatically `[S22]` | `[S22][S34]` |
| Software request workflow (agentic: "Help manage software request") | Requested item approved + belongs to software category + not sourced + `Assigned to` not empty on `sc_req_item` `[S45]` | Auto-allocates from `alm_license` or creates a purchase order; Microsoft 365 license assignment agent needs SaaS LM + active M365 integration `[S45]` | `[S45]` |
| Reclaim Asset catalog request | User submits the catalog item | Creates request + tasks; `sam_user` closes tasks `[S44]` | `[S44]` |
| Automatic reclamation rule creation | Creating a direct SaaS integration profile or connecting an SSO app | A reclamation rule is created for the software product — **review it** `[S22]` | `[S22]` |

Flow names, sys_ids, and decision branches: **UNVERIFIED** — inspect Flow Designer → All on an entitled instance.

### 2.6 Plugin payloads that behave like scripts

| Plugin | Payload / effect | Source |
|---|---|---|
| `com.sn_samp_master_ws` | Loads Professional + Software Asset Workspace in one step; **after activation you cannot access the classic UI** `[S1][S35]` | `[S1][S35]` |
| `com.sn_samp_master` | Pre-Brazil bundle: Professional + all publisher packs + `com.sn_samp_workbench` `[S1]` | `[S1]` |
| `com.snc.file_signature_normalization` | Normalizes discovered file signatures while creating install records; **library file-signature rules beat custom file rules**; also activated with File-based Discovery `[S1][S60]` | `[S1][S60]` |
| `com.sn_sam_ml_normalization` | Real-time ML normalization of unrecognized software `[S60]` | `[S60]` |
| Publisher packs (`com.sn_samp_adobe`, `com.sn_samp_citrix`, `com.sn_samp_ibm`, `com.snc.samp.microsoft`, `com.snc.samp.oracle`, `com.sn_samp_sap`, `com.sn_samp_vmware`, `com.sn_samp_eng_app`) | Extra reconciliation capabilities and publisher-specific metrics `[S1]` | `[S1]` |
| `sn_sam_saas_int` | Subscription/consumption metric groups; SaaS profiles auto-create reclamation rules `[S1][S22]` | `[S1][S22]` |
| `com.snc.samp_usage_sccm` / `com.snc.samp.usage_sccm_2016` | SCCM usage data; **deprecated in Tokyo** — use Service Graph connector for Microsoft SCCM `[S1][S3]` | `[S1][S3]` |
| `com.snc.orchestration.client_sf_distribution` | Install/uninstall functionality; SAM Pro licence covers **uninstall/reclamation only** `[S1]` | `[S1]` |
| `com.snc.procurement` | Enables Purchase Orders related list on software model results `[S21]` | `[S21]` |
| `app-itam-procurement-integration` | Entitlement import errors/notifications from purchase receipts `[S43]` | `[S43]` |
| `sn_now_assist_sam` | AI agent collection for software requests `[S45]` | `[S45]` |
| `com.glide.domain.msp_extensions.installer` | Enables domain-specific SAM application properties `[S32]` | `[S32]` |
| `com.snc.pa_domain_support` | Domain separation for the Success portal `[S37]` | `[S37]` |

### 2.7 Customize-vs-leave matrix (summary)

| Component | Leave | Extend (safe) | Customize only with acceptance |
|---|---|---|---|
| Install→discovery-model BR | ✔ always | — | Never |
| Reconciliation script includes | ✔ | Custom license metrics, resource values | Move pre-Yokohama customizations only |
| Normalization jobs | ✔ | Pattern rules, custom products, wide-net/ML toggles | — |
| Matching job | ✔ | Software-model version criteria, manual match lock | — |
| Dedup job | ✔ | `sam_sw_dedup_rule` per product | — |
| Exclude-CI job | ✔ | Boolean column + property | — |
| Health scan | ✔ | KPI categories | — |
| Reclamation flow | ✔ | Reclamation rules, filters | Only as a last resort |
| Workspace/classic menus | ✔ | Related-list config on CI forms | — |

### 2.8 Audit recipe for unpublished objects (do this on your own instance)

The docs' component article lists only roles, plugins, scheduled jobs and demo data — it explicitly does **not** enumerate business rules, UI policies or client scripts `[S60]`. To inventory them without inventing names:

1. Scheduled jobs: `All > Scheduled jobs` → filter `Name starts with SAM` (count and compare to §2.2).
2. Business rules: System Definition → Business Rules; filter `Collection` by `cmdb_sam_sw_install`, `cmdb_sam_sw_discovery_model`, `cmdb_software_product_model`, `alm_license`. Record sys_ids before any upgrade.
3. UI policies / client scripts: System UI → UI Policies / Client Scripts; same table filters.
4. ACLs: System Security → Access Control (ACL); filter by those tables.
5. Script includes: System Definition → Script Includes; filter name prefix `samp`/`SAM`; reconcile against `com.sn_itam_samp`.
6. Flows: Flow Designer → All; export the list and record the ones triggered by SAM tables.

Mark all sys_ids **instance-specific**; only names/behaviour documented here transfer between releases.
---
## 3. Maintenance — add a new software model

A software model is created manually only when no entitlement/PPN path can create it: **no PPN available**, **PPN not in the Content Library**, or the product is a **custom/homegrown** product `[S5]`. Otherwise prefer the entitlement/PPN route (§3.4), which creates the model automatically and links it to rights in one step.

### 3.1 Prerequisites and roles

| # | Prerequisite | Table / where |
|---|---|---|
| 1 | Product exists in the Content Library **or** a custom product record exists (`Publisher` + `Product`; the pair is used during discovery-model normalization) | Custom product form `[S6][S7]`; product/publisher records `samp_sw_product` / `samp_sw_publisher` (`samp_sw_publisher` must relate to `core_company`) `[S60]` |
| 2 | Role: `sam_user` or `model_manager` (classic); workspace equivalent under License operations `[S5]` | Roles `[S1]` |
| 3 | If using version criteria: know whether installs arrive as 10.1 / 10.2 / … so the criterion (e.g. "Starts with 10") matches them `[S2]` | — |
| 4 | Optional: discovery map present in Content Library if you want installs matched automatically | `[S8]` |
| 5 | Optional: publisher pack installed for publisher-specific metrics | `[S1]` |

### 3.2 Step-by-step (classic path — field-level detail)

Navigate `All > Software Asset > Licensing > Software Models` → **New** `[S5]`.

| Step | Action | Table | Fields touched / notes |
|---|---|---|---|
| 1 | Fill in the software publisher details and Save | `cmdb_software_product_model` | Publisher, Product, Version criteria (e.g. `Starts with 10`), Edition, Platform, Language, Install condition. Version criterion is what discovery models match against — many discovery models may map to one model `[S2][S4]` |
| 2 | Suite designation (optional) | `cmdb_software_product_model` related lists | **Suite Parents** related list (add all software included with the suite) or **Suite Components** related list (add the parent suite). If a discovery map is attached and predefined suites exist, suite components are created automatically `[S5]` |
| 3 | Metric attributes | `cmdb_software_product_model` → **Metric Attributes** related list | Set the attribute value; entitlements with this publisher info automatically get the **Metric Group** populated, restricting license metrics to that publisher's set `[S5]` |
| 4 | Vendor catalog item (optional) | **Vendor Catalog Item** related list | Associates the model with a vendor item for catalog/publishing workflows `[S5]` |
| 5 | Client access (optional) | **Client Access** related list | Specifies number of devices/users accessing the software (used by Citrix/Oracle metrics) `[S5]` |
| 6 | Downgrade rights (optional) | **Downgrade Rights** related list | If a discovery map with downgrade rights is attached, rights populate automatically; downgraded versions appear hierarchically `[S5]`. Records live in `samp_sw_downgrade_model` / `samp_downgrade_model` and are deleted with the model `[S4]` |
| 7 | Product lifecycles (optional) | **Software Product Lifecycles** related list | Create/view `sam_sw_product_lifecycle` and `sam_custom_sw_product_lifecycle` records; based on publisher/product/edition/version attributes; view across all versions via **Show Product Lifecycles for all Versions** `[S5]` |
| 8 | Publish to service catalog (optional, self-service) | Related link **Publish to Software Catalog** → set Category = **Software** → OK | Makes the model requestable; catalog item currency follows `glide.model.catalog_item_currency` (default false = session currency) `[S5][S49]` |
| 9 | Review matching | Related link **Show Matching Discovery Models** | Shows discovery maps matching the model's publisher/product `[S5]` |

Then **Update** to save related-list changes `[S5]`.

Workspace equivalent: `Workspaces > Software Asset Workspace > License operations` (lists entitlements, software models, import errors, discovery models, subscriptions, contracts, IBM ASP/ILMT integrations) `[S36]`.

### 3.3 Field map — Software Model form (documented fields)

| Field | Meaning | Source |
|---|---|---|
| Publisher | Normalized publisher (from `samp_sw_publisher`) | `[S4][S5]` |
| Product | Product name (matches normalized discovery model Product) | `[S4]` |
| Version | Version criterion, e.g. exact or `Starts with 10` | `[S2]` |
| Edition | Edition of the purchased software | `[S4]` |
| Platform | Windows / macOS / UNIX | `[S10]` |
| Language | Dutch, English, French, German, Italian, Spanish (+ discovered additions) | `[S10]` |
| Install condition | When set, the matching job will not match this model to installs; auto-create then builds a model without the condition `[S9]` |
| Subscription condition / DB option | Block matching in the same way as install condition `[S9]` |
| Discovery map | Content Library map attached to the model | `[S8][S9]` |
| Created source | List-view column; value **System property** marks auto-created models (via the three auto-create properties) | `[S8]` |
| Automatically matched | On the **discovery model**, not the software model; `false` = manual lock the matching job respects | `[S9]` |

### 3.4 Entitlement side — creating/importing `alm_license`

Software entitlements record the rights purchased and link back to the software model `[S4]`.

**PPN and software-model resolution scenarios (import time)** `[S4]`:

| Scenario | System behaviour |
|---|---|
| **PPN blank, standard import** | 1) Exact match attempt on Publisher + Product + Version + Edition + Platform + Language → assign. 2) Relaxed search allowing any platform/language → assign, no error. 3) No match: if `com.snc.samp.automaticsmrcreation`-style auto-create is enabled **and** publisher + product identified → create model; else error record **`PPN and SM not found`** |
| **PPN blank, MLS import** | No fallback to other fields; row continues to downstream validation and usually fails at license-metric resolution |
| **PPN provided, exists in Content Library** | Exactly one software model → assigned. Multiple models → error **`Multiple software models found for the Publisher Part Number. Please choose a software model.`** |
| **PPN missing/inactive in Content Library** | Exact-only search on Publisher/Product/Version/Edition/Platform/Language. Found → PPN-not-found noted internally; entitlement created without PPN reference if no other errors. Not found → auto-create if enabled + standard import + publisher & product identified; else error `PPN and SM not found` |

Other documented entitlement constraints:
- **Microsoft:** if `License Duration` = Contractual, start and end dates are mandatory; the **Step-up** license type is Microsoft-only `[S4]`.
- Import errors land in `samp_entitlement_import`; bulk runs in `samp_bulk_import` `[S43]`.
- Entitlement state must reach **in use** (Publish) to be eligible for reconciliation `[S60]`.

### 3.5 What "insert" vs "update" means here

| Situation | Behaviour |
|---|---|
| First entitlement with a new PPN/model | Inserts `alm_license`; may insert `cmdb_software_product_model` via auto-create |
| Same PPN re-imported | Resolves to the existing model; updates the entitlement; multiple models for one PPN error out instead of guessing `[S4]` |
| Auto-create properties enabled and no model matches | New software model inserted (Created source = System property), created across versions for the edition — never against a specific version `[S8]` |
| Model matched but has an install condition | Treated as no match; a new model without the condition is auto-created `[S9]` |
| Model deleted | All related records in `samp_sw_downgrade_model` / `samp_downgrade_model` are automatically deleted `[S4]` |
| Manual software model edited | Normal reconciliation uses it; matching job keeps most-specific-wins unless a manual lock exists on the discovery model `[S9]` |
---
## 4. Maintenance — normalize a software model

"Normalize" in SAM means two distinct operations that are easy to conflate:

1. **Discovery-model normalization** — map the discovered string (`Discovered publisher/product/version`) to normalized Publisher/Product/Version/Edition using Content Library rules `[S11]`.
2. **Software-model matching** — attach the normalized discovery model to a purchased `cmdb_software_product_model` via the scheduled matching job `[S9]`.

Both must be right before reconciliation produces trustworthy license positions. This section covers both plus the reclassification loop when they go wrong.

### 4.1 Normalization process and statuses

When a new discovery model enters the CMDB, normalization compares discovered values against the **SAM Content Library** and writes matches into the normalized columns of `cmdb_sam_sw_discovery_model` `[S11]`:

- Normalized **Publisher** — e.g. discovered `Microsoft Corp` → `Microsoft` `[S11]`
- Normalized **Product**, **Version**, **Edition** `[S11]`
- Normalized **Platform** (Windows / macOS / UNIX), **Language**, **Full version** `[S10]`

Statuses on `cmdb_sam_sw_discovery_model.Normalization status` `[S2][S10]`:

| Status | Meaning | Can be manually normalized? | Can be reverted? |
|---|---|---|---|
| `New` | Not yet run through normalization | Yes (classic/workspace) | n/a |
| `Normalized` | Full publisher+product+version match (or publisher+product for Not Licensable/Child/Driver/Patch types) | — | Yes → `Match Not Found` |
| `Partially Normalized` | Publisher+product matched; version editable | Yes | Yes → `Match Not Found` |
| `Publisher Normalized` | Publisher only | Yes | Yes → `Match Not Found` |
| `Match Not Found` | Nothing matched | Yes | n/a |
| `Manually Normalized` | Operator filled values or accepted a suggestion | — | **No** |
| Pattern-rule normalized | Normalized by a pattern rule | — | **No** |

Revert also **resets fields to their original unnormalized values and deactivates rules associated with the discovery model** `[S12]`. Foundation/Basic instances only ever see **Manually Normalized** and **New** `[S60]`.

### 4.2 Rule families (the SAM analog of IRE's four)

| Family | Scope | Notes | Source |
|---|---|---|---|
| **Product Map / Package Map** | One rule per **distinct discovery model** (even minor differences get separate rules) | Created/maintained by ServiceNow Content Service | `[S11]` |
| **Pattern normalization** | One rule covering **many models** sharing a data pattern (e.g. all `Microsoft Office 2019*` → Microsoft Office) | Customizable by you via Pattern Normalization Rules | `[S11][S15]` |
| **Enhanced pattern normalization** | Complex edition/version variants using include/exclude terms and conditional mapping (`standard`, `STD`, `stand` → Standard) | Presence/absence of terms decides coverage | `[S11]` |
| **Wide-net normalization** | Similar discovered field values normalized together, reducing one-rule-per-model volume | Only certain products eligible (set by Content Service); property `com.snc.samp.wide_net_normalization.enabled` default enabled; applies only to models not fully normalized by content rules | `[S11][S34]` |
| **Machine-learning normalization** | Real-time predictions for unrecognized software | Plugin `com.sn_sam_ml_normalization`; property `com.snc.samp.enable.ml_normalization` default enabled; only after content rules fail | `[S60][S34][S11]` |

Ordering (as documented): content rules first; wide-net then ML handle leftovers `[S60]`.

### 4.3 Manual normalization procedures

**Workspace** `[S13]`:
1. `All > Software asset > Software Asset Workspace > License operations > Discovery models`
2. Select a record whose status is `Partially Normalized`, `Publisher Normalized`, or `Match Not Found`
3. Ellipsis icon → **Normalize**
4. Status becomes `Manually Normalized` (`sam_admin` or `sam_user`)

**Classic** `[S12]`:
1. `All > Software Asset > Discovery > Discovery models`
2. Open a record with one of the three statuses above
3. Fill `Publisher`, `Product`, `Version` as appropriate (custom product selectable from the Product lookup)
4. Save → status `Manually Normalized`
5. Optional: **Revert Normalization**

Editing normally read-only fields (or changing Product type) also flips status to `Manually Normalized` `[S2][S10]`.

### 4.4 Normalization suggestions

Suggestions are created for **every manually normalized discovery model**, and also during the weekly normalization pass whenever values differ from Content Service predictions (or even when they match) `[S14]`.

| Action | Effect `[S14]` |
|---|---|
| Accept | Publisher, Product, Version, Edition, Platform, Language copied from the suggestion; status `Manually Normalized` → `Normalized`; suggestion status → Accepted; Normalization date updated |
| Reject | Manually normalized values retained; status stays `Manually Normalized`; suggestion status → Rejected |
| Auto-accept | Property `com.snc.samp.auto_accept_normalization_suggestion` (enabled by default) accepts automatically when there are no differences. Domain-separated environments can override per domain via a new `sys_application_property` value record |

Records live in `samp_normalization_suggestion` (Activity center labels the same object `samp_normalization_suggestions`) `[S14][S43]`. A caution icon next to `Normalization status` opens the suggestion `[S10]`.

### 4.5 Software-model matching (the second half of "normalize")

Scheduled job **`SAM – Discovery Model to Software Model matching`** `[S9]`:

1. For each normalized publisher + normalized product pair in `cmdb_sam_sw_discovery_model`, fetch software models with matching publisher and product.
2. If the software model has **no install condition, subscription condition, or DB option**, compare normalized publisher, product, edition, version.
3. On match, write the **Software model** reference onto `cmdb_sam_sw_discovery_model`.
4. Most-specific model wins; otherwise the most generic `[S9]`.
5. If a matching model has an **install condition**, it is skipped; auto-create then creates a model without the condition `[S9]`.

**Manual override:** set the desired software model on the discovery model form. The `Automatically matched` column becomes **unchecked**, and the job will not override it on later runs `[S9]`.

**Version rounding note:** exact match is searched first; if none, round down to major version (`8.0.4` → `8.0`) `[S2]`.

### 4.6 Pattern normalization rule — create and apply

Navigate `All > Software Asset > Administration > Pattern Normalization Rules` → New (role `sam_admin`) `[S15]`.

| Field | Purpose |
|---|---|
| Name | Unique rule name |
| Discovered publisher contains | Text to search for in the discovered publisher field |
| Discovered product contains | Text to search for in the discovered product field |
| Discovered publisher is empty | Applies the rule where publisher is unknown |
| Active | Enables/disables the rule |
| Normalized Attributes → Publisher / Product / Edition / Product type / Version / Platform / Language | Values written to the normalized columns |

Then click **Apply Rule** to normalize applicable discovery models immediately `[S15]`. Create custom products/companies **before** writing rules that reference them `[S15]`.

### 4.7 Custom products and content-service consolidation

Custom product form fields `[S6][S7]`: `Publisher`, `Product`, `Subscription software`, `Product type` (Child / Driver / Licensable / Not Licensable / Patch / Unknown), `Product classification` (UNSPSC), `Exclude from content service`, `Active`.

If Content Service is opted in and `Exclude from content service` is **off**, the platform `[S7]`:
1. Automatically creates and sends a content request to ServiceNow
2. After approval + next content update, maps the library product to your custom product
3. Generates a **product suggestion** to consolidate; accept replaces all references with the library product, reject keeps the custom product

Exclusion flags also exist on the **Software Discovery Model** and **Custom Part Number** forms `[S16]`.

### 4.8 Reconciliation and reclassification steps

**What reconciliation uses from normalization** `[S60]`:
- Only discovery models with Product type **Licensable** are considered
- **License under management** must be selected
- Matching consumes normalized Publisher/Product/Version/Edition/Platform/Language

**Reclassification loop when a model was matched wrong:**

| Step | Action | Where |
|---|---|---|
| 1 | Identify wrong matches (caution icon = suggestion exists; `Show Matching Discovery Models`) | Discovery model form `[S10][S5]` |
| 2 | Fix at the source: correct the discovery model's normalized values, or edit/replace the software model's version criterion | `[S12][S5]` |
| 3 | Or lock a specific software model manually and let `Automatically matched = false` protect it | Discovery model form `[S9]` |
| 4 | Revert an incorrect automatic normalization (Normalized/Partially/Publisher → Match Not Found) if the values themselves were wrong | Classic form `[S12]` |
| 5 | Wait for (or trigger) the matching job to re-point discovery models at the corrected software model | §4.5 |
| 6 | Re-run reconciliation; verify license position changed accordingly | `[S20][S18]` |
| 7 | If Product type was changed (e.g. Not Licensable → Licensable), status becomes `Manually Normalized` and reconciliation scope changes | `[S10]` |

**Reclassification risks:** changing product type re-scopes compliance (Not Licensable rows vanish from license positions); reverting resets rules associated with the discovery model; manual locks survive but hide future better matches — review locked models quarterly.
---
## 5. High-probability items — the recurring concerns every org must handle

These are the four items that appear in every SAM operating cadence, plus the stale/duplicate hygiene that keeps them honest. Each subsection names its exact tables and fields.

### 5.1 License position

**Report:** Software Asset Management **License Position report** — compliance details for each software model in a single list; viewable/exportable `[S18]`.

Source tables: `samp_product_result` (product-level) and `samp_license_metric_result` (metric-level) `[S43][S28]`.

| Field on the License Position list | Meaning `[S18]` |
|---|---|
| Software publisher / Software product / Edition / Version | Model identity |
| Software model status | `Compliant` (green dot) or `Not Compliant` (red dot) |
| License metric | Metric driving the result |
| Total spend | Total cost of rights owned |
| Rights owned | Sum of all active rights |
| Rights used | Rights allocated in use + not allocated in use |
| Rights needed | Rights needed to cover unlicensed installs |
| Rights available | Rights owned − rights used |
| Unlicensed installs | Installs not covered by any entitlement |
| True-up cost | Estimated remediation cost based on least rights needed |
| Potential savings | Estimated savings from reclaiming unused installs |
| Over-licensed amount | Cost of unused rights |
| Software model | Model name |
| Group / Subgroup | Reconciliation grouping dimensions |

**Multi-report behaviour** `[S18]`:
- A model with two entitlements (perpetual SA + subscription) produces **two license metric results**, one with `Active maintenance = true` and one `false` → two license position reports.
- Any unlicensed installations → one report; any unlicensed subscriptions → one report; both present → two reports.

**Operational rule:** "Unknown" is not "compliant" — un-normalized or unmatched rows surface as unknown/unlicensed until fixed. Never present an unknown position as clean.

### 5.2 Compliance reconciliation

**Cadence:** weekly scheduled job by default; **on demand** per publisher or all publishers, with group/subgroup scoping `[S20][S21]`. Group/subgroup values: country, department, company, region, cost center; defaults set via `com.snc.samp.recon.group` / `.subgroup` (both None by default) `[S34]`.

**Three result tiers** `[S21]`:

```
samp_reconciliation_result
   └─ Product Results            samp_product_result
        ├─ Software Model Results
        │    ├─ License Metric Results   samp_license_metric_result
        │    └─ Remediation Options
        ├─ Licensed Installs
        ├─ Unlicensed Installs           (SAP: Unlicensed Users / Unlicensed Engines)
        ├─ Unlicensed Subscriptions      (subscription software)
        └─ Removal Candidates
```

| Tier | Created when | Related lists |
|---|---|---|
| Product Results | Always for licensable products after recon, even without defined software models `[S21]` | Software Model Results, Licensed Installs, Unlicensed Installs, Unlicensed Subscriptions, Removal Candidates |
| Software Model Results | Only when a software model or entitlement exists for the product `[S21]` | License Metric Results, Remediation Options, Licensed Installs, Unlicensed Installs, Unlicensed Subscriptions, Unlicensed Consumptions, Unlicensed Options (Oracle), Removal Candidates, Purchase Orders (needs `com.snc.procurement`) |
| License Metric Results | Per license metric on the model; multiple results possible (multiple licences purchased) `[S21]` | Rights Used By (not for IBM RVU), Licensed Installs, Installs Used (SAP: System Users), Downgrades/Upgrades, Licensed Subscriptions, Cloud Special Rights (AWS/Azure only) |

**License Metric Results allocation fields** `[S63]`: Rights owned, Rights used, Rights available, Over-licensed amount; right allocations = **Allocated in use**, **Not allocated in use**, **Allocated not in use**, **Not allocated**, **Allocations needed** (Per Named User/Device only). When *Not allocated in use* > 0 the platform auto-creates the **Create Allocations** and **Remove Unallocated Installs** remediation options (except User CAL/Device CAL); when *Allocated not in use* > 0 it creates **Remove Allocations**. **Nontransferable rights** apply only to Microsoft Per Core / Per Core with CAL (leftover core-pack rights). Related lists: **Rights Used By** (`Used by`, `Rights used`, cloud `Cloud Provider`/`Dual Use Rights Applied`/`Host Type`/`Edition Flexibility Applied`), **Rights Needed By**, **Licensed Installs**, **Downgrades/Upgrades**, **SAP System Users** (named-user metrics), **Licensed Subscriptions**. Two license metric results are generated when a model has perpetual-SA and subscription entitlements (Active maintenance true/false) `[S18][S63]`.

**Remediation options** available from Software Model Results `[S21][S27]`:
- Create allocations / remove allocations (lock or free license assignment)
- Remove unallocated installs
- Remove unlicensed installs
- Create purchase order for new licences (with procurement plugin)

**Compliance statuses:** `Compliant` vs `Not Compliant` `[S18]`. Entitlement types Enterprise/ULA/ELA/ETLA/SCE stay compliant even with unlicensed installs `[S60]`.

Where to view: Core UI `All > Software Asset > Reconciliation > Historical Results`, or Workspace `License usage` → publisher card → Product Results `[S21]`. Simplified triage in the **License Workbench** view; single-list view in the **License Position** report `[S20]`.

### 5.3 Reclamation

Reclamation rules aggregate usage over time and flag rights that are allocated but under-used or unused `[S22]`.

| Rule type | Measures | Default? |
|---|---|---|
| Total Usage Time | Aggregate hours used in the period | Yes |
| Last Used Date | Most recent usage date | No |
| Peak Concurrent Usage | Engineering apps | No |
| Active Transaction Codes | SAP | No |

Usage evidence is tracked at **product level** (not version/edition) in `samp_sw_usage`; records can be created manually from third-party or SCCM integrations (`sam_admin`/`sam_user`) with `Publisher`, `Product`, `Configuration Item`, `User`, plus either monthly metering data (`Month`, `Year`, `Usage count`, `Total seconds used`) or a `Last used time` `[S61]`. When the CI Status/Hardware Status becomes Retired or Stolen, installs related to that CI are deleted `[S61]`. Core UI entry is inactive while the Software Asset Workspace is active.

**Tables/fields:**
- Removal candidates: `samp_sw_reclamation_candidate` (state, active, justification, cost) `[S43]`
- Actual savings: sum of potential savings in a month of **Closed complete** removal candidates `[S43]`
- Reclamation flow timeout: `sam_reclamation_flow_error_timeout` = 30 days → Closed canceled `[S34]`

**Suite behaviour** `[S22]`: adding a suite parent pulls component usage automatically; components cannot be edited/deleted while attached (edit/delete the parent instead); filter conditions on the parent apply to children and become read-only on children. Products/processes update with Content Service changes.

**SaaS/SSO:** creating a direct integration profile or connecting an SSO app **auto-creates a reclamation rule** — review it before relying on it `[S22]`. Upgrading to Brazil does **not** convert old rules to bulk reclamation; delete and re-add the product to trigger automatic component addition `[S22]`.

**Catalog reclaim request** `[S44]`: Service Catalog → search "Reclaim asset" → fields `Requested by`, `Requested for`, `Employee separation`, `Asset`, `Reclaim date`, `Reclaim method`, `Legal hold method`, `Notes/Special instructions`; `sam_user` closes the resulting tasks.

### 5.4 True-up cost

True-up cost is estimated from the **least number of rights needed** `[S18]`:

| Input | Behaviour `[S19]` |
|---|---|
| License cost **or** license+maintenance cost specified on the software model | Used for true-up calculations |
| Neither specified | Falls back to the **average software entitlement cost** — can materially misstate true-up |
| Entitlement created via a license metric | An **Override License Cost** related-list record is created if none exists for that metric, with license cost and license+maintenance cost set to zero; maintenance licences may override either value |
| Oracle Employee metric | True-up shown for a one-year subscription period |

**License types change reconciliation behaviour** `[S64]` — load entitlements with the right type:

| License type | Reconciliation impact |
|---|---|
| Perpetual | Indefinite use; no maintenance benefits until SA/maintenance entitlements are linked |
| Perpetual + Software Assurance | Microsoft; SAM auto-applies SA benefits (new-version rights, mobility, unlimited virtualization) |
| Perpetual + Maintenance | Non-Microsoft (Oracle, VMware); SAM auto-applies maintenance benefits |
| Subscription | Compliance driven by user subscriptions pulled from portals (Jira, M365, Adobe CC) |
| Software Assurance / Maintenance alone | **Not reconciled unless linked to a base perpetual licence** — link them |
| Upgrade / Step-up / Subscription Step-up | Edition upgrades without a new full licence; use the **Upgraded Entitlements** tab on the entitlement |
| Add on / From SA | Microsoft 365 transition USLs; must be linked to a perpetual Office legacy licence with active SA |

**Publisher traps that distort true-up** `[S60]`:
- Oracle core-factor / aggregation (`com.snc.samp.oracle.reconlevel` ESX vs ESX cluster vs vCenter(s))
- IBM PVU/RVU math and ILMT dependency
- SAP named-user definitions
- Microsoft SQL Server core-to-core ratios and Software Assurance step-ups
- Suites roll up (counting components and parent double-counts rights)

### 5.5 Duplicate and stale-data hygiene

| Concern | Mechanism | Tables/fields |
|---|---|---|
| Duplicate installs across sources (Discovery + SCCM) | One install row per source per publisher/product/version/edition; `SAM - Deduplicate Install Table` marks one **Active** = true (IBM special case prefers ServiceNow Discovery rows) | `cmdb_sam_sw_install.Active` `[S24]` |
| Wrong version-matching level | Custom dedup rule with Version Level Exact/Major/Any + Stale Record Threshold (Days); product must already be a normalized `cmdb_software_product_model` row | `sam_sw_dedup_rule` `[S26][S25]` |
| Uninstalled software retained | REST Table API query then DELETE per sys_id | `cmdb_sam_sw_install` `installed_on`, `publisher`, `version`, `product` `[S23]` |
| Devices out of scope | Boolean column on Hardware (e.g. `u_exclude_from_sam`) named in `com.snc.samp.exclude_device_flag`; `SAM — Adjust Installs for excluded CIs` enforces | `cmdb_ci_hardware` `[S29]` |
| Missing discovery models | Names containing `Security Update` never create models (missing rows, not duplicates) | `[S2]` |
| Auto-created models you did not intend | Three auto-create properties; check **Created source** = System property in the Software Model list | `cmdb_software_product_model` `[S8]` |
| Reconciliation counts inflated | Dedup job + exclude flag + removal of uninstalled installs before trusting license positions | §5.2 |

**Operating rhythm:** dedupe before each reconciliation; exclude-CI flag reviewed at scope changes; uninstalled-install cleanup after decommission waves.
---
## 6. Key workspaces & dashboards — where SAM teams work daily

### 6.1 Software Asset Workspace (primary, Brazil+)

Entry: `Workspaces > Software Asset Workspace` `[S36]` or `All → Software asset → Software Asset Workspace` `[S60]`. Activating the Workspace **hides** classic menus for features that moved; several admin menus stay classic-only `[S35]`.

| View | What it is for | Source |
|---|---|---|
| **Software asset overview** | Landing page: create entitlements, run reconciliation, key metrics, alerts/notifications, time-sensitive actions | `[S36][S43]` |
| **License usage** | Publisher compliance status, reconciliation results, reclaim unused software, run/view reports | `[S36][S21]` |
| **License operations** | Entitlements, software models, import entitlement errors, discovery models, user subscriptions, engineering applications data, contracts, IBM ASP/ILMT integrations | `[S36]` |
| **Software asset analytics** | Consolidated dashboards: SaaS, discovered inventory, optimization, lifecycle management, cloud cost simulator, Engineering License, normalization and content | `[S36]` |
| **Success portal** | Success goals, health checks, value builder tasks, maturity items | `[S36][S37]` |
| **Renewals calendar** | Entitlements and contracts nearing expiry or expired | `[S36]` |
| **Overlapping usage** | Feature-level usage of SaaS and SSO applications | `[S36]` |
| **Content Library portal** | Data stored in the SAM Content Service | `[S36]` |

Key sub-paths used in procedures:

| Path | Purpose | Source |
|---|---|---|
| License operations > Discovery models | Manual normalize / review | `[S13]` |
| License operations > Content > Custom software products | Create custom products | `[S7]` |
| Administration > Deduplication rules | Create dedup rules | `[S26]` |
| SAM Implementation > Published products | Phase-wise scope freeze | `[S30][S31]` |
| Success portal > Health check | Run scans | `[S39]` |
| Software asset analytics > Normalization and content | Trend charts | `[S17]` |
| License usage > License Metrics Result > Licenses Required By | Allocation verification (`Is Virtual`, `Allocated in use`, `Not allocated in use`, `Allocation`) | `[S27]` |
| License Operations > Licensing > Software entitlements > Device Allocations | Manual host/VM allocation | `[S27]` |

### 6.2 Classic menus that remain classic-only (even after Workspace activation) `[S35]`

`Software Asset Demand` (Create New, Demands, Demand Requirement), Administration (**Custom Products**, **Custom part Numbers**, **Custom License Metrics**, Software Asset Demand Actions, **Pattern Normalization Rules**, **Reclamation Rules**, Job Results, Content Service Setup, Refresh Processor Definitions, Migrate Software Results, Properties, Revert Customizations, Software Model with De-activated Discovery Maps), SaaS License (Unrecognized Subscription Identifier, SSO Integration Profiles, Direct Integration Profiles), SAP Compliance and Optimization (SAP Connections, Connection Setup, Scheduled Import, Transform History).

Other classic entry points still referenced by docs: `All > Software Asset > Administration > Properties` `[S34]`, `All > Software Asset > Discovery > Discovery models` `[S12]`, `All > Software Asset > Licensing > Software Models` `[S5]`, `All > Software Asset > Reconciliation > Historical Results` `[S21]`, `All > Product Catalog > Catalog Definition > Vendor Items` `[S47][S48]`, `All > Product Catalog > Product Model > All Models` `[S49]`.

### 6.3 Named dashboards and reports (with source tables)

| Dashboard / report | Where | Widgets / content | Source table(s) | Source |
|---|---|---|---|---|
| **Software asset overview dashboard** | Workspace > Software asset overview | Publishers out of compliance; Products out of compliance; Over-licensed amount; Expiring maintenance and subscription; Total true-up Cost; Top 5 publishers true-up cost; Potential Savings; Actual savings; Software Spend; Software installs normalization status; End of life products | `samp_product_result`, `alm_license`, `samp_sw_reclamation_candidate`, `samp_license_metric_result`, `cmdb_sam_sw_discovery_model`, `sam_sw_product_lifecycle` | `[S43]` |
| **Normalization and content dashboard** | Workspace > Software asset analytics > Normalization and content | Percentage of normalized installs; Software installs normalization status donut; Central Data Service Download Status related list | `cmdb_sam_sw_discovery_model`; CDS fields: Name, Current count, Expected count, Last updated on, Next action | `[S17]` |
| **Health Check dashboard** | Success portal > Health check | Scan findings + recommendations, downloadable reports | KPI categories from Content Service | `[S38][S39]` |
| **Success portal** | Workspace > Success portal | SAM maturity; Completed success goals; Total success savings; Projected savings; All goals by status (Draft, In Progress, Pending Review, Completed, Canceled); Health checks passed; Completed value builder tasks; Open activities | Success goals/activities; domain-separated with `com.snc.pa_domain_support` | `[S37]` |
| **License Position report** | Report inside SAM | One row per software model with rights/spend/unlicensed/true-up/savings/over-license | `samp_product_result`, `samp_license_metric_result` | `[S18]` |
| **License Workbench** | Workspace > License usage (publisher license overview) | Colour-coded compliance banner; financial calculations on cards; per-user publisher pinning; sort/filter; navigation tree (publisher → product → model → metric); tabs **All Publishers**, **Publishers Out of Compliance**, **Pinned Publishers** | `samp_product_result`, `samp_license_metric_result` | `[S62]` |
| **Software Lifecycle Report** | Analytics | Products nearing end of life with install count > 0; drill to installs | `sam_sw_product_lifecycle_report` | `[S43]` |
| **CMDB success advisor for SAM** | Activity center alert "Review CMDB data quality" | Software install data-quality metrics + remediation actions; scope via Edit dashboard scope | `samp_ws_activity_center_items` | `[S43]` |
| **Renewals calendar** | Workspace | Entitlement/contract expiries within 90 days | `ast_contract`, `alm_license` | `[S43]` |
| **Overlapping usage** | Workspace | SaaS/SSO feature-level overlap | SaaS subscription records | `[S36]` |

### 6.4 Activity center alerts and notifications (daily ops surface)

Alerts requiring `sam_admin`: Scheduled jobs failed; Last content download failed. Table of sources `[S43]`:

| Alert / notification | Source table |
|---|---|
| Removal candidates identified | `samp_sw_reclamation_candidate` |
| New normalization suggestions | `samp_normalization_suggestions` |
| Unrecognized subscription identifiers | `samp_sw_unrecognized_subscription_identifier` |
| New software request | `sc_request` |
| Last reconciliation failure / completed | `samp_reconciliation_result` |
| Scheduled jobs failed | `samp_job_log` |
| Entitlement import errors | `samp_entitlement_import` |
| New entitlement import error via purchase receipts | `samp_entitlement_import` (+ procurement integration) |
| Last content download failed | `asset_job_log` |
| Failed/completed entitlement import | `samp_bulk_import` |
| New CPE normalization suggestion | `sn_samp_vr_cpe_mapping_suggestion` |
| Renewals coming up in 90 days | `ast_contract`, `alm_license` |
| New SSO applications identified last week | `samp_sso_application` |
| Products nearing end of life | `sam_sw_product_lifecycle_report` |
| New PPNs added to the library | `samp_sw_product_definition` |
| Software asset demands approved | `samp_demand` |
| New entitlement created via purchase receipts | `alm_license` |
| Review CMDB data quality | `samp_ws_activity_center_items` |

### 6.5 Roles needed per screen

| Screen | Role | Source |
|---|---|---|
| Normal manual normalize | `sam_admin` or `sam_user` | `[S13]` |
| Custom products / pattern rules / dedup rules / published products / properties | `sam_admin` | `[S6][S7][S15][S26][S30][S34]` |
| Classic software model create | `sam_user` or `model_manager` | `[S5]` |
| Delete installs | `sam_developer` | `[S23]` |
| View reconciliation results | `sam_user` | `[S20][S21]` |
| Maturity item changes | `sam_admin` (view: `sam_user`) | `[S41]` |
| SaaS profiles | `sam_integrator` | `[S1]` |
| Property edit (wide-net/ML/billing) | admin role | `[S34]` |
| Catalog publish from product model | `catalog_admin`; vendor items | `model_manager` | `[S47][S48][S49]` |
---
## 7. Parameter inventory

Two layers, deliberately separated:

- **§7.2 — must-consider parameters:** the ~20 settings that decide whether SAM is trustworthy at go-live. Review these first.
- **§7.3 — full per-screen parameter list:** every documented field/property grouped by the screen or form where you set it, including pack-specific tunables.

All properties are set under `All > Software Asset > Administration > Properties` unless a different screen is named `[S34]`. Where the docs print only a display name, the programmatic name is marked UNVERIFIED rather than guessed.

### 7.2 Must-consider parameters (prioritized)

**Tier 0 — decide before go-live (wrong values produce wrong license positions immediately):**

| Property | Default | Effect if wrong | Guidance |
|---|---|---|---|
| `com.snc.samp.automaticsmrcreation` | Off (opt-in) | Auto-created software models in non-compliant state for licensable unlicensed products; pollutes the model list | Leave **off** during Crawl; enable only when you want unlicensed counts on the License Position report `[S8][S34]` |
| `com.snc.samp.automaticsmcreation` | No | Auto-creates models for not-licensable products (APM use) | Enable only for APM scope `[S8][S34]` |
| `com.snc.samp.unlicensed_smr_creation` | False | Controls software-model results for unlicensed models | Set True only if you need result rows for unlicensed software `[S8][S34]` |
| `com.snc.samp.manage.published.products` | false | Phase-wise scope: reports/dashboards show only published products | Enable for staged rollouts; remember to re-run recon after changes `[S30][S34]` |
| `com.snc.samp.exclude_device_flag` | empty | Names the Boolean column on `cmdb_ci_hardware` that excludes devices from SAM | Set before first reconciliation or excluded devices skew compliance `[S29][S34]` |
| Content Service opt-in | Not opted in | Without it, Match Not Found volume stays high; normalization hit ratios suffer | Opt in unless data-sharing policy forbids it; reversible `[S16]` |
| `com.snc.samp.recon.group` / `com.snc.samp.recon.subgroup` | None | Reconciliation grouping dimensions; group and subgroup must differ | Choose Company/Cost Center/Country/Department/Region based on CI attribute quality `[S34]` |

**Tier 1 — tune during stabilization:**

| Property | Default | Effect | Guidance |
|---|---|---|---|
| `com.snc.samp.auto_accept_normalization_suggestion` | Enabled | Auto-accepts suggestions when no differences exist | Keep enabled; review per-domain overrides in domain-separated instances `[S14]` |
| `com.snc.sam.auto_suite_inference` | false | Maps installs to suite entitlements automatically | Enable when suites matter for compliance `[S34]` |
| `com.snc.samp.recon.enablecustommetrics` | Yes | Applies custom license metrics in reconciliation | Set No only to debug metric effects `[S34]` |
| `com.snc.samp.debug` | No | Recon + on-prem import debug logging | Enable temporarily; performance impact `[S34]` |
| `sn_sam_workspace.sam_license_operations_list_count` | 5,000,000 | List count cap on License operations view | Lower for very large estates to keep UI responsive `[S34]` |
| `sam_reclamation_flow_error_timeout` | 30 days | Reclamation flow moves to Closed canceled after timeout | Align with operating cadence `[S34]` |

**Tier 2 — publisher-pack specific (only when the pack is active):**

| Property | Default | Pack | Effect |
|---|---|---|---|
| `com.snc.samp.oracle.reconlevel` | ESX cluster | Oracle | Aggregation level for Oracle/WebLogic on VMware: ESX, ESX cluster, vCenter(s) |
| `com.snc.samp.oracle.hostaffinityenabled` | opt-in | Oracle | VM-host affinity rules at vCenter(s) level |
| `com.snc.samp.citrix.app.license.period` | 90 | Citrix | License period (days) considered in reconciliation |
| `com.snc.samp.eng.app.peak.usage.period` | 30 | Engineering Apps | Peak usage consumption window (days); `sam_admin` only |
| RHEL Virtual Datacenters threshold | 3.2 | IBM | Ratio to choose RHEL Server vs Virtual Datacenters; programmatic name UNVERIFIED |
| `com.snc.samp.windowserver.license.threshold` | 4.59 | Microsoft | Windows Server Datacenter vs Standard cost ratio |
| `com.snc.samp.sqlserver.standard_sa.to.enterprise_sa.cost.ratio` | 0.25 | Microsoft | SQL Standard SA vs Enterprise SA cost ratio |
| `com.snc.samp.ms.sa.to.nonsa.cost.ratio` | 1.25 | Microsoft | SA vs non-SA cost ratio |
| `sn_samp_ibm_lic.default_region` | North America and South America | IBM (+IBM License Compliance app) | Default region for physical hosts |
| `sn_samp_ibm_lic.ilmt_api_version` | version picker | IBM | ILMT/BigFix API version used for connection |
| `com.snc.samp.use_lifecycle_approximation` | enabled | — | Include approximate lifecycle dates in the lifecycle report |
| `com.snc.samp.generate.calculated.lifecycles` | opt-in | — | Calculate EOS/EOES/EOL from lifecycle averages |
| `com.snc.samp.sam_ci_billing_threshold` | 30 | Cloud Insights | Age after which cloud billing data is stale for SQL-on-AWS licence typing |
| `samp.spend_prediction_service.max_label_attempts` | 3 | Spend Detection | Label attempts before giving up on a transaction |
| `com.snc.samp.ml.overrride_ml_model_version` | override | ML | Alternate ML prediction model version; admin write access only; spelling as printed |
| `com.snc.samp.wide_net_normalization.enabled` | enabled | — | Wide-net fallback for models content rules could not normalize |
| `com.snc.samp.enable.ml_normalization` | enabled | ML | ML fallback after content rules |
| `com.snc.samp.recon.max_workers` | unset | — | Parallel publisher jobs during reconciliation |
| `com.snc.samp.ire.datasource.integration` | — | 3rd-party IRE | Enables REST writes into `cmdb_sam_sw_install`; role `sam_developer` |
| `glide.model.catalog_item_currency` | false | Catalog | true = model currency on catalog items; false = user session currency |

### 7.3 Full per-screen parameter list

#### A. Administration > Properties (SAM properties page) `[S34]`

Every property documented on the Brazil page, with its documented description (abridged) and default. This is the canonical reconciliation/defaults screen.

| Property | Default | Description |
|---|---|---|
| `com.snc.samp.recon.group` | None | Default Group for the weekly reconciliation run: Company, Cost Center, Country, Department, Region |
| `com.snc.samp.recon.subgroup` | None | Secondary grouping; except None, group ≠ subgroup |
| `com.snc.samp.recon.enablecustommetrics` | Yes | Apply custom license metrics in reconciliation |
| `com.snc.samp.debug` | No | Debug reconciliation results and on-premise import logging (performance impact) |
| `com.snc.samp.automaticsmrcreation` | opt-in | Auto-create software models for licensable unlicensed products |
| `com.snc.samp.automaticsmcreation` | No | Auto-create software models for not-licensable products (APM) |
| `com.snc.samp.unlicensed_smr_creation` | False | Create software-model results for unlicensed products |
| `com.snc.samp.exclude_device_flag` | empty | Name of true/false column on `cmdb_ci_hardware` excluding devices from SAM |
| `com.snc.samp.citrix.app.license.period` | 90 | Citrix licence period (days) |
| `sam_reclamation_flow_error_timeout` | 30 | Days before a reclamation error goes to Closed canceled |
| `com.snc.samp.eng.app.peak.usage.period` | 30 | Engineering peak usage period (days) |
| `com.snc.samp.recon.max_workers` | unset | Parallel reconciliation scheduled jobs |
| `com.snc.samp.oracle.reconlevel` | ESX cluster | Oracle/WebLogic aggregation on VMware |
| `com.snc.samp.oracle.hostaffinityenabled` | opt-in | Host-affinity accounting at vCenter(s) |
| `com.snc.samp.wide_net_normalization.enabled` | enabled | Wide-net normalization fallback |
| `com.snc.samp.enable.ml_normalization` | enabled | ML normalization fallback |
| `com.snc.samp.sam_ci_billing_threshold` | 30 | Stale cloud-billing-data threshold (days) |
| RHEL Virtual Datacenters threshold | 3.2 | RHEL licence-type optimization ratio |
| `com.snc.samp.windowserver.license.threshold` | 4.59 | Windows Server Datacenter/Standard cost ratio |
| `sn_samp_ibm_lic.default_region` | North America and South America | Default IBM host region |
| `sn_samp_ibm_lic.ilmt_api_version` | picker | ILMT/BigFix API version |
| `com.snc.samp.sqlserver.standard_sa.to.enterprise_sa.cost.ratio` | 0.25 | SQL SA cost ratio |
| `com.snc.samp.ms.sa.to.nonsa.cost.ratio` | 1.25 | MS SA/non-SA cost ratio |
| `com.snc.samp.use_lifecycle_approximation` | enabled | Approximate lifecycle dates in reports |
| `com.snc.samp.generate.calculated.lifecycles` | opt-in | Calculated EOS/EOES/EOL |
| `com.snc.samp.manage.published.products` | false | Phase-wise published-product reporting |
| `samp.spend_prediction_service.max_label_attempts` | 3 | Spend labelling attempts |
| `com.snc.sam.auto_suite_inference` | false | Suite inference from child models |
| `sn_sam_workspace.sam_license_operations_list_count` | 5,000,000 | License operations list count cap |

#### B. Application Properties (per-domain overrides) `[S32]`

Screen: `All > Software Asset Management > Administration > Application Properties` → Application Property Values related list. Requires `com.glide.domain.msp_extensions.installer`.

| Field | Values |
|---|---|
| Value | `true` / `false` |
| Domain | Target domain |

Documented uses: `com.snc.samp.manage.published.products` (as application property `com.snc.samp.manage.published.product`) and Oracle reconciliation properties (`com.snc.samp.oracle.reconlevel`, `com.snc.samp.oracle.hostaffinityenabled`) per domain `[S32][S34]`. `sys_application_property` value records also carry `auto_accept_normalization_suggestion` overrides `[S14]`.

#### C. Custom Software Product form `[S6][S7]`

`Publisher`, `Product`, `Subscription software`, `Product type` (Child/Driver/Licensable/Not Licensable/Patch/Unknown), `Product classification` (UNSPSC), `Exclude from content service`, `Active`.

#### D. Pattern Normalization Rule form `[S15]`

`Name`, `Discovered publisher contains`, `Discovered product contains`, `Discovered publisher is empty`, `Active`, Normalized Attributes: `Publisher`, `Product`, `Edition`, `Product type`, `Version`, `Platform` (Windows/macOS/UNIX), `Language` (Dutch/English/French/German/Italian/Spanish). Related link **Apply Rule**.

#### E. Deduplication rule form `[S26]`

`Product`, `Active`, `Version Level` (Major version / Exact version / Any), `Stale Record Threshold (Days)`.

#### F. Discovery Model form `[S10]`

`Display name`, `Normalization status`, `Publisher`, `Product`, `Version`, `Discovered publisher`, `Discovered product`, `Discovered version`; Additional Information: `Product type`, `Platform`, `Language`, `Edition`, `Full version`, `Exclude from content service`. Related list **Software Installation**: Display name, Publisher, Version, Installed on.

#### G. Software Installation form `[S33]`

Header: `Display name`, `Discovery model`, `Publisher`, `Version`, `Edition Override`.
Installation tab: `Prod id` (deprecated), `Install location`, `Install date`, `Revision` (deprecated), `Instance key`, `Installed on`, `Uninstall string`, `ISO serial number`.
Reconciliation tab: `Entitlement` (deprecated), `Inferred suite`, `Omit from suites`.

#### H. Normalization Suggestion form `[S14]`

`Discovery model`, `Suggestion status`, `Discovered publisher/product/version`, `Suggested publisher/product/version/edition/platform/language`, normalized `Publisher/Product/Version/Edition/Platform/Language`.

#### I. Maturity item details `[S42]`

`Name`, `Type` (Process/End user/SaaS/Data center/Cloud), `Short description`, `Success goal`, `State` (New/Work in Progress/Closed Complete/Closed Skipped), `Maturity level` (Crawl/Walk/Run), `Suggested maturity level`, `Start date`, `Completed date`, `Purpose`, `Steps to complete`, `Work notes`.

#### J. Reclaim Asset catalog request `[S44]`

`Requested by`, `Requested for`, `Employee separation`, `Asset`, `Reclaim date`, `Reclaim method`, `Legal hold method`, `Notes/Special instructions`.

#### K. Software Model form + related lists `[S5]`

Fields as §3.3. Related lists: **Suite Parents**, **Suite Components**, **Metric Attributes**, **Vendor Catalog Item**, **Client Access**, **Downgrade Rights**, **Software Product Lifecycles**. Related links: **Publish to Software Catalog**, **Show Matching Discovery Models**, **Show Product Lifecycles for all Versions**.

#### L. Software Entitlement (`alm_license`) documented fields `[S4]`

`Publisher Part Number` (PPN), `License metric`, `License type`, `Purchased rights`, `License Duration` (Contractual requires start/end), `Step-up` (Microsoft-only), plus allocation-related lists (**Device Allocations**, **User Allocations**) and the **Override License Cost** related list `[S19][S27]`.

#### M. License Metric Results / allocation fields `[S21][S27]`

Rights owned, rights used, allocated in use, not allocated in use, allocated not in use, licenses required by, rights needed, rights available; allocations live in `alm_entitlement_user` / `alm_entitlement_asset` (the metric picks one list, not both) `[S60]`.

#### N. Hardware exclusion `[S29]`

Boolean column on `cmdb_ci_hardware` (example `u_exclude_from_sam`), default false; its name is entered in `com.snc.samp.exclude_device_flag`.

#### O. CI related-list configuration `[S58]`

Computer CI form → Configure → Related Lists → add **Software Installation → Installed on** → Save. Post-SAM, update any legacy related lists/reference fields that pointed at `cmdb_ci_spkg`.

### 7.4 Prioritization summary

| When | Set |
|---|---|
| Before first discovery run | Content Service opt-in; exclude-device flag; auto-create properties off; published-products decision |
| Before first entitlement import | PPN strategy; software-model version criteria; metric attributes/metric groups |
| Before first reconciliation | Group/subgroup; custom metrics toggle; dedup rules; normalize + match backlog cleared |
| Weekly ops | Re-run recon after publishing/removing products; review removal candidates; job-result review |
| Never edit directly | OOB business rules, reconciliation script includes, normalization jobs, matching job logic |

### 7.5 Undocumented-property caveat

The official pages do not publish an exhaustive numeric catalog of every `Application Property`; some values surface only inside the running instance `[S59]`. Audit `sys_properties` filtered by `nameLIKEcom.snc.samp%` / `samp.%` / `sn_sam_%` and compare against this list before changing anything in production.
---
## 8. Discovery feed and CI/license insertion-update rules

### 8.1 Sources that write `cmdb_sam_sw_install`

| Source | Plugin / mechanism | Notes | Source |
|---|---|---|---|
| ServiceNow Discovery | Discovery plugin required; patterns can be customized | Base system patterns used by SAM include Citrix XenApp, Citrix XenDesktop, VMware vCenter, Microsoft SQL Server, Microsoft Exchange Server, Oracle Database `[S3]` | `[S3]` |
| Microsoft SCCM 2012 v2 / 2016 | `com.snc.integration.sccm2012v2` / `com.snc.integration.sccm2016`; usage plugins `com.snc.samp_usage_sccm` / `com.snc.samp.usage_sccm_2016` | **Deprecated in Tokyo** — new work uses Service Graph connector for Microsoft SCCM; 2016 plugin supports SCCM 1606/1906/1910/2002 `[S1][S3]` | `[S1][S3]` |
| SaaS License Management | `sn_sam_saas_int` | Subscriptions/consumption rather than classic installs; profiles auto-create reclamation rules `[S1][S22]` | `[S1][S22]` |
| File Signature Normalization | `com.snc.file_signature_normalization` (also with File-based Discovery) | Matched files write `cmdb_sam_sw_install`; library file-signature rules beat custom ones `[S1][S60]` | `[S1][S60]` |
| IBM ILMT / BigFix Inventory | IBM publisher pack; v2 APIs preferred | Region defaults via `sn_samp_ibm_lic.*` `[S34][S60]` | `[S34][S60]` |
| Third-party via IRE REST | `com.snc.samp.ire.datasource.integration`, role `sam_developer` | Payload keys `publisher`, `version`, `display_name` (+ optional edition); parent CI identified by `name`; send `sys_class_name` so the CI is not reclassified; uninstalls must be DELETEd via Table API `[S57][S60]` | `[S57][S60]` |
| Manual delete | REST Table API | Query `installed_on=<ci_sys_id>` then DELETE per sys_id; `sam_developer` `[S23]` | `[S23]` |

Intune/Jamf are Service Graph CMDB connectors, not native SAM install sources `[S60]`.

### 8.2 Insert-vs-update decision matrix (SAM scope)

| Incoming event | Match key | Insert if | Update if | Control that can stop insert |
|---|---|---|---|---|
| Software install written by a source | Discovered Publisher + Product + Version against `cmdb_sam_sw_discovery_model` `[S2][S3]` | No matching discovery model → create model + set reference | Model exists → set reference on install `[S2][S3]` | Name contains `Security Update` → no model `[S2]`; exclude-device flag `[S29]` |
| Install from a second source | Same key, different source | Duplicate install row allowed; dedup job marks Active | Active flag changes after dedup run | `sam_sw_dedup_rule` version level; dedup Active=false excludes from recon `[S24][S26]` |
| Discovery-model normalization | Content Library / pattern / wide-net / ML | Normalized columns written | Status transitions | Revert rules; manual lock via pattern/manual status `[S12]` |
| Discovery model → software model | Version/edition/language/platform/install condition | Auto-create property enabled and no match | Existing model matched; most specific wins | Install condition blocks match; manual `Automatically matched=false` `[S9]` |
| Entitlement import | PPN or Publisher+Product+Version+Edition+Platform+Language `[S4]` | New entitlement/model | PPN resolves to existing model | Multiple models for PPN error; MLS blank-PPN has no fallback `[S4]` |
| Catalog item publish | Vendor item / product model | Publish/link creates catalog item | Vendor-item edits sync after publish | Do not publish; different roles (`model_manager` vs `catalog_admin`) `[S47][S48][S49]` |

### 8.3 Duplicate-prevention layers

1. Discovery-model primary key + version rounding `[S2]`
2. `Security Update` exclusion `[S2]`
3. Content Service recognition quality (opt-in) `[S16]`
4. Dedup job + custom dedup rules `[S24][S26]`
5. Exclude-device flag `[S29]`
6. Uninstall cleanup via REST `[S23]`
7. Reconciliation result tiers exposing unlicensed/duplicate counts `[S21]`

### 8.4 CMDB-layer governance that also touches software installs (cross-reference)

SAM's install-level business rule is the primary gate for `cmdb_sam_sw_install`. When software data enters through CMDB integrations rather than SAM-native Discovery, the four IRE mechanisms still apply to the CI payload: **Identification Rule** (`cmdb_identifier` + `cmdb_identifier_entry`), **IRE Data Source Rule** (`cmdb_ire_data_source_rule`, insert-only gate), **Reconciliation Rule** (static `cmdb_reconciliation_definition` / dynamic `cmdb_dynamic_reconciliation_definition`, update-only attribute authority), and **Data Refresh Rule** (staleness-based refresh). Insert is never gated by reconciliation; blocked inserts raise `INSERT_NOT_ALLOWED_FOR_SOURCE` (parked partial under `CreateOrUpdateCIEnhanced()`). Full decision logic, precedence rules and traps: sibling repo `ALT_PARALLELSWARM/final/DISCOVERY_INSERT_VS_UPDATE_GUIDE.md` `[X1]` and the CMDB-focused SAM reference on branch `kilo/sam-module-config-reference` `[X2]`.

---

## 9. Order of operations

### 9A. Setup sequence (implementation)

1. Healthy CMDB + discovery coverage first (maturity Crawl: establish healthy CMDB, identify tools, processes, roles) `[S40][S60]`.
2. Install SAM from Product Hub (guided) or Store `[S51]`; activate `com.sn_samp_master_ws` (or `com.sn_samp_master`) `[S1]`.
3. Request/activate optional plugins: publisher packs, SaaS LM, ML normalization, spend detection `[S1]`.
4. Assign roles (`sam_admin`, `sam_user`, `sam_integrator`, `sam_developer` only to trained admins) `[S1]`.
5. Opt in to Content Service (default off) `[S16]`.
6. Wire discovery sources (Discovery patterns; SCCM via Service Graph connector for new work) `[S3]`.
7. Load entitlements before discovery where you want PPN-driven models first `[S60][S3]`.
8. Let daily jobs normalize discovery models `[S11]`.
9. Clear the Match Not Found backlog: custom products, pattern rules, manual normalization `[S6][S7][S15]`.
10. First reconciliation; review product/software-model/metric results and remediation options `[S20][S21]`.
11. Phase-wise published products (enable `com.snc.samp.manage.published.products`, add products, re-run recon) `[S30]`.
12. Reclamation rules; catalog onboarding for requestable software (Run stage) `[S22][S40]`.
13. Success portal: goals, health checks, maturity items `[S37]`.

### 9B. Runtime pipeline (one installation)

1. Source writes `cmdb_sam_sw_install` `[S3]`.
2. Business rule matches/creates `cmdb_sam_sw_discovery_model` (Publisher + Display Name + Version) `[S2]`.
3. Daily normalization assigns status; wide-net then ML handle leftovers `[S11][S60]`.
4. Matching job attaches normalized discovery models to software models `[S9]`.
5. Dedup job sets Active flags (IBM priority case) `[S24]`.
6. Weekly/on-demand reconciliation computes compliance, license positions, removal candidates `[S20][S18]`.
7. Remediation actions (allocations, remove installs, purchase orders) `[S21][S27]`.
8. Reclamation flow reclaims unused rights `[S22]`.
9. `SAM — Adjust Installs for excluded CIs` enforces scope `[S29]`.
10. Dashboards/alerts reflect latest results `[S43]`.

---

## 10. Verification, health and observability

| Check | Where | Frequency | Source |
|---|---|---|---|
| Normalization status distribution | Software asset overview → normalization status widget | Daily | `[S43]` |
| Normalization trend charts | Analytics > Normalization and content (after J1+J3 run) | Daily | `[S17]` |
| Content download freshness | Central Data Service Download Status related list (Name/Current count/Expected count/Last updated on/Next action) | Daily | `[S17]` |
| Reconciliation success/failure | Activity center alert/notification; `samp_reconciliation_result` | Weekly | `[S43]` |
| Scheduled job failures | Activity center → `samp_job_log` (sam_admin) | Weekly | `[S43]` |
| Entitlement import errors | Activity center → `samp_entitlement_import` | Per import | `[S43]` |
| Health score | Success portal > Health check > Execute Scan > View result (Scan Findings) | Ad hoc/weekly full scan | `[S38][S39]` |
| Removal candidates | Activity center → `samp_sw_reclamation_candidate` | Weekly | `[S43]` |
| License position | License Position report export | After each recon | `[S18]` |
| Job Results table | `All > Software Asset > Administration > Job Results` (`samp_job_log`) | Ops | `[S59]` |

Health-check suites shipped in the corpus: SQL Server Config, SQL Server CMDB, Windows Server CMDB, Windows Server Config, Oracle Database, Java - Oracle, WebLogic Server - Oracle, Microsoft 365, General `[S38]`.

---

## 11. Anti-patterns and troubleshooting

### 11.1 Anti-patterns

| # | Anti-pattern | Why it hurts | Source |
|---|---|---|---|
| 1 | Treating a discovery model as a catalog item or a licence | Wrong object layer; reconciliation ignores catalogs | `[S60]` |
| 2 | Running discovery before entitlements when PPN-driven models were wanted | Match Not Found backlog; manual rework | `[S60]` |
| 3 | Editing OOB reconciliation script includes instead of using properties/custom metrics | Forked logic; upgrade deprecation | `[S20]` |
| 4 | Enabling auto-create properties during Crawl | Software-model table fills with non-compliant auto rows | `[S8][S56]` |
| 5 | Rolling out all publishers on day one | Scope explosion; datacenter packs are Walk-stage | `[S40][S56]` |
| 6 | Skipping Content Service opt-in | Match Not Found stays high; hit ratios suffer | `[S16]` |
| 7 | Overlaying the install→discovery-model business rule | Breaks SAM's double-write contract | `[S60]` |
| 8 | Publishing to the software catalog with the wrong role (`model_manager` vs `catalog_admin`) | Publish link missing or wrong ownership | `[S47][S48][S49]` |
| 9 | Assuming Workspace activation keeps classic navigation | Classic-only menus hide; admins get lost | `[S35]` |
| 10 | Acting on the first reconciliation as a purchase order | Data-quality loop skipped; over-buying | `[S56]` |
| 11 | Both SSO and a direct SaaS integration on the same app | Double-counted subscriptions/reclamation | `[S56]` |

### 11.3 Runbook — SAM go-live week (condensed)

1. **CMDB ready:** installs can land on CIs; owner/location/department/cost center present for recon grouping `[S60]`.
2. **Plugins:** `com.sn_samp_master_ws` active; publisher packs scoped; Workspace confirmed; classic-only menus bookmarked `[S1][S35]`.
3. **Content Service:** opted in (unless policy forbids); sharing toggles reviewed `[S16]`.
4. **Scope controls:** exclude-device Boolean + property; published-products decision; auto-create properties off `[S29][S30][S8]`.
5. **Discovery:** schedule runs; base patterns verified (SQL/Exchange/Oracle/Citrix/vCenter); SCCM via Service Graph connector if needed `[S3]`.
6. **Entitlements:** PPN strategy set; import template tested on a small batch; errors triaged in `samp_entitlement_import` `[S4][S43]`.
7. **Normalize:** wait for daily jobs; clear Match Not Found via custom products/pattern rules/manual normalize `[S11][S6][S15]`.
8. **Match:** confirm discovery models attached to software models; manual locks only where intended `[S9]`.
9. **Reconcile:** weekly job or on-demand; review three tiers; do not treat first run as a bill `[S20][S21][S56]`.
10. **Operate:** removal candidates, renewals calendar, health scan, success goals `[S43][S37]`.

### 11.2 Troubleshooting matrix

| Symptom | Likely cause / first check | Source |
|---|---|---|
| Every install creates a new discovery model | Business rule broken/overlaid; Security Update exception; check primary key fields | `[S2][S60]` |
| Discovery models stuck at Match Not Found | Content Service not opted in; no pattern rules; product not in library | `[S16][S60]` |
| Manually normalized values disappear after next run | Pattern-normalized or auto-accept suggestion overwrote them; manual/pattern statuses cannot revert | `[S12][S14]` |
| Software model never attached | Install/subscription condition/DB option blocking; version criterion too strict; matching job not scheduled | `[S9]` |
| Two models for one product | Auto-create ran while a close model existed; multiple PPNs resolve differently | `[S4][S60]` |
| Licences counted twice on a device | Dedup not configured; version level mismatch (Exact vs Major); check Active flags | `[S25][S26]` |
| Excluded devices still counted | Property names the wrong column; job not run since flag change | `[S29]` |
| True-up cost implausibly low/high | No licence cost on model → average entitlement cost used; override records zeroed | `[S19]` |
| Reports show unpublished products | `com.snc.samp.manage.published.products` disabled, or recon not re-run after publishing change | `[S30]` |
| Reconciliation shows Unknown positions | Normalization/product-type/License-under-management prerequisites unmet | `[S60]` |
| "PPN and SM not found" on import | Blank PPN + auto-create off, or MLS import without PPN fallback | `[S4]` |
| "Multiple software models found…" | Ambiguous PPN mapping; pick the correct model manually | `[S4]` |
| Uninstalled installs inflate rights | Cleanup not performed; use REST DELETE per CI | `[S23]` |
| Health scan findings won't clear | Underlying config issue persists; re-run after fixing tasks | `[S39]` |
| Workspace menus missing after activation | Classic-only features moved; use classic paths in §6.2 | `[S35]` |
---
## 12. Source index

All Brazil articles were fetched via the ServiceNow docs khub content API (ITAM map) by `grok-4.6__xai__kilo` on 2026-11-13 and are retained verbatim in `agents/grok-4.6__xai__kilo/SNC_SAM__WT1/research/raw/`. Pages print **Release version: Brazil** unless noted; update dates are listed. Australian corroboration comes from `agents/beam__kilo__cli/SNC_SAM__WT1/research/` and the two committed consolidated references. Copies of every cited file are mirrored in `research/servicenow-sam/sources/` so this guide is self-contained.

| ID | Title | Release / updated | Local file |
|---|---|---|---|
| S1 | Components installed with Software Asset Management Professional | Brazil, Sep 10 2026 | `raw/components_installed_sam_pro.txt` |
| S2 | Discovery models and software installations | Brazil, Sep 10 2026 | `raw/discovery_models_and_installs.txt` |
| S3 | Software discovery | Brazil, Sep 10 2026 | `raw/software_discovery.txt` |
| S4 | Software models and software entitlements | Brazil, Sep 10 2026 | `raw/software_models_and_entitlements.txt` |
| S5 | Create software models in SAM classic | Brazil, Sep 10 2026 | `raw/create_software_models_classic.txt` |
| S6 | Add a custom software product in SAM classic | Brazil, Nov 5 2026 | `raw/add_custom_software_product_classic.txt` |
| S7 | Add custom software products in workspace | Brazil, Sep 10 2026 | `raw/add_custom_software_products_workspace.txt` |
| S8 | Automatic creation of software models | Brazil, Jul 31 2025 | `raw/automatic_creation_of_software_models.txt` |
| S9 | Software model relationship to software installation | Brazil, Sep 10 2026 | `raw/model_relationship_to_install.txt` |
| S10 | Discovery models fields | Brazil, Sep 10 2026 | `raw/discovery_models_fields.txt` |
| S11 | Software normalization | Brazil, Sep 10 2026 | `raw/software_normalization.txt` |
| S12 | Manually normalize a software discovery model in SAM classic | Brazil, Sep 10 2026 | `raw/manually_normalize_classic.txt` |
| S13 | Manually normalize a software model in the Software Asset Workspace | Brazil, Sep 10 2026 | `raw/manually_normalize_workspace.txt` |
| S14 | Normalization suggestions for discovery models | Brazil, Sep 10 2026 | `raw/normalization_suggestions.txt` |
| S15 | Add a software pattern normalization rule | Brazil, Nov 5 2026 | `raw/add_software_pattern_normalization_rule.txt` |
| S16 | Software Asset Management Content Service | Brazil, Sep 10 2026 | `raw/sam_content_service.txt` |
| S17 | Normalization and content dashboard | Brazil, Sep 10 2026 | `raw/normalization_and_content_dashboard.txt` |
| S18 | Software license compliance position | Brazil, Sep 10 2026 | `raw/license_compliance_position.txt` |
| S19 | Accurately reporting your software true-up cost | Brazil, Sep 10 2026 | `raw/true_up_cost.txt` |
| S20 | Software reconciliation for compliance | Brazil, Sep 10 2026 | `raw/software_reconciliation_for_compliance.txt` |
| S21 | Software reconciliation results | Brazil, Sep 10 2026 | `raw/software_reconciliation_results.txt` |
| S22 | Software reclamation rules | Brazil, Sep 10 2026 | `raw/software_reclamation_rules.txt` |
| S23 | Delete uninstalled software from the Software Installation table | Brazil, Sep 10 2026 | `raw/remove_uninstalled_software.txt` |
| S24 | Duplicate software installations in SAM | Brazil, Sep 10 2026 | `raw/duplicate_software_installations.txt` |
| S25 | Software install deduplication | Brazil, Sep 10 2026 | `raw/software_install_deduplication.txt` |
| S26 | Create a custom deduplication rule | Brazil, Sep 10 2026 | `raw/create_custom_dedup_rule.txt` |
| S27 | Allocation management on Software Asset Management | Brazil, Sep 10 2026 | `raw/allocation_management.txt` |
| S28 | Software license metrics | Brazil, Sep 10 2026 | `raw/software_license_metrics.txt` |
| S29 | Exclude software assets on CIs | Brazil, Oct 19 2026 | `raw/exclude_software_assets_on_cis.txt` |
| S30 | Publish a specific set of your software products | Brazil, Sep 10 2026 | `raw/publish_specific_set_of_products.txt` |
| S31 | Remove published software products | Brazil, Sep 10 2026 | `raw/remove_published_software_products.txt` |
| S32 | Set the domain-specific property to publish your software products | Brazil, Sep 10 2026 | `raw/publish_domain_specific_property.txt` |
| S33 | Software installation fields | Brazil, Sep 10 2026 | `raw/software_installation_fields.txt` |
| S34 | Software Asset Management properties | Brazil, Mar 12 2026 | `raw/sam_properties.txt` |
| S35 | Exploring Software Asset Management | Brazil, Sep 10 2026 | `raw/exploring_sam.txt` |
| S36 | Software Asset Workspace | Brazil, Sep 10 2026 | `raw/software_asset_workspace.txt` |
| S37 | Success portal view in Software Asset Workspace | Brazil, Sep 10 2026 | `raw/success_portal.txt` |
| S38 | Software Asset Management health check | Brazil, Sep 10 2026 | `raw/sam_health_check.txt` |
| S39 | Run a health check scan for SAM | Brazil, Sep 10 2026 | `raw/run_health_check_scan.txt` |
| S40 | Maturity stages of your SAM program | Brazil, Sep 10 2026 | `raw/maturity_stages_sam.txt` |
| S41 | View all maturity items for SAM | Brazil, Sep 10 2026 | `raw/maturity_items.txt` |
| S42 | Maturity item details | Brazil, Sep 10 2026 | `raw/maturity_item_details.txt` |
| S43 | Software asset overview | Brazil, Sep 10 2026 | `raw/software_asset_overview.txt` |
| S44 | Create a catalog request to reclaim assets | Brazil, Sep 10 2026 | `raw/catalog_request_to_reclaim.txt` |
| S45 | Software request workflow (agentic) | Brazil, Sep 10 2026 | `raw/software_request_workflow.txt` |
| S46 | Create success goals for SAM | Brazil, Sep 10 2026 | `raw/create_success_goals.txt` |
| S47 | Link an item to the software catalog | Brazil, Sep 10 2026 | `raw/link_item_to_software_catalog.txt` |
| S48 | Publish an item to the software catalog | Brazil, Sep 10 2026 | `raw/publish_item_to_software_catalog.txt` |
| S49 | Publish models to the hardware or software catalog | Brazil, Sep 10 2026 | `raw/publish_models_to_hw_or_sw_catalog.txt` |
| S50 | Configuring Software Asset Management | Brazil, Sep 10 2026 | `raw/configuring_sam.txt` |
| S51 | Software Asset Management installation methods | Brazil, Sep 10 2026 | `raw/sam_installation_methods.txt` |
| S52 | AI in Software Asset Management | Brazil, Sep 10 2026 | `raw/ai_in_sam.txt` |
| S53 | Request Software Asset Management | Brazil, Sep 10 2026 | `raw/request_software_asset_management.txt` |
| S54 | Software Asset Management landing | Brazil, Sep 10 2026 | `raw/sam_landing.txt` |
| S55 | Manage phase-wise Software Asset Management implementation | Brazil, Sep 10 2026 | `raw/phase_wise_implementation.txt` |
| S56 | Implementation-success digest (community Path to Value / Office Hours) — corroboration only | 2026-11-13 | `research/IMPLEMENTATION_SUCCESS.md` |
| S57 | Australia-family SAM config inventory (tables, Foundation plugin, matching job, IRE 3rd-party) | 2026-11-13 | `research/CONFIG_INVENTORY_AUSTRALIA.md` |
| S58 | Discovery with Software Asset Management (Australia) + Configure a CI to display SAM data | 2026-03-12 | `agents/beam__kilo__cli/SNC_SAM__WT1/research/servicenow-sam/sources/discovery_with_sam.txt` |
| S59 | Beam consolidated SAM module reference (Australia-pinned) | 2026-11-13 | `final/FINAL_SAM_MODULE_REFERENCE.md` |
| S60 | Grok WT1 SAM configuration reference (Brazil-pinned) | 2026-11-13 | `agents/grok-4.6__xai__kilo/SNC_SAM__WT1/05_FINAL/SAM_CONFIG_REFERENCE.md` |
| S61 | View or create software usage (`samp_sw_usage`) | Brazil, Sep 10 2026 | `raw/view_or_create_software_usage.txt` |
| S62 | Software license usage (License Workbench) | Brazil, Sep 10 2026 | `raw/software_license_usage.txt` |
| S63 | Software model results license metric results fields | Brazil, Sep 10 2026 | `raw/software_model_results_lmr_fields.txt` |
| S64 | Impact of different license types on software reconciliation | Brazil, Sep 10 2026 | `raw/impact_license_types_on_recon.txt` |
| S65 | Grok WT3 CIS-SAM cheat sheet (quiz grounded in WT1 + docs) | 2026-11-13 | `agents/grok-4.6__xai__kilo/SNC_SAM__WT3/05_FINAL/CIS_SAM_CHEATSHEET.md` |
| X1 | ALT_PARALLELSWARM Discovery insert-vs-update decision guide (latest findings) | 2026-11-13 | `ALT_PARALLELSWARM/final/DISCOVERY_INSERT_VS_UPDATE_GUIDE.md` |
| X2 | CMDB-focused SAM config reference (remote branch `kilo/sam-module-config-reference`) | 2026-11-13 | `agents/kilo-sam-pro__kilo__sam-module/SNC_DISC__WT1/05_FINAL/SAM_CONFIG_REFERENCE.md` |

Additional corpus consulted but not individually cited: `raw/sam_overview.txt`, `raw/sam_health_check.txt`, `raw/ai_in_sam.txt`, `raw/software_asset_workspace.txt`, `raw/maturity_*.txt`, `raw/request_software_asset_management.txt`, `raw/publish_domain_specific_property.txt`, `plans/grok-4.6__xai__kilo__WT1/PLAN.md`.

---

## 13. Gaps & UNVERIFIED

1. **Business-rule identity.** The install→discovery-model business rule has no published name/sys_id. Behaviour is documented (`[S2][S3]`); the object itself must be identified on-instance (§2.8).
2. **UI policies, client scripts, ACLs.** Not enumerated by any component article. Treat as UNVERIFIED; audit recipe §2.8.
3. **Reconciliation job name and exact schedule.** "Weekly default, on demand" is documented (`[S20][S21]`); the scheduled-job record's exact name/quartz expression is not printed.
4. **Spelling variants preserved:** `samp_normalization_suggestion` vs `samp_normalization_suggestions`; `com.snc.samp.manage.published.product` vs `com.snc.samp.manage.published.products`; `com.snc.samp.ml.overrride_ml_model_version` (three r's).
5. **RHEL Virtual Datacenters threshold** — default 3.2 documented, programmatic property name not printed (UNVERIFIED).
6. **Reclamation rule / removal candidate table names beyond `samp_sw_reclamation_candidate`** — classic UI modules are named, underlying records UNVERIFIED.
7. **Entitlement unique key** (PPN + metric + company…) — docs warn on PPN mismatch but publish no unique index.
8. **Dedup primary-selection ranking** — discovery-source reliability, completeness, latest version tiers documented (`[S25]`) but the reliability ordering itself is not published.
9. **Publisher arithmetic** — Oracle core-factor math, IBM PVU tables, SAP named-user definitions are publisher-specific and only summarized here.
10. **Release drift** — Brazil pin used; Australia/Yokohama/Xanadu deltas not diffed. Some values are explicitly version-gated in the docs (e.g., CrowdStrike metrics from Yokohama Patch 1 / SaaS LM 15.0.8 / SAM store app 2.1.0; newer IBM metrics from Australia Patch 6).
11. **Foundation vs Professional deltas** — only partially documented (normalization statuses differ); property applicability per tier UNVERIFIED.
12. **Login-gated content** — Now Create SAM Success Pack, Success Checklist PDFs, Customer Success Center procedures: not opened.
13. **Community learning packs are unreliable** — the `sam-buffy/KiloCode` pack (2026-11-04) teaches wrong tables (`alm_software`, `alm_software_installation`), wrong roles (`sam_license_manager`, `sn_sam.admin`) and a wrong navigation parent (SAM → HAM). Official docs win; see `05_FINAL/CURRICULUM_COMPARE.md` for the line-by-line verdict.
14. **No live instance** — nothing here was executed against an entitled SAM instance. Every procedural step is transcribed from documentation and should be rehearsed in a sub-production instance first.
15. **`samp_vmware_license_key` / `samp_vmware_license_key_usage`** come from the Australia abstract set (`[S58]`, Kingston+) and were not corroborated in the Brazil corpus; verify presence/usage on your release.
16. **Usage-table naming corrected in round 3:** the official table is **`samp_sw_usage`** `[S61]` — the curriculum's `cmdb_sam_sw_usage` and any `samp_discovered_model`-style guesses are wrong. Earlier revisions of this guide listed the usage table as UNVERIFIED; that caveat is now closed.
17. **CMDB-layer IRE behaviour for software installs** (§8.4) is cross-referenced, not re-derived here; treat X1/X2 claims as sibling-corpus evidence until checked against CMDB docs in a future pass.

*End of guide.*

---

# FINAL — SAM module deep dive (consolidated)

**Agent:** `kilo-sam-deepdive__kilo__cli` · **Model:** Kilo (inherited) · **Harness:** Kilo CLI
**Date:** 2026-11-13 · **Branch:** `docs/sam-module-deep-dive`
**Companion documents:** `research/servicenow-sam/SAM_MODULE_DEEP_DIVE.md` (identical guide), `CURRICULUM_COMPARE.md`, `CURRICULUM_FINDINGS.md`, `FINAL_FEEDBACK.md`

This file is the consolidated final output: the full operational deep dive above, followed by final thoughts and a concrete proposal for improving the live CIS-SAM curriculum page (<https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/sam/sam-guide/>).

---

## 14. Final thoughts

**Source hierarchy that worked.** Official product docs > exam curriculum > community packs. Every time that hierarchy was violated, errors entered the corpus: the curriculum's `cmdb_sam_sw_usage` and `sam_sw_reconciliation_result`, its nightly cadence, its SUMN branding, its plugin tip, and the sam-buffy pack's wrong tables/roles/nav. Two independent agents (this one and grok WT3) reached the same corrections from official pages, so the error register is high-confidence.

**Coverage achieved.** The fleet now has four complementary SAM references: this deep dive (operations: OOB components, maintenance procedures, license concerns, workspaces, parameters), grok WT1 (config surface + per-property source ledger), kilo-sam-pro (CMDB/IRE governance layer for software install writes), and the ALT_PARALLELSWARM decision guide (insert-vs-update rules). None alone covers the module end-to-end.

**Honest limits.** No entitled instance was available; every procedural claim is documentation-derived. OOB business-rule sys_ids, UI policies and ACLs remain unpublished; the reconciliation script include move at Yokohama needs manual migration; Foundation vs Professional deltas are only partially documented. Verify in sub-production before production changes.

**Ranked next actions.**
1. Instance verification pass: audit BRs/UI policies/ACLs with §2.8; confirm `samp_sw_usage` participation in on-prem reconciliation numerators.
2. Merge order: land `kilo/sam-module-config-reference` first (purely additive), then `docs/sam-module-deep-dive`; both leave shared fleet files untouched.
3. Property audit: diff `sys_properties` (`com.snc.samp%`, `samp.%`, `sn_sam_%`) against §7 before go-live.
4. Release-drift diff: Brazil vs Australia vs Yokohama/Xanadu for Tier 0/1 properties.
5. Keep the curriculum's practice guidance (60–90 day reclaim window, optimization priority) but label it as practice, not vendor default.

---

## 15. Concepts to add to the live sam-guide

The live page (verified byte-identical to the repo file, 1,074 lines, 2026-11-12) is strong on concepts but carries naming/cadence errors and omits the operational layer. Concretely:

### 15.1 Corrections to fold in (highest priority)

1. **Table names:** replace `cmdb_sam_sw_usage` → **`samp_sw_usage`**; replace `sam_sw_reconciliation_result` → **`samp_reconciliation_result`** with the three-tier hierarchy (Product Results → Software Model Results → License Metric Results).
2. **Cadence:** change "default nightly" → "**weekly default; on demand** per publisher/group/subgroup".
3. **Branding:** drop "SUMN" or mark it community shorthand; use Content Library + `SAM - Normalize discovery models using content library rules`.
4. **Plugin tip:** Foundation `com.snc.sams`; Professional `com.sn_samp_master_ws` (loads `com.sn_samp_master` + `sn_sam_workspace`).
5. **Navigation:** root breadcrumbs at `Workspaces > Software Asset Workspace` and classic `All > Software Asset > …` / `All > Software asset > …`.
6. **Sample code:** label snippets illustrative, not OOB; remove custom fields from any "expected" listing.
7. **Mark UNVERIFIED:** `license_metric_type`, `normalized_software_model`, `compliance_state`, `entitlement_count`/`install_count`.

### 15.2 New sections worth adding

| Proposed section | Why | Source |
|---|---|---|
| **Out-of-the-box SAM components** | Currently missing; administrators cannot discover shipped jobs without filtering `Name starts with SAM` | DD §2 (jobs J1–J15, install→discovery-model BR, recon script includes, flows) |
| **SAM parameter quick reference** | No prioritized property list exists; Tier 0 go-live blockers (auto-create off, published products, exclude flag, recon grouping) are scattered | DD §7.2 |
| **License position & reconciliation result fields** | The result schema is wrong/absent; rights owned/used/available, allocation breakdown, rights needed, unlicensed installs are the daily ops surface | DD §5.1–§5.2, `[S18][S63]` |
| **Software usage & reclamation data** | Usage is central to reclamation but undocumented; `samp_sw_usage`, Total Usage Time vs Last Used Date, CI retirement deletes related installs | DD §5.3, `[S61]` |
| **License-type impact on reconciliation** | Perpetual+SA/Maintenance linking, Upgrade/Step-up semantics materially change compliance; currently absent | DD §5.4, `[S64]` |
| **Duplicate/stale hygiene playbook** | Installs are never auto-deleted; dedup levels, Active flag, REST cleanup, exclude-CI flag | DD §5.5, `[S23][S24][S26][S29]` |
| **CMDB-layer governance cross-ref** | When installs arrive via CMDB integrations, IRE identification/data-source/reconciliation/data-refresh rules apply | DD §8.4, X1/X2 |

### 15.3 Concepts to keep, clearly labelled as practice (not vendor defaults)

- Optimization priority order and the 60–90 day reclamation window.
- Indicative KPI targets (keep the "indicative" label).
- Entitlement hygiene rules (one entitlement per contract line; never overwrite quantity; maintenance ≠ licence).
- Publisher trap table (Oracle server-level licensing, IBM PVU/ILMT, SAP named users, MS SQL cores, Adobe VIP).

### 15.4 Suggested one-paragraph addition to "Where to Find It"

> SAM is delivered in two navigation generations. Use **Workspaces > Software Asset Workspace** for daily operations (overview, license usage, license operations, analytics, success portal, renewals, overlapping usage, content library portal). Several administration features remain classic-only even after Workspace activation: Custom Products, Custom Part Numbers, Custom License Metrics, Pattern Normalization Rules, Reclamation Rules, Job Results, Content Service Setup, Properties, SaaS integration profiles, SAP connections. Roles: `sam_admin`, `sam_user`, `sam_developer`, `sam_integrator`, `sam_spend_import`.

*End of final.*
