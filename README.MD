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
