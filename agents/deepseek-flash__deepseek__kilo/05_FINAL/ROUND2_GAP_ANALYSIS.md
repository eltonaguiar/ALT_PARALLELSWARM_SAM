# ROUND 2 — Perplexity cross-check, module-setup cross-reference, and missed items

**Agent:** `deepseek-flash__deepseek__kilo` · **Model:** `deepseek/deepseek-flash` · **Provider:** DeepSeek · **Harness:** Kilo CLI
**Date:** 2026-11-13 · **Release pin:** Brazil (Australia corroboration marked **C**)
**Inputs:** (a) this fleet's SAM docs — `grok-4.6__xai__kilo` WT1/WT2/WT3, `beam__kilo__cli` WT1, `final/FINAL_SAM_MODULE_REFERENCE.md`; (b) `ALT_PARALLELSWARM` CMDB/Discovery finals; (c) the Perplexity review supplied by the user; (d) Brazil ITAM corpus.
**Purpose:** verify the critique rather than accept it, find what the *repo* missed, and close the gaps with new content + a gate checklist.

Verdict legend: **Covered** = already correct in this repo (cite section) · **Partial** = present but too thin to run from · **Missing** = not in the repo before this file · **Wrong** = critique does not hold for this repo.

---

## 0. Executive verdict

The Perplexity review is directionally right about **what SAM needs** and largely wrong about **what this repo already contains**. The repo (especially `grok-4.6__xai__kilo` WT1 and this pass's `SAM_MODULE_REFERENCE.md`) already covers entitlements, software models, normalisation, Content Library/PPN, suite logic, dedup, discovery-model governance and IRE. What it genuinely lacked was the **operational layer around the data**: roles/RACI, source-system contracts, numeric test cases, acceptance gates, rollback/exception, change control, audit evidence, SaaS lifecycle, a per-publisher metric matrix, and cloud/container scope. Those are added below.

**The one-line distinction the critique gets exactly right:** CMDB establishes *what exists*; SAM must additionally establish *what was purchased, how it may be used, what is installed or consumed, and whether the two reconcile*. Our reference has that pipeline; it did not have the governance that makes the pipeline trustworthy.

---

## 1. Perplexity claim-by-claim audit

| # | Perplexity claim | Where the repo stands | Verdict | Action |
|---|---|---|---|---|
| 1 | Entitlement data (purchase, metrics, quantities, contracts, maintenance dates, upgrade/downgrade, allocations) overlooked | `alm_license` §2.5, §10 steps 11–13; licence types §7.3; downgrade rights §2.3; allocations §14.3 | **Covered** | None |
| 2 | Software models (publisher, product, version/edition, discovery map, suites, upgrade/downgrade) overlooked | §2.3, §6.4, §10 | **Covered** | None |
| 3 | Normalisation rules / exception handling overlooked | §5 (six statuses, transitions, suggestions, revert), §6, §11 | **Covered** | None |
| 4 | License metrics / vendor-specific selection overlooked | Metrics named in §7.3/§7.5 and §14, but no per-publisher matrix | **Partial** | Added §4.11 vendor metric matrix |
| 5 | SaaS seat/usage ingestion, subscriptions, renewals, consumption overlooked | Mentioned in §12.3 and §13 only; no lifecycle | **Partial** | Added §4.10 |
| 6 | Content Library / PPN dependency overlooked | §5.6, §10 Path A (all PPN resolution branches), §14 | **Covered** | None |
| 7 | Prerequisite/dependency sequence missing | §1 has the setup order | **Partial** | Added §4.12 dependency map |
| 8 | Roles (`sam_admin`, `sam_user`, `model_manager`, `asset`, `procurement_user`, `contract_manager`) | §3 lists some; no duty matrix | **Partial** | Added §4.2 |
| 9 | "Define the SAM data model before configuration" | §2 is that data model | **Covered** | None |
| 10 | Inventory sources (Discovery, SCCM/MECM, Jamf, other) | §4 and §13 | **Covered** (Jamf flagged as SGC, not native) | None |
| 11 | Import entitlements before reconciliation | §1 step 6 | **Covered** | None |
| 12 | High-value publishers first, validate discovery maps/metrics | §1 step 3, §10, §14.1, §6.4 | **Covered** | None |
| 13 | Run/validate reconciliation, inspect shortfall/surplus, Workbench | §7, §12.3 | **Covered** | None |
| 14 | Pilot before scale | §1 step 10, §14.1 `manage.published.products` | **Covered** | None |
| 15 | CI-to-install linkage for per-device/per-user metrics | §2.1 `installed_on`, §4.5, §12 | **Covered** | None |
| 16 | Duplicate and stale install records; decommission/retired/re-imaged | §4.6, §9 (CI retired/stolen deletes installs), §16 | **Covered** | None |
| 17 | IRE for all CMDB sources, no uncontrolled duplicates | §4.4 | **Covered** for installs; note CMDB IRE is in `ALT_PARALLELSWARM` | None |
| 18 | Discovery-model governance / review approval | §5 (suggestions, manual), §11 | **Partial** — no owner/RACI | Added §4.3 |
| 19 | Suite/relationship logic (upgrades, downgrades, cross-grade) | §6.4, §7.3, §10 | **Covered** for suites/downgrades; **cross-grade** not named | Added to §4.11/§4.14 |
| 20 | Data ownership / RACI | not present | **Missing** | Added §4.3 |
| 21 | Source-system contracts (frequency, required fields, error handling) | scattered in §4/§13 | **Partial** | Added §4.4 |
| 22 | Role-based access separation | §3/§13 only | **Partial** | Added §4.2 |
| 23 | Auditability (entitlement ↔ PO ↔ invoice ↔ contract ↔ allocation ↔ result) | not present | **Missing** | Added §4.9 |
| 24 | Optimisation workflow owners | §9 covers mechanics, not owners | **Partial** | Added §4.3/§4.7 |
| 25 | Change control for compliance-affecting config | not present | **Missing** | Added §4.8 |
| 26 | Test cases with expected results | not present | **Missing** | Added §4.5 |
| 27 | Data-quality acceptance criteria/thresholds | not present | **Missing** | Added §4.6 |
| 28 | Rollback / exception procedures | not present | **Missing** | Added §4.7 |
| 29 | SaaS custom integration caveat | only implied | **Partial** | Added §4.10 |
| 30 | Vendor-specific licensing (generic "Common" is insufficient) | metrics listed, no matrix | **Partial** | Added §4.11 |

---

## 2. Cross-reference: setting up a new ServiceNow module (generic) vs SAM

A generic module rollout is usually sequenced *prerequisite → data model → configure → ingest → validate → pilot → scale → operate*. SAM needs two extra stages that the repo's CMDB-shaped plan did not foreground: **commercial-data loading** and **position validation** (not just "CI inserted correctly").

| # | Generic module stage | What SAM adds | Repo coverage before round 2 | Gap closed here |
|---|---|---|---|---|
| 1 | Entitlement/subscription + plugin prerequisites | Pro vs Foundation vs SaaS tiers; publisher packs; Workspace installer | §1, §13 | Dependency map §4.12 |
| 2 | Roles and access | Six SAM roles + adjacent asset/procurement/contract roles | names only | §4.2 |
| 3 | Data model / ownership | Five record types + who owns each | data model §2 | RACI §4.3 |
| 4 | Source systems and contracts | Discovery/SCCM/SGC/FBD/ILMT/SaaS + required fields, frequency, error handling | §4, §13 | §4.4 |
| 5 | Commercial data import | Entitlements, PPN, contracts, POs, maintenance/SA links | §2.5, §10 | Procurement/EA §4.14 |
| 6 | Content / normalisation | Content Library, PPN, pattern rules, exceptions | §5, §6, §10, §11 | Vendor matrix §4.11 |
| 7 | Configuration | Properties, dedup, exclusions, published products | §14 | Acceptance gates §4.6 |
| 8 | Validation | Numeric expected-result tests, not "looks right" | none | §4.5 |
| 9 | Pilot | Published-product scope freeze | §1, §14.1 | Checklist |
| 10 | Scale / operate | Job SLAs, change control, audit | none | §4.7–§4.9 |
| 11 | **Commercial position validation** (SAM-only) | Owned vs installed/consumed reconciles; Unknown ≠ compliant | §7 | §4.5/§4.6 |
| 12 | **Rollback / exception** | Misclassified model, wrong metric, duplicate feed | none | §4.7 |

---

## 3. What the repo (all agents) genuinely overlooked

Ranked by impact. Each is now closed in §4 and in `SAM_IMPLEMENTATION_CHECKLIST.md`.

1. **Role/duty separation.** The fleet listed role names, never what each role may change. A `sam_user` who can manual-normalise can change compliance; a `model_manager` cannot administer metrics. Needed before go-live.
2. **RACI for data.** No owner for entitlements, contracts, models, normalisation exceptions, dedup, reconciliation review, or reclamation. 80% of SAM failures are ownership failures (community corroboration).
3. **Source-system contracts.** No required-field/frequency/error contract per feed. Silent partial feeds are the main cause of a position that moves without a business event.
4. **Numeric test cases.** No expected-result examples, so "reconciliation works" was unfalsifiable.
5. **Data-quality gates.** No minimum normalisation/entitlement/CI-coverage thresholds before production.
6. **Rollback/exception.** No procedure for a misclassified model, a wrong-metric import, a duplicate source, or normalisation revert limits (Manually/pattern cannot revert).
7. **Change control.** Software model, metric group, discovery map, dedup rule, normalisation rule, published list and recon grouping all move compliance; none were under change control in the docs.
8. **Audit evidence chain.** No explicit PO → contract → entitlement → allocation → install → result trace.
9. **SaaS lifecycle.** Subscriptions, unrecognised identifiers, SSO vs direct integration, overlap, renewal, and the custom-integration caveat were named but not sequenced.
10. **Per-publisher metric matrix.** Metrics were listed, but not mapped publisher → metric group → traps.
11. **Cloud/virtual/container scope.** BYOL, dedicated hosts, dual-use, edition flexibility, Oracle options, PVU/ILMT regions, vMotion/DRS cluster peak, containerised workloads — only fragments existed.
12. **Prerequisite map.** Plugin/subscription/pack/connector/optional-app dependency graph was implicit.
13. **Procurement/enterprise agreements.** Purchase receipts, procurement integration, Microsoft MLS, and the "enterprise agreements stay Compliant" behaviour were not joined up.
14. **Cross-grade rights.** Named in neither the fleet docs nor the curriculum; upgrade/step-up covered, cross-grade not.
15. **Upgrade/migration and domain separation.** Revert-customizations, Yokohama script-include move, domain-specific properties were scattered.

---

## 4. New content (the missing pieces)

### 4.1 End-to-end entitlement-to-consumption chain

```
CONTRACT  ast_contract ── PO / procurement ── invoice
   │ vendor (core_company), terms, start/end, renewals
   ▼
ENTITLEMENT  alm_license
   │ PPN → samp_sw_product_definition; type; metric; rights; dates;
   │ license cost / +maintenance; state Build→Published→In use
   ├── allocation ─ alm_entitlement_user  (named user)
   └── allocation ─ alm_entitlement_asset (device / CAL)
   ▼
SOFTWARE MODEL  cmdb_software_product_model
   │ publisher → samp_sw_publisher → core_company
   │ product, version(+condition), edition(+condition), platform, language
   │ install condition, discovery map, metric group, suite parent/child,
   │ downgrade/cross-grade rights, license under management
   ▼
DISCOVERY MODEL  cmdb_sam_sw_discovery_model
   │ normalized publisher/product/version/edition + status
   │ software_model (matched), automatically_matched
   ▼
INSTALL  cmdb_sam_sw_install
   │ installed_on → cmdb_ci_hardware; user context; active (dedup)
   ▼
USAGE  samp_sw_usage  (product level; last-used / total time / peak)
   ▼
CONSUMPTION CALC  samp_license_metric_result
   │ rights owned / used / available; allocated-in-use / not-allocated-in-use /
   │ allocated-not-in-use / not-allocated / allocations-needed;
   │ unlicensed installs; true-up; potential savings; over-licensed
   ▼
POSITION  samp_product_result → Software Model Result → License Position
```

**Trust condition:** every arrow must be populated. An empty `installed_on`, an un-normalised discovery model, a model without `License under management`, or an entitlement in `Build` breaks the chain and the position is not defensible.

### 4.2 Roles and duties

| Role | May do | Must not do | Notes |
|---|---|---|---|
| `sam_admin` | Import entitlements, run reconciliation, manage reclamation rules, custom products, pattern rules, Content Service, publish products, change properties | Platform script changes (that is `sam_developer`) | Contains `sam_user`, `sam_spend_import`, `asset`, `model_manager`, `contract_manager` **V** |
| `sam_user` | View, manual-normalise, review results, create removal candidates | Admin functions (imports, properties, content setup) | Contains `pa_viewer`, `cmdb_read`, `report_user`, `sn_remote_dir_sync.reader` **V** |
| `sam_developer` | Write scripts comparable to `sys_admin` | Unsupervised production script changes | Must be a trained admin **V** |
| `sam_integrator` | Create/manage SaaS integration profiles | Entitlement/financial administration | Contains `sam_user`, `connection_admin`, `flow_operator` **V** |
| `sam_spend_import` | Import spend transactions | View SAM without another role | Contains `pa_viewer` **V** |
| `model_manager` | Product models / software catalog work | Administer all model aspects | Cannot administer every model field **V** |
| `catalog_admin` | Publish models to hardware/software catalog | SAM licensing changes | Product Catalog **V** |
| `procurement_user` | Source requests, create POs | Change entitlements directly | Procurement/Asset Workspace **V** |
| `contract_manager` | Contract records/renewals | Licence metric changes | `ast_contract` |
| `asset` | Asset records | SAM reconciliation configuration | Shared HAM |
| `sn_cmdb_admin` / `admin` | CMDB/IRE configuration, form layout | Day-to-day SAM licensing | See `ALT_PARALLELSWARM` |
| `discovery_admin` | Discovery schedules/credentials | SAM normalisation decisions | Discovery |

**Separation rule:** the person who can manual-normalise (`sam_user`) and the person who can change a software model/metric (`sam_admin`) should not be the same person in a controlled environment; normalisation changes compliance.

### 4.3 RACI (minimum viable)

| Data / decision | Accountable | Responsible | Consulted | Informed |
|---|---|---|---|---|
| Entitlements & POs | SAM manager | SAM admin | Procurement, Finance | ITAM lead |
| Contracts / renewals | Contract manager | Procurement | SAM manager, Legal | Finance |
| Software models & metric groups | SAM manager | SAM admin | Publisher owner | Architecture |
| Normalisation exceptions | SAM manager | SAM analyst (`sam_user`) | Publisher owner | Service owner |
| Discovery coverage / CI quality | CMDB owner | Discovery admin | SAM manager | IT ops |
| Dedup rules | SAM manager | SAM admin | Discovery admin | Audit |
| Reconciliation review | SAM manager | SAM analyst | Finance | CIO |
| Reclamation decisions | Service owner | SAM admin | HR/Legal, endpoint team | User |
| Published-product scope | SAM programme lead | SAM admin | Finance | All stakeholders |
| Change control (compliance-affecting) | SAM programme lead | SAM admin | CMDB owner, Audit | CIO |

### 4.4 Source-system contracts

| Source | Required fields | Frequency | Error handling | Notes |
|---|---|---|---|---|
| ServiceNow Discovery | publisher, product/display name, version, edition (optional), `installed_on`, user context if available, last seen | schedule-driven (daily/weekly) | Discovery log + `samp_job_log`; missing CI → no install target | `software_sccm_managed` must be consistent |
| SCCM / SGC | same + device/user identity, last scan, uninstall signal | daily | SGC import errors; dedup | Legacy plugins deprecated Tokyo |
| Jamf / Intune / Tanium (SGC) | device identity, software inventory, last check-in | daily | Connector errors → CMDB gaps | Not native SAM sources |
| FBD | file name/size/version/publisher, CI, path | monthly (default) | unrecognised → `cmdb_unidentified_file_set` | Needs signature normalisation |
| ILMT / BigFix | IBM product, PVU/RVU, host, region | daily/weekly | integration errors; region missing blocks PVU | `sn_samp_ibm_lic.default_region` |
| SaaS direct profile | subscription identifier, user, status, renewal | daily/weekly | `samp_sw_unrecognized_subscription_identifier` | Auto-creates reclamation rule |
| SSO | app, assigned users, last login | daily | disconnected apps | Do not double-source with direct profile |
| Spend Detection | vendor, description, GL account, amount | per import | `samp_entitlement_import` / spend errors | Financial data |
| Procurement | PO, line, PPN, quantity, price, dates | per PO | procurement import errors | Receipts can create entitlements |
| Contract repository | vendor, product, rights, start/end, maintenance | per contract | manual reconciliation | `ast_contract` |

**Contract clause to demand from every feed:** *"Send an explicit uninstall/absence signal or a last-seen timestamp; never send only a full snapshot without a deletion indicator."* SAM does not auto-delete installs; a silent feed leaves phantom rights used.

### 4.5 Test cases (numeric, expected results)

| # | Setup | Expected |
|---|---|---|
| T1 Per-device shortfall | 1 entitlement, metric Per Device, rights **10**; **12** active installs on 12 distinct CIs | Rights owned 10, used 12, available −2 (or 0 + unlicensed 2), **Unlicensed installs 2**, status **Not Compliant**, true-up = 2 × price |
| T2 Named-user allocations | 1 entitlement, Per Named User, rights **5**; **3** allocations in use; **5** installs unallocated | Allocated in use 3, Not allocated in use 5, Allocations needed **2**; remediation Create Allocations + Remove Unallocated Installs |
| T3 Suite roll-up | Suite parent rights **100**; components installed 60 + 40 | With `auto_suite_inference` or suite entitlement mapping: used **100**, Compliant. Without: components can count **200** → apparent shortfall 100 |
| T4 Maintenance alone | Entitlement type **Maintenance**, rights 100, no base perpetual | **Not reconciled** (ignored). Link to base perpetual → benefits apply |
| T5 Dedup level | Same product on one device at `2019`, `2019.1`, `2019`; level **Major** | 1 primary, 2 duplicates `active=false`; used = 1. Level **Exact** → 2019 and 2019.1 both count |
| T6 Normalisation | Discovered `Microsoft Corp / Office 2019 / 16.0`, no edition | Publisher Normalized or Partially Normalized (not Normalized); after manual edition → Manually Normalized → Normalized on accepted suggestion |
| T7 PPN blank | Import row with no PPN, publisher+product present, auto-create **on** | Model auto-created, import succeeds. Auto-create **off** → error `PPN and SM not found` |
| T8 Excluded CI | 20 installs on a leased device; `Exclude from SAM = true` | After `SAM — Adjust Installs for excluded CIs`: those 20 drop out of compliance |
| T9 Retired CI | CI Status → Retired | Related installations are **deleted**; rights used drops; record the business event |
| T10 Subscription | 1 User Subscription entitlement 50; 60 active unique user subscriptions | Rights used 60, unlicensed subscriptions 10, Not Compliant |

### 4.6 Data-quality acceptance gates (recommended, calibrate per estate)

These are **programme gates**, not ServiceNow SLOs; the product publishes no numeric targets.

| Gate | Threshold before production | Query/evidence |
|---|---|---|
| Installs with `installed_on` | ≥ 98% | `cmdb_sam_sw_install` group by empty `installed_on` |
| Discovery models resolved | ≥ 90% `Normalized` + `Manually Normalized`; 0 `New` older than 48h | `cmdb_sam_sw_discovery_model` by status |
| Licensable models configured | 100% have `License under management` and a Licensable product type | model list |
| Entitlement completeness | ≥ 98% have PPN **or** model link, metric, rights > 0, start/end | `alm_license` |
| Duplicate active installs | ≤ 1 active per device+product+edition | dedup output |
| Reconciliation | completes without failure; historical results retained | `samp_job_log`, Historical Results |
| Unlicensed variance | explained line-by-line or < 5% of rights owned | License Position |
| Job health | 0 failed `SAM*` jobs in 7 days | `samp_job_log` |
| CDS status | `Current count` = `Expected count` | Normalization and content dashboard |
| Reclamation hygiene | every candidate has justification + owner | `samp_sw_reclamation_candidate` |

### 4.7 Rollback and exception procedures

| Exception | Do | Do not | Recovery |
|---|---|---|---|
| Model misclassified (wrong product type / edition) | Correct the field; expect **Manually Normalized**; re-run matching + recon | Delete the model if installs/discovery models reference it | Revert only if status allows; Manually/pattern-normalised cannot revert |
| Wrong metric on entitlement import | Create a corrected entitlement; retire/cancel the wrong one with reason | Edit rights to hide the error | Historical results preserve the before/after |
| Normalisation wrong | Manual normalise or pattern rule; revert only Normalized/Partially/Publisher | Revert Manually Normalized or pattern-normalised | Revert → `Match Not Found`, then normalise again |
| Duplicate source feed | Fix source contract / dedup rule; set loser `active=false` via dedup | Bulk-delete installs without export | Export affected rows first; Table API delete only confirmed uninstalled |
| PPN/model mismatch on bulk import | Correct PPN or create custom PPN; re-import failed rows | Reuse a wrong PPN to "make it load" | `samp_entitlement_import` error rows are the work queue |
| Discovery model missing (`Security Update`) | Accept by design; do not force | Create manually (not supported) | Use content/custom product if it must be tracked |
| Excluded device wrongly excluded | Clear the boolean; wait for the adjust job | Delete installs | Job re-includes them |
| Bad reconciliation run | Re-run after fix; compare Historical Results | Overwrite prior results | Results are history, not a single mutable table |
| Pre-change safety | Export models, entitlements, dedup/pattern rules, published list | Rely on rollback of a script | Change ticket stores the export |

**Hard limits to teach:** normalisation revert excludes Manually Normalized and pattern-normalised rows; uninstalls are not auto-deleted; a CI retired/stolen deletes related installs; auto-created models cannot be created against a specific version.

### 4.8 Change control — what moves compliance

Require a change record + before/after reconciliation snapshot for:

1. software model create/edit (publisher, product, version/edition condition, install condition);
2. metric group / license metric / metric attributes;
3. discovery map / suite membership / downgrade-cross-grade rights;
4. pattern normalisation rule, wide-net/ML toggles, content version activation;
5. dedup rule / version level / stale threshold;
6. exclude-device flag and property;
7. published-product list and `manage.published.products`;
8. reconciliation grouping (`recon.group`/`.subgroup`) and custom-metric toggle;
9. Discovery software properties (`discover_software`, `software_simplify`, `software_sccm_managed`);
10. entitlement import batch or procurement integration change.

### 4.9 Audit evidence chain

```
PO / invoice ──► ast_contract (vendor, term) ──► alm_license (rights, PPN, metric, dates)
      ──► alm_entitlement_user|asset (allocations)
      ──► cmdb_sam_sw_install (installed_on, active, discovery_source)
      ──► samp_license_metric_result (rights algebra) ──► License Position
```

Evidence to retain: import file + `samp_bulk_import`/`samp_entitlement_import` result, `samp_job_log`, reconciliation Historical Results snapshot, before/after exports for every change ticket, and the dedup/pattern rule versions in force. This is what an auditor asks for when a position is challenged.

### 4.10 SaaS subscription lifecycle

1. Install `sn_sam_saas_int` (requires `com.snc.samp`); role `sam_integrator`.
2. Create a **direct integration profile** per SaaS publisher; on creation a **reclamation rule is auto-created** — review it **V**.
3. Ingest **subscriptions** (not classic installs); map subscription identifiers to users.
4. Unmatched identifiers land in `samp_sw_unrecognized_subscription_identifier`; resolve with user-resolution rules (Otto can generate them) **V**.
5. SSO apps appear in `samp_sso_application`; do **not** attach SSO **and** a direct profile to the same app **C**.
6. Consumption metric group (SaaS Consumption / User Subscription) drives rights.
7. **Overlapping usage** view shows feature-level overlap; use it before renewal.
8. Renewals calendar joins subscription end dates; reclamation candidate → forfeit/unassign seat.
9. **Custom integration caveat:** where no OOB connector exists, subscription/usage data must be integrated (API/import); SAM will not invent seats from CMDB installs.

### 4.11 Vendor metric matrix (selection traps)

| Publisher | Metric group / metrics | Traps |
|---|---|---|
| **Adobe** | Per Device, Per User, User Subscription | Subscription-driven; needs SaaS/Adobe pack |
| **Citrix** | Concurrent User, Per Device, Per Processor, Per User, Per User/Device | Requires discovery of the Delivery Controller/licence server; `com.snc.samp.citrix.app.license.period` 90 |
| **IBM** | Authorized User, AU Value Unit, Employee/External UVU, PVU, RVU, VPC, Per Processor, Per Device/User, plus Australia-P6 metrics | PVU/RVU need ILMT/BigFix + region; full vs sub-capacity; VPC via separate store app |
| **Microsoft** | Per Core, Per Core (with CAL), Per Processor, Per Device, Per User, Server (Per Instance), Server (Per Server), Device/User CAL, User Subscription | SA/maintenance must be linked to perpetual; Per Core physical/virtual OSE deprecated; cluster peak capacity with vMotion/DRS; Azure dual-use / edition flexibility / host type fields; pre-Oct-2019 legacy flag |
| **Oracle** | Named User Plus, Per Processor, Employee | `samp_oracle_options` eligibility; `reconlevel` ESX / ESX cluster (default) / vCenter(s); host affinity; Hyper-Threading on AWS; Employee true-up is 1 year |
| **Red Hat** | Per Socket-pair, Per Core | IBM pack; RHEL VDC vs Server threshold 3.2 |
| **SAP** | Named User, Engine Measurement, Digital Access, User Subscription, FUE | SAP named-user type normalization; SAP connections; System Users related list |
| **VMware** | Per Application Instance, Per Device, Per Named User, Per OSI, Per Processor, Per Core | Per Processor = 1 right per 32 cores (metric attribute default 32); Per Core minimum 16 cores/processor |
| **Subscription (generic)** | User Subscription, SaaS Consumption | Subscription records, not installs; unrecognised identifiers |

**Selection rule:** the metric must match the contract's counting basis (device vs user vs core vs processor vs consumption); a metric mismatch is a methodology error, not a data error, and cannot be fixed by normalisation.

### 4.12 Prerequisite / dependency map

```
SAM subscription ─► com.sn_samp_master_ws (Pro + Workspace)
                      ├─ com.sn_samp_master (core)
                      └─ sn_sam_workspace (store)
Required: healthy CMDB (cmdb_ci_hardware) + Discovery OR SCCM/SGC
Optional: publisher packs (Adobe/Citrix/IBM/Microsoft/Oracle/SAP/VMware/Eng)
Optional: sn_sam_saas_int (SaaS) · com.sn_sam_spend (spend)
Optional: com.snc.procurement + app-itam-procurement-integration
Optional: com.snc.orchestration.client_sf_distribution (uninstall)
Optional: com.glide.domain.msp_extensions.installer (domain props)
Optional: com.snc.pa.domain_support (domain PA)
Optional: Health Check store app · sn_now_assist_sam (Otto)
Optional: com.snc.discovery.file_based_discovery + com.snc.file_signature_normalization
Content: Content Service (opt-in) + CDS
```

### 4.13 Cloud / virtual / container scope

- **Virtualisation:** host vs VM allocation; cluster allocation is discouraged (shows as **Allocated not in use**); Microsoft cluster peak capacity with vMotion/DRS; Oracle aggregation level + host affinity; SQL Server Standard host-level licensing is not supported by Microsoft rules **V**.
- **Cloud:** Cloud Special Rights tab for AWS/Azure installs; dual-use, host type (shared/dedicated), edition flexibility; legacy licence flag pre-1 Oct 2019; `com.snc.samp.sam_ci_billing_threshold` 30 days; Oracle Hyper-Threading on AWS **V**.
- **Containers/Kubernetes:** the SAM install/model chain assumes a CI with installs. Containerised workloads are not a first-class install target; licensing must be handled publisher-by-publisher (cores/vCPU/consumption) and is **not** solved by CMDB install discovery. Flag as an explicit programme gap — do not claim SAM covers it.
- **VDI/non-persistent:** high install churn; rely on dedup stale threshold + usage, and confirm whether the publisher licenses by device, user, or concurrent session.

### 4.14 Procurement, contracts, enterprise agreements

- `com.snc.procurement` + `app-itam-procurement-integration`: purchase orders; purchase receipts can create entitlements; import errors surface in the Activity center **V**.
- Microsoft MLS: step-up licence type is Microsoft-only; `Contractual` duration requires start/end **V**.
- Enterprise/ULA/ELA/ETLA/SCE agreements remain **Compliant** even with unlicensed installs **C** — do not report them as true-up candidates; track them as contractual coverage.
- **Cross-grade** (e.g. edition trade within a family) is not a first-class licence type in the docs; model it with upgrade/step-up entitlements plus a documented commercial note, and validate with the publisher.

### 4.15 Upgrade / migration / domain separation

- Brazil: classic UI limited support; activating Workspace hides moved classic menus, but admin menus remain classic-only (Custom Products, Pattern Normalization Rules, Reclamation Rules, Content Service Setup, Properties, SaaS profiles, SAP connections) **V**.
- From Yokohama, reconciliation script includes move to `com.sn_itam_samp`; migrate customisations **V**.
- Revert Customizations module exists; run after first install/upgrade for features to work **V**.
- Domain separation: `com.glide.domain.msp_extensions.installer` enables domain-specific published-products and Oracle properties; PA domain support `com.snc.pa.domain_support`; AI domain separation supported **V**.
- Migration Basic SAM → Pro is **irreversible**; migrate `cmdb_ci_spkg` → `cmdb_sam_sw_install` **C**.

---

## 5. Where this repo already exceeds the critique

- **Six** normalisation statuses, not four; full transition and revert matrix (`SAM_MODULE_REFERENCE.md` §5).
- Content Service data-type and exclusion detail, including NSC IL5 receive-only (§5.6).
- Exact three-tier reconciliation model and every rights bucket → remediation (§7.2).
- Dedup Exact/Major/Any with primary-selection tiebreak and IBM preference (§4.6).
- Model vs publisher vs vendor vs PPN vs catalog item disambiguation (§2.4) — the critique's "software models" point without the vendor confusion.
- Insert/update matrix incl. IRE data-source gate and partial payloads (§4.5).
- All 60+ Brazil property names with defaults and blast radius (§14).
- Reporting widgets mapped to source tables (§12.2) — the critique says "reporting" but not which table feeds which widget.

## 6. What remains unverifiable without an instance

Business-rule/UI-policy/ACL names and sys_ids; internal column names for label-only fields; the exact Software Model Results table; custom-product/pattern-rule/reclamation-rule table names; vendor catalog item table; default reconciliation cadence on *this* instance. Queries are in `SAM_MODULE_REFERENCE.md` Appendix A.

## 7. Revised artefacts

- `05_FINAL/MODULE_IMPLEMENTATION_PLAN.md` — the 15-section programme plan the second review asked for, instantiated for SAM.
- `05_FINAL/SAM_IMPLEMENTATION_CHECKLIST.md` — the go/no-go gates extracted from it.

---

## 8. Second review — cross-module implementation controls

The second Perplexity pass is correct that technical configuration is not an implementation plan. Audit against the repo:

| Dimension it requires | Before this repo pass | Verdict | Where now |
|---|---|---|---|
| Business case, KPIs, baseline, sponsor | absent | **Missing** | MIP §1 |
| Explicit definitions of compliant/under/over/reclaimable | partial (§7) | **Partial** | MIP §1.2, Checklist Phase 1 |
| Scope matrix (process/data/region/BU/integration/exclusion) | thin | **Partial** | MIP §2 |
| Ownership, RACI, escalation | names only | **Missing** | MIP §3, Round 2 §4.3 |
| Operating model, runbook, SLAs, on-call | absent | **Missing** | MIP §14 |
| Data governance: source-of-truth, standards, thresholds, retention | data model only | **Partial** | MIP §6, Round 2 §4.6 |
| Integration architecture: retries, idempotency, count reconciliation | feeds listed | **Partial** | MIP §7, Round 2 §4.4 |
| Security: ACLs, delegation, PII, credential vaulting | roles only | **Partial** | MIP §8 |
| Config vs customization vs vendor content + upgrade strategy | anti-patterns only | **Partial** | MIP §9 |
| Environments, source control, release, rollback | absent | **Missing** | MIP §10 |
| Test strategy (unit/integration/workflow/recon/security/perf/UAT/regression) | absent | **Missing** | MIP §11, Round 2 §4.5 |
| Cutover/migration runbook + definition of complete | absent | **Missing** | MIP §12 |
| Adoption, training, comms, champions | absent | **Missing** | MIP §13 |
| Hypercare, support model, continuous improvement | absent | **Missing** | MIP §14 |
| Risks/issues/decisions/dependencies | risk table in plan only | **Partial** | MIP §15 |
| End-to-end process design upstream/downstream | pipeline only | **Partial** | MIP §5 |
| Source-system inventory with owners | partial | **Partial** | Round 2 §4.4 |
| Data dictionary / reference standards | tables only | **Partial** | MIP §6.2 |
| Config vs custom upgrade strategy | anti-patterns | **Partial** | MIP §9 |
| SAM production-readiness gates | absent | **Missing** | Checklist |

### 8.1 The distinction this review adds

The first review said *"CMDB establishes what exists; SAM establishes what was purchased, how it may be used, what is installed/consumed, and whether they reconcile."* The second adds the programme layer: *who owns each of those, how it is governed, tested, released, secured, adopted, and improved*. Both are now written.

### 8.2 Three things still not solved by documentation

1. **Containers/Kubernetes** — SAM's install/model chain is CI-centric; containerised workloads need publisher-specific licensing outside `cmdb_sam_sw_install`. This is an explicit scope exclusion, not a doc gap.
2. **Enterprise agreements** — product behaviour is "stays Compliant even with unlicensed installs" **C**; the programme must model contractual coverage, not rely on the position to be literally true.
3. **Commercial sensitivity** — entitlements/contracts expose pricing and user/device associations; ACL design and privacy review are organisation-specific and cannot be defaulted.

### 8.3 Verdict on the two reviews

- Technical gaps: **mostly already covered**; the genuine additions are the vendor metric matrix, SaaS lifecycle, role duties, and the ops layer.
- Programme gaps: **real and now documented** in `MODULE_IMPLEMENTATION_PLAN.md` + `SAM_IMPLEMENTATION_CHECKLIST.md`.
- Nothing in either review contradicts a ServiceNow-documented fact in `SAM_MODULE_REFERENCE.md`; where the reviews use practice figures (60–90-day reclaim window, 85–95% normalisation hit rate) they remain **P**, not product defaults.
