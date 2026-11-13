# FINAL — ServiceNow SAM (Software Asset Management) Module & Discovery Configuration Reference

- **Compiled by:** `beam` / provider **Kilo** / harness **cli** (`beam__kilo__cli`)
- **Date:** 2026-11-13
- **Release basis:** Official `docs.servicenow.com` **Australia** (2026-03-12 → 2026-09-30 per pages).
- **Purpose:** Exhaustive configuration reference for the ServiceNow Software Asset Management (SAM)
  module, with emphasis on the changed CMDB/Discovery contract introduced when SAM is activated.

---

## 0. Provenance & method

Sources were fetched from the ServiceNow khub API (Australia maps) on 2026-11-13 and retained as
raw text in this agent's `research/` folder. Where two sources disagreed, the discrepancy is
flagged in §"Known gaps" rather than silently resolved.

Primary sources used:
- `Discovery with Software Asset Management` (Australia) — table contract.
- `Basic Software Asset Management discovery models and software installations` (Australia).
- `Basic Software Asset Management software discovery and normalization` (Australia).
- `Software discovery models` (legacy plugin) (Australia).
- `Software normalization` (Australia).
- `Software discovery and normalization` (Australia).
- `Manually normalize a software model …` / `Manually normalize a software discovery model …` (Australia).
- `Software reconciliation for compliance` + `Software reconciliation results` (Australia).
- `Delete uninstalled software from the Software Installation table` (Australia).
- `Configure a CI to display Software Asset Management data` (Australia).
- `Configure SCCM for Software Asset Management` (Australia).
- `Software Asset Management administration` (Australia).
- `Configuring Software Asset Management` (Australia).
- Domain separation Oracle reconciliation properties page (Australia).

---

## 1. SAM module — what it changes

### 1.1 Plugin activation and scope
- The SAM application's presence changes how **Discovery stores software installation data**: new
  tables are created and a business rule on `cmdb_sam_sw_install` matches/creates a Software
  Discovery Model record.
- Plugin referenced for the related-list/CI display configuration:
  `Software Asset Management (com.sn_samp_master_ws)` (role `admin` to configure).
- Additional optional plugins referenced:
  - `Software Asset Management – Machine Learning Normalization (com.sn_sam_ml_normalization)`
  - `Integration — Microsoft SCCM 2012 v2 / 2016` and their Software Usage plugins (legacy; to be
    replaced by the Service Graph connector for Microsoft SCCM)
  - `Domain Support - Domain Extensions Installer (com.glide.domain.msp_extensions.installer)`
    for domain-specific Oracle reconciliation properties

`Important:` When SAM is installed, the `Software Installation [cmdb_sam_sw_install]` table becomes
the appropriate source for **all current** software data. Update any related lists or customized
reference fields you added to CI records to point at it.

### 1.2 Roles
- `sam_admin` — configure administrative tasks (content service opt-in, processor definitions,
  pattern normalizations, custom part numbers, metrics).
- `sam_user` — view/read configurations; run manual normalization; view reconciliation results.
- `admin` / `sn_cmdb_admin` — required for CI form related-list and property configuration.
- (Discovery roles remain unchanged: `discovery_admin` / `admin` for schedules and reconfiguration.)

### 1.3 Entry points (Australia)
- `All > Software Asset > …` (core UI) — Discovery models, Reconciliation, Administration,
  Job Results.
- `All > Software asset > Software Asset Workspace > License operations > Discovery models`
  (new workspace).
- `All > Configuration > Servers > All` / `cmdb_ci_computer.list` — to configure the related list
  that surfaces SAM data on a CI.
- `All > Software Asset > Administration > Application Properties` — SAM application properties.
- `All > Software Asset > Administration > Job Results` — `Software Asset Job Result` records.

### 1.4 Tables created by SAM
| Table | Label | Purpose |
|---|---|---|
| `cmdb_sam_sw_discovery_model` | Software Discovery Model | Created/updated by a business rule when Discovery populates `cmdb_sam_sw_install`; holds normalized publisher/product/version/edition plus normalization status and approval; is the key to matching installs to software models/entitlements. |
| `cmdb_software_product_model` | Software Model | Specific version/configuration of purchased software; connects purchases (entitlements) with discovered installations. (Label exists in both scopes; SAM uses this scope.) |
| `cmdb_sam_sw_install` | Software Installation | Discovered (or SCCM-imported) software installations; the appropriate source for all current software data once SAM is active. |
| `samp_vmware_license_key` | VMWare License Key | Populated by Discovery (Kingston+). |
| `samp_vmware_license_key_usage` | VMWare License Key Usage | Populated by Discovery (Kingston+). |

Tables **not** used by SAM/Discovery with SAM:
- `cmdb_ci_spkg` (legacy Software)
- `cmdb_software_product_model` in its ITSM Software Asset Management rôle is unaffected-scope
  (the SAM copy is the one used).

---

## 2. Order of operations (SAM)

1. **Activate the plugin(s).** Install/activate Software Asset Management (`com.sn_samp_master_ws`).
   Optionally activate ML Normalization. Outcome: SAM tables are created and Discovery behaviour
   changes on the next run.
2. **Roles + entry points** assigned (`sam_admin`, `sam_user`, discovery roles).
3. **Discovery sources configured** (Discovery schedules per §1.4 of the Discovery reference, and/or
   SCCM via the Service Graph connector for Microsoft SCCM; legacy SCCM plugins are deprecated in
   the Tokyo release).
4. **CI forms configured** — add `Software Installation -> Installed on` related list so operators
   can view SAM data from a CI (see §4).
5. **Run Discovery** (or SCCM import) → populates `cmdb_sam_sw_install` (and legacy data if needed).
   For instances migrating from pre-SAM Discovery, run the `Migrate Basic Software Asset Management
   software installations` script to copy `cmdb_ci_spkg` → `cmdb_sam_sw_install`.
6. **Normalization** runs (scheduled job `SAM - Normalize discovery models using content library
   rules`, daily) and assigns normalization statuses; optional ML job.
7. **Manual normalization** of partially-normalized / not-found records via the workspace or
   classic UI; approval of software discovery models.
8. **Reconciliation runs** (weekly, or on demand by publisher/group/subgroup) → compliance results
   and license positions; remediation actions.
9. **Duplicate / stale-data hygiene**: remove uninstalled software from `cmdb_sam_sw_install`;
   opt into content-service sharing for cross-org normalization.

Domain-separated order additionally: activate `com.glide.domain.msp_extensions.installer`, then
configure Oracle reconciliation application properties per domain via
`All > Software Asset > Administration > Application Properties`.

---

## 3. Discovery → SAM data flow (insert / update)

### 3.1 Runtime behaviour
When Discovery (or SCCM) returns software data:
- Discovery **populates** `cmdb_sam_sw_install`.
- A business rule on `cmdb_sam_sw_install` searches for a matching record in
  `cmdb_sam_sw_discovery_model`.
  - If a match exists → **update** the Software Installation record (the discovery model is reused).
  - If no match exists → **create** a new Software Discovery Model record (which is then
    normalized/approved).

### 3.2 Insert-vs-update rules for installed software
- SAM has **no IRE-style identification rules** here; matching is the business rule on
  `cmdb_sam_sw_install` against the (Publisher, Product, Version, Edition primary key of)
  `cmdb_sam_sw_discovery_model`.
- Duplicate Software Installations are created when the **same** publisher, product, version
  **and** edition are discovered through **multiple discovery sources**.
- Software discovery models **cannot be created manually**; they are only created by Discovery.
  They are normalized against the SAM Content Library. The platform matches a newly created
  discovery model to an existing software model using:
  - Display Name + Publisher + Version, or
  - Display Name + Version (if Publisher empty), or
  - Display Name only (if both Publisher and Version empty).
  Version matching searches for an exact match first, then rounds down to the major version
  when an exact match is absent (e.g. `8.0.4` matches `8.0`).

### 3.3 What "insert" vs "update" means in SAM
| Scenario | Behaviour |
|---|---|
| Install discovered on a CI not previously seen by that source | New `cmdb_sam_sw_install` row created; business rule tries to match/create Software Discovery Model |
| Install seen before, software unchanged | Business rule finds the existing discovery model; install record is updated/reconciled |
| Same software discovered via two sources (Discovery + SCCM) | Two instalation records (duplicate-type record), each pointing at the same discovery model; cleanup by removing uninstalled installs per §7 |
| Install marked uninstalled on the CI | The software-installations list can drift; clean with the REST Table API delete flow (§7) |
| Manual normalization re-pointed to a different software model | Software discovery model's normalization status changes; reconciliation uses the corrected match |

---

## 4. CI-side configuration to display SAM data

- Navigate: `All > Configuration > Servers > All` (or `cmdb_ci_computer.list`), open a computer CI.
- Right-click header → `Configure > Related Lists`.
- From `Available`, add `Software Installation -> Installed on` to `Selected` → `Save`.
- Result: the `Software Installations` tab appears on the computer CI's related-list section.

This is the primary UI touch-point for operators who want to see SAM software data in the CI
context. Update any earlier custom related-lists / reference fields from `cmdb_ci_spkg` to
`cmdb_sam_sw_install` after SAM activation.

---

## 5. Software Discovery Models

### 5.1 Storage and population
- Stored in `cmdb_sam_sw_discovery_model`.
- Cannot be created manually — only by Discovery.
- When Discovery populates `cmdb_sam_sw_install`, a business rule matches/creates the discovery
  model row.

### 5.2 Manual normalization
- Only allowed when normalization status is `Partially Normalized`, `Publisher Normalized`, or
  `Match Not Found`.
- Workspace path (new UI): `Software Asset Workspace > License operations > Discovery models`
  → select record → ellipsis → `Normalize` → status becomes `Manually Normalized`.
- Classic path: `All > Software Asset > Discovery > Discovery models`, open a record with the
  matching status, fill `Publisher`/`Product`/`Version`, save (status becomes
  `Manually Normalized`). Approved via `Approved` checkbox on the legacy form.
- To revert normalization: `Revert Normalization` (sets values back; rules associated with the
  discovery model are reset to original). Status behaviour:
  - `Normalized` / `Partially Normalized` / `Publisher Normalized` → revert to `Match Not Found`.
  - `Manually Normalized` and pattern-rule-normalized models **cannot** be reverted.
- Editing capabilities:
  - New UI: full normalize action only (status changes).
  - Legacy UI: editing only the `Software model` field and the `Approved` check box is permitted.

### 5.3 Normalization suggestions
- Generated for every manually normalized discovery model; predicted values for
  `Publisher`, `Product`, `Version` based on the discovery source.
- Operator can accept or reject each suggestion from the Software Asset Workspace.

### 5.4 Machine-learning normalization
- Available by activating `Software Asset Management – Machine Learning Normalization
  (com.sn_sam_ml_normalization)`.
- Use to improve real-time normalization of unrecognized discovered software.

---

## 6. Normalization

### 6.1 Process
When a new software discovery model enters the CMDB, the normalization process compares
discovered `Publisher`/`Product`/`Version`/`Edition` against the
**Software Asset Management Content Library** and writes the matched values to the
*normalized* columns on `cmdb_sam_sw_discovery_model`. Those normalized fields are then used by
reconciliation, license position calculation, and software lifecycle processes. Example:
discovered publisher `Microsoft Corp` normalized to `Microsoft`.

### 6.2 Benefits
- Establishes a definitive inventory of all installed software.
- Standardizes names from many discovery tools (removes alias drift).
- Reconciliation uses the standard values for accurate entitlement matching.
- Audit counts match records.

### 6.3 Scheduling
- Scheduled job **`SAM - Normalize discovery models using content library rules`** (daily) —
  normalizes discovery models based on content rules and assigns a normalization status.
- Scheduled job **`SAM - Discovery Model Normalization job`** (daily) — updates the
  normalization trend charts on the Normalization and content dashboard.
- Machine-learning normalization augments the above when the ML plugin is active.

### 6.4 Normalization statuses
- `Normalized` / `Partially Normalized` / `Publisher Normalized` / `Match Not Found` /
  `Manually Normalized` (with the revert rules in §5.2).

### 6.5 Normalization rules (content-service)
Reference families documented: `Product Map`, `Package Map`, `Pattern Normalization`,
`Wide-net Normalization`. Operators can detect and fix normalization issues using the
content-service sharing opt-in (see §10).

---

## 7. Duplicates and stale data

### 7.1 Duplicate software installations (the SAM double-write)
- Duplicate Software Installations occur when the same publisher/product/version/edition is
  discovered through **multiple discovery sources** (e.g. Discovery + SCCM).
- Matching in SAM happens by the discovery-model primary key at §3.2, so duplicate *installation*
  rows are distinct from duplicate *CI* problems (no `duplicate_of` mechanism is described for
  software installs). Remediate by removing uninstalled software.

### 7.2 Removing uninstalled software from cmdb_sam_sw_install
- Used when software is no longer on a CI but still present in the table.
- Procedure: use the REST Table API
  `GET api/now/table/cmdb_sam_sw_install?sysparm_query=installed_on=<ci_sys_id>` to fetch the
  installs on a CI, then delete the uninstalled records. Query by publisher/product/version
  (comma-separated list of fields) when needed.
- Role required: `sam_developer`.
- Software installs for specific publishers (Oracle, VMware, Citrix) can be deleted the same way.
- Role/permission: REST Table API GET as documented under "Table API-GET".

### 7.3 Normalization approval
- Discovery Models are **not approved** when created. An admin must review and approve them
  (legacy UI: `Approved` check box on the discovery model form) before reconciliation relies on
  them. Unapproved/un-normalized models with status `Match Not Found` must be normalized first.

---

## 8. Compliance reconciliation

### 8.1 Overview
- Automated license reconciliation keeps license positions accurate without manual calculations.
- Runs **weekly** by default, or **on demand** for specific publishers/groups/subgroups.
  Group/subgroup dimensions: country, department, company, region, cost center.
- Legacy path to set default group/subgroup for the weekly run:
  `Software Asset > Administration > Properties`.
- Required role to view reconciliation results: `sam_user`.
- Upgrade note (Yokohama+): reconciliation script includes are reorganized; customization
  review required.

### 8.2 Outputs
- Reconciliation results list the compliance status of software products vs. discovery and
  entitlements.
- Three tiers:
  1. **Product results** — compliance status, true-up cost, potential savings across all models
     and installs of a product.
  2. **Software Model results** — per-model detail including `License Metric Results` and
     `Unlicensed Installs`.
  3. **License Metric Results** — rights owned, rights used, allocation breakdown.
- Results accessible in both the Core UI and the Software Asset Workspace.
- Remediation available from model results: create/remove allocations, remove unallocated
  installs, remove unlicensed installs.
- `License Workbench` view and the `License Position` report simplify review.

### 8.3 Oracle reconciliation (summary)
- Reconciliation runs weekly/on demand; rights are calculated for named users, physical devices,
  and physical hosts (VM allocations counted as "allocated not in use" per the rule).
- Options table: `samp_oracle_options`, included only if
  `Considered for licensing = Yes` and the DB option is tied to a physical server, virtual server
  with a physical-server relationship, or an end-user device.
- Aggregation level for VMware virtualization defined by the
  `com.snc.samp.oracle.reconlevel` property; VM-host affinity governed by
  `com.snc.samp.oracle.hostaffinityenabled`.

---

## 9. Insert vs update — decision matrix (SAM scope)

| Situation | SAM behaviour |
|---|---|
| Discovery populates install on a CI not yet tied to a discovery model | New `cmdb_sam_sw_install` row + new `cmdb_sam_sw_discovery_model` created by the business rule |
| Software discovered again, same publisher/product/version/edition | Business rule finds the existing discovery model → install record updated |
| Same software found via two discovery sources | Duplicate installation records (per §7.1); recommend source consolidation; remove stale rows |
| Install no longer on CI | Stale install row retained until REST deletion (§7.2) |
| Software model re-correction | Re-run normalization/reconciliation against the corrected match |
| Normalization not found (Match Not Found) | Discovery model retained in `Match Not Found`; must be manually normalized before clean reconciliation |
| Software discovery model rejected not found | Content-service sharing can be opted in to improve matching (§10) |
| SAM plugin not active | Legacy `cmdb_ci_spkg` schema behaviour is used; no SAM tables or business rule applies |

---

## 10. Configuration options

### 10.1 Roles & entry points recap
See §1.2 and §1.3.

### 10.2 Plugin ownership of data
- Activate `com.sn_samp_master_ws` for SAM.
- Use ML Normalization plugin to add real-time ML matches.
- SCCM integration: prefer the Service Graph connector for Microsoft SCCM; legacy SCCM plugins
  are deprecated as of Tokyo.

### 10.3 CI form (related lists)
- Configure in: `All > Configuration > Servers > All` → open CI → right-click →
  `Configure > Related Lists` → `Software Installation -> Installed on` (§4).

### 10.4 SCCM as a discovery source
- Procedure: `All > Software Asset > Configure SCCM` (activate the integration plugin for your
  SCCM version and the software-usage plugin if usage data desired).
- Set `Discover` schedule type and credentials as appropriate in Discovery.

### 10.5 Properties and administration
- SAM application properties: `All > Software Asset > Administration > Application Properties`.
- Shared information (content service): `All > Software Asset > Administration > Content Service`
  — opt in to share unnormalized software installation data with SAM Content Service (improves
  automatic normalization); reversible.
- Domain-separated (per-domain) properties use the Application Properties related list after
  activating the Domain Support - Domain Extensions Installer plugin (§10.6).

### 10.6 Domain separation (Oracle reconciliation)
- Activating `com.glide.domain.msp_extensions.installer` exposes domain-specific SAM application
  properties.
- Domain-separated properties exist for:
  - `com.snc.samp.oracle.reconlevel` (aggregation level for Oracle/WebLogic on VMware)
  - `com.snc.samp.oracle.hostaffinityenabled` (VM-host affinity rules for Oracle reconciliation
    on VMware)
- Configuration path per domain: Application Properties → Application Property Values related
  list.

### 10.7 Content service & migration
- Content-service opt-in shares unnormalized installs to improve matching (and the collective
  content library).
- Migration path for SAM 1.x → new workspace: `Overwrite customizations for Software Asset
  Management migration` if needed.

### 10.8 Normalization jobs
- `SAM - Normalize discovery models using content library rules` (daily)
- `SAM - Discovery Model Normalization job` (daily, trend charts)

### 10.9 Major configurable behaviour knobs (named in docs)
| Knob | Where | Effect |
|---|---|---|
| SAM plugin activation | Plugins | Changes the Discovery→CMDB software table contract |
| ML Normalization plugin | Plugins | Real-time ML-based normalization |
| Application Properties | SAM Administration | Per-publisher/per-feature tuning (Oracle aggregation, host affinity, scheduling) |
| CI related list setup | CI form configure | Surfaces SAM installs for operators |
| Content service sharing | SAM Administration | Opt-in data sharing for normalization |
| Domain Extensions Installer | Plugins | Enables per-domain property values |
| SCCM/Service Graph connector | Integrations | Software data source selection |

---

## 11. Key tables

| Table | Label | Notes |
|---|---|---|
| `cmdb_sam_sw_install` | Software Installation | Primary Discovery output for SAM; the source of truth for current software data |
| `cmdb_sam_sw_discovery_model` | Software Discovery Model | Cannot be created manually; populated by the business rule; holds normalized values + status + approval |
| `cmdb_software_product_model` | Software Model | Purchased software rights connected to discovered installs |
| `cmdb_ci_computer` / `cmdb_ci_server` | Computer / Server CI | The CI that installs reference; displays SAM data via related list |
| `samp_vmware_license_key` | VMWare License Key | Populated by Discovery (Kingston+) |
| `samp_vmware_license_key_usage` | VMWare License Key Usage | Populated by Discovery (Kingston+) |
| `samp_oracle_options` | Oracle Options | Eligibility filtered by `Considered for licensing` + server relationship |
| `cmdb_ci_spkg` | Software (legacy) | Pre-SAM discovery target; migrated via the migration script |

---

## 12. Known gaps / caveats

- **Property catalog depth:** The official docs do not publish a full numeric catalog of every SAM
  Application Property; the docs prescribe navigating to
  `All > Software Asset > Administration > Application Properties` and modifying per-publisher values
  (e.g. reconciliations' grouping settings, reconciliation scheduling details are described as
  concepts but not exhaustive).
- **Pattern inventory:** The OOTB Discovery patterns for software (e.g. which apps SAM
  specifically leverages — SQL Server, Exchange Server, Oracle Database) are documented at the
  "Basic SAM" level; the exhaustive list of probes/patterns is intentionally not reproduced.
- **Machine-learning algorithmic detail** is not covered (plugin effect only).
- **Migration/version differences** beyond Yokohama and Kingston notes are not diffed here.
- **Classic UI** has limited support from Australia; classic steps are included but the new
  workspace is the primary path.
- **KB articles** cited by the docs but not opened (Now Support restricted access).
- The **Discovery reference** (CMDB/IRE/reconciliation) is a sibling: for the underlying 4-phase
  Discovery flow and CMDB-level identification/reconciliation properties, see
  `ALT_PARALLELSWARM` (`final/FINAL_deepseek-v4-pro.md`). This document focuses on the
  SAM-module-specific additions.
