TESTbased on what agents did here, with extensive documentaiton on CMDB module and discovery/ rules all the possible configuration options for CI insertion/update, rules etc. in https://github.com/eltonaguiar/alt_parallelswarm  , apply the same in https://github.com/eltonaguiar/alt_parallelswarm_SAM for SAM Module , following similar phases and folder structure e.g. plan first. etc.

--------------

## FINAL — SAM module compilation · `deepseek-flash__deepseek__kilo`

- **Agent:** `deepseek-flash__deepseek__kilo`
- **Model:** `deepseek/deepseek-flash`
- **Provider:** DeepSeek · **Harness:** Kilo CLI
- **Timestamp:** `2026-11-13T15:35:00Z`
- **Release pin:** ServiceNow **Brazil** (ITAM map `PMOYmdGTPDs40EbYh10h4g`); Australia corroboration marked **C**
- **Folder:** [`agents/deepseek-flash__deepseek__kilo/`](agents/deepseek-flash__deepseek__kilo/)
- **Merged final:** [`final/FINAL_deepseek-flash__deepseek__kilo.md`](final/FINAL_deepseek-flash__deepseek__kilo.md)

### What this pass adds

A phased SAM reference at parity with the CMDB/Discovery reference, **plus** the two rounds of external review that the fleet's earlier SAM docs did not cover.

| File | What it is |
|---|---|
| [`01_PLAN/PLAN.md`](agents/deepseek-flash__deepseek__kilo/01_PLAN/PLAN.md) | Phased plan: prereq → corpus → contract → normalisation → reconciliation → OOB scripts → reporting/integrations → parameters → QA → round 2 → publish |
| [`05_FINAL/SAM_MODULE_REFERENCE.md`](agents/deepseek-flash__deepseek__kilo/05_FINAL/SAM_MODULE_REFERENCE.md) | Deep reference: tables/fields, six normalisation statuses, insert/update, OOB jobs/BRs/flows, add-model and normalise-model runbooks, reporting map, integrations, full property inventory |
| [`05_FINAL/ROUND2_GAP_ANALYSIS.md`](agents/deepseek-flash__deepseek__kilo/05_FINAL/ROUND2_GAP_ANALYSIS.md) | Claim-by-claim verification of the Perplexity review, fleet-wide gap list, roles/RACI, feed contracts, numeric test cases T1–T10, acceptance gates, rollback/change control/audit, SaaS, vendor metric matrix |
| [`05_FINAL/MODULE_IMPLEMENTATION_PLAN.md`](agents/deepseek-flash__deepseek__kilo/05_FINAL/MODULE_IMPLEMENTATION_PLAN.md) | 15-dimension programme plan: business case/KPIs, scope, ownership, data governance, integration architecture, security, config-vs-custom, release, testing, cutover, adoption, hypercare |
| [`05_FINAL/SAM_IMPLEMENTATION_CHECKLIST.md`](agents/deepseek-flash__deepseek__kilo/05_FINAL/SAM_IMPLEMENTATION_CHECKLIST.md) | Go/no-go gates across 10 phases with evidence and gate owners |
| [`05_FINAL/FINAL_SUMMARY.md`](agents/deepseek-flash__deepseek__kilo/05_FINAL/FINAL_SUMMARY.md) | Goal met? blockers? what remains instance-only |

### Merged fleet work (all SAM sources)

`grok-4.6__xai__kilo` WT1 (Brazil config reference, 42 sources) · WT2 (curriculum compare) · WT3 (CIS-SAM quiz map) · `beam__kilo__cli` WT1 (table contract, Discovery→SAM rule, migration) · this pass (deep reference + round 2 + programme layer). Conflicts are recorded, not smoothed over: **weekly** reconciliation (docs) vs "nightly" (curriculum); `samp_sw_usage` vs `cmdb_sam_sw_usage`; `samp_license_metric_result` vs "sam_sw_reconciliation_result"; six normalisation statuses vs five; Pro `com.sn_samp_master_ws` vs Foundation `com.snc.sams`.

### Direct answers to the review questions

- **Reporting:** covered — every named workspace, dashboard, widget and report is mapped to its source table (overview → `samp_product_result`, `alm_license`, `samp_license_metric_result`, `samp_sw_reclamation_candidate`, `cmdb_sam_sw_discovery_model`, `sam_sw_product_lifecycle`; License Workbench; Normalization and content; Success portal; Health Check; License Position; Renewals; Overlapping usage; CMDB success advisor for SAM).
- **Every combination?** Ten matrices: normalisation status × manual/revert; rule family × scope; dedup Exact/Major/Any × tiebreak; insert/update across install/discovery model/software model/entitlement/allocation/catalog; rights buckets × remediation; licence types; product types; PPN scenarios; scope controls; recon grouping.
- **Software Model Normalization:** full runbook — auto (Product/Package Map, Pattern, Enhanced Pattern, Wide-net, ML) → manual → suggestion → revert limits → model matching job → reconciliation → product-type reclassification.
- **Software Model vs Vendor:** disambiguated — `core_company` (vendor) → `samp_sw_publisher` → `samp_sw_product_definition` (PPN) → `cmdb_software_product_model` (model) → `cmdb_sam_sw_discovery_model` (discovered) → `sc_cat_item` (catalog) → `alm_license` (rights).
- **"4 normalisation statuses":** the field carries **six** values on `cmdb_sam_sw_discovery_model`: `New`, `Match Not Found`, `Publisher Normalized`, `Partially Normalized`, `Normalized`, `Manually Normalized`. The docs publish the label "Normalization status" but not the internal column — marked `U` with the `sys_dictionary` query to settle it.
- **Typical integrations:** Discovery, FBD + file signature, SCCM→Service Graph connector, Intune/Jamf/Tanium (SGC), ILMT/BigFix, SaaS LM, SSO, Spend Detection, Procurement, CSD, OpenLM/Open iT, SAP, Citrix, third-party IRE REST, HAM contracts, Content Service, Otto.

### What was genuinely missing before this pass

Role/duty separation · RACI · source-system feed contracts · numeric test cases · data-quality acceptance gates · rollback/exception procedures · change control for compliance-affecting config · audit evidence chain · SaaS lifecycle · per-publisher metric matrix · cloud/virtual/container scope · prerequisite dependency map · procurement/EA handling · cross-grade rights · upgrade/migration/domain separation. All are now written in the round-2 and programme-plan files.

### Honest boundary

No live instance was available, so business-rule/UI-policy/ACL names, sys_ids, and label-only column names remain `U` and are listed with verification queries. Container/Kubernetes licensing is an explicit scope exclusion, not a solved capability. This is a documentary reference plus an operable plan — not a tested deployment.

### Round 3 — bidirectional delta with the live SAM guide

- [`GUIDE_VS_REPO_DELTA.md`](agents/deepseek-flash__deepseek__kilo/05_FINAL/GUIDE_VS_REPO_DELTA.md) — what the guide has that the repo lacks, what the repo has that the guide lacks, and 18 corrections the guide needs (wrong usage table, non-existent result table, nightly cadence, plugin names, custom `u_*` fields).
- [`LEARNING_LAYER.md`](agents/deepseek-flash__deepseek__kilo/05_FINAL/LEARNING_LAYER.md) — the guide's teaching assets (exam map, ELI5, five-record mnemonic, compliance positions, publisher traps, lab, quiz, SLA targets, SaaS waste pattern) preserved and corrected in this repo.
- [`LEARNING_PROTOCOL_ADDITIONS.md`](agents/deepseek-flash__deepseek__kilo/05_FINAL/LEARNING_PROTOCOL_ADDITIONS.md) — ten reusable artefacts for `ServiceNow_Learning`, mapped to its ORIENT → MODEL → PRACTISE → PROVE → TEACH loop.

The guide is the better teacher; this repo is the better reference. Neither should absorb the other wholesale — the guide keeps its voice and links here for depth.

---

# SAM Cheat sheet

> Core concepts, one screen. Links point to the deep docs or source notes where available. Marks follow **V/C/U/P**; where a cheat-sheet table has no per-row mark, the deep doc is authoritative.

## 1. One sentence

**SAM reconciles what you own (entitlements) against what exists and is used (normalized installs + usage) per software model and license metric, and turns the difference into a compliance position.** **V**

## 2. The chain (memorize this order)

```text
CI (CMDB/IRE)
  └─ cmdb_sam_sw_install            # one install on one device
       └─ cmdb_sam_sw_discovery_model  # raw fingerprint, normalized
            └─ cmdb_software_product_model  # purchased product profile
                 └─ alm_license             # rights + metric + dates
                      └─ reconciliation     # rights vs demand
                           ├─ samp_product_result
                           ├─ Software Model Results
                           └─ samp_license_metric_result
```

**Install → discovery model → software model → entitlement → result.** **V**

**Usage note:** `samp_sw_usage` is **product-level** and references publisher/product + CI + user; it feeds reconciliation and does **not** reference the install row. **V**

## 3. The four gates

| Gate | Pass condition |
|---|---|
| Schema + edition | Correct plugin; SAM tables present |
| CMDB + CI identity | One CI per device; IRE rules reviewed |
| Discovery feed | One trusted source populating installs |
| Normalization + entitlements | Models normalize; every entitlement has model + metric |

## 4. IRE rule families (CMDB only)

| Rule family | Insert? | Update? | One-line |
|---|---|---|---|
| **Identification** | Yes | Yes | Same CI or new CI? |
| **Reconciliation** (static/dynamic) | No | Yes | Which source may write this field? |
| **Data refresh** | No | Yes | Is the value stale enough to hand off? |
| **IRE data source** | Yes (blocks) | No | May this source create this class? |

**Order:** identify first. Match → reconcile + data refresh. No match → data source rule gates the insert. **V**

## 5. Normalization statuses (six)

| Status | Manual normalize? | Revert? |
|---|---|---|
| New | No | No |
| Match Not Found | Yes | No |
| Publisher Normalized | Yes | Yes |
| Partially Normalized | Yes | Yes |
| Normalized | No | Yes |
| Manually Normalized | No | No |

All reverts go to **Match Not Found**. Pattern-normalized models cannot be reverted. **V**

## 6. Reconciliation results (three tiers)

| Tier | Table | Answers |
|---|---|---|
| Product | `samp_product_result` | Is the product compliant? What is the cost/savings? |
| Software model | Software Model Results | Which model is the problem? |
| License metric | `samp_license_metric_result` | Rights owned vs used vs available, by metric |

**Run record:** `samp_reconciliation_result` **V**. There is no documented single `sam_sw_reconciliation_result` analysis table **C**.

## 7. Rights algebra

**Rights owned** = active entitlements sharing the metric.
**Rights used** = allocated in use + not allocated in use + installed.
**Rights available** = owned − used.
**Allocated not in use** = wasted rights → remove allocations.
**Not allocated in use** = unallocated consumption → create allocations or remove unallocated installs.

**V**

## 8. Insert vs update (the short version)

| Layer | Insert gate | Update gate |
|---|---|---|
| CI | IRE identification + data source rule | IRE reconciliation + data refresh |
| Install | Discovery writes | Same discovery-model reference |
| Discovery model | Business rule creates | Normalization / manual normalize |
| Software model | Auto-create property or admin | Model matching / admin |
| Entitlement | Create/import | New true-up record, never overwrite history |
| Result | New run | Re-run; do not edit |

## 9. Key tables

| Table | What it is |
|---|---|
| `cmdb_sam_sw_install` | Installs (source of truth for current software) |
| `cmdb_sam_sw_discovery_model` | Raw fingerprints + normalized fields + status |
| `cmdb_software_product_model` | Purchased product profile |
| `alm_license` | Entitlement |
| `samp_sw_usage` | Usage evidence |
| `samp_product_result` | Product compliance/cost |
| `samp_license_metric_result` | Rights per metric |
| `samp_reconciliation_result` | Reconciliation run |
| `samp_sw_reclamation_candidate` | Reclamation candidates |
| `sam_sw_dedup_rule` | Custom dedup rules |

## 10. Key properties

| Property | What it does |
|---|---|
| `com.snc.samp.recon.group` / `.subgroup` | Weekly reconciliation grouping |
| `com.snc.samp.automaticsmrcreation` | Auto-create models for licensable products |
| `com.snc.samp.exclude_device_flag` | Exclude CIs from SAM |
| `com.snc.samp.manage.published.products` | Phase-wise scope |
| `com.snc.samp.oracle.reconlevel` | Oracle VMware aggregation |
| `com.snc.samp.enable.ml_normalization` | ML normalization |
| `com.snc.samp.wide_net_normalization.enabled` | Wide-net normalization |
| `sn_sam_workspace.sam_license_operations_list_count` | Workspace list count threshold |

## 11. Key jobs

| Job | Cadence |
|---|---|
| `SAM - Normalize discovery models using content library rules` | Daily |
| `SAM - Discovery Model Normalization job` | Daily |
| `SAM - Daily Job` | Daily |
| `SAM - Trigger Full Scan` | Weekly |
| `SAM — Adjust Installs for excluded CIs` | Not documented |
| `SAM - Software License Reconciliation` | Weekly default (schedule configurable) |
| `SAM – Discovery Model to Software Model matching` | Not documented |

## 12. Top traps

1. **Metric mismatch** between model and entitlement → silently meaningless result.
2. **Duplicate installs** from multiple sources → inflated demand; configure dedup.
3. **Unnormalized titles** → unlicensed/unknown; normalize before auto-create.
4. **Maintenance treated as a license** → false compliance.
5. **Leftover installs on out-of-scope devices** → phantom demand; Retired/Stolen CI status deletes installs, but leased/ignored devices need the exclude-CI job.
6. **First reconciliation treated as an invoice** → wrong true-up; use it as a data-quality loop.
7. **Dead SaaS connector** → "no waste" illusion; monitor health.
8. **Confusing vendor / publisher / PPN / model / discovery model / catalog item** → wrong links.

## 13. Where to go next

| Need | Go to |
|---|---|
| Full architecture | [`05_FINAL/01_SAM_MODULE_GUIDE.md`](finalv2/05_FINAL/01_SAM_MODULE_GUIDE.md) |
| IRE rules | [`05_FINAL/02_CMDB_IRE_GOVERNANCE.md`](finalv2/05_FINAL/02_CMDB_IRE_GOVERNANCE.md) |
| Pipeline + dedup | [`05_FINAL/03_DISCOVERY_TO_SAM_PIPELINE.md`](finalv2/05_FINAL/03_DISCOVERY_TO_SAM_PIPELINE.md) |
| Normalization | [`05_FINAL/04_NORMALIZATION_AND_DEDUP.md`](finalv2/05_FINAL/04_NORMALIZATION_AND_DEDUP.md) |
| Reconciliation | [`05_FINAL/05_ENTITLEMENTS_METRICS_RECONCILIATION.md`](finalv2/05_FINAL/05_ENTITLEMENTS_METRICS_RECONCILIATION.md) |
| Config inventory | [`05_FINAL/06_CONFIGURATION_REFERENCE.md`](finalv2/05_FINAL/06_CONFIGURATION_REFERENCE.md) |
| Runbook | [`05_FINAL/07_OPERATIONS_RUNBOOK.md`](finalv2/05_FINAL/07_OPERATIONS_RUNBOOK.md) |
| Sources | [`05_FINAL/08_SOURCE_NOTES.md`](finalv2/05_FINAL/08_SOURCE_NOTES.md) |
| Guide delta | [`GUIDE_CROSS_REFERENCE.md`](finalv2/GUIDE_CROSS_REFERENCE.md) |

**External links:**

- Official docs: <https://www.servicenow.com/docs/>
- Public SAM guide: <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/sam/sam-guide/>
- v1 merged reference: [`final/FINAL_SAM_MODULE_REFERENCE.md`](final/FINAL_SAM_MODULE_REFERENCE.md)
- v1 config reference: [`final/FINAL_SAM_CONFIG_REFERENCE.md`](final/FINAL_SAM_CONFIG_REFERENCE.md)

---

*End of SAM Cheat sheet. Full reference: [`finalv2/README.md`](finalv2/README.md).*
