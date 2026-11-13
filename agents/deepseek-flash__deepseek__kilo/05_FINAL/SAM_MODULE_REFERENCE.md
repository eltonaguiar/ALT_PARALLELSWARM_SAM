# ServiceNow SAM — Module & Discovery Configuration Reference (Brazil)

**Agent:** `deepseek-flash__deepseek__kilo` · **Model:** `deepseek/deepseek-flash` · **Provider:** DeepSeek · **Harness:** Kilo CLI
**Worktree:** `SNC_SAM__WT1` · **Date:** 2026-11-13
**Release pin:** ServiceNow docs **Brazil**, ITAM map `PMOYmdGTPDs40EbYh10h4g` (pages *Updated Sep 10 2026* unless noted). Australia-family facts are marked **C** and labelled.
**Companion:** `ALT_PARALLELSWARM` covers the Discovery/IRE/CMDB half. This file covers the SAM half and the software boundary between them.

> **Confidence marks.** **V** = printed verbatim on the cited Brazil page. **C** = corroborated by an Australia-family page or by the reference repo. **U** = the docs publish only the UI label; the internal column/table is unverified — resolve with `sys_dictionary`/`sys_db_object` before scripting. The docs never print a column name they do not mean; where they print only a label, this file does not invent one.

---

## 0. Mental model — five record types, one pipeline

```
Discovery · SCCM/SGC · FBD · SaaS · ILMT · 3rd-party IRE
        │ writes installations
        ▼
Software Installation            cmdb_sam_sw_install              (one copy of software on one CI)
        │ business rule matches Publisher + Display name + Version
        ▼
Software Discovery Model         cmdb_sam_sw_discovery_model      (deduped discovered string; cannot be created manually)
        │ normalise vs Content Library; match to a model
        ▼
Software Model                   cmdb_software_product_model      (what you purchased/manage)
        │ entitlements + allocations
        ▼
Entitlement                      alm_license                      (rights you own)
        │ weekly/on-demand reconciliation
        ▼
Product Result → Software Model Result → License Metric Result
        │
        ├─ License Position (Compliant / Not Compliant)
        ├─ True-up cost / over-licensed amount
        └─ Reclamation (usage → removal candidate → uninstall/forfeit)
```

Consequences that explain most SAM defects:

1. **A discovery model is not a software model.** Discovery creates the former; humans/imports create the latter. Discovery models cannot be created in the UI.
2. **A software model is not a catalog item.** Publishing a model to the service catalog is a separate, optional, Product-Catalog action.
3. **An entitlement is not an installation.** `alm_license` records rights; `cmdb_sam_sw_install` records copies. Reconciliation is the join.
4. **Normalisation is the gate.** Only `Licensable` products are reconciled; un-normalised or `Match Not Found` rows produce bad or missing positions.
5. **SAM does not delete uninstalled software.** Install rows persist until a delete flow removes them; this inflates counts if ignored.

---

## 1. Order of operations

### 1.1 Setup (implementation order)

| # | Step | Why here | Exit check |
|---|---|---|---|
| 0 | Healthy CMDB + Discovery coverage | SAM writes onto `cmdb_ci_hardware`; no CI, no install target | `cmdb_ci_computer` populated; owners/location present |
| 1 | Install SAM from **Product Hub** (first time) or **ServiceNow Store** | Guided vs direct install | Plugin active |
| 2 | Activate **`com.sn_samp_master_ws`** (Pro + Workspace in one step) | Brazil installer; loads `com.sn_samp_master` + `sn_sam_workspace` | Workspace reachable; classic limited |
| 3 | Add publisher packs only if in scope (Adobe, Citrix, IBM, Microsoft, Oracle, SAP, VMware, Engineering) | Packs add metrics and cost | Only contracted packs active |
| 4 | Opt in to **Content Service** (default **off**) | Improves normalisation; no PII, custom-product exception | Content Service Setup saved |
| 5 | Wire discovery sources (§4) | Installs must land before reconciliation | Test CI produces `cmdb_sam_sw_install` rows |
| 6 | Load **entitlements** (`alm_license`) — bulk import / PPN | Docs' Discovery/SCCM path says entitlements **before** discovery | Entitlement state = Published/In use |
| 7 | Let the daily normalisation jobs run | Assigns statuses and normalised columns | Dashboard % normalised rises |
| 8 | Create custom products / pattern rules / manual normalise | Closes `Match Not Found` | Unnormalised backlog trending down |
| 9 | First **reconciliation** | Weekly default or on demand | Product Results exist |
| 10 | Enable `com.snc.samp.manage.published.products` + publish a **small** product set (optional) | Phase-wise scope freeze | Published list = MVP publishers |
| 11 | Reclamation rules → removal candidates → catalog reclaim | Optimisation after compliance is trusted | Candidate count and savings visible |
| 12 | Publish requestable software to the service catalog | Run-stage maturity | Catalog item links to model |
| 13 | Success portal: goals, health check, maturity items | Programme tracking | Baseline metrics captured |

### 1.2 Runtime (one installation)

1. Source writes `cmdb_sam_sw_install`.
2. **Install→discovery-model business rule** (unnamed in docs, `U`): if the key `Publisher + Display name + Version` exists on `cmdb_sam_sw_discovery_model`, set `discovery_model`; else insert a discovery model and set it.
3. Daily `SAM - Normalize discovery models using content library rules` assigns a **normalisation status** and normalised columns.
4. Fallbacks in order: **wide-net** (`com.snc.samp.wide_net_normalization.enabled`, default on) → **ML** (`com.snc.samp.enable.ml_normalization`, default on).
5. `SAM – Discovery Model to Software Model matching` writes the `software_model` reference and `Automatically matched` flag.
6. Reconciliation matches installs → software models → entitlements → results.
7. `SAM - Deduplicate Install Table` sets one install `active=true`, duplicates `active=false`.
8. `SAM — Adjust Installs for excluded CIs` honours the exclude-device flag.
9. Reclamation rules aggregate usage; candidates are produced.

---

## 2. Record types, tables, and the model-vs-vendor axis

### 2.1 Software Installation — `cmdb_sam_sw_install` **V**

| Field (UI label) | Column | Notes |
|---|---|---|
| Display name | `display_name` **C** | Discovered product + edition |
| Discovery model | `discovery_model` **C** | Reference to `cmdb_sam_sw_discovery_model` |
| Publisher | `publisher` **C** | Discovered publisher, not normalised |
| Version | `version` **C** | Discovered version |
| Edition Override | `U:edition_override` | Editable when edition was not discovered; needed for reconciliation |
| Installed on | `installed_on` **V** | Reference to hardware CI; used by the Table API delete recipe |
| Install location | `install_location` **C** | Path |
| Install date | `install_date` **C** | Date |
| Instance key | `instance_key` **C** | Instantiation ID; not a documented match key |
| Uninstall string | `uninstall_string` **C** | Uninstall command |
| ISO serial number | `iso_serial_number` **C** | Form field, not a documented identity key |
| Active | `active` **V** | Dedup sets duplicates false; only active rows reconcile |
| Inferred suite | `inferred_suite` **C** | Inferred suite model |
| Omit from suites | `omit_from_suites` **C** | Exclude from suite counting |
| Prod id / Revision / Entitlement | — | Deprecated; still shown empty |

**Key behaviour.** SAM has **no IRE identification rule** for installs. Duplicate install rows are *expected* across discovery sources; the dedup job decides which is primary. There is no `duplicate_of` mechanism for software installs.

### 2.2 Software Discovery Model — `cmdb_sam_sw_discovery_model` **V**

| Field (UI label) | Column | Notes |
|---|---|---|
| Display name | `display_name` **C** | Auto-generated from discovered publisher + product + version |
| **Normalization status** | `U:norm_status` | Six values — see §5.1 |
| Publisher | `publisher` **C** | **Normalised** publisher |
| Product | `product` **C** | Normalised product |
| Version | `version` **C** | Normalised version |
| Discovered publisher | `discovered_publisher` **C** | Raw |
| Discovered product | `discovered_product` **C** | Raw |
| Discovered version | `discovered_version` **C** | Raw |
| Product type | `product_type` **C** | Child / Driver / Licensable / Not Licensable / Patch / Unknown — only **Licensable** reconciles |
| Platform | `platform` **C** | Windows / macOS / UNIX |
| Language | `language` **C** | Dutch / English / French / German / Italian / Spanish + discovered |
| Edition | `edition` **C** | Normalised edition |
| Full version | `full_version` **C** | Normalised full version |
| Exclude from content service | `U:exclude_from_content_service` | Custom products only, when opted in |
| Software model | `software_model` **C** | Set by the matching job or manually |
| Automatically matched | `U:automatically_matched` | `false` when a human set the model; job will not override |
| Normalization date | `U:normalization_date` | Updated when a suggestion is accepted |
| Approved | `U:approved` | Legacy checkbox; new installs are not auto-approved |

**Primary key:** `Publisher + Display name + Version` **V**. Version matching is exact first, then rounds down to major (`8.0.4` → `8.0`) **V**.
**Never created manually** **V**. Not created when the install name contains `Security Update` **V**.

### 2.3 Software Model — `cmdb_software_product_model` **V**

Extends `cmdb_model` **C**. One model can cover many discovery models via version/edition conditions (`Version = Starts with 10` covers 10.1 and 10.2) **V**.

| Field / related list | Column / table | Notes |
|---|---|---|
| Publisher | `publisher` **C** | Points at publisher record |
| Product | `product` **C** | Product name |
| Version / Version condition | `version`, `U:version_condition` | `Starts with`, etc. |
| Edition / Edition condition | `edition`, `U:edition_condition` | |
| Platform / Language | `platform`, `language` | |
| Install condition | `U:install_condition` | Match is skipped if present but unmet |
| Discovery map | `U:discovery_map` | From Content Library; drives suites/downgrades |
| Suite Parents / Suite Components | related lists (`U` join table) | Parent↔child suite membership |
| Metric Attributes | related list | Sets `metric_group`; entitlements inherit it |
| Created source | `U:created_source` | `System property` = auto-created |
| License cost / License + maintenance cost | `U:license_cost`, `U:license_plus_maintenance_cost` | True-up uses these first |
| License under management | `U:license_under_management` | Must be selected for reconciliation (Australia **C**) |
| Vendor Catalog Item | related list (`U` table) | Links procurement vendor item |
| Client Access | related list | Client-access records (CAL/Citrix) |
| Downgrade Rights | `samp_sw_downgrade_model`, `samp_dmap_downgrade_model`, `samp_downgrade_model` **V** | Auto-populated from discovery map |
| Product Lifecycles | `sam_sw_product_lifecycle`, `sam_custom_sw_product_lifecycle` **V** | EOS/EOES/EOL |

### 2.4 Software **model vs publisher vs vendor vs PPN vs catalog item**

This is the highest-value disambiguation in SAM.

| Concept | Record | Table | What it is | Not |
|---|---|---|---|---|
| Vendor / company | company record | `core_company` **C** | Legal entity; has vendor flag; contract counterparty | Not a product or a licence |
| Publisher | SAM publisher | `samp_sw_publisher` **C** | SAM's publisher identity; **must relate to `core_company`** | Not the vendor contract record |
| Publisher part number (PPN) | content definition | `samp_sw_product_definition` **V** | Vendor ordering SKU used to resolve a model on import | Not an entitlement |
| Software model | model profile | `cmdb_software_product_model` **V** | Purchasable/managed product profile at version/edition granularity | Not a discovered string; not a catalog item |
| Discovery model | discovered string | `cmdb_sam_sw_discovery_model` **V** | Deduped discovered identity | Not purchasable; cannot be created manually |
| Vendor catalog item | procurement item | `U:pc_vendor_cat_item` (verify) | Vendor's item used to publish/link a catalog item | Not a software model |
| Catalog item | requestable item | `sc_cat_item` **C** | What a user orders in the service catalog | Not a licence and not created by discovery |
| Entitlement | rights | `alm_license` **V** | Rights owned, linked to a software model | Not an install |

**Rules that follow:**
- Custom product creation may create a `core_company` publisher if absent **V**.
- A software model's publisher is not the same field as `ast_contract.vendor`; contract renewal reporting joins on the contract, not the publisher.
- PPN resolution can auto-create a model; a blank PPN on an MLS import does **not** search other fields **V**.

### 2.5 Entitlement and allocation — `alm_license`, `alm_entitlement_user`, `alm_entitlement_asset`

| Field | Notes |
|---|---|
| Publisher part number | PPN; drives model resolution |
| License type | Perpetual, Perpetual + SA, Subscription, Perpetual + Maintenance, Upgrade, SA, Maintenance, Step-up, Subscription Step-up, Add-on, From SA **V** |
| License metric | Publisher-specific metric, e.g. Per Core, PVU, Named User Plus **V** |
| Rights / purchased rights | Sum becomes **Rights owned** |
| Start / end date | Expiry drives Renewals calendar |
| License duration | `Contractual` requires start/end for Microsoft **V** |
| State | Build → Published → In use; only in-use reconciles **C** |
| Company / cost / currency | Financial reporting |
| License cost / License + maintenance cost | Override licence cost record; created at **zero** when a metric is first used **V** |
| Metric group | Inherited from model metric attributes |
| Subscription period / Agreement type | Subscription and enterprise agreements |
| Upgraded Entitlements | Links step-up/upgrade base |
| Allocations | `alm_entitlement_user` (user) **or** `alm_entitlement_asset` (device), not both **C** |

Allocation quantity cannot exceed entitlement rights **C**. Device allocation core logic: exact cores → actual machine cores; fewer than machine → machine cores counted; more → entered number, surplus = **Allocated not in use** **V**.

### 2.6 Supporting tables

| Table | Purpose |
|---|---|
| `samp_product_result` **V** | Tier-1 reconciliation result |
| `U:samp_sw_model_result` | Tier-2 (label "Software Model Results"; internal name not printed) |
| `samp_license_metric_result` **V** | Tier-3 rights algebra |
| `samp_sw_usage` **V** | Usage records, product level |
| `samp_sw_reclamation_candidate` **V** | Removal/reclamation candidates, justification, state, savings |
| `sam_sw_dedup_rule` **V** | Custom dedup rule (`product`, `active`, version level) |
| `samp_normalization_suggestion` **V** / `samp_normalization_suggestions` **V** | Suggestion records (spelling differs between two pages) |
| `samp_sw_resource_value` **V** | Unit consumption for Resource Consumption / Concurrent metrics |
| `samp_sw_product`, `samp_sw_publisher` **C** | Content product/publisher |
| `samp_sw_product_definition` **V** | PPN content |
| `sam_sw_product_lifecycle`, `sam_custom_sw_product_lifecycle` **V** | Lifecycle dates |
| `samp_sw_product_lifecycle_report` **V** | Lifecycle report source |
| `samp_oracle_options` **C** | Oracle options eligibility |
| `samp_custom_lic_exception_rules` **V** | Custom non-licensable edition rules |
| `samp_sw_unrecognized_subscription_identifier` **V** | Unmatched subscriptions |
| `samp_sso_application` **V** | SSO app discovery |
| `samp_job_log` **V** | Job results |
| `samp_entitlement_import`, `samp_bulk_import` **V** | Import errors / status |
| `samp_reconciliation_result` **V** | Reconciliation run result (not the same as the tier tables) |
| `samp_ws_activity_center_items` **V** | Workspace alert items |
| `sn_samp_vr_cpe_mapping_suggestion` **V** | CPE normalisation suggestions |
| `alm_entitlement_user`, `alm_entitlement_asset` **V** | Allocations |
| `ast_contract` **V** | Contract renewals; shared with HAM |
| `cmdb_ci_hardware` **V** | Exclude-from-SAM boolean lives here |
| `cmdb_ci_spkg` **V** | Legacy install table (pre-SAM); migrated |
| `samp_vmware_license_key`, `samp_vmware_license_key_usage` **C** | VMware discovery |
| `cmdb_file_information`, `samp_file_name`, `samp_custom_file_name`, `cmdb_unidentified_file_set`, `cmdb_swid_tag` **C** | File-based discovery |
| `sys_object_source_info`, `cmdb_ire_partial_payloads` **C** | Third-party IRE insert path |

---

## 3. Out-of-box scripts — jobs, rules, flows, actions

### 3.1 Scheduled jobs (find with `Name starts with SAM`)

| Job | Target | What it writes | Customise? | Risk if you do |
|---|---|---|---|---|
| `SAM - Normalize discovery models using content library rules` (daily) | `cmdb_sam_sw_discovery_model` | Normalised Publisher/Product/Version/Edition/Platform/Language/Full version + Normalization status | **Leave** | Overlay breaks content-rule updates and status semantics; use pattern rules/custom products instead |
| `SAM - Discovery Model Normalization job` (daily) | `cmdb_sam_sw_discovery_model` (aggregates) | Feeds Normalization and content dashboard trends | **Leave** | Dashboard numbers diverge from the real normaliser |
| `SAM – Discovery Model to Software Model matching` | `cmdb_sam_sw_discovery_model.software_model`, `Automatically matched` | Model reference | **Leave** | Manual overrides get overwritten; breaks `Automatically matched` contract |
| `SAM - Deduplicate Install Table` | `cmdb_sam_sw_install.active` | Primary/duplicate flag | **Leave**; tune via `sam_sw_dedup_rule` | Duplicate rows re-enter reconciliation; IBM source-preference inverted |
| `SAM — Adjust Installs for excluded CIs` | `cmdb_sam_sw_install` | Removes/excludes installs on flagged CIs | **Leave** | Excluded devices leak into compliance |
| `SAM - Daily Job` | dashboard aggregates | Counts/trends | **Leave** | Dashboard stale |
| `SAM - Trigger Full Scan` (weekly) | Health Check KPIs | Health scores/findings | **Leave**; add KPIs in the app | Custom KPI scripts collide on upgrade |
| `SAM - Label Spend Transactions` | spend transactions | Spend labels; `samp.spend_prediction_service.max_label_attempts` default 3 | **Leave** | Mislabeled spend |
| `SAM- Create downgrades/upgrades for a software entitlement` (weekly) | `samp_sw_downgrade_model` etc. | Downgrade rights | **Leave** | Missing downgrade coverage |
| `Download software content: Downgrade Rights` (weekly) | content | Downgrade content sync | **Leave** | Stale rights |
| `SAM - Central Data Service Download Status` | CDS status | Counts, expected, next action | **Leave** | Blind content failures |
| Weekly reconciliation job(s) per publisher | results tables | Product/Model/Metric results | **Configure via properties**, not script | Custom script includes deprecated/moved at Yokohama **V** |

### 3.2 Business rules

| Object | Trigger | Effect | Customise? |
|---|---|---|---|
| Install→discovery-model rule (name `U`) | insert/update on `cmdb_sam_sw_install` | Match `Publisher + Display name + Version`; set or create `cmdb_sam_sw_discovery_model` | **No** — extension point is normalisation metadata, not this rule |
| Product-type edit → status rule (`U`) | update on discovery model | Changing Product type sets **Manually Normalized** | No |
| CI retired/stolen → install cleanup (`U`) | CI status change | Installations related to the CI are **deleted** **V** | No — document the blast radius |
| Edge case | A source re-inserts a `Security Update` install | No discovery model is created (hard-coded) | No |

### 3.3 Flows

| Flow | Trigger | Property |
|---|---|---|
| Reclamation flow | removal candidate / reclaim request | `sam_reclamation_flow_error_timeout` default **30 days** then Closed canceled **V** |
| Reclaim asset catalog request | employee separation / role change | Reclaim Asset catalog item **V** |
| Software request agentic workflow (Otto) | approved, assigned, unsourced software request | Needs Procurement + `sn_now_assist_sam`; AI agents allocate or raise PO **V** |

### 3.4 Script includes / APIs

| Object | Note | Risk |
|---|---|---|
| Reconciliation script includes | Moved to Store app `com.sn_itam_samp` from Yokohama **V** | Customised legacy includes are deprecated; migrate customisations |
| `CMDBTransformUtil` / `CreateOrUpdateCIEnhanced()` | For third-party/import-set writes through IRE **C** | Plain `createOrUpdateCI()` fails the whole batch on one bad item |
| Migration script (Basic SAM → Pro) | Copies `cmdb_ci_spkg` → `cmdb_sam_sw_install` **C** | Do not write to `cmdb_ci_spkg` after migration |
| Table API delete recipe | `GET/DELETE api/now/table/cmdb_sam_sw_install` | Deleting wrong sys_ids loses audit evidence |

### 3.5 UI actions

`Normalize` (workspace ellipsis) · `Revert Normalization` · `Apply Rule` (pattern rule) · `Accept` / `Reject` suggestion · `Execute Scan` (health) · `Create Allocations` / `Remove Allocations` / `Remove Unallocated Installs` / `Remove Unlicensed Installs` (remediation) · `Publish to Software Catalog` · `Link to Software Catalog Item` · `Create PPN` · **V** for all labels.

### 3.6 Customise-vs-leave decision rule

- **Leave** any OOB object whose name is a scheduled job or whose script is content-driven. Change behaviour through **properties**, **custom products**, **pattern normalisation rules**, **custom license metrics**, **custom PPNs**, **custom dedup rules**, **reclamation rules**, or the **published-product list**.
- **Extend** only via those extension points; they survive upgrades.
- **Never** overlay the install→discovery-model business rule, the normalisation job, the matching job, or the dedup job. Their contracts (status values, `Automatically matched`, `active`) are read by other OOB code.

### 3.7 Customisation risks (ranked)

1. Overlaying the normaliser → status values drift and reconciliation silently skips rows.
2. Editing the matching job → `Automatically matched` lies; manual model choices get reverted.
3. Scripting dedup → two active installs per device, inflated rights used.
4. Custom reconciliation includes → break at Yokohama migration.
5. Post-migration writes to `cmdb_ci_spkg` → invisible installs.
6. UI policy/ACL overlays on discovery-model status → users bypass normalisation (`U` today; audit `sys_ui_policy`/`sys_security_acl`).

---

## 4. Discovery rules and the CI/licence insert-update contract

### 4.1 ServiceNow Discovery → SAM

- Plugin: Discovery required. Base patterns cited for SAM: **Citrix XenApp, Citrix XenDesktop, VMware vCenter, Microsoft SQL Server, Microsoft Exchange Server, Oracle Database** **V**.
- Discovery writes `cmdb_sam_sw_install`; the business rule then matches/creates the discovery model **V**.
- Discovery-side properties that change SAM data: `glide.discovery.discover_software` (true), `glide.discovery.enable.software_filter` (true), `glide.discovery.software_filter_keys` (`Language Pack, Hotfix Security Update`), `glide.discovery.enable.software_simplify` (true), `glide.discovery.enable.software_simplify_sccm` (false), `glide.discovery.software_sccm_managed` (false — true suppresses software from SCCM-managed machines), `glide.discovery.populate_software_instance_table` (false; legacy), `glide.discovery.sam_batch_update_size` (100) **C/V** from the reference repo.
- **Ip-scan discovery does not update the CMDB**; only `Configuration items` schedules write CIs **C**.

### 4.2 SCCM and Service Graph

- Legacy plugins: `com.snc.integration.sccm2012v2`, `com.snc.integration.sccm2016`; usage add-ons `com.snc.samp_usage_sccm`, `com.snc.samp.usage_sccm_2016` **V**.
- Deprecated in Tokyo; new work uses the **Service Graph connector for Microsoft SCCM** **V**; Migration Readiness Tool exists **V**.
- Intune / Jamf / Tanium are Service Graph CMDB connectors; the SAM discovery pages do **not** list them as native install sources **C** — treat as CMDB feed + IRE/third-party write.

### 4.3 File-Based Discovery (FBD)

- Plugin `com.snc.discovery.file_based_discovery` **C**; needs `com.snc.file_signature_normalization` **V**.
- Runs during exploration; records files, matches signatures, writes `cmdb_sam_sw_install`.
- Tables: `cmdb_file_information`, `samp_file_name` (vendor allow-list), `samp_custom_file_name` (your additions), `cmdb_unidentified_file_set`, `cmdb_swid_tag` **C**.
- Properties: `glide.discovery.file_discovery.wildcard.windows` (additive), `glide.discovery.file_discovery.blacklist.windows` (hard filter) **C**.
- Content sync ~24h; default monthly; library file-signature rules **beat** custom rules **C**.

### 4.4 Third-party IRE insert

- Enable `com.snc.samp.ire.datasource.integration`; role `sam_developer` **C**.
- Send a related record to `cmdb_sam_sw_install` on the parent computer CI; payload keys `publisher`, `version`, `display_name` (+ optional edition); identify the parent by `name`; send `sys_class_name` to prevent reclassification **C**.
- IRE gates apply: `cmdb_ire_data_source_rule` can block inserts; partial payloads park in `cmdb_ire_partial_payloads`; plain `createOrUpdateCI()` fails whole batches **C**.
- **Uninstall is not propagated.** The third party must DELETE install rows via Table API **V**.

### 4.5 Insert vs update matrix (SAM scope)

| Incoming item | Match key | Insert when | Update when | Control that can stop the insert |
|---|---|---|---|---|
| Software installation | source-specific; duplicates allowed across sources | always possible | same-source refresh (`U`) | exclude-CI flag; dedup `active=false` |
| Discovery model | Publisher + Display name + Version **V** | rule finds no model | rule finds model → set `discovery_model` | name contains `Security Update`; cannot create manually |
| Software model | version/edition/language/platform/install condition **V** | no match + auto-create property on | reconciliation reuses existing | leave auto-create off; published-product list affects reporting only |
| Entitlement | PPN, else publisher+product+version+edition+platform+language **V** | import creates | PPN maps to existing model | PPN errors; MLS blank PPN will not invent a model |
| Allocation | entitlement + user/device | create | quantity/cores re-evaluated | cannot exceed rights |
| Catalog item | vendor item / model publish **V** | publish/link | vendor-item sync after publish | do not publish |

### 4.6 Duplicates and dedup

Duplicate installs arise when the **same publisher+product+version+edition** is seen by **multiple sources** **V**.

**Version levels** **V**:

| Level | Duplicate test | Use for |
|---|---|---|
| `Exact` | full normalised version + edition identical | discrete lifecycles |
| `Major` (default) | major version identical (`2019.1` = `2019`) | most enterprise software |
| `Any` | ignore version; one install per product+edition per device | auto-updating software (Chrome) |

**Primary selection, in order** **V**: (1) discovery-source reliability, (2) information completeness, (3) latest version. Custom rule table `sam_sw_dedup_rule`, fields `product`, `active`, version level, stale threshold **V**. A rule can only be assigned to a **normalised software model** **V**.

**IBM special case:** ServiceNow Discovery installs stay `active=true`; duplicates from an authorised provider are set `active=false` by `SAM - Deduplicate Install Table` **V**.

---

## 5. Normalisation — the six statuses and every transition

### 5.1 The status field and its values

- Table: `cmdb_sam_sw_discovery_model` **V**. UI label: **Normalization status**. Internal column: `U:norm_status` (docs publish the label only).
- Values **V**:

| # | Status | Meaning | Reconcilable? | Manual normalise allowed? | Revert allowed? |
|---|---|---|---|---|---|
| 1 | `New` | Created, normaliser has not run | No (not yet) | Not listed — wait for job | n/a |
| 2 | `Match Not Found` | No rule matched | No | **Yes** | n/a (already base) |
| 3 | `Publisher Normalized` | Publisher matched only | Partial | **Yes** | **Yes** → Match Not Found |
| 4 | `Partially Normalized` | Publisher + product matched; version missing/editable | Partial | **Yes** | **Yes** → Match Not Found |
| 5 | `Normalized` | Publisher + product + version (or publisher+product for Not Licensable/Child/Driver/Patch) | **Yes** | No (already done) | **Yes** → Match Not Found |
| 6 | `Manually Normalized` | Human set the values | **Yes** | — | **No** |

> **Answer to "are there 4 statuses?"** The four *automatic outcomes* are `Match Not Found`, `Publisher Normalized`, `Partially Normalized`, `Normalized`. The field actually carries **six** values because `New` (pre-run) and `Manually Normalized` (user-set) also exist. Foundation/Basic SAM, by contrast, only has `Manually Normalized` and `New` **C**.

### 5.2 Transition matrix

| From | Trigger | To | Side effects |
|---|---|---|---|
| New | daily content job | Normalized / Partially / Publisher / Match Not Found | normalised columns written |
| Match Not Found | manual normalise | Manually Normalized | suggestion record created |
| Partially / Publisher | manual normalise | Manually Normalized | suggestion record created |
| Normalized | edit a read-only field | Manually Normalized | values diverge from package/pattern |
| Any | change **Product type** | Manually Normalized **V** | reconciliation eligibility may change |
| Manually Normalized | accept suggestion / auto-accept property | Normalized **V** | Publisher/Product/Version/Edition/Platform/Language copied; `Normalization date` updated; suggestion = Accepted |
| Manually Normalized | reject suggestion | Manually Normalized **V** | suggestion = Rejected |
| Normalized / Partially / Publisher | `Revert Normalization` | Match Not Found **V** | all normalised fields reset; associated rules deactivated |
| Manually Normalized / pattern-normalised | revert attempt | unchanged **V** | not permitted |

### 5.3 Manual normalisation paths

- Workspace: `Software asset > Software Asset Workspace > License operations > Discovery models` → record → ellipsis → **Normalize**; role `sam_admin` or `sam_user` **V**.
- Classic: `All > Software Asset > Discovery > Discovery models` → open a record in Partially/Publisher/Match Not Found → fill Publisher, Product, Version (create a custom product from the lookup if needed) → Save; role `sam_user` **V**.
- Product-type change also lands in `Manually Normalized` **V**.

### 5.4 Normalisation suggestions

- Generated for every manually normalised discovery model, weekly **V**.
- Table `samp_normalization_suggestion` **V** (the overview page calls it `samp_normalization_suggestions` **V** — a docs inconsistency).
- Fields: Discovery model, Suggestion status, Discovered publisher/product/version, Suggested publisher/product/version/edition/platform/language, Publisher/Product/Version/Edition/Platform/Language (normalised) **V**.
- Accept → model becomes `Normalized`, values copied, suggestion `Accepted`, `Normalization date` updated **V**.
- Reject → stays `Manually Normalized`, suggestion `Rejected` **V**.
- Auto-accept: `com.snc.samp.auto_accept_normalization_suggestion` default **enabled**; accepts only when there are no differences **V**. Domain-separated domains can override with `sys_application_property` **V**.

### 5.5 Rule families and precedence

| Family | Scope | How it works | When it wins |
|---|---|---|---|
| **Product Map / Package Map** | one rule per distinct discovery model (Content Service) | exact mapping of discovered → normalised values | first, exact |
| **Pattern normalization** | one rule covers many models | substring/pattern match on discovered publisher/product | after product/package map |
| **Enhanced pattern normalization** | complex variants | include/exclude terms for edition/version; conditional mapping | extends pattern rules |
| **Wide-net normalization** | eligible products only | groups similar discovered values without per-product rules | fallback after content rules; `com.snc.samp.wide_net_normalization.enabled` default on |
| **ML normalization** | plugin `com.sn_sam_ml_normalization` / property `com.snc.samp.enable.ml_normalization` default on | predicts values for unmatched models | fallback after wide-net |

Custom pattern rule form (`All > Software Asset > Administration > Pattern Normalization Rules`, role `sam_admin`) **V**: Name, Discovered publisher contains, Discovered product contains, Active, Discovered publisher is empty, Normalized Publisher/Product/Edition/Product type/Version/Platform/Language; **Apply Rule** to run immediately. Create custom product/publisher records first **V**.

### 5.6 Content Service

- Default **off**; opt in from Configuration Console or Content Service Setup **V**.
- Shares only the listed data types; discovery models shared for statuses Match not found / Publisher normalized / Partially / Manually / (Normalized with empty version) **V**.
- Exclusions: `Exclude from content service` on discovery model, custom product, custom PPN **V**. NSC DOD IL5 can only receive content, not send **V**.
- Deactivating a Normalization Library content version removes its rules **V**.

---

## 6. Software model normalisation — matching, reclassification, model↔vendor

### 6.1 Two different "normalisations"

| Term | Object | What is normalised |
|---|---|---|
| **Discovery-model normalisation** | `cmdb_sam_sw_discovery_model` | Raw discovered publisher/product/version/edition → canonical values |
| **Software-model matching** | `cmdb_sam_sw_discovery_model.software_model` | Normalised discovery model → purchasable `cmdb_software_product_model` |

Both must succeed before a clean licence position.

### 6.2 Matching job `SAM – Discovery Model to Software Model matching`

- For each normalised publisher+product pair, gets software models with matching publisher/product **V**.
- If the model has no install condition / subscription condition / DB option, matching uses edition and version **V**.
- Most **specific** model wins; if none, most **generic** **V**.
- If the best match has an install condition that fails, it is **not** a match; an auto-created model may be used instead **V**.
- Writes `software_model`; a manual set makes `Automatically matched = false` and the job will not override **V**.

### 6.3 Reclassification (what can change class/identity)

| Change | Effect | Table |
|---|---|---|
| Product type (e.g. Unknown → Licensable) | Status → **Manually Normalized**; reconciliation eligibility changes | `cmdb_sam_sw_discovery_model` |
| Manual software-model choice | `Automatically matched=false`; job stops overriding | `cmdb_sam_sw_discovery_model` |
| Edition override on install | Allows reconciliation when edition was missed | `cmdb_sam_sw_install` |
| Dedup re-level (Exact/Major/Any) | Primary install can change | `sam_sw_dedup_rule` |
| Suite inference (`com.snc.sam.auto_suite_inference`) | Installs map to suite entitlement | property |
| PPN/model correction | Future imports resolve correctly; re-run reconciliation | `alm_license`, `cmdb_software_product_model` |

There is no IRE-style class-move (upgrade/downgrade/switch) for `cmdb_sam_sw_install`; the CMDB class-move rules belong to `ALT_PARALLELSWARM`.

### 6.4 Suite handling

- Suite parent / suite component related lists on the software model; discovery maps can auto-build components **V**.
- Reclamation rules on a suite parent automatically pull components/product processes; editing the parent rewrites children; **you cannot edit children while the parent is present** **V**.
- `com.snc.sam.auto_suite_inference` default **false**; when true, installs map to the suite entitlement **V**.
- Suite over-count is a top cause of inflated rights used; `Omit from suites` on an install is the per-row control **V**.

### 6.5 Model vs vendor — operational rules

- Publisher must relate to `core_company`; a company record can exist without being a SAM publisher, and vice versa **C**.
- Vendor Catalog Item links procurement data to the model; it is **not** the publisher record **V**.
- Publishing a model to the software catalog creates a catalog item; editing the vendor item afterwards syncs to the catalog **V**.
- Contract vendor lives on the contract (`ast_contract`), not on the model; renewal reporting joins contracts/entitlements, not publishers **V**.

---

## 7. Licence position and compliance

### 7.1 Three result tiers **V**

| Tier | Table | Contains | Generated when |
|---|---|---|---|
| Product Results | `samp_product_result` | Per publisher+product: compliance, true-up, over-licensed, potential savings; related Software Model Results, Licensed/Unlicensed Installs, Unlicensed Subscriptions, Removal Candidates | Reconciliation runs; licensable products get results even without models |
| Software Model Results | `U:samp_sw_model_result` | One row per software model **only if** a model or entitlement exists; related License Metric Results, Remediation Options, installs, subscriptions, consumptions, Oracle options, Purchase Orders | Model/entitlement exists |
| License Metric Results | `samp_license_metric_result` | Rights owned/used/available, allocation breakdown, true-up, unlicensed counts | Per metric per model |

Two LMRs (and two licence-position reports) exist when a model has a perpetual-SA entitlement and a subscription entitlement — one with `active maintenance = true`, one false **V**.

### 7.2 Rights algebra (every bucket → remediation)

| Field (label) | Meaning | If > 0, remediation offered |
|---|---|---|
| Rights owned | Sum of active rights on entitlements sharing the metric | — |
| Rights used | allocated-in-use + not-allocated-in-use (installed) | — |
| Rights available | owned − used | — |
| Allocated in use | allocated and licensing an install | — |
| **Not allocated in use** | used but unallocated | **Create Allocations**, **Remove Unallocated Installs** (except User CAL / Device CAL) **V** |
| **Allocated not in use** | allocated but no install | **Remove Allocations** **V** |
| Not allocated | owned − allocated, regardless of install | — |
| Allocations needed | only Per Named User / Per Named Device | **Create Allocations** |
| **Unlicensed installs** | installs covered by no entitlement | **Purchase Rights**, **Remove Unlicensed Installs** |
| Rights needed | rights to cover unlicensed installs | — |
| Nontransferable rights | leftover core-pack rights (Microsoft Per Core / Per Core with CAL only) | — |
| Over-licensed amount | cost of unused rights | — |
| True-up cost | cost to remediate at the least rights needed | — |
| Potential savings | savings if removal candidates are reclaimed | — |

### 7.3 Licence types → reconciliation impact **V**

| Type | Publisher | Impact |
|---|---|---|
| Perpetual | all | No maintenance rights; add SA/maintenance for upgrades/BYOL/support |
| Perpetual + Software Assurance | Microsoft | SA benefits auto-applied |
| Subscription | all subscription products | Driven by subscriptions from the portal; also non-subscription products using subscription licences |
| Perpetual + Maintenance | non-Microsoft | Maintenance benefits auto-applied |
| Upgrade | all | Link lower→higher edition via Upgraded Entitlements |
| Software Assurance | Microsoft | **Not reconciled unless linked to a base perpetual** |
| Maintenance | all | **Not reconciled unless linked to a base perpetual** |
| Step-up / Subscription Step-up | all / subscription | Edition upgrade within term |
| Add-on / From SA | Microsoft | Must be linked to a perpetual Office legacy licence with active SA |
| Enterprise / ULA / ELA / ETLA / SCE | all | Stay **Compliant** even with unlicensed installs **C** |

### 7.4 Product type → reconciliation **V**

| Product type | Licensable | Reconciled |
|---|---|---|
| Licensable | yes | **yes** |
| Child | no | no |
| Driver | no | no |
| Not Licensable | no | no |
| Patch | no | no |
| Unknown | not until changed | no — changing to Licensable sets Manually Normalized |

`License under management` must also be selected (Australia **C**).

### 7.5 License-position report fields **V**

Software publisher, Software product, Edition, Version, **Software model status** (`Compliant` green dot / `Not Compliant` red dot), License metric, Total spend, Rights owned, Rights used, Rights needed, Rights available, Unlicensed installs, True-up cost, Potential savings, Over-licensed amount, Software model, Group, Subgroup.

### 7.6 Grouping

`com.snc.samp.recon.group` and `.subgroup` default **None**; values Company, Cost Center, Country, Department, Region; **group ≠ subgroup** **V**. Group/subgroup are also fields on Product/LMR results **V**.

---

## 8. True-up and over-licensing

- **True-up cost** = least rights needed × average price per right from entitlements; the lowest-cost **Purchase Rights** option **V**.
- **Over-licensed amount** = cost of unused rights **V**.
- Cost source order: software-model **License cost** or **License + maintenance cost**; if absent, **average entitlement cost** **V**.
- Creating an entitlement with a metric creates an **Override License Cost** record at **zero** if none exists; override it to get accurate true-up **V**.
- Oracle **Employee** metric true-up is reported for a one-year subscription period **V**.
- Never edit entitlement quantity to "fix" a position; add a true-up entitlement instead (community/curriculum guidance; not a product restriction).

---

## 9. Reclamation and optimisation

| Object | Table | Notes |
|---|---|---|
| Reclamation rule | classic `Administration > Reclamation Rules` **V** | Rule types: Total Usage Time (default), Last Used Date, Peak Concurrent Usage (engineering), Active Transaction Codes (SAP) **C** |
| Software usage | `samp_sw_usage` **V** | Product level, not version/edition; fields Publisher, Product, Reclamation type, CI, User, Month, Year, Usage count, Total seconds used, Last used time **V** |
| Removal candidate | `samp_sw_reclamation_candidate` **V** | Justification, state, active, potential savings |
| Reclamation flow | — | Timeout `sam_reclamation_flow_error_timeout` 30 days → Closed canceled **V** |
| CSD uninstall | `com.snc.orchestration.client_sf_distribution` **V** | SAM Pro licence covers **uninstall/reclamation only**; install/distribution needs extra licence |
| SaaS/SSO | `samp_sso_application` **V** | Creating a direct integration profile auto-creates a reclamation rule — review it **V** |
| Reclaim request | Service Catalog **V** | Fields Requested by/for, Employee separation, Asset, Reclaim date, Reclaim method, Legal hold method, Notes |

Rules aggregate usage over a period/minimum hours/latest date; suite parent pulls components; filter on the parent applies to children **V**.

**Usage caveat:** if a CI's Status or Hardware Status becomes Retired or Stolen, installations related to that CI are **deleted** **V** — this changes compliance counts and must be communicated.

---

## 10. Maintenance — add a new software model (step by step, every table/field)

Two entry paths. Choose A when a PPN exists; B when it does not or the product is custom.

### Path A — PPN-driven (preferred)

1. Confirm the PPN exists in the Content Library (`samp_sw_product_definition` **V**). If not, use Path B or create a custom PPN.
2. Import/create the entitlement with the PPN. Resolution **V**:
   - PPN found, one model → assign it;
   - PPN found, multiple models → error `Multiple software models found…` (human chooses);
   - PPN not found/inactive → exact publisher+product+version+edition+platform+language search; if found, entitlement is created without PPN; if not, auto-create (if enabled) or error `PPN and SM not found`.
3. Writes: `alm_license` (rights) → link to `cmdb_software_product_model` (existing or auto-created) → `samp_sw_product_definition` reference.
4. Verify `Created source` on the model; run reconciliation.

### Path B — manual

| # | Action | Table | Fields written |
|---|---|---|---|
| 1 | Decide publisher/product/version/edition/platform/language/install condition | — | — |
| 2 | If product absent from Content Library, create **Custom Software Product** (`Software Asset > Administration > Custom Products` or Workspace `License operations > Content > Custom software products`); role `sam_admin` **V** | custom product (table `U`) + `core_company` / `samp_sw_publisher` | Publisher, Product, Subscription software, Product type, Product classification (UNSPSC), Exclude from content service, Active |
| 3 | Create **Software Model** (`Software Asset > Licensing > Software Models` → New; role `sam_user`/`model_manager`) **V** | `cmdb_software_product_model` | publisher, product, version/version condition, edition/edition condition, platform, language, install condition, discovery map, `created_source=Manual` |
| 4 | Suite membership (if any) | suite parent/component related lists (`U` join) | parent↔child |
| 5 | Metric Attributes → metric group | `cmdb_software_product_model` metric attributes related | `metric_group` (entitlements inherit it) |
| 6 | Vendor association / catalog link (optional) | Vendor Catalog Item related (`U` table); `sc_cat_item` on publish | vendor item, catalog item |
| 7 | Client Access (CAL/Citrix) | client access records | user/device access |
| 8 | Downgrade Rights | `samp_sw_downgrade_model`, `samp_dmap_downgrade_model`, `samp_downgrade_model` | downgrade versions (auto from discovery map if present) |
| 9 | Product Lifecycles | `sam_sw_product_lifecycle`, `sam_custom_sw_product_lifecycle` | publisher, product, edition, version, phase, dates |
| 10 | Publish to Software Catalog (optional) | `sc_cat_item` | Category=Software; currency via `glide.model.catalog_item_currency` |
| 11 | Create/import **Entitlement** | `alm_license` | PPN, license type, license metric, rights, start/end, license duration, state, company, cost, license cost, license + maintenance cost, metric group, subscription period, agreement type, upgraded entitlements |
| 12 | Publish entitlement → **In use** | `alm_license` state | eligible for reconciliation |
| 13 | Allocations (if named user/device or CAL) | `alm_entitlement_user` **or** `alm_entitlement_asset` | user/device, quantity/cores |
| 14 | Run matching job / reconciliation | discovery model `software_model`; result tables | `Automatically matched`, results |

**Automated alternative:** enable `com.snc.samp.automaticsmrcreation` (licensable) / `com.snc.samp.automaticsmcreation` (not licensable) / `com.snc.samp.unlicensed_smr_creation` (results only) **V**. Auto-created models are created **across versions for a specific edition, never against a specific version**, attach a discovery map only if one exists, and are flagged `Created source = System property` **V**. Recommendation: leave auto-create **off** during Crawl so the model table stays curated.

---

## 11. Maintenance — normalise a software model (operational runbook)

1. **Triage.** Workspace `Software Asset Workspace > Software asset analytics > Normalization and content` or the "Software installs normalization status" widget. Pull counts by status from `cmdb_sam_sw_discovery_model`.
2. **Let automation run first.** Confirm the two daily jobs completed. Check fallbacks enabled (wide-net, ML).
3. **Pattern rule** for a family of variants (e.g. `Microsoft Office 2019*`): create rule, **Apply Rule**. Use enhanced pattern for edition/version synonyms.
4. **Manual normalise** only Partially / Publisher / Match Not Found. Fill Publisher/Product/Version. Result: `Manually Normalized`.
5. **Handle suggestions.** Review `samp_normalization_suggestion`; Accept (→ `Normalized`) or Reject (stays). Check `com.snc.samp.auto_accept_normalization_suggestion` before bulk review.
6. **Revert if wrong.** Only Normalized / Partially / Publisher can revert → `Match Not Found`; Manually and pattern-normalised cannot. Reverting deactivates associated rules.
7. **Re-match the model.** Let `SAM – Discovery Model to Software Model matching` run; if a manual model is correct, leave `Automatically matched=false` so it is not overridden.
8. **Re-run reconciliation** for affected publisher/group. Verify Product → Model → Metric results.
9. **Reclassify product type** where needed (Unknown → Licensable). This forces `Manually Normalized` — re-check reconciliation participation.
10. **Content Service feedback.** For recurring misses, opt in / submit a content request; custom products are an interim fix, not a substitute for content.

**Do not** edit the normalisation job, the status choice values, or the install business rule. **Do** extend through pattern rules, custom products, custom PPNs, and metrics.

---

## 12. Workspaces, dashboards, and reports

### 12.1 Software Asset Workspace — views **V**

| View | What it answers |
|---|---|
| **Software asset overview** | Landing: compliance trend, true-up, savings, normalisation rate, alerts |
| **License usage** | Compliance by publisher; License Workbench; reconciliation drill-down; reclaim |
| **License operations** | Entitlements, software models, import errors, discovery models, user subscriptions, engineering apps, contracts, IBM ASP/ILMT |
| **Software asset analytics** | Consolidated analytics: SaaS, discovered inventory, optimisation, lifecycle, cloud cost simulator, engineering licence, normalisation/content |
| **Success portal** | Goals, health check, value builder, Crawl/Walk/Run maturity |
| **Renewals calendar** | Entitlements/contracts nearing or past expiry |
| **Overlapping usage** | Feature-level SaaS/SSO usage |
| **Content Library portal** | Data in the SAM Content Service |

### 12.2 Software asset overview widgets → source **V**

| Widget | Source table |
|---|---|
| Publishers out of compliance | `samp_product_result` |
| Products out of compliance | `samp_product_result` |
| Over-licensed amount | `samp_product_result` |
| Expiring maintenance and subscription | `alm_license` |
| Total true-up cost | `samp_product_result` |
| Top 5 publishers true-up cost | `samp_product_result` |
| Potential savings | `samp_product_result` |
| Actual savings | `samp_sw_reclamation_candidate` |
| Software spend | `samp_license_metric_result` |
| Software installs normalization status | `cmdb_sam_sw_discovery_model` |
| End of life products | `sam_sw_product_lifecycle` |
| Activity center | `samp_ws_activity_center_items`, `samp_normalization_suggestion`, `samp_sw_unrecognized_subscription_identifier`, `sc_request`, `samp_reconciliation_result`, `samp_job_log`, `samp_entitlement_import`, `samp_bulk_import`, `sn_samp_vr_cpe_mapping_suggestion`, `ast_contract`, `alm_license`, `samp_sso_application`, `sam_sw_product_lifecycle_report`, `samp_sw_product_definition`, `samp_demand` |

### 12.3 Other dashboards / reports

| Surface | Metrics / notes | Source |
|---|---|---|
| **Normalization and content** (PA) | % normalized installs; installs by status; CDS Download Status (Name, Current count, Expected count, Last updated on, Next action) | `cmdb_sam_sw_discovery_model`; CDS status **V** |
| **License Workbench** | All Publishers / Out of Compliance / Pinned; navigation tree; total spend, true-up, over-licensed, potential savings, agreement type; Rights Used By / Rights Needed By / Licensed Installs / Installs Used / Downgrades-Upgrades / Licensed Subscriptions / Cloud Special Rights | results + `alm_license` **V** |
| **License Position** | Per-model compliance list with green/red dot, financials | results **V** |
| **Removal Summary / Optimization** | Removal candidates by justification; potential vs actual savings | `samp_sw_reclamation_candidate` **V** |
| **Compliance Summary / License Summary** | Publisher/product compliance | `samp_product_result` |
| **Publisher Analytics** | Citrix, IBM, Microsoft, Oracle, SAP, VMware (pack required) | pack tables **V** |
| **Office 365 / Adobe Cloud** | Pack dashboards | pack tables **V** |
| **SaaS dashboards** | Subscriptions, usage, overlap | `sn_sam_saas_int` tables, `samp_sso_application` |
| **Lifecycle report** | EOS/EOES/EOL, installs | `samp_sw_product_lifecycle_report` **V** |
| **Success portal** | SAM maturity; completed/total/projected savings; all goals; health checks passed; completed value-builder tasks; open activities | goals, `samp_job_log`, health **V** |
| **Health Check** | Suites: SQL Server Config/CMDB, Windows Server Config/CMDB, Oracle Database, Java-Oracle, WebLogic-Oracle, Microsoft 365, General; Scan Findings → tasks | health app; weekly `SAM - Trigger Full Scan` **V** |
| **Renewals calendar** | Entitlements/contracts expiring | `alm_license`, `ast_contract` **V** |
| **Overlapping usage** | Feature-level SaaS/SSO usage | SSO/SaaS tables **V** |
| **CMDB success advisor for SAM** | Install data-quality metrics + remediation; opens from "Review CMDB data quality" alert | `samp_ws_activity_center_items` **V** |

**Reporting gap closed in this pass:** the earlier fleet docs named Success portal widgets but not the source tables; the table above ties every widget to a table.

---

## 13. Integrations (plugin → direction → target → uninstall behaviour)

| Integration | Plugin / app | Direction | Target | Notes |
|---|---|---|---|---|
| ServiceNow Discovery | Discovery (required) | in | `cmdb_sam_sw_install` | Patterns incl. SQL Server, Exchange, Oracle DB, vCenter, Citrix **V** |
| File-Based Discovery | `com.snc.discovery.file_based_discovery` + `com.snc.file_signature_normalization` | in | `cmdb_sam_sw_install`, file tables | Library signatures beat custom **C** |
| SCCM 2012 v2 / 2016 | `com.snc.integration.sccm2012v2`, `com.snc.integration.sccm2016` | in | installs | Deprecated Tokyo; use SGC **V** |
| SCCM usage | `com.snc.samp_usage_sccm`, `com.snc.samp.usage_sccm_2016` | in | `samp_sw_usage` | Deprecated **V** |
| Service Graph connector for Microsoft SCCM | Store app | in | CMDB + installs | Recommended new path; Migration Readiness Tool **V** |
| Intune / Jamf / Tanium | Service Graph connectors | in | CMDB | Not native SAM install sources **C** |
| ILMT / BigFix Inventory | IBM pack; `sn_samp_ibm_lic.ilmt_api_version` | in | IBM usage/PVU | v2 APIs for new work **C** |
| SaaS License Management | `sn_sam_saas_int` | in | subscriptions | Requires `com.snc.samp`; creates subscriptions not installs **V** |
| SSO integration | SaaS LM | in | `samp_sso_application` | Do not attach SSO **and** a direct profile to the same app **C** |
| Software Spend Detection | `com.sn_sam_spend` | in | spend transactions | `sam_spend_import` role **V** |
| Procurement | `com.snc.procurement` | out | purchase orders | Purchase receipts can create entitlements **V** |
| Procurement Integration | `app-itam-procurement-integration` | both | POs/entitlements | Import-error alerts **V** |
| Client Software Distribution | `com.snc.orchestration.client_sf_distribution` | out | uninstall | Uninstall only under SAM Pro **V** |
| Engineering apps | `sn_samp_eng_app` + OpenLM / Open iT | in | concurrent/peak usage | `com.snc.samp.eng.app.peak.usage.period` 30 **V** |
| SAP | SAP pack | in | SAP named users/transactions | SAP Connections menus **V** |
| Citrix | Citrix pack | in | Citrix Delivery Controller | Schedule required for licence server data **V** |
| Third-party IRE REST | `com.snc.samp.ire.datasource.integration` | in | `cmdb_sam_sw_install` | Role `sam_developer`; DELETE required for uninstalls **C** |
| HAM / contracts | shared `alm_asset`, `ast_contract` | shared | renewals | Same contract hierarchy as HAM **C** |
| Content Service | CDS | both (opt-in) | content library | Default off; NSC IL5 receive-only **V** |
| AI / Otto | `sn_now_assist_sam`; Now LLM / Azure OpenAI / Gemini / Claude | assist | requests, reclamation, contracts | Domain separation supported **V** |

---

## 14. Parameter inventory

### 14.1 Must-consider (decide before go-live)

| # | Parameter | Default | Why it matters | Blast radius |
|---|---|---|---|---|
| 1 | `com.snc.samp.automaticsmrcreation` | opt-in | Auto-creates models for unlicensed licensable installs | Model sprawl if on in Crawl; leave **off** |
| 2 | `com.snc.samp.automaticsmcreation` | No | Auto-creates not-licensable models (APM) | Same |
| 3 | `com.snc.samp.unlicensed_smr_creation` | False | Creates model results for unlicensed models | Changes position volume |
| 4 | `com.snc.samp.manage.published.products` | false | Phase-wise reporting scope | Reports ignore unpublished products |
| 5 | `com.snc.samp.exclude_device_flag` | empty | Boolean column on `cmdb_ci_hardware` | Excludes devices from compliance |
| 6 | `com.snc.samp.recon.group` / `.subgroup` | None | Default reconciliation grouping | Re-run recon after change; group ≠ subgroup |
| 7 | `com.snc.samp.wide_net_normalization.enabled` | enabled | Fallback normalisation | Turning off increases Match Not Found |
| 8 | `com.snc.samp.enable.ml_normalization` | enabled | ML fallback | Same |
| 9 | `com.snc.samp.auto_accept_normalization_suggestion` | enabled | Auto-accept identical suggestions | Silently moves Manually→Normalized |
| 10 | `com.snc.samp.auto_suite_inference` | false | Maps installs to suite entitlement | Over/under-counts suites |
| 11 | `com.snc.samp.recon.enablecustommetrics` | Yes | Custom metric participation | Custom metrics ignored if No |
| 12 | `com.snc.samp.recon.max_workers` | unset | Parallel publisher jobs | Too high starves the instance |
| 13 | `com.snc.samp.debug` | No | Reconciliation/import debug | Performance hit |
| 14 | `com.snc.samp.oracle.reconlevel` | ESX cluster | Oracle/WebLogic aggregation | Large licence swings |
| 15 | `com.snc.samp.oracle.hostaffinityenabled` | opt-in | VM-host affinity | Requires vCenter(s) level |
| 16 | `com.snc.samp.ire.datasource.integration` | — | Enables third-party IRE inserts | Duplicate/untrusted installs if opened carelessly |
| 17 | `glide.discovery.software_sccm_managed` | false | Stops Discovery writing software for SCCM machines | Double-sourcing |
| 18 | `glide.discovery.enable.software_simplify` | true | Normalises names/versions at discovery | Off → duplicate installs |
| 19 | `glide.discovery.discover_software` | true | Master software discovery switch | Off → no installs from Discovery |
| 20 | `sn_sam_workspace.sam_license_operations_list_count` | 5,000,000 | Workspace list cap | Hides exact counts above cap |

### 14.2 Full property list (docs-named, defaults as printed) **V**

**Reconciliation / models**
`com.snc.samp.recon.group` (None) · `com.snc.samp.recon.subgroup` (None) · `com.snc.samp.recon.enablecustommetrics` (Yes) · `com.snc.samp.debug` (No) · `com.snc.samp.recon.max_workers` · `com.snc.samp.automaticsmrcreation` · `com.snc.samp.automaticsmcreation` (No) · `com.snc.samp.unlicensed_smr_creation` (False) · `com.snc.samp.auto_suite_inference` (false) · `com.snc.samp.exclude_device_flag` · `com.snc.samp.manage.published.products` (false) · `com.snc.samp.wide_net_normalization.enabled` (on) · `com.snc.samp.enable.ml_normalization` (on) · `com.snc.samp.ml.overrride_ml_model_version` (docs spelling) · `com.snc.samp.auto_accept_normalization_suggestion` (on)

**Cost / lifecycle**
`com.snc.samp.use_lifecycle_approximation` (on) · `com.snc.samp.generate.calculated.lifecycles` · `com.snc.samp.sam_ci_billing_threshold` (30) · `com.snc.samp.citrix.app.license.period` (90) · `com.snc.samp.eng.app.peak.usage.period` (30) · `sam_reclamation_flow_error_timeout` (30) · `com.snc.samp.windowserver.license.threshold` (4.59) · RHEL VDC threshold (3.2; internal name `U`) · `com.snc.samp.sqlserver.standard_sa.to.enterprise_sa.cost.ratio` (0.25) · `com.snc.samp.ms.sa.to.nonsa.cost.ratio` (1.25) · `samp.spend_prediction_service.max_label_attempts` (3) · `glide.model.catalog_item_currency` (false)

**Oracle / IBM / domain**
`com.snc.samp.oracle.reconlevel` (ESX cluster) · `com.snc.samp.oracle.hostaffinityenabled` · `sn_samp_ibm_lic.default_region` (North America and South America) · `sn_samp_ibm_lic.ilmt_api_version` · `com.snc.samp.ire.datasource.integration` **C** · `com.snc.samp.manage.published.products` application property per domain (needs `com.glide.domain.msp_extensions.installer`)

**Workspace / UI**
`sn_sam_workspace.sam_license_operations_list_count` (5,000,000)

**Discovery-side (changes what SAM receives)**
`glide.discovery.discover_software` (true) · `glide.discovery.enable.software_filter` (true) · `glide.discovery.software_filter_keys` (`Language Pack, Hotfix Security Update`) · `glide.discovery.enable.software_simplify` (true) · `glide.discovery.enable.software_simplify_sccm` (false) · `glide.discovery.software_sccm_managed` (false) · `glide.discovery.populate_software_instance_table` (false) · `glide.discovery.sam_batch_update_size` (100) · `glide.discovery.file_discovery.wildcard.windows` · `glide.discovery.file_discovery.blacklist.windows` · `glide.discovery.enable_file_tracking` (true) · `glide.discovery.file_tracking.max_file_size` (500000) · `glide.discovery.file_tracking.max_files_per_ci` (50) **C/V**

### 14.3 Per-screen parameters

**Discovery schedule (software-relevant):** Discover = **Configuration items** (IP scan never writes CIs) · MID selection · Max run time · Max Idle time · Shazzam batch size · SNMP version · Location · Active · Run options (On Demand/Daily/Weekly/Monthly/Periodically/Once/After Discovery) · max concurrent invocations (3). **C/V**

**Software Model form:** publisher, product, version/version condition, edition/edition condition, platform, language, install condition, discovery map, suite parents/components, metric attributes, created source, license cost, license + maintenance cost, license under management, vendor catalog item, client access, downgrade rights, product lifecycles. **V**

**Entitlement form:** PPN, license type, license metric, rights, start/end, license duration, state, company, cost, license cost, license + maintenance, metric group, subscription period, agreement type, upgraded entitlements, allocations. **V**

**Discovery Model form:** normalization status, publisher/product/version (normalised), discovered publisher/product/version, product type, platform, language, edition, full version, exclude from content service, software model, automatically matched, normalization date, approved. **V**

**Installation form:** display name, discovery model, publisher, version, edition override, installed on, install location/date, instance key, uninstall string, ISO serial, active, inferred suite, omit from suites. **V**

**Dedup rule:** product, active, version level (Major default / Exact / Any), stale record threshold (days). **V**

**Pattern rule:** name, discovered publisher contains, discovered product contains, active, discovered publisher is empty, normalized publisher/product/edition/product type/version/platform/language. **V**

**Custom product:** publisher, product, subscription software, product type, product classification (UNSPSC), exclude from content service, active. **V**

**Reclamation rule:** applies to (Installed/Subscription Software), software products, product processes, filter condition, usage threshold/date. **V**

**Allocation:** user/device, quantity, core count behaviour (exact/less/more), host vs VM, cluster warning. **V**

### 14.4 Property families that are **not** official

`glide.cmdb.sam.*` is not a documented family in the Australia properties page **C** — do not script against it. Use `com.snc.samp.*`, `sn_sam_workspace.*`, `sn_samp_ibm_lic.*`, `samp.*`.

---

## 15. Verification checklist (day-1, no purchase order)

1. `cmdb_sam_sw_install` row exists for a test CI, with `discovery_model` set.
2. Discovery model status is not `New` after the daily job; if `Match Not Found`, normalise or add a pattern rule.
3. `software_model` is populated and `Automatically matched` reflects whether a human intervened.
4. Software model has `License under management` and a Licensable product type.
5. Entitlement state is `In use`; rights > 0; metric group set.
6. Reconciliation produces Product → Software Model → License Metric results with non-zero rights owned.
7. License Position shows Compliant/Not Compliant with a true-up figure (not blank).
8. `samp_job_log` has no failed `SAM*` jobs; CDS status counts match expected.
9. Normalization and content dashboard % is rising; `Match Not Found` trend falling.
10. Test a reclaim: usage record → candidate → removal candidate appears in overview.

---

## 16. Anti-patterns

- Treating a **discovery model** as a catalog item, a **catalog item** as a licence, or a **vendor** as a publisher.
- Discovering before entitlements when PPN-driven model creation was the intent.
- Enabling `automaticsmrcreation` in Crawl, then mass-deleting models.
- Editing entitlement quantity instead of adding a true-up.
- Reconciling `Match Not Found` or non-licensable rows and trusting the number.
- Leaving uninstalled rows in `cmdb_sam_sw_install`; counts inflate.
- Assuming reconciliation is nightly (Brazil: weekly + on demand).
- Treating maintenance/SA as a licence without a base perpetual.
- Publishing all publishers on day one instead of phase-wise.
- Adding both SSO and a direct SaaS profile for the same app.
- Customising the normaliser/matching/dedup jobs instead of extension points.
- Building on `glide.cmdb.sam.*` (not a real family).

---

## Appendix A — `U` (instance-verify) list

| Item | Query to settle |
|---|---|
| Discovery-model status column | `sys_dictionary.list?sysparm_query=name=cmdb_sam_sw_discovery_model^elementLIKEstatus` |
| `automatically_matched`, `approved`, `normalization_date`, `edition_override` | `sys_dictionary` on the respective table |
| Software Model Results table | `sys_db_object.list?sysparm_query=nameLIKEsamp^nameLIKEresult` |
| Custom product / pattern rule / reclamation rule tables | inspect form's table via `sys_db_object` or list URL |
| Install→discovery-model business-rule name/sys_id | `sys_script.list?sysparm_query=collection=cmdb_sam_sw_install` |
| UI policies / client scripts / ACLs on SAM tables | `sys_ui_policy`, `sys_script_client`, `sys_security_acl` filtered `sam`/`samp` |
| Vendor catalog item table | `sys_db_object.list?sysparm_query=nameLIKEvendor_cat` |
| RHEL VDC threshold internal name | `sys_properties.list?sysparm_query=value=3.2^nameLIKEsamp` |
| Default reconciliation cadence on this instance | inspect the scheduled job record, not the docs |

## Appendix B — source ledger

Brazil ITAM map `PMOYmdGTPDs40EbYh10h4g`; local corpus `agents/grok-4.6__xai__kilo/SNC_SAM__WT1/research/raw/`. Primary pages used:

`software_normalization`, `manually_normalize_classic`, `manually_normalize_workspace`, `normalization_suggestions`, `normalization_and_content_dashboard`, `discovery_models_fields`, `discovery_models_and_installs`, `software_discovery`, `software_installation_fields`, `software_install_deduplication`, `duplicate_software_installations`, `model_relationship_to_install`, `software_models_and_entitlements`, `software_license_metrics`, `software_model_results_lmr_fields`, `license_compliance_position`, `software_reconciliation_for_compliance`, `software_reconciliation_results`, `impact_license_types_on_recon`, `true_up_cost`, `software_reclamation_rules`, `allocation_management`, `sam_properties`, `software_asset_overview`, `software_asset_workspace`, `components_installed_sam_pro`, `sam_installation_methods`, `sam_content_service`, `software_license_usage`, `view_or_create_software_usage`, `exclude_software_assets_on_cis`, `remove_uninstalled_software`, `software_request_workflow`, `catalog_request_to_reclaim`, `create_software_models_classic`, `add_custom_software_product_classic`, `add_software_pattern_normalization_rule`, `automatic_creation_of_software_models`, `create_custom_dedup_rule`, `exploring_sam`, `sam_overview`, `configuring_sam`, `sam_health_check`, `run_health_check_scan`, `ai_in_sam`, `success_portal`, `maturity_stages_sam`, `maturity_items`, `maturity_item_details`, `request_software_asset_management`, `publish_domain_specific_property`, `publish_specific_set_of_products`, `remove_published_software_products`, `publish_models_to_hw_or_sw_catalog`, `link_item_to_software_catalog`, `create_success_goals`, `sam_landing`.

Australia corroboration: `CONFIG_INVENTORY_AUSTRALIA.md`; `ALT_PARALLELSWARM/research/servicenow-discovery/DISCOVERY_END_TO_END_GUIDE.md` (FBD, software properties, IRE).
