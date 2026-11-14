# Configuration Reference

> **Status legend:** **V** verified; **C** corroborated; **U** unverified/instance-dependent; **P** practice.
> **Release pin:** **Brazil** for SAM; **Australia** for IRE. Plugin IDs, table names, and property defaults are release-sensitive — verify in your instance.

---

## 1. Plugin matrix

| Capability | Plugin | Entitlement | Notes |
|---|---|---|---|
| SAM Professional master (Brazil+) | `com.sn_samp_master_ws` | Professional | Loads `com.sn_samp_master` + `sn_sam_workspace`. **V** |
| SAM Professional (pre-Brazil) | `com.sn_samp_master` | Professional | Loads `com.snc.samp`, publisher packs, UI components. **V** |
| SAM Professional core | `com.snc.samp` | Professional | Loaded by the master. **V** |
| SAM Foundation | `com.snc.sams` | Foundation | Separate edition; auto-activates the SAM store app. **V** |
| SAM store application | `com.sn_itam_samp` | Professional/Foundation | Auto-activated by the master or Foundation; reconciliation script includes moved here from Yokohama. **V** |
| SAM UI Components | `com.sn_samp_workbench` | Professional | Loaded by `com.sn_samp_master` (pre-Brazil path). **V** |
| Software Asset Workspace | `sn_sam_workspace` | Professional | Store app. **V** |
| ML normalization | `com.sn_sam_ml_normalization` | Professional | Property `com.snc.samp.enable.ml_normalization`. **V** |
| SaaS License Management | `sn_sam_saas_int` | Professional + Store request | Adds Subscription/Consumption metrics. **V** |
| Spend Detection | `com.sn_sam_spend` | Professional | Financial transaction analysis. **V** |
| Engineering Applications | `com.sn_samp_eng_app` | Professional | OpenLM / Open iT concurrent licensing. **V** |
| Adobe pack | `com.sn_samp_adobe` | Professional | Adobe subscription reconciliation. **V** |
| Citrix pack | `com.sn_samp_citrix` | Professional | Virtual apps/desktops. **V** |
| IBM pack | `com.sn_samp_ibm` | Professional | PVU/RVU and Red Hat. **V** |
| Microsoft pack | `com.snc.samp.microsoft` | Professional | SQL Server etc. **V** |
| Oracle pack | `com.snc.samp.oracle` | Professional | Oracle DB/WebLogic. **V** |
| SAP pack | `com.sn_samp_sap` | Professional | Named user compliance. **V** |
| VMware pack | `com.sn_samp_vmware` | Professional | vCenter/vSphere. **V** |
| SCCM 2012 v2 usage | `com.snc.samp_usage_sccm` | Professional | *Will be deprecated in the Tokyo release.* **V** |
| SCCM 2016 usage | `com.snc.samp.usage_sccm_2016` | Professional | *Will be deprecated in the Tokyo release.* **V** |
| SCCM 2012 v2 integration | `com.snc.integration.sccm2012v2` | Professional | Prefer the SCCM Service Graph connector. **V** |
| SCCM 2016 integration | `com.snc.integration.sccm2016` | Professional | Prefer the SCCM Service Graph connector. **V** |
| CSD (uninstall/reclamation) | `com.snc.orchestration.client_sf_distribution` | Professional | Install functionality needs extra licensing. **V** |
| File Signature Normalization | `com.snc.file_signature_normalization` | Professional | File-based discovery. **V** |
| Domain Extensions Installer | `com.glide.domain.msp_extensions.installer` | — | Enables domain-specific Oracle properties. **C** |

> **Edition warning:** Foundation and Professional are different products. Upgrading editions is a programme decision, not a plugin toggle to make casually. **P**

---

## 2. Roles

| Role | Purpose | Contains (Brazil) |
|---|---|---|
| `sam_admin` | Full SAM administration | `sam_user`, `sam_spend_import`, `asset`, `model_manager`, `contract_manager` **V** |
| `sam_user` | All SAM features except admin | `pa_viewer`, `cmdb_read`, `report_user`, `sn_remote_dir_sync.reader` **V** |
| `sam_developer` | Script-writing (trained admins only) | `sam_admin` **V** |
| `sam_integrator` | SaaS integration profiles | `sam_user`, `connection_admin`, `flow_operator` **V** |
| `sam_spend_import` | Spend data import | `pa_viewer` **V** |
| `sn_cmdb_admin` / `itil_admin` | IRE configuration (full) | — **V** (IRE pages) |
| `sn_cmdb_editor` / `itil` | IRE configuration (read) | — **V** (IRE pages) |

**Not official:** `sam_license_manager`, `sn_sam.admin`. Do not use them in runbooks. **C**

---

## 3. Table inventory

### 3.1 Core SAM

| Table | Label | Purpose | Evidence |
|---|---|---|---|
| `cmdb_sam_sw_install` | Software Installation | Discovered/imported installs; source of truth for current software data | **V** |
| `cmdb_sam_sw_discovery_model` | Software Discovery Model | Raw fingerprint; normalized fields + status; never manually created | **V** |
| `cmdb_software_product_model` | Software Model | Purchased product profile; links entitlements to installs | **V** |
| `alm_license` | Software Entitlement | Rights record with metric, quantity, dates, contract | **V** |
| `samp_sw_usage` | Software Usage | Usage evidence at product level | **V** |
| `samp_product_result` | Product Results | Product-level compliance/cost/savings | **V** |
| `samp_license_metric_result` | License Metric Results | Rights algebra per metric | **V** |
| `samp_reconciliation_result` | Reconciliation Result | Reconciliation run record (alert source) | **V** |
| `samp_sw_reclamation_candidate` | Removal Candidate | Reclamation candidates and savings | **V** |
| `sam_sw_product_lifecycle` | Product Lifecycle | EOL/EOS data | **V** |
| `samp_sw_product_definition` | Software Product Definition | PPN / product definition | **V** |
| `samp_normalization_suggestion` | Normalization Suggestions | Suggested normalized values; overview labels the list `samp_normalization_suggestions`; verify exact table | **V/C/U** |
| `samp_entitlement_import` | Entitlement Import Error | Import errors | **V** |
| `samp_job_log` | Software Asset Job Result | Job run results | **V** |
| `sam_sw_dedup_rule` | Custom Deduplication Rules | Product-level dedup rules | **V** |
| `samp_sw_unrecognized_subscription_identifier` | Unrecognized Subscription Identifier | SaaS subscription matching | **V** |
| `samp_sso_application` | SSO Application | SaaS SSO discovery | **V** |
| `samp_vmware_license_key` | VMware License Key | Discovery-populated | **U** |
| `samp_oracle_options` | Oracle Options | Oracle licensing options | **U** |
| `cmdb_ci_spkg` | Software (legacy) | Pre-SAM discovery target | **U** |
| `samp_bulk_import` | Entitlement Import | Bulk import status | **V** |
| `asset_job_log` | Asset Job Log | Content download failures | **V** |

### 3.2 CMDB / IRE

| Table | Purpose | Evidence |
|---|---|---|
| `cmdb_identifier` | Identifier rules | **V** |
| `cmdb_identifier_entry` | Identifier criteria entries | **V** |
| `cmdb_reconciliation_definition` | Static reconciliation definitions | **V** |
| `cmdb_dynamic_reconciliation_definition` | Dynamic reconciliation definitions (CMDB 360) | **V** |
| `cmdb_ire_data_source_rule` | Insert-gate rules | **V** |
| `cmdb_datasource_last_update` | Last writer per attribute | **V** |
| `cmdb_ire_partial_payloads` | Partial payloads (retryable) | **V** |
| `cmdb_ire_incomplete_payloads` | Incomplete payloads (logging only) | **V** |
| `cmdb_dynamic_ire_skip_class` | Classes excluded from dynamic IRE | **U** (secondary source only) |

### 3.3 Org / evidence

| Table | Purpose |
|---|---|
| `ast_contract` | Contract evidence |
| `alm_asset` | Asset base |
| `core_company` | Vendor/company |
| `samp_sw_publisher` | Normalized publisher (secondary source) **C/U** |
| `sc_cat_item` | Catalog item (requestable software) **C** |

---

## 4. The six layers of software identity

Use this to prevent the most common architecture error — conflating vendor, publisher, part number, model, and catalog item:

| Layer | Record | Question |
|---|---|---|
| 1. Vendor | `core_company` | Who sells it? |
| 2. Publisher | `samp_sw_publisher` | Who publishes it? |
| 3. Product definition (PPN) | `samp_sw_product_definition` | Which exact purchasable SKU? |
| 4. Software model | `cmdb_software_product_model` | Which purchased product/version profile? |
| 5. Discovery model | `cmdb_sam_sw_discovery_model` | What did we observe? |
| 6. Catalog item | `sc_cat_item` | What can a user request? |

**C** for the layer names; **V** for the core tables (`cmdb_software_product_model`, `cmdb_sam_sw_discovery_model`, `sc_cat_item`, `core_company`). Verify `samp_sw_publisher` / `samp_sw_product_definition` in your release. **U**

**Rule:** catalog is last, not first. Publishing a catalog item does not create a software model or an entitlement. **P**

---

## 5. Property inventory (must-consider)

| Property | Effect | Default |
|---|---|---|
| `com.snc.samp.recon.group` | Weekly reconciliation group | `None` **V** |
| `com.snc.samp.recon.subgroup` | Weekly reconciliation subgroup; must differ from group when not `None` | `None` **V** |
| `com.snc.samp.recon.max_workers` | Parallel jobs | No default documented **V** |
| `com.snc.samp.recon.enablecustommetrics` | Custom metrics in reconciliation | `Yes` **V** |
| `com.snc.samp.debug` | Debug reconciliation | `No` **V** |
| `com.snc.samp.automaticsmrcreation` | Auto-create models for licensable products | Release-dependent **V** |
| `com.snc.samp.automaticsmcreation` | Auto-create models for not-licensable products | `No` **V** |
| `com.snc.samp.unlicensed_smr_creation` | Disables model-result creation for unlicensed models when `False`; `True` creates them | `False` **V** |
| `com.snc.samp.exclude_device_flag` | Name of the boolean column on `cmdb_ci_hardware` (e.g. `u_exclude_from_sam`); property default not stated; column default `false` | Not stated **V** |
| `com.snc.samp.manage.published.products` | Published-products scope | `false` **V** |
| `com.snc.samp.oracle.reconlevel` | Oracle VMware aggregation | `ESX cluster` **V** |
| `com.snc.samp.oracle.hostaffinityenabled` | VM-host affinity; applies only when `reconlevel = vCenter(s)` | No default documented **V** |
| `com.snc.sam.auto_suite_inference` | Infer suite parent | `false` **V** |
| `com.snc.samp.wide_net_normalization.enabled` | Wide-net normalization | Enabled **V** |
| `com.snc.samp.enable.ml_normalization` | ML normalization | Enabled **V** |
| `sn_sam_workspace.sam_license_operations_list_count` | Workspace count threshold | `5000000` **V** |
| `sam_reclamation_flow_error_timeout` | Reclamation error timeout (days) | `30` **V** |
| `com.snc.samp.eng.app.peak.usage.period` | Engineering peak window (days) | `30` **V** |
| `com.snc.samp.citrix.app.license.period` | Citrix app license period (days) | `90` **V** |
| `com.snc.samp.sam_ci_billing_threshold` | Cloud billing data staleness (days) | `30` **V** |
| `com.snc.samp.use_lifecycle_approximation` | Include approximate lifecycle dates | Enabled **V** |
| `com.snc.samp.generate.calculated.lifecycles` | Generate calculated EOS/EOES/EOL dates | No default documented **V** |
| `com.snc.samp.windowserver.license.threshold` | Windows Server Datacenter vs Standard cost ratio | `4.59` **V** |
| `com.snc.samp.sqlserver.standard_sa.to.enterprise_sa.cost.ratio` | SQL Server Standard SA vs Enterprise SA cost ratio | `0.25` **V** |
| `com.snc.samp.ms.sa.to.nonsa.cost.ratio` | Microsoft SA vs non-SA cost ratio | `1.25` **V** |
| `sn_samp_ibm_lic.default_region` | Default IBM device region | North America and South America **V** |
| `sn_samp_ibm_lic.ilmt_api_version` | ILMT/BigFix Inventory API version | No default documented **V** |
| `samp.spend_prediction_service.max_label_attempts` | Spend label retries | `3` **V** |

Access: `All > Software asset > Administration > Properties`, or the Configuration Console for SAM. **V**

---

## 6. Scheduled job inventory

Official cadence is stated only where the Brazil page states it. "Not documented" means the job exists in v1/secondary evidence but the fetched pages do not publish a cadence.

| Job | Cadence | Purpose | Evidence |
|---|---|---|---|
| `SAM - Normalize discovery models using content library rules` | Daily | Normalize models; assign status | **V** |
| `SAM - Daily Job` | Daily | Required for overview/dashboard widgets | **V** |
| `SAM - Discovery Model Normalization job` | Daily | Update normalization trend charts | **V** |
| `SAM - Central Data Service Download Status` | Daily | Update CDS download status | **V** |
| `SAM - Trigger Full Scan` | Weekly | Health-check KPIs | **V** |
| `SAM — Adjust Installs for excluded CIs` | Not documented | Apply exclude-CI flag | **V** |
| `SAM - Software License Reconciliation` | Weekly default (schedule configurable) | Main compliance calculation | **V** (cadence); **C** (job-name attribution) |
| `SAM – Discovery Model to Software Model matching` | Not documented | Map discovery models to software models | **V** (job name) / **U** (cadence) |
| `SAM - Deduplicate Install Table` | Not documented | Dedup installs | **C** |
| `SAM - Subscription Maintenance` | Not documented | Subscription lifecycle | **C** |
| `SAM - Get install count for software model` | Not documented | Install counts | **C** |
| `SAM/CI - Populate Licensing Data` | Not documented | CI licensing data | **C** |
| `SAM - Apply latest content changes` | Manual | Content updates | **C** |
| `SAM - Label Spend Transactions` | Not documented | Label spend transactions | **V** (property reference) |

Filter in **Scheduled jobs**: `Name starts with SAM`. **V**

> Do not publish a specific hour for a job unless the official page states it. The reconciliation page says **weekly default**, not a specific day/time. **V/U**

---

## 7. UI entry points

| Task | Workspace path | Classic path |
|---|---|---|
| Overview | Software Asset Workspace → Software asset overview | — |
| Reconciliation | Workspace → License usage | `All > Software asset > Reconciliation > Historical Results` **V** |
| Discovery models | Workspace → License operations → Discovery models | `All > Software asset > Discovery > Discovery models` **C** |
| Software usage | Workspace → License operations → Discovery → Software usage | `All > Software asset > Discovery > Software usage` **V** |
| Dedup rules | Workspace → Administration → Deduplication rules | — **V** |
| Properties | — | `All > Software asset > Administration > Properties` **V** |
| Content Library | — | Classic Administration menu exposes **Content Service Setup**, **Custom Products**, **Pattern Normalization Rules**, etc.; a "Content Library" menu item is **U** in Brazil |
| Content Service | — | `All > Software asset > Administration > Content Service` **C** |
| IRE rules | — | `All > Configuration > CI Class Manager` / `Identification/Reconciliation` **V** |

Classic UI support becomes limited **from Brazil**; after activating `com.sn_samp_master_ws`, the classic UI is **inaccessible**. Prefer the workspace. **V**

---

## 8. Integrations

| Direction | System | Mechanism | Purpose |
|---|---|---|---|
| Inbound | ServiceNow Discovery | Patterns, MID Server | Installs on servers |
| Inbound | SCCM / MECM | Service Graph connector (preferred) | Installs, devices, metering |
| Inbound | Intune | Service Graph connector | Endpoint installs |
| Inbound | Jamf Pro | Service Graph connector | Apple estate |
| Inbound | ACC | Agent | Endpoint inventory |
| Inbound | BigFix / Tanium / Flexera / Lansweeper | Import/API | Specialized inventory |
| Inbound | M365 / Salesforce / Adobe / Zoom | SaaS direct integrations | Subscriptions and seats |
| Inbound | Oracle LMS | CSV/extract | Audit-grade usage |
| Inbound | IBM ILMT / BigFix Inventory | API/CSV | PVU sub-capacity evidence |
| Inbound | SAP | CSV/API | Named-user classification |
| Outbound | Procurement | PO creation | True-up purchase |
| Outbound | CSD | Orchestration | Uninstall/reclaim |
| Outbound | Reporting / finance | Platform reports / export | Cost allocation |

**V** for the documented Discovery/SCCM/SaaS/procurement/CSD paths; **C** for the broader third-party list. The **Intune/Jamf Pro** Service Graph connectors are **U** in the fetched Brazil SAM pages and **C** in the wider connector set.

---

## 9. Domain separation

- Oracle reconciliation properties support domain separation via **Application Properties** after activating `com.glide.domain.msp_extensions.installer`. **C**
- Domain-specific values are set on the Application Property Values related list. **C**
- Reconciliation rules can be scoped to domains; parent-domain rules apply to child domains unless overridden. **V**

---

## 10. Change-control surface

| Change | Blast radius | CAB? |
|---|---|---|
| Manual normalize one model | Low | Owner approval |
| Add pattern/wide-net rule | Medium | Sample-test |
| Create/match a software model | Medium | High-spend review |
| Change license metric on model/entitlement | **High** | Yes |
| Change reconciliation group/subgroup | **High** | Yes |
| Change IRE identifier attributes | **High** | Yes |
| Disable a SaaS connector | **High** | Yes |
| Change published-products scope | Medium/High | Yes |
| Change exclude-CI flag/property | Medium | Yes if broad |

**P** (synthesized from the operational evidence). Use a Change Record and a rollback plan for High items.

---

## 11. Verification checklist

```text
# Edition and plugins
sys_plugins.list  (filter on sn_samp, sn_sam, com.snc.samp)

# Tables present
sys_db_object.list  (name STARTS WITH cmdb_sam OR STARTS WITH samp_)

# Roles
sys_user_role.list  (name IN sam_admin, sam_user, sam_developer, sam_integrator)

# Jobs
sysauto_script.list (name STARTS WITH SAM)

# Properties
sys_properties.list (name STARTS WITH com.snc.samp OR com.snc.sam)

# IRE
cmdb_identifier.list
cmdb_reconciliation_definition.list
cmdb_ire_data_source_rule.list
```

**V** for table/record names; **U** for exact filters in your release.
