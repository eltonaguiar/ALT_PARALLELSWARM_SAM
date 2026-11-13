# FINAL — ServiceNow SAM (Software Asset Management) Configuration Reference

**Compiled by:** `sam-research` / provider **Freebuff (Codebuff)** / harness **kilo-cli**  
**Date:** 2026-11-13  
**Release basis:** Official `docs.servicenow.com` **Xanadu / Yokohama / Zurich** (pinned per page)  
**Purpose:** Exhaustive configuration reference for the ServiceNow Software Asset Management (SAM) module, following the same methodology as the CMDB/Discovery reference in `ALT_PARALLELSWARM`.

---

## 0. Evidence policy + release scope

Sources were fetched from ServiceNow product documentation (Australia/Xanadu/Yokohama/Zurich maps), Now Learning outlines, Now Create Success Pack public outlines, ServiceNow Store listings, Support KB, and the `ServiceNow_Learning` / `ServiceNow_Learning_TSOM` repos. Every non-obvious claim carries `[S<n>]` mapping to the evidence digest in `research/EVIDENCE_DIGEST.md`. Anything not directly sourced is marked **UNVERIFIED** and listed in Section 17. Professional-only features flagged with ⚠️.

**Primary sources (32):**
- [S1] SAM Implementation Best Practices (ebook)
- [S2] SAM Implementation Best Practices White Paper
- [S3] Performance, KPIs, and Metrics Guide
- [S4] CoreIO: Crawl, Walk, Run SAM
- [S5] Community: Hand Book to Kick Start SAM
- [S6] Community: Guidance on SAM PRO License Renewal
- [S7] Components installed with SAM Professional (Xanadu)
- [S8] Configure SAM using Configuration Console (2026-09-10)
- [S9] SAM Guided Experiences (Yokohama)
- [S10] Microsoft 365 Optimization with SAM Pro (2026-06-26)
- [S11] SAM Publisher Packs Data Sheet
- [S12] Software normalization (Xanadu)
- [S13] Software discovery and normalization (Zurich)
- [S14] SAM Content Service (Xanadu)
- [S15] Add pattern normalization rule (Yokohama)
- [S16] Fix "Match Not Found" with Pattern Normalization (video, 2026-05-28)
- [S17] SAM Process Guide (Paris)
- [S18] Software reconciliation for compliance (Xanadu)
- [S19] Software license metrics (Xanadu, 2026-09-10)
- [S20] Discovery models and software installations
- [S21] Normalization statuses (Yokohama, 2025-01-30)
- [S22] Community: Software Installation Normalization fields
- [S23] Community: SAM Pro reconciliation jobs (Yokohama, 2026-01-06)
- [S24] Basic SAM Configuration (Japanese blog, 2026-08-25)
- [S25] CIS-SAM Exam Study Guide
- [S26] Explained: SAM System Properties (2023-02-02)
- [S27] Configure scheduled jobs (Config Console)
- [S28] Learning repo: 08-SAM-SETUP.md (2026-11-04)
- [S29] Learning repo: 03-breadcrumbs.md (2026-11-04)
- [S30] Learning repo: 04-fields.md (2026-11-04)
- [S31] Learning repo: sam_readiness.py (2026-11-04)
- [S32] Learning repo: sn_probe.js (2026-11-04)

---

## 1. Mental model: 3 SAM gates, and where normalisation/reconciliation sit

SAM has **three hard gates** that must be cleared before any compliance number is defensible [S1][S2][S28]:

| Gate | Why it is hard | How the probe sees it |
|---|---|---|
| **SAM schema + entitlement** | No tables, no reconciliation. Foundation and Professional are different products | `samp_*` / `cmdb_sam_*` tables present |
| **CMDB populated, with identification rules** | Duplicate CIs double-count installs. Note: identification rules are a **CMDB/IRE** mechanism, not SAM configuration | `cmdb_ci` row count; CI Identifiers configured |
| **A discovery / connector feed** | Hand-typed installs are an asset register, not SAM | Discovery / Service Graph plugin; sample CI has `discovery_source` |

**Three distinct layers — do not conflate:**

| Layer | Question | Configured in | Scope |
|---|---|---|---|
| **CI identification rules (IRE)** | Is this CI new or the one I already have? | CI Class Manager / CI Identifiers, per CI class | **CMDB** — all CIs (servers, laptops, network gear). HAM relies on this |
| **Asset↔CI reconciliation (HAM)** | Which asset record is this CI? | HAM asset sync on **serial number** | Hardware assets ↔ CIs — separate from identification |
| **Software normalisation / recognition** | Are these two software titles the same product? | SAM normalisation, content library / publisher packs | **SAM** — this is SAM's real "identification" problem [S28] |
| **Licence metric** | Per user, device, or core? | Entitlement record | **SAM** — commercial decision |
| **Licence reconciliation** | Rights vs installs → compliance | SAM reconciliation | **SAM** — the number you defend [S28] |

> **Rule of thumb:** Deduplicating *a machine* → CMDB/IRE. Deduplicating *a software title* → normalisation in SAM. Deduplicating *a quantity of rights* → a licence metric (commercial decision) [S28].

---

## 2. Data model / tables you will touch

| Table | Label | Purpose | Notes |
|---|---|---|---|
| `cmdb_sam_sw_install` | Software Installation | Discovered/SCCM-imported installs; **the source of truth for current software data once SAM is active** [S7] | Primary key: Publisher + Display Name + Version |
| `cmdb_sam_sw_discovery_model` | Software Discovery Model | Raw fingerprint from Discovery; cannot be created manually; normalized against Content Library [S12][S20] | Normalization statuses: Normalized, Partially Normalized, Publisher Normalized, Match Not Found, Manually Normalized, New [S21] |
| `cmdb_software_product_model` | Software Model | Canonical normalized product; connects purchases (entitlements) with discovered installs [S7] | Must link `product` field for reconciliation [S24] |
| `cmdb_sam_publisher` / `samp_publisher` | Publisher | Normalized publisher reference | Content Library maintains |
| `cmdb_sam_product` / `samp_product` | Product | Normalized product reference | |
| `cmdb_sam_entitlement` / `samp_entitlement` | Entitlement | Rights record with metric, quantity, dates [S17] | Professional: `samp_entitlement`; Foundation: `alm_license` |
| `alm_license` | License (legacy label) | Entitlement record in Foundation | Verify table name per edition [S28] |
| `alm_asset` | Asset | Hardware/software asset base | Shared with HAM |
| `ast_contract` | Contract | PO/contract evidence for entitlements [S28] | |
| `cmdb_ci_computer` / `cmdb_ci_server` | Computer / Server CI | Host CI for installs; displays SAM data via related list [S7] | |
| `samp_vmware_license_key` | VMWare License Key | Populated by Discovery (Kingston+) [S7] | |
| `samp_oracle_options` | Oracle Options | Eligibility filtered by `Considered for licensing` + server relationship [S7] | |
| `cmdb_ci_spkg` | Software (legacy) | Pre-SAM discovery target; migrated via script [S7] | |

---

## 3. Configuration surface (catalog, grouped by where you set it)

### 3.1 Plugin activation (System Applications > All Available Applications)

| Plugin | ID | Entitlement gate | Notes |
|---|---|---|---|
| SAM Professional (master) | `com.sn_samp_master` / `com.sn_samp_master_ws` (Xanadu+) | **Professional** | Loads all SAM Pro plugins [S7] |
| SAM Foundation | `com.snc.samp` | **Foundation** | Pre-Xanadu master plugin [S7] |
| Software Asset Workspace | `com.sn_sam_workspace` | **Professional** | New UI [S7] |
| ML Normalization | `com.sn_sam_ml_normalization` | **Professional** | Real-time ML matches [S7] |
| SaaS License Management | `com.sn_sam_saas_int` | **Professional** (Store request) | SaaS connectors [S7][S10] |
| Spend Detection | `com.sn_sam_spend` | **Professional** | Financial transaction analysis [S7] |
| Engineering Apps | `com.sn_samp_eng_app` | **Professional** | Concurrent licenses (OpenLM/Open iT) [S7] |
| Publisher packs (Adobe, Citrix, IBM, Microsoft, Oracle, SAP, VMware) | `com.sn_samp_*` | **Professional** (per publisher) | Publisher-specific metrics/rules [S7][S11] |
| SCCM/Intune/Jamf (legacy) | `com.snc.samp_usage_sccm` etc. | **Professional** | Deprecated in Tokyo; use Service Graph Connectors [S7] |

### 3.2 Roles (User Administration > Roles)

| Role | Purpose | Contains |
|---|---|---|
| `sam_admin` | Full SAM admin: import entitlements, manage reclamation, run reconciliation, create custom products/patterns, Content Service setup [S7] | |
| `sam_user` | View/read configs; manual normalization; view reconciliation results [S7] | |
| `sam_integrator` | Integration user for data feeds [S28] | |
| `it_demand_user` | No longer auto-installed with SAM Pro [S7] | |

### 3.3 Guided Setup / Configuration Console

| Entry point | Path | Notes |
|---|---|---|
| Configuration Console | Manage Platform > Software Asset Management > Configure | Requires `sn_samp_admin` Store app + `sam_admin` + `ia_user` roles [S8] |
| SAM Guided Setup | Workspaces > Software Asset Workspace > Success Portal > Product Setups | Prescriptive steps for SaaS/on-premise products [S9] |
| Entitlement Playbook | Software Asset Workspace > landing page (Store install required) | Step-by-step entitlement creation [S9] |
| Product Guided Setups | Success Portal > Product Setups > Microsoft SQL Server / Windows Server / M365 | One instance at a time [S9][S10] |

### 3.4 Discovery / Connector feeds

| Source | Configuration path | Notes |
|---|---|---|
| ServiceNow Discovery | All > Discovery > Home > Schedules | Horizontal patterns; MID Server required [S1][S2] |
| Service Graph Connector for Microsoft SCCM | Store > Service Graph Connector for Microsoft SCCM | **Preferred**; legacy SCCM plugins deprecated in Tokyo [S7][S10] |
| Service Graph Connector for Microsoft Intune | Store | Modern replacement for Intune connector [S10] |
| Service Graph Connector for Jamf Pro | Store | macOS/iOS management [S1][S2] |
| Agent Client Collector (ACC) | All > Discovery > Home | Lightweight endpoint agent [S1][S2] |
| SaaS Direct Integrations (M365, Salesforce, Adobe, etc.) | License Operations > Direct Integration Profiles | API credentials, tenant config [S10] |

### 3.5 Normalisation engine + Content Library

| Component | Path | Key config |
|---|---|---|
| Content Library status | All > Software Asset > Administration > Content Library | Shows downloaded publisher packs [S28] |
| Pattern Normalization Rules | All > Software Asset > Administration > Pattern Normalization Rules | Custom rules for "Match Not Found" models [S15][S16] |
| Normalization Suggestions | Software Asset Workspace > License Operations > Discovery Models | Accept/reject ML/Content Service predictions [S12] |
| ML Normalization | Activate `com.sn_sam_ml_normalization` plugin | Real-time ML for unrecognized software [S12] |
| Content Service opt-in | All > Software Asset > Administration > Content Service | Share unnormalized data to improve library [S14] |

### 3.6 Entitlement management

| Element | Path | Critical fields [S17][S30] |
|---|---|---|
| Entitlement record | All > Software Asset > Licenses > All (or `alm_license` / `samp_entitlement`) | Product (normalized), Quantity, Licence metric, Start/end date, Licence type, Contract link |
| Contracts | All > Asset Management > Contracts > All | Links to entitlements for audit trail |
| Purchase Orders | Procurement integration | Unit cost, vendor, PO number |

### 3.7 Licence metrics

| Metric group | License metrics (examples) [S19] | Notes |
|---|---|---|
| **Common** | Per Core, Per Device, Per Named Device, Per Named User, Per Processor, Per User, User CAL, Device CAL, User/Device CAL, Concurrent User, Resource Consumption | Base metrics available without publisher packs |
| **Microsoft** | Per Core (SQL), Per User, Per Device, User CAL, Device CAL | Publisher pack required [S11] |
| **Oracle** | Processor, Named User Plus | Core factor table; PVU for IBM [S11] |
| **IBM** | PVU, RVU, Authorized User | Sub-capacity needs ILMT [S11] |
| **Adobe** | Per Device, Per User, User Subscription | Named-user VIP/ETLA [S11] |
| **SAP** | Named User (by usage type) | Indirect access audit risk [S11] |
| **Citrix** | Concurrent User, Per Device, Per Processor, Per User, Per User/Device | |
| **VMware** | Per Processor, Per VM | |
| **Consumption (SaaS)** | SaaS Consumption | Requires SaaS License Management plugin [S19] |
| **Subscription** | User Subscription | SaaS subscriptions [S19] |

⚠️ **Professional only:** Publisher-specific metric groups (Microsoft, Oracle, IBM, Adobe, SAP, Citrix, VMware) [S19]

### 3.8 SAM Reconciliation

| Element | Path | Config [S18][S24][S26] |
|---|---|---|
| Reconciliation job | All > Software Asset > Reconciliation > Results | Weekly (Mon 02:00 default); on-demand by publisher/group/subgroup |
| Default group/subgroup | Software Asset > Administration > Properties | `com.snc.samp.recon.group` (Company/Cost Center/Country/Department/Region/None), `com.snc.samp.recon.subgroup` |
| Parallel workers | SAM Properties | `com.snc.samp.recon.max_workers` (default 4) [S24][S26] |
| Suite batch size | SAM Properties | `com.snc.samp.recon.suite.min_batch_size` [S24] |
| Custom metrics enabled | SAM Properties | `com.snc.samp.recon.enablecustommetrics` (default true) [S26] |
| Component licenses for Microsoft | SAM Properties | `com.snc.samp.use_component_licenses` [S24] |
| Debug reconciliation | SAM Properties | `com.snc.samp.debug` [S24] |

### 3.9 Scheduled jobs (Configuration Console > Governance > Scheduled jobs) [S23][S27]

| Job | Frequency | Purpose |
|---|---|---|
| SAM - Software License Reconciliation | Weekly (Mon 02:00) | Main compliance calculation |
| SAM - Daily Job | Daily | Maintenance |
| SAM - Subscription Maintenance | Daily | Renewed/subscription licenses |
| SAM - Discovery Model to Software Model matching | Daily | Map discovery models to software models |
| SAM - Normalize discovery models using content library rules | Daily | Normalization + status assignment |
| SAM - Get install count for software model | Daily | Install count aggregation |
| SAM/CI - Populate Licensing Data | Daily | CI licensing data population |
| SAM - Deduplicate Install Table | Daily | Clean duplicate installs |
| SAM - Apply latest content changes (On Demand) | Manual | Content library updates |

---

## 4. Order of operations — setup sequence (A) and runtime reconciliation sequence (B)

### 4A. Setup sequence (what an implementer does on a blank instance)

1. **Install/confirm SAM plugin** — `com.sn_samp_master_ws` (Xanadu+) or `com.snc.samp` (pre-Xanadu) + entitlement [S7][S28]
2. **Install Publisher Packs** — per in-scope publishers (Microsoft, Oracle, IBM, Adobe, SAP, VMware, Citrix) [S7][S11]
3. **Install optional plugins** — ML Normalization, SaaS License Management, Spend Detection, Engineering Apps [S7]
4. **Guided Setup / Configuration Console** — read all steps before executing [S8][S9][S28]
5. **Roles + integration user** — `sam_admin`, `sam_user`, dedicated integration user [S28]
6. **Foundation data** — companies, locations (with time zones), departments, cost centres, users, groups [S2][S28]
7. **Discovery / connector feed** — configure ONE first (SCCM OR Intune OR ACC OR Service Graph), pilot scope [S1][S2][S28]
8. **CI identification rules** — for computer classes (CMDB/IRE prerequisite, **not SAM config**) [S28]
9. **Content Library download** — verify publisher packs reachable [S28]
10. **Normalisation** — run/review; top-5 titles each map to exactly one product [S28]
11. **Entitlements from contracts/POs** — every entitlement traces to a document [S28]
12. **Licence metrics per publisher** — platform metric matches contract wording [S28]
13. **Reconciliation** — run, read exceptions, explain top 3 gaps [S28]
14. **Dashboards + cadence** — named owner, weekly review [S28]

### 4B. Runtime reconciliation sequence (what happens per reconciliation run)

```
ENTITLEMENTS (valid date range)
    │
    ▼
NORMALIZED INSTALLS (de-duped per device/user per metric)
    │
    ▼
USAGE EVIDENCE (reclamation, "not in use", use-based licensing)
    │
    ▼
PUBLISHER RULES & EXCLUSIONS (ignore lists, VM rules, suite roll-ups, downgrade rights)
    │
    ▼
CALCULATE POSITION (per model + per metric)
    │
    ▼
PERSIST RECONCILIATION RESULT (timestamped, with inputs)
    │
    ▼
ROLL UP (publisher → portfolio dashboards) [S17][S18][S25]
```

---

## 5. SAM Plugin activation and Guided Setup, step by step

| Step | Action | Verification |
|---|---|---|
| 1 | System Applications > All Available Applications > All → Search "Software Asset Management" → Activate | SAM menu group exists in filter navigator; `v_plugin` shows active [S28] |
| 2 | Activate Publisher Packs (Microsoft, Oracle, etc.) | Content Library shows downloaded packs [S11] |
| 3 | Install `sn_samp_admin` from Store for Configuration Console | Configuration Console accessible [S8] |
| 4 | Run Guided Setup (if shipped) | Type "guided setup" in filter navigator; verify with probe [S28] |
| 5 | Create integration user with `sam_integrator` role | Impersonate SAM user: sees licence position, cannot edit schema [S28] |

---

## 6. Roles, integration users, and ACLs for SAM

| Role | Capabilities | ACL notes |
|---|---|---|
| `sam_admin` | Import entitlements, reclamation rules, reconciliation, custom products/patterns, Content Service [S7] | Full write on `cmdb_sam_*`, `samp_*`, `alm_license` |
| `sam_user` | View configs, manual normalization, view reconciliation [S7] | Read on SAM tables; no write |
| `sam_integrator` | Data feed integration (SCCM, Intune, etc.) | Write on `cmdb_sam_sw_install`, `cmdb_sam_sw_discovery_model` |
| `admin` / `sn_cmdb_admin` | CI form related-list config, system properties [S7] | |

---

## 7. Discovery / connector feeds for SAM

### 7.1 Traditional connectors (legacy, deprecated in Tokyo)

| Connector | Plugin | Status |
|---|---|---|
| SCCM 2012 v2 Software Usage | `com.snc.samp_usage_sccm` | Deprecated → use Service Graph Connector [S7] |
| SCCM 2016 Software Usage | `com.snc.samp.usage_sccm_2016` | Deprecated → use Service Graph Connector [S7] |

### 7.2 Modern connectors (Service Graph Connectors)

| Connector | Store app | Data fed |
|---|---|---|
| Microsoft SCCM | Service Graph Connector for Microsoft SCCM | Installs, devices, usage metering [S10] |
| Microsoft Intune | Service Graph Connector for Microsoft Intune | Installs, device compliance [S28] |
| Jamf Pro | Service Graph Connector for Jamf Pro | macOS/iOS installs [S28] |
| BigFix (HCL) | IntegrationHub spoke | Installs, usage [S28] |

### 7.3 SaaS Direct Integrations

| SaaS | Connector | Data fed |
|---|---|---|
| Microsoft 365 | Microsoft Graph API (Entra ID Spoke) | Subscriptions, assigned seats, usage [S10] |
| Salesforce | REST API | Seat assignments, last login [S28] |
| Adobe Creative Cloud | Adobe VIP/ETLA API | Named-user subscriptions [S28] |
| Zoom | REST API | Host licenses, usage [S28] |

---

## 8. Normalisation engine + Content Library / Publisher Packs

### 8.1 Normalization process [S12]

1. **Discovery creates** `cmdb_sam_sw_install` with raw Publisher/Display Name/Version
2. **Business rule** on `cmdb_sam_sw_install` matches/creates `cmdb_sam_sw_discovery_model`
3. **Normalization** compares discovery model against Content Library → writes normalized Publisher/Product/Version/Edition
4. **Status assigned** (Normalized / Partially Normalized / Publisher Normalized / Match Not Found / Manually Normalized / New) [S21]

### 8.2 Normalization rule types [S12]

| Rule type | Description | Created by |
|---|---|---|
| **Product Map / Package Map** | One rule per distinct discovery model (e.g., 1000 models = 1000 rules) | Content Service (auto) |
| **Pattern Normalization** | Single rule addressing multiple models via substring match (e.g., "Microsoft Office 2019*") | SAM admin (manual) [S15][S16] |
| **Enhanced Pattern Normalization** | Conditional mapping; handles variations (STD/Standard/stand → Standard) | SAM admin (manual) [S12] |
| **Wide-net Normalization** | Groups similar discovered values; reduces need for individual rules | Content Service (auto, selective) [S12] |

### 8.3 Normalization statuses [S21]

| Status | Description | Editable fields |
|---|---|---|
| **Normalized** | Fully normalized on publisher, product, version | None (read-only); edit → Manually Normalized |
| **Partially Normalized** | Publisher + product only | Version editable → Manually Normalized |
| **Publisher Normalized** | Publisher only | Product + version editable → Manually Normalized |
| **Match Not Found** | No match in Content Library | All key fields editable → Manually Normalized |
| **Manually Normalized** | Admin filled fields manually | Cannot revert |
| **New** | Not yet processed by normalization job | — |

### 8.4 Key KPI: **Normalization coverage > 85% before first reconciliation** [S6]

> "Reconciliation doesn't run unless normalization is clean. Unnormalized installs simply don't get picked up. Always check the normalization coverage % before your first reconciliation run and set a KPI (typically targeting >85%)."

### 8.5 Pattern normalization rule form [S15]

| Field | Description |
|---|---|
| Name | Unique rule name |
| Discovered publisher contains | Substring match on publisher |
| Discovered product contains | Substring match on product |
| Discovered publisher is empty | For sources reporting product without publisher |
| Normalized Publisher / Product / Edition / Version / Platform / Language | Target normalized values |
| Product type | Licensable / Child / Driver / Not Licensable / Patch |
| Apply Rule | Related link to execute immediately |

---

## 9. Entitlement management: contracts, POs, metrics, licence types

### 9.1 Entitlement record critical fields [S17][S30]

| Field | Verdict | Why |
|---|---|---|
| Product (normalized) | **Critical** | Wrong product = entitlement never matches installs |
| Quantity / rights | **Critical** | The number you defend in audit |
| Licence metric | **Critical** | Wrong metric = permanently wrong compliance |
| Start / end date | **Critical** | Expired entitlement → unlicensed installs |
| Licence type (subscription/perpetual) | **Critical** | Changes how "owned" is calculated |
| Publisher / contract link | Useful | Traceability to PO; auditors ask for it |
| Downgrade rights | Useful (critical for Microsoft/Adobe) | Ignoring them overstates non-compliance [S28] |

### 9.2 Entitlement hygiene rules [S28]

- **One entitlement per contract line**, not per PO
- **Never overwrite quantity** to fix a report; create true-up/adjustment record
- **Maintenance ≠ license** — maintenance-only must not count as usage rights
- **Metric mismatch is silent** — per-device entitlement vs per-user usage = meaningless number

---

## 10. Licence metrics — configuration and pitfalls

### 10.1 Metric group controls available metrics [S17][S19]

> "The available License metrics are dependent on which Metric groups are available in an instance. A Metric group controls which license metrics are available to be used. It is possible that not all Metric groups will be available in an instance. It is best to check which Metric groups are available, and only select the license metrics available for the Metric group. The Metric group selected does not have to correspond to the publisher of the software title."

### 10.2 Common metric pitfalls

| Pitfall | Consequence | Fix |
|---|---|---|
| Per-core contract modelled as per-device | Looks compliant, fails audit | Match metric to contract wording [S28] |
| Per-user entitlement vs per-device usage | Silent mismatch | Align both sides [S30] |
| Microsoft SQL Server core factor | Minimum 4 cores/socket; physical cores × factor | Configure `samp_processor_definition` [S28] |
| Oracle core factor table | Per processor family; server-level licensing | `com.snc.samp.oracle.reconlevel`, `hostaffinityenabled` [S7] |
| IBM PVU sub-capacity | Requires ILMT or equivalent evidence | ILMT integration [S28] |
| SAP named user classification | Developer/Professional/Limited/ESS | Indirect access audit risk [S28] |

### 10.3 Custom license metrics [S19][S26]

- Add via **Add a custom license metric** (scripted)
- Resource Value table (`samp_sw_resource_value`) for 1:1 calculation
- Property `com.snc.samp.recon.enablecustommetrics` (default true) enables them in reconciliation

---

## 11. SAM Reconciliation: definition, scope, exceptions, priority rules

### 11.1 Overview [S18]

- **Automated license reconciliation** keeps positions accurate without manual calculations
- **Runs weekly** (default Mon 02:00) or **on demand** for specific publishers/groups/subgroups
- **Group/subgroup dimensions:** country, department, company, region, cost center
- **Default group/subgroup** set in Software Asset > Administration > Properties
- **Required role to view:** `sam_user`; **run on-demand:** `sam_admin`

### 11.2 Outputs — three tiers [S18][S25]

| Tier | What it shows |
|---|---|
| **Product Results** | Compliance status, true-up cost, potential savings across all models of a product |
| **Software Model Results** | Per-model detail: License Metric Results, Unlicensed Installs |
| **License Metric Results** | Rights owned, rights used, allocation breakdown (Allocated in use / Not Allocated in use / Allocated not in use / Not Allocated) |

### 11.3 Remediation from model results [S18]

- Create/remove allocations
- Remove unallocated installs
- Remove unlicensed installs
- Create purchase order for new licenses

### 11.4 Oracle reconciliation specifics [S7]

| Property | Purpose |
|---|---|
| `com.snc.samp.oracle.reconlevel` | Aggregation level for Oracle/WebLogic on VMware |
| `com.snc.samp.oracle.hostaffinityenabled` | VM-host affinity rules for Oracle on VMware |
| `samp_oracle_options` | Eligibility: `Considered for licensing = Yes` + physical server relationship |

### 11.5 Reconciliation system properties [S24][S26]

| Property | Default | Effect |
|---|---|---|
| `com.snc.samp.recon.enablecustommetrics` | true | Enable custom metrics in reconciliation |
| `com.snc.samp.use_component_licenses` | false | Use component licenses when suite config insufficient (Microsoft) |
| `com.snc.samp.debug` | false | Debug reconciliation results (performance impact) |
| `com.snc.samp.recon.max_workers` | 4 | Parallel reconciliation jobs |
| `com.snc.samp.recon.suite.min_batch_size` | — | SuiteEngine batch size |
| `com.snc.samp.recon.group` | None | Default group for weekly run |
| `com.snc.samp.recon.subgroup` | None | Default subgroup (≠ group) |
| `com.snc.samp.enable.ml_normalization` | false | ML normalization for unrecognized software |

---

## 12. Compliance calculation — insert vs update of installs, entitlement consumption

### 12.1 Three-layer insert vs update decision table

| Layer | Insert Trigger | Update Trigger | Blocking Rules |
|---|---|---|---|
| **Software Install Recognition** (`cmdb_sam_sw_install`) | New discovered install (source + native key) | Same install re-discovered (version change, last seen update) | Duplicate detection via source+native key; Normalisation status |
| **Entitlement Consumption** | First install of a normalised product consumes entitlement | Install count changes, version upgrade/downgrade, metric change | Metric definition, entitlement quantity, licence type |
| **Reconciliation Exceptions** | New exception detected (over-consumption, metric mismatch) | Exception resolved or changed severity | Reconciliation scope, exception thresholds, priority rules |

### 12.2 Software install recognition flow [S7][S12][S20]

```
DISCOVERY / SCCM / INTUNE
       │
       ▼
POPULATES cmdb_sam_sw_install (Publisher, Display Name, Version, Edition)
       │
       ▼
BUSINESS RULE on cmdb_sam_sw_install
       │
       ├─ MATCH found in cmdb_sam_sw_discovery_model (Publisher+Product+Version+Edition PK)
       │     → UPDATE install record; discovery model reused
       │
       └─ NO MATCH
             → CREATE new cmdb_sam_sw_discovery_model
                   → NORMALIZATION JOB assigns status
                   → MANUAL NORMALIZATION if Match Not Found
```

### 12.3 Duplicate installation handling [S7]

- **Duplicate Software Installations** = same publisher/product/version/edition discovered through **multiple discovery sources** (e.g., Discovery + SCCM)
- Matching happens by discovery-model primary key, so duplicate *installation* rows are distinct from duplicate *CI* problems
- **No `duplicate_of` mechanism** for software installs (unlike CMDB IRE)
- **Remediate:** Remove uninstalled software via REST Table API [S7]

### 12.4 Entitlement consumption logic [S17]

| Metric | Consumption calculation |
|---|---|
| **Per Device** | Each unique device with normalized install = 1 right consumed |
| **Per User** | Each unique user with install = 1 right (all installs for user count as 1) |
| **Per Named User/Device** | Requires explicit allocation; unallocated = non-compliant |
| **Per Core** | CPU core count × CPU count (core factor for Oracle/IBM) |
| **Per Processor** | Physical processor count |
| **User CAL / Device CAL** | Each user/device accessing server = 1 right |
| **User Subscription** | Each active unique subscription record assigned to user = 1 right |
| **Concurrent User** | Peak simultaneous users in period (requires Resource Value record) |

### 12.5 Reconciliation exception types [S18][S25]

| Exception | Meaning | Typical cause |
|---|---|---|
| **Under-licensed** | Entitlements < demand | True-up needed or reclaim |
| **Over-licensed** | Entitlements > demand | Money wasted; reclaim/reduce renewal |
| **Unlicensed** | Installs exist, no matching entitlement | Remove, purchase, or reclassify |
| **Not counted** | Excluded by rule (ignore list, excluded CI/publisher) | Review annually — exclusions creep |
| **Unknown** | Insufficient data (unmatched model, no usage feed) | **Never report as compliant** [S28] |

---

## 13. Duplicate prevention in SAM (normalisation vs CMDB identification rules)

### 13.1 The distinction [S28]

| Duplicate type | Layer | Mechanism | Resolution |
|---|---|---|---|
| **Duplicate CI** (same machine) | CMDB/IRE | CI Identifiers on `cmdb_ci_computer` | `duplicate_of` field; de-duplication tasks |
| **Duplicate Software Install** (same install from 2 sources) | SAM | Discovery-model PK match (Publisher+Product+Version+Edition) | No `duplicate_of`; remove stale via REST API |
| **Duplicate Software Model** (same product, different records) | Normalisation | Content Library + Pattern Normalization | Normalize to single model; Publisher Pack rules |

### 13.2 Normalization as duplicate prevention [S12][S16]

- **Content Library** provides canonical mappings for known publishers
- **Pattern Normalization Rules** catch custom/niche software the library misses
- **Match Not Found** = normalization backlog; each unmatched model splits entitlements and invents shortages
- **KPI:** >90% discovery models normalized [S28]

### 13.3 Cross-source duplicate suppression [S28]

- Configure **one primary inventory source per platform class**
- Or implement **explicit duplicate suppression** (business rules on `cmdb_sam_sw_install`)
- Decommissioned devices must be excluded — stale CIs inflate demand

---

## 14. Remediating exceptions and false positives

| Exception type | Remediation action | Owner |
|---|---|---|
| **Under-licensed** | True-up purchase OR reclaim unused installs | SAM admin + Procurement |
| **Over-licensed** | Reclaim, reduce renewal quantity, renegotiate | SAM admin + Finance |
| **Unlicensed** | Remove install, purchase entitlement, reclassify as freeware | SAM admin + IT Ops |
| **Unknown** | Fix normalization or data feed — **do not report as compliant** | SAM admin |
| **Metric mismatch** | Align entitlement metric to software model metric | SAM admin + Legal |
| **Suite component over-count** | Configure suite membership + roll-up rules | SAM admin |

### 14.1 Reclamation workflow [S28]

```
Identify (reconciliation + usage) → Validate with owner → Notify user → Grace period (60-90 days)
    → Reclaim/remove → Re-run reconciliation → Confirm savings recorded
```

> **Never reclaim based on a single night's data.** Usage feeds have gaps. Require sustained inactivity window and business owner sign-off.

---

## 15. Verification: SAM Health, Reconciliation Results, Licence Position dashboards

### 15.1 SAM Health Dashboard [S10]

- Install **ITAM Health Check** from Store
- Assesses SAM configurations, identifies issues in complex calculators
- Provides recommendations for correcting errors

### 15.2 Key dashboards/indicators to stand up [S28][S31]

| Dashboard | Indicator | Healthy target |
|---|---|---|
| Compliance by publisher | % compliant or over-licensed | > 95% |
| Normalization backlog | Open unmatched discovery models | Trend down |
| Entitlements expiring | 30/60/90 day renewals | 100% reviewed |
| Reclamation candidates | No usage 90 days | Validated in 10 business days |
| SaaS seat utilization | % assigned seats active in 90 days | > 85% |
| Reconciliation freshness | Models with stale results | < 24h old |
| Cost of over-licensing | $ value of over-licensed entitlements | Trend down |

### 15.3 SAM Readiness Scorecard (probe-based) [S31]

| Check | Hard gate? | Pass condition |
|---|---|---|
| 1. SAM schema installed | **YES** | `samp_*`/`cmdb_sam_*` tables > 0 |
| 2. Asset tables present | **YES** | `alm_asset` exists |
| 3. CMDB populated | **YES** | `cmdb_ci` rows > 100 |
| 4. Discovery/connector plugin | **YES** | Discovery/Service Graph/ACC plugin active |
| 5. Contracts table | NO | `ast_contract` exists |
| 6. Licence record table | NO | `alm_license`/`samp_entitlement` exists |
| 7. Guided Setup module | NO | Asset/Software/SAM module present |
| 8. Active automation flows | NO | `sys_hub_flow` active > 0 |
| 9. Analytics indicators | NO | `pa_indicators` > 0 |
| 10. Probe ran clean | NO | No query errors |

> **Hard failure in schema, assets, or CMDB caps the grade** — SAM on top of missing discovery produces confident nonsense [S31].

---

## 16. Anti-patterns

| # | Anti-pattern | Consequence | Fix |
|---|---|---|---|
| 1 | Installing SAM and calling it done | Plugin is 5% of work; discovery/normalisation are 95% [S28] | Follow build order; prove Crawl before Walk |
| 2 | Partial discovery published as full compliance | Coverage % hidden; audit exposure [S28] | Always publish coverage % next to number |
| 3 | Wrong licence metric (per-core as per-device) | Looks compliant, fails audit [S28] | Match metric to contract; legal review |
| 4 | Normalisation left alone | One product = 6 variants; splits entitlements [S28] | Target >85% coverage; pattern rules for gaps |
| 5 | Entitlements without contract/PO evidence | Rights you cannot document [S28] | One entitlement per contract line |
| 6 | Ignoring downgrade rights | Overstates non-compliance; buy twice [S28] | Document downgrade rights on entitlement |
| 7 | Multiple discovery sources, no de-duplication | Same install counted twice [S28] | One primary source per platform; suppress dupes |
| 8 | Treating installs as usage | Installed ≠ used; optimization needs metering [S28] | Usage feeds (SCCM metering, BigFix, EUC) |
| 9 | No owner for output | Compliance reports nobody reads change nothing [S28] | Named owner; weekly review cadence |
| 10 | Expired entitlements unnoticed | Position silently flips to unlicensed [S28] | Scheduled job to expire lapsed entitlements [S28] |
| 11 | Reporting "Unknown" as compliant | Hidden audit exposure [S28] | Report Unknown explicitly; assign owner |
| 12 | Reclaiming on one night's usage | Removes licenses people need [S28] | 60-90 day inactivity window + owner sign-off |
| 13 | Dead SaaS connector unmonitored | "No waste" illusion [S28] | Connector health monitoring + owner |
| 14 | IT-only ownership, no finance partner | No authority to reclaim/renegotiate [S28] | Joint IT + Procurement + Finance |

---

## 17. Open questions (explicitly UNVERIFIED)

| # | Question | Why unverified |
|---|---|---|
| 1 | Exact list of SAM Application Properties beyond the 5 in `com.snc.samp.*` | Docs prescribe navigating to Application Properties but don't publish full catalog [S24] |
| 2 | Full precedence order: Content Library vs Pattern Normalization vs Enhanced Pattern vs Wide-net | Docs say "Content Library takes precedence over custom file signature rules" but don't spell out pattern normalization precedence [S16] |
| 3 | Exact behavior when ML Normalization and Content Library both match a model | Plugin effect documented but algorithmic detail not covered [S12] |
| 4 | SAM Foundation vs Professional table name differences in current releases | Probe detects `samp_*` vs `cmdb_sam_*` but exact mapping per edition not fully documented [S31] |
| 5 | Migration path details: `cmdb_ci_spkg` → `cmdb_sam_sw_install` script behavior | Referenced in docs but not detailed [S7] |
| 6 | Oracle `samp_oracle_options` exact eligibility logic for VMware | Described at high level; edge cases not covered [S7] |
| 7 | SaaS License Management connector health monitoring specifics | "Alerting when connector silently stops syncing" recommended but no OOB mechanism documented [S28] |
| 8 | Custom license metric script template and Resource Value table schema | Referenced but not fully documented in public docs [S19] |
| 9 | Exact reconciliation calculation for Concurrent User metric with Resource Value | Described as "1:1 ratio" but edge cases not detailed [S19] |
| 10 | Suite roll-up behavior for Microsoft Office / Adobe Creative Cloud in mixed entitlement scenarios | "Suite membership must be configured" but exact roll-up logic not public [S28] |

---

## 18. Source ledger

| Ref | Source | Type | Release label | URL |
|---|---|---|---|---|
| [S1] | SAM Implementation Best Practices | Ebook | — | servicenow.com/content/dam/.../eb-getting-value-for-software-asset-management.pdf |
| [S2] | SAM Implementation Best Practices White Paper | White paper | — | community.servicenow.com/.../Software%20Asset%20Management%20Implementation%20Best%20Practices%20White%20Paper.pdf |
| [S3] | Performance, KPIs, and Metrics Guide | Success playbook | — | servicenow.com/content/dam/.../performance-kpi-metrics-guide.pdf |
| [S4] | Crawl, Walk, Run: SAM Program | Partner blog | 2025-11-27 | coreio.com/blog/crawl-walk-run-servicenow-sam-part1 |
| [S5] | Hand Book to Kick Start SAM | Community | 2025-02-28 | community.servicenow.com/.../hand-book-to-kick-start-the-software-asset-management-sam |
| [S6] | Guidance on SAM PRO License Renewal | Community | 2026-03-19 | community.servicenow.com/.../guidance-on-sam-pro-license-renewal-process |
| [S7] | Components installed with SAM Professional | Product docs | **Xanadu** | docs.servicenow.com/r/xanadu/.../sam-installed-components.html |
| [S8] | Configure SAM using Configuration Console | Product docs | **2026-09-10** | docs.servicenow.com/r/it-asset-management/.../configure-sam-from-config-console.html |
| [S9] | SAM Guided Experiences | Product docs | **Yokohama** | docs.servicenow.com/r/yokohama/.../playbook-entitlementsetup-workspace.html |
| [S10] | M365 Optimization with SAM Pro | Community | 2026-06-26 | community.servicenow.com/.../microsoft-365-optimization-with-sam-pro-part-1 |
| [S11] | SAM Publisher Packs Data Sheet | Data sheet | — | servicenow.com/standard/.../ds-sam-publisher-packs.html |
| [S12] | Software normalization | Product docs | **Xanadu** | docs.servicenow.com/r/it-asset-management/.../sam-normalization.html |
| [S13] | Software discovery and normalization | Product docs | **Zurich** | docs.servicenow.com/r/zurich/.../c_SAMDiscovery.html |
| [S14] | SAM Content Service | Product docs | **Xanadu** | docs.servicenow.com/r/xanadu/.../c_SAMContentService.html |
| [S15] | Add pattern normalization rule | Product docs | **Yokohama** | docs.servicenow.com/r/yokohama/.../t_AddAPatternNormRule.html |
| [S16] | Fix "Match Not Found" with Pattern Normalization | Video | 2026-05-28 | youtube.com/watch?v=avUZJVm_NvU |
| [S17] | SAM Process Guide | PDF (Paris) | **Paris** | community.servicenow.com/.../Software%20Asset%20Management%20Process%20Guide%20-%20Paris%20Release.pdf |
| [S18] | Software reconciliation for compliance | Product docs | **Xanadu** | docs.servicenow.com/r/xanadu/.../c_SAMReconciliation.html |
| [S19] | Software license metrics | Product docs | **Xanadu (2026-09-10)** | docs.servicenow.com/r/it-asset-management/.../c_SAMLicenseMetrics.html |
| [S20] | Discovery models and software installations | Product docs | — | docs.servicenow.com/r/it-asset-management/.../c_DiscoveryModels.html |
| [S21] | Normalization statuses | Product docs | **Yokohama (2025-01-30)** | docs.servicenow.com/r/yokohama/.../normalization-status.html |
| [S22] | Software Installation Normalization fields | Community | 2022-02-15 | community.servicenow.com/.../software-installation-normalization-fields |
| [S23] | SAM Pro reconciliation jobs | Community | 2026-01-06 (Yokohama) | community.servicenow.com/.../sam-pro-reconciliation-not-bringing-in-new-entitlement |
| [S24] | Basic SAM Configuration | Japanese blog | 2026-08-25 | note.com/u_sn_notes/n/nc5d999da777c |
| [S25] | CIS-SAM Exam Study Guide | Exam guide | — | blog.snowycode.com/post/cis-sam-exam-study-guide-servicenow |
| [S26] | Explained: SAM System Properties | Community | 2023-02-02 | community.servicenow.com/.../explained-software-asset-management-system-properties |
| [S27] | Configure scheduled jobs | Product docs | — | docs.servicenow.com/r/it-asset-management/.../manage-scheduled-jobs-sam-using-config-console.html |
| [S28] | Learning repo: 08-SAM-SETUP.md | Learning repo | 2026-11-04 | github.com/eltonaguiar/ServiceNow_Learning/blob/main/docs/08-SAM-SETUP.md |
| [S29] | Learning repo: 03-breadcrumbs.md | Learning repo | 2026-11-04 | github.com/eltonaguiar/ServiceNow_Learning/blob/main/docs/03-breadcrumbs.md |
| [S30] | Learning repo: 04-fields.md | Learning repo | 2026-11-04 | github.com/eltonaguiar/ServiceNow_Learning/blob/main/docs/04-fields.md |
| [S31] | Learning repo: sam_readiness.py | Learning repo | 2026-11-04 | github.com/eltonaguiar/ServiceNow_Learning/blob/main/scripts/sam_readiness.py |
| [S32] | Learning repo: sn_probe.js | Learning repo | 2026-11-04 | github.com/eltonaguiar/ServiceNow_Learning/blob/main/scripts/sn_probe.js |

---

*Compiled 2026-11-13. This reference follows the same methodology as the CMDB/Discovery reference in `ALT_PARALLELSWARM` (`final/DISCOVERY_INSERT_VS_UPDATE_GUIDE.md`). For the underlying 4-phase Discovery flow and CMDB-level identification/reconciliation, see that document.*