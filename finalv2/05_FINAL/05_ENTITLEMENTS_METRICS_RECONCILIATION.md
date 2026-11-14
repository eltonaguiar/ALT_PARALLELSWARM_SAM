# Entitlements, License Metrics, and Reconciliation

> **Status legend:** **V** verified; **C** corroborated; **U** unverified/instance-dependent; **P** practice.
> **Release pin:** **Brazil** (updated 2025-07-31 → 2026-10-19).

---

## 1. Software model vs entitlement

| Record | Table | What it is |
|---|---|---|
| **Software model** | `cmdb_software_product_model` | A profile of purchased software: publisher, product, version/edition scope, metric attributes. Multiple entitlements can link to one model. **V** |
| **Entitlement** | `alm_license` | The rights record: software model, license metric, quantity, dates, license type, contract/PO evidence. **V** |

The model says **what it is**; the entitlement says **what you may use**. Reconciliation needs both, plus normalized installs. **V/P**

---

## 2. Entitlement anatomy

Minimum fields for a defensible record:

| Field | Why it matters |
|---|---|
| Software model | Must be the normalized model, not a free-text product |
| Publisher / product / version / edition | Used in PPN and model resolution |
| License metric | Determines how demand is counted |
| Purchased quantity | Numerator in the compliance calculation |
| License type | Perpetual / subscription / maintenance / SA / upgrade / step-up / add-on / From SA |
| Start and end date | Expiry drives compliance and renewals |
| Contract (`ast_contract`) | Audit evidence chain |
| Purchase order / invoice | Audit evidence |
| Unit cost / currency | Cost, true-up, savings |
| Cost center / owned by | Chargeback and accountability |
| PPN (publisher part number) | Content Library model resolution |
| Allocations (user/device) | Required for named-user / named-device metrics |
| Source system + record ID | Idempotency and import error handling |

**V** for the documented fields and PPN behavior; **P** for the audit-evidence minimum set.

**Hygiene rules:**

- One entitlement per contract line, not per PO line. **P**
- Never overwrite quantity to make a report look compliant; create a true-up or adjustment record. **P**
- Maintenance alone does not grant usage rights. **V**
- Metric mismatch between model and entitlement is a silent failure. **P**

---

## 3. PPN and model resolution

When importing entitlements, the system resolves the software model differently depending on whether a **Publisher Part Number (PPN)** is present, whether the import is standard (custom) or MLS, and whether automatic model creation is enabled. **V**

### 3.1 PPN blank (standard/custom import)

1. Try exact match on **Publisher, Product, Version, Edition, Platform, Language**. **V**
2. If no exact match, try a relaxed search (any platform or language). **V**
3. If no match:
   - auto-create enabled (default) and publisher + product identified → create a model; **V**
   - otherwise → error **`PPN and SM not found`**. **V**

For **MLS** imports, a blank PPN does not trigger a model search from other fields; the row continues but likely fails downstream. **V**

### 3.2 PPN provided

- PPN exists in the Content Library:
  - exactly one model → assign; **V**
  - multiple models → error **`Multiple software models found for the Publisher Part Number`**. **V**
- PPN missing/inactive:
  - exact search on Publisher/Product/Version/Edition/Platform/Language; **V**
  - if model found → entitlement created without PPN reference (if no other errors); **V**
  - if not found, auto-create enabled, the import is **standard (custom)**, and publisher/product are identified → create model; **V**
  - otherwise → error **`PPN and SM not found`**. **V**

**Import errors** are reviewed on the entitlement import error record; a `Create PPN` action can generate a custom part number. **V**

---

## 4. License types and their reconciliation impact

| License type | Publisher applicability | Impact |
|---|---|---|
| **Perpetual** | All | Indefinite use; no maintenance rights unless linked to a maintenance/SA entitlement. **V** |
| **Perpetual + Software Assurance** | Microsoft | SA benefits applied automatically (new-version rights, mobility, virtualization). **V** |
| **Subscription** | All subscription products; also non-subscription products using subscription licenses | Compliance driven by user subscriptions; SA benefits may apply. **V** |
| **Perpetual + Maintenance** | All (notably Oracle, VMware) | Maintenance benefits applied automatically. **V** |
| **Upgrade** | All | Link upgraded entitlements to the higher edition; use the **Upgraded Entitlements** tab. **V** |
| **Software Assurance** | Microsoft | Not reconciled unless linked to a base perpetual license. **V** |
| **Maintenance** | All | Not reconciled alone; must link to a base perpetual license. **V** |
| **Step-up** | All per the license-types page; the entitlement-import page restricts step-up to **Microsoft** | Edition upgrade within active maintenance/SA. **C/U** — the two official pages conflict; verify your release |
| **Subscription Step-up** | Subscription products | Same as step-up for subscriptions. **V** |
| **Add-on** | Microsoft | Must link to a perpetual Office legacy license with active SA. **V** |
| **From SA** | Microsoft | Must link to a perpetual Office legacy license with active SA. **V** |

**Rule:** a license type that does not grant usage rights must not be counted as a usage right. **V/P**

---

## 5. License metrics — summary

Metrics are grouped by publisher; publisher packs add their groups. **V**

| Metric group | Representative metrics | Notes |
|---|---|---|
| **Common** | Per Core, Per Device, Per Named Device, Per Named User, Per Processor, Per User, User CAL, Device CAL, User/Device CAL, Concurrent User, Resource Consumption | Base metrics |
| **Adobe** | Per Device, Per User, User Subscription | Adobe pack |
| **Citrix** | Concurrent User, Per Device, Per Processor, Per User, Per User/Device | Citrix pack + Discovery |
| **IBM** | Authorized User, Authorized User Value Unit, Employee/External UVU, Per Device, Per Named User, Per Processor, Per User, PVU, RVU, VPC, and additional resource metrics | IBM pack; ILMT for sub-capacity |
| **Microsoft** | Device CAL, Per Core, Per Core (with CAL), Per Device, Per Processor, Per User, Server (Per Instance/Per Server), User CAL, User Subscription | Microsoft pack |
| **Oracle** | Named User Plus, Per Processor, Employee | Oracle pack |
| **Red Hat** | Per Socket-pair, Per Core | IBM pack |
| **SAP** | Named User, Engine Measurement, Digital Access, User Subscription, FUE | SAP pack |
| **Subscription** | User Subscription | SaaS License Management |
| **Consumption** | SaaS Consumption | SaaS License Management |
| **VMware** | Per Application Instance, Per Device, Per Named User, Per OSI, Per Processor, Per Core | VMware pack |

**V** (Brazil license metrics page). This is a summary, not the full metric catalog; use the page for the complete list and descriptions. Two groups are easy to miss:

- **CrowdStrike**: Reserved Hourly Average Sensor, Sensor Subscription. **V**
- **Concurrent Licenses** (under Common): Floating, Token, Network — available with the Engineering Applications plugin + OpenLM / Open iT. **V**

**Metric attributes** (for example, VMware maximum cores per processor) are set on the software model's **Metric Attributes** related list. **V**

**Resource Value table:** `samp_sw_resource_value` supports a 1:1 calculation between **Unit consumption** and **Licenses required** for Resource Consumption, Concurrent User, and custom metrics. **V**

---

## 6. Reconciliation — how it works

Reconciliation is a scheduled job, **weekly by default**, and can be run on demand for all or specific publishers, groups, and subgroups. **V**

Group/subgroup dimensions: **country, department, company, region, cost center**. Defaults are set in `All > Software asset > Administration > Properties`. **V**

### 6.1 Conceptual steps

1. Gather active entitlements for the software model (date-valid). **V/P**
2. Gather normalized, licensable installs mapped to the model, deduplicated per device (and per user/device as the metric requires). **V/P**
3. Apply usage evidence for reclamation and "not in use" classification. **V/P**
4. Apply publisher rules, exclusions, suite roll-ups, downgrade/upgrade rights. **V/P**
5. Compute rights owned / used / available and the compliance position per metric. **V**
6. Persist product, software-model, and license-metric results. **V**
7. Roll up to dashboards and the License Position report. **V**

### 6.2 What reconciliation is not

It is a **report**, not a correction. Fix the model, entitlement, normalization, or dedup rule — do not edit the result. **P**

---

## 7. Three tiers of results

### 7.1 Product Results (`samp_product_result`)

For all models and installs of a product, per publisher. **V**

Related lists include:

- Software Model Results **V**
- Licensed Installs **V**
- Unlicensed Installs (SAP: Unlicensed Users or Unlicensed Engines) **V**
- Unlicensed Subscriptions **V**
- Removal Candidates **V**

Product results include compliance status, true-up cost, over-licensed amount, and potential savings, and are generated for licensable products even without a defined software model. **V**

### 7.2 Software Model Results

For each model related to the product. Created only when a software model or entitlement exists for the product. **V**

Related lists:

- License Metric Results **V**
- Remediation Options **V**
- Licensed Installs **V**
- Unlicensed Installs (SAP: Unlicensed Users) **V**
- Unlicensed Subscriptions **V**
- Unlicensed Consumptions **V**
- Unlicensed Options (Oracle) **V**
- Removal Candidates **V**
- Purchase Orders (when Procurement plugin active) **V**

### 7.3 License Metric Results (`samp_license_metric_result`)

For each metric associated with the model. **V**

Form fields include:

- **License metric** **V**
- **Software model result** **V**
- **Group / Subgroup** **V**
- Rights owned **V**
- Rights used **V**
- Rights available **V**
- Over-licensed amount **V**
- Right allocations: **Allocated in use**, **Not allocated in use**, **Allocated not in use**, **Not allocated**, **Allocations needed** **V**
- Rights Used By (hidden for IBM RVU) **V**
- Rights Needed By **V**
- Licensed Installs (not available for SAP metrics) **V**
- Installs Used (SAP) **V**
- Downgrades/Upgrades **V**
- Licensed Subscriptions **V**
- Cloud Special Rights (AWS/Azure) **V**
- Nontransferable rights (Microsoft Per Core / Per Core with CAL) **V**
- Legacy license (AWS/Azure dedicated hosts) **V**

**No single `sam_sw_reconciliation_result` table is documented for these tiers** (**C** — absence in the fetched pages). The run record is `samp_reconciliation_result` (**V**); the analysis is the three tiers above (**V**). The **Software Model Results table name is not documented** in the Brazil pages; v1's `samp_sw_model_result` is **U**. See [`../CONFLICT_LOG.md`](../CONFLICT_LOG.md) C-02.

---

## 8. Rights algebra

| Bucket | Definition | What it tells you |
|---|---|---|
| **Rights owned** | Sum of active rights from entitlements sharing the metric | Supply |
| **Rights used** | Allocated in use + not allocated in use + installed | Demand currently consuming rights |
| **Rights available** | Rights owned − rights used | Headroom |
| **Allocated in use** | Allocated and licensing an install | Healthy consumption |
| **Not allocated in use** | Licensing an install but not allocated | Remediation: create allocations or remove unallocated installs |
| **Allocated not in use** | Allocated but not licensing an install | Wasted rights; remediation: remove allocations |
| **Not allocated** | Owned − allocated, regardless of install | Unassigned supply |
| **Allocations needed** | Allocations required for compliance (named user/device) | Gap |

**V** (Brazil license metric result fields page).

When **Not allocated in use > 0**, two remediation options are created automatically (except User CAL / Device CAL): **Create Allocations** and **Remove Unallocated Installs**. When **Allocated not in use > 0**, **Remove Allocations** is created. **V**

---

## 9. Compliance positions

**Software model status** (on the software model / License Position report) is **Compliant** or **Not Compliant**. **V** Product-level compliance is the **Product Results** status. **V**

The richer vocabulary is interpretive and useful for teaching:

| Position | Meaning | Action |
|---|---|---|
| Compliant | Rights ≥ demand | Monitor |
| Over-licensed | Rights > demand | Reclaim / reduce renewal |
| Under-licensed | Rights < demand | True-up or reclaim |
| Unlicensed | Installs with no entitlement | Remove / buy / reclassify |
| Not counted | Excluded by rule | Review annually |
| Unknown | Insufficient data | Fix normalization or feed; do not report as compliant |

**P** for the six-state vocabulary; **V** for the binary product field. Do not present "Unknown" as a product status value.

---

## 10. License Position report

The report shows compliance details for each software model in one list. **V**

| Field | Meaning |
|---|---|
| Software publisher | Publisher of the model |
| Software product | Product |
| Edition / Version | Model scope |
| Software model status | Compliant / Not Compliant |
| License metric | Counting basis |
| Total spend | Cost of rights owned |
| Rights owned | Sum of active rights |
| Rights used | Allocated + not allocated and installed |
| Rights needed | Rights to cover unlicensed installs |
| Rights available | Owned − used |
| Unlicensed installs | Installs not covered by entitlements |
| True-up cost | Estimated remediation cost based on the **least number of rights needed** (lowest-cost purchase-rights option) |
| Potential savings | Estimated savings from reclaiming unused installs |
| Over-licensed amount | Cost of unused rights |
| Software model | Model name |
| Group / Subgroup | Reconciliation grouping |

**V**

Two license position reports are generated when a model has both perpetual-SA and subscription entitlements (active maintenance true/false). A single report is generated for unlicensed installs, and another for unlicensed subscriptions; if both exist, two reports. **V**

---

## 11. Remediation and reclamation

Available remediation from model results:

- Create or remove allocations. **V**
- Remove unallocated installs. **V**
- Remove unlicensed installs. **V**
- Purchase rights (creates a purchase order when Procurement is active). **V**

Reclamation (optimization):

- Removal candidates are generated for unused software. **V**
- Reclamation rules and workflows; CSD can automate uninstall. **V**
- `sam_reclamation_flow_error_timeout` defaults to **30 days** before a reclamation flow closes as canceled. **V**
- Engineering applications peak usage period defaults to **30 days** (`com.snc.samp.eng.app.peak.usage.period`). **V**
- Citrix application license period defaults to **90 days** (`com.snc.samp.citrix.app.license.period`). **V**

**Practice:** require a sustained inactivity window (typically 60–90 days) and business owner sign-off before reclaiming. **P**

**Reading caveats:** **Licensed Installs** is not available for SAP metrics, and **Rights Used By** is hidden for the IBM RVU metric. **V** Brazil also has an upgrade note for reclamation rules involving suite parents; review it before upgrading. **C**

---

## 12. SaaS license management

- Requires `sn_sam_saas_int` (Store request) and SAM Professional. **V**
- Adds **Subscription** and **Consumption** metric groups. **V**
- Pulls subscriptions and assigned seats from vendor APIs; user-based metrics dominate. **V/P**
- Key records include `samp_sw_unrecognized_subscription_identifier`, `samp_sso_application`, and subscription profiles. **V**
- **Overlapping usage** and **SSO vs direct integration** are documented dashboard/analysis areas. **C**
- A dead connector looks identical to "no waste". Monitor connector health and assign an owner. **P**

---

## 13. Reporting map

| Widget / report | Source table |
|---|---|
| Publishers out of compliance | `samp_product_result` **V** |
| Products out of compliance | `samp_product_result` **V** |
| Over-licensed amount | `samp_product_result` **V** |
| Total true-up cost | `samp_product_result` **V** |
| Top 5 publishers true-up cost | `samp_product_result` **V** |
| Potential savings | `samp_product_result` **V** |
| Actual savings | `samp_sw_reclamation_candidate` **V** |
| Software spend | `samp_license_metric_result` **V** |
| Software installs normalization status | `cmdb_sam_sw_discovery_model` **V** |
| End of life products | `sam_sw_product_lifecycle` **V** |
| Expiring maintenance/subscription | `alm_license` **V** |
| Last reconciliation failure/completed | `samp_reconciliation_result` **V** |
| Scheduled jobs failed | `samp_job_log` **V** |
| Entitlement import errors | `samp_entitlement_import` **V** |
| New normalization suggestions | `samp_normalization_suggestion` (singular) **V**; overview labels the list `samp_normalization_suggestions` **C** |
| New PPNs added | `samp_sw_product_definition` **V** |
| Upcoming renewals | `ast_contract`, `alm_license` **V** |
| Entitlement import status | `samp_bulk_import` **V** |
| Content download failures | `asset_job_log` **V** |

---

## 14. Health check

The Health Check Store app reviews SAM configuration and recommends corrections. **V**

Current check categories include:

- SQL Server Config **V**
- SQL Server CMDB **V**
- Windows Server CMDB **V**
- Windows Server Config **V**
- Oracle Database **V**
- Java - Oracle **V**
- WebLogic Server - Oracle **V**
- Microsoft 365 **V**
- General **V**

The scheduled job **`SAM - Trigger Full Scan`** runs weekly on KPI categories from the Content Service. Results appear on the Health Check dashboard. **V**

---

## 15. Key properties

| Property | Effect | Default |
|---|---|---|
| `com.snc.samp.recon.group` | Default weekly reconciliation group | `None` **V** |
| `com.snc.samp.recon.subgroup` | Default subgroup (must differ from group) | `None` **V** |
| `com.snc.samp.recon.max_workers` | Parallel reconciliation jobs | No default documented **V** |
| `com.snc.samp.recon.enablecustommetrics` | Use custom metrics in reconciliation | `Yes` **V** |
| `com.snc.samp.debug` | Debug reconciliation results (performance impact) | `No` **V** |
| `com.snc.samp.automaticsmrcreation` | Auto-create models for licensable products | Release-dependent **V** |
| `com.snc.samp.automaticsmcreation` | Auto-create models for not-licensable products | `No` **V** |
| `com.snc.samp.unlicensed_smr_creation` | **Disables** model-result creation for unlicensed models when `False`; when `True`, creates them | `False` **V** |
| `com.snc.samp.exclude_device_flag` | Name of the boolean column on `cmdb_ci_hardware` to exclude CIs (e.g. `u_exclude_from_sam`); property default not stated; column default `false` | Not stated **V** |
| `com.snc.samp.manage.published.products` | Restrict reports to published products | `false` **V** |
| `com.snc.samp.oracle.reconlevel` | Oracle/WebLogic VMware aggregation level | `ESX cluster` **V** |
| `com.snc.samp.oracle.hostaffinityenabled` | Apply VM-host affinity; only applicable when `oracle.reconlevel = vCenter(s)` | No default documented **V** |
| `com.snc.sam.auto_suite_inference` | Infer parent suite for child models | `false` **V** |
| `com.snc.samp.wide_net_normalization.enabled` | Wide-net normalization | Enabled **V** |
| `com.snc.samp.enable.ml_normalization` | ML normalization | Enabled **V** |
| `sn_sam_workspace.sam_license_operations_list_count` | Workspace list count threshold | `5000000` **V** |

---

## 16. Verification queries

```text
# Entitlements with no model or metric
alm_license.list  (software_model is empty OR license_metric is empty)

# Models with multiple metrics / conflicting metrics
cmdb_software_product_model.list
samp_license_metric_result.list

# Latest reconciliation run
samp_reconciliation_result.list  (order by sys_created_on desc)

# Product / model / metric results
samp_product_result.list
samp_license_metric_result.list

# Reclamation candidates
samp_sw_reclamation_candidate.list

# Import errors
samp_entitlement_import.list  (error status = open)
```

**V** for table names; **U** for exact field API names.

---

## 17. Unverified items

- Exact reconciliation day/time in your instance (the docs say weekly; the day/time is schedule configuration). **U**
- `samp_entitlement` / `cmdb_sam_entitlement` are **not documented for Brazil**; do not use them in new work. `alm_license` is the documented table. Verify only if migrating from an older release. **U**
- Publisher-specific rule details (Oracle core factors, IBM PVU tables, SAP indirect access) are contract-specific and not reproduced here. **U**
- Whether your instance has custom license metrics enabled and which ones. **U**
