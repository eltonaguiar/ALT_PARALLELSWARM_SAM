# Bidirectional Coverage Gap Analysis — ALT_PARALLELSWARM_SAM vs TSOM SAM Guide

**Date:** 2026-11-13
**Scope:** Compare what is documented in this repository (`FINAL_grok-4.0__xai__kilo.md`, `FINAL_SAM_MODULE_REFERENCE.md`, `FINAL_SAM_CONFIG_REFERENCE.md`, the WT checklists, and `FINAL_CROSS_REFERENCE_COVERAGE_ANALYSIS.md`) against the published TSOM/SAM guide at `https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/sam/sam-guide/` (source: `ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/sam/sam-guide.md`), and cross-reference to the public learning protocol site (`https://eltonaguiar.github.io/ServiceNow_Learning/`).

## Direction A — Documented in this repo, NOT yet on the SAM guide page

Recommended to ADD to `docs/modules/sam/sam-guide.md` (or a "Carry-Over Addendum"):

1. **SAM Pro vs Foundation & role matrix**
   - Plugins `com.snc.sams` / `com.sn_samp_master_ws` / `com.snc.samp` , SaaS LM `sn_sam_saas_int`.
   - Roles: `sam_admin` (contains `sam_user`, `sam_spend_import`, `asset`, `model_manager`, `contract_manager`), `sam_user`, `sam_developer` (script work only if trained), `sam_integrator`, `sam_spend_import`.
   - `sam_license_manager` / `sn_sam.admin` = **not** official (curriculum-wrong).
   - Missing from page: **1 of 1 guides found** shows neither role matrix nor IRE REST payload.

2. **Four Discovery-to-SAM catalog paths (A–D)**
   - Path A: catalog (requestable, `sc_cat_item`), Path B: SAM model before discovery, Path C: discovered software linked to SAM model, Path D: block/exclude/do-not-manage.
   - Page currently collapses configuration of requestable-vs-observed and has no explicit framing of "catalog last, not first."

3. **Phase-wise published products + exclude-CI flag**
   - `com.snc.samp.manage.published.products` and the re-run of reconciliation after publishing a product set.
   - `com.snc.samp.exclude_device_flag` + job `SAM — Adjust Installs for excluded CIs`.
   - Auto-creation gate `com.snc.samp.automaticsmrcreation` (off in Crawl); `com.snc.sam.auto_suite_inference` (false by default; turn on only after suites verified).
   - Suite parent/child publish warning ("do not publish a top-level suite in a pilot").

4. **Foundation vs Pro / 3rd-party IRE data source contract**
   - REST payload keys: `publisher`, `version`, `display_name` (+ optional edition); parent CI identified by `name`; send `sys_class_name` so the CI is not reclassified.
   - Property `com.snc.samp.ire.datasource.integration`.
   - Role required: `sam_developer`.

5. **Normalization coverage numbers used as onboarding gates**
   - ~85%+ normalization hit rate out-of-the-box on SCCM-class sources;
   - ~95%+ after Content Service opt-in.
   - Treat these as Path-to-Value figures, not SLAs; use as gate criterion before enabling `automaticsmrcreation`.

6. **Organizational MVP baseline (carry-over)**
   - "80% process and governance, 20% tool"; 80% of spend concentrated in Microsoft, VMware, Adobe, Oracle, IBM, SAP, Salesforce.
   - Crawl / Walk / Run phases and the difference between Crawl and Act on First Recon.

7. **Operational runbooks added in this repo (Section 7 of the cross-reference)**
   - Entitlement import contract column map (table in `FINAL_CROSS_REFERENCE_COVERAGE_ANALYSIS.md` §7.1).
   - Dead-SaaS-connector monitoring (drift + stale alert designs + dual-auth hazard rule).
   - Hypercare KPI list + thresholds (job filter `Name starts with SAM`).
   - Rollback/deactivation runbook (scenario → procedure).
   - Change-control blast-radius rubric (change × blast radius × CAB flag).
   - Privacy/PII/identity specifics.
   - Guided Setup vs phase-wise decision at Sprint 0 (and the re-scoping cost).
   - "Found rocks": maintenance ≠ license, metric-mismatch flips to Unknown, exclude-CI long tail, subscription-without-usage, billing-cycle alignment.
   - Cutover/cleanup: publishing correction SLA = ≤ 5 business days after validated change; data refresh every ≤ 2 weeks.

8. **Foundation vs Pro edition decision** (irreversible upgrade to Pro) — described in this repo; not foregrounded on guide.

9. **CIS/SAM scope freeze**: ~85%+ normalization hit rate after opt-in, and published-products freeze with re-run of recon for the product set.

10. **Data-source reliability ranking, dedup, stale installs**
   - "Brazil Exact / Major / Any" dedup rule naming; dedup job `Software Install Deduplication` / `SAM – Discovery Model to Software Model matching`.

## Direction B — Covered on the SAM guide page, NOT yet in any final doc of this repo (i.e., gaps in this repo that should be mirrored here)

1. **Lab Steps 1–7**
   - Step 6 ("Prove normalization matters") and Step 7 ("Teach back") now partially reflected; still no runnable sub-prod activation instructions beyond navigate paths.
   - Add exact search filter on `sys_index_search_all` for discovery-model status-counts.

2. **Reusable code blocks** [knowledge base material]
   - Business Rule: "Flag an installation with no normalized software model" (`before` BR).
   - Scheduled Job: "Expire entitlements past their end date" (basic `gr` get-list + setValue).
   - Script Include: per-publisher compliance summary.
   - Client Script: require a metric when creating an entitlement.
   - OOB report definitions (Top unlicensed products, unused installations, contested entitlements, recent removals).
   - Page covers these; **this repo does not**.

3. **Mnemonics / exam-weight mapping**
   - Exam-weight table (~15/25/30/20/10) + traps.
   - Memory aids: Three-Record Types table, IRE before reconciliation flip "Unknown ≠ compliant."

4. **Quiz items**
   - 14 CIS-SAM style questions split by domain; page has dedicated section.

5. **Migration/cutover specifics for `alm_software`/`cmdb_ci_spkg`**
   - Guide mentions deprecation timeline; this repo mentions migration in one line.

6. **Processor-pack matrix with version specifics**
   - Version of Oracle LMS scripts, ILMT versions. Page carries vendor-specific packs names.

## Recommended actions

1. **Add an Addendum to `docs/modules/sam/sam-guide.md`** capturing Section A (new items above) — see `SAM_EXTENSION_ADDENDUM` below. This is a documentation change; safe, additive, and does not alter earlier exams.
2. **Mirror Section B items into this repo** by adding a `docs/`-ish file answering "how to run the lab in sub-prod + reusable snippets", optional — but for parity, add `final/FINAL_SAM_LAB_RUNBOOK.md`.
3. **Add a SAM entry to `ServiceNow_Learning`** (the public learning protocol site) using the HAM-guide template, pointing back to the TSOM SAM guide + the ALT_PARALLELSWARM_SAM repo. Surface `ServiceNow_Learning/docs/modules/sam/sam-learning-map.md` (see creation below).
