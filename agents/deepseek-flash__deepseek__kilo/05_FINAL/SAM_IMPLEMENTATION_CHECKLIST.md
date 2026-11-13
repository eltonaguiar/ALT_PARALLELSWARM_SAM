# SAM IMPLEMENTATION CHECKLIST — go/no-go gates

**Agent:** `deepseek-flash__deepseek__kilo` · **Date:** 2026-11-13 · **Release:** Brazil
Use with `MODULE_IMPLEMENTATION_PLAN.md` (why) and `SAM_MODULE_REFERENCE.md` (how). Each gate needs **evidence**, not an assertion.

Legend: ☐ not met · ☑ met · N/A with reason. **G** = gate owner role. Thresholds marked **P** are programme practice; calibrate.

---

## Phase 0 — Commercial and platform prerequisites

| ☐ | Gate | Evidence | G |
|---|---|---|---|
| ☐ | SAM subscription/entitlement confirmed; tier chosen (Pro `com.sn_samp_master_ws`, Foundation `com.snc.sams`, or SaaS) | contract/subscription record; plugin list | Sponsor |
| ☐ | SAM Pro + Workspace installed; publisher packs limited to contracted set | `sys_plugins`; pack list | SAM admin |
| ☐ | Discovery (or SCCM/SGC) active and validated; MID healthy | Discovery Home; MID status | Discovery admin |
| ☐ | Required roles assigned and separated: `sam_admin`, `sam_user`, `sam_developer`, `sam_integrator`, `sam_spend_import`, `model_manager`, `catalog_admin`, `procurement_user`, `contract_manager`, `asset`, `sn_cmdb_admin`, `discovery_admin` | role membership export | SAM manager |
| ☐ | No shared `sam_admin` + `sam_developer` account in production | role matrix | Security |
| ☐ | Optional apps decided: SaaS LM, Spend Detection, Procurement integration, CSD, domain installer, PA domain support, Health Check, Otto | decision log | Programme lead |
| ☐ | Content Service decision recorded (opt-in / not) and exclusions set | Content Service Setup | SAM admin |
| ☐ | Credential vaulting/rotation for integrations | vault record | Security |

## Phase 1 — Scope and business case

| ☐ | Gate | Evidence | G |
|---|---|---|---|
| ☐ | Decisions the module must improve are written down | business case | Sponsor |
| ☐ | Baseline captured: status counts, installs vs products vs models, unlicensed results, CI owner/location %, last successful recon | baseline report | SAM manager |
| ☐ | KPI definitions agreed: Compliant, Under-licensed, Over-licensed, Reclaimable, Normalisation coverage, Reconciliation accuracy, True-up exposure | definitions doc | SAM manager + Finance |
| ☐ | Pilot publisher/product list agreed (MVP, typically top-spend publishers) | scope doc | Programme lead |
| ☐ | Explicit exclusions written (regions, BUs, publishers, containers, labs) | scope doc | Programme lead |
| ☐ | Out-of-scope commercial realities named (e.g. enterprise agreements stay Compliant) | scope doc | SAM manager |
| ☐ | Value-review cadence agreed (monthly ×3, then quarterly) | governance calendar | Sponsor |

## Phase 2 — Data model and reference data

| ☐ | Gate | Evidence | G |
|---|---|---|---|
| ☐ | Entity chain documented: `core_company`/`samp_sw_publisher` → `cmdb_software_product_model` → `cmdb_sam_sw_discovery_model` → `cmdb_sam_sw_install` → `alm_license` → `samp_license_metric_result` | data dictionary | SAM manager |
| ☐ | Publisher standard: canonical `samp_sw_publisher` linked to `core_company`; no free-text variants | sample audit | Data steward |
| ☐ | Product/version/edition/language/platform standards agreed | standards doc | SAM manager |
| ☐ | Product-type rules agreed (Licensable vs Not Licensable/Child/Driver/Patch/Unknown) | standards doc | SAM manager |
| ☐ | Suite parent/child standard and `auto_suite_inference` decision | decision log | SAM manager |
| ☐ | Entitlement metric matches the contract counting basis for every pilot publisher | §4.11 metric matrix sign-off | SAM manager + publisher owner |
| ☐ | Maintenance/SA linkage rule: never reconciled without base perpetual | standards doc | SAM manager |
| ☐ | Retention/archival rules: installs, results, import files, job logs | retention doc | Audit |

## Phase 3 — Source systems and integration contracts

| ☐ | Gate | Evidence | G |
|---|---|---|---|
| ☐ | Every source has a written contract: record types, required fields, frequency, latency, dedup key, error/retry, count reconciliation, owner | feed contracts | Integration lead |
| ☐ | Installs carry `installed_on` (CI) and user context where the metric needs it | data profile | Discovery admin |
| ☐ | Third-party installs use IRE (`com.snc.samp.ire.datasource.integration`), not direct inserts | integration design | SAM admin |
| ☐ | Uninstall/absence signal defined per source (SAM does not auto-delete) | feed contract | Integration lead |
| ☐ | Error queues owned: `samp_entitlement_import`, `samp_bulk_import`, `samp_job_log`, SGC/Discovery logs | runbook | SAM admin |
| ☐ | Count reconciliation alert threshold set | monitoring config | Integration lead |
| ☐ | SaaS feeds (if in scope) cover subscriptions **and** consumption/usage | integration design | SAM integrator |
| ☐ | SSO and direct profile not both attached to the same app | config review | SAM integrator |

## Phase 4 — Entitlements, contracts, procurement

| ☐ | Gate | Evidence | G |
|---|---|---|---|
| ☐ | Entitlements imported for pilot publishers; PPN or model link present | import report | SAM admin |
| ☐ | Every entitlement has metric, rights > 0, start/end, state Published/In use | `alm_license` query | SAM admin |
| ☐ | Contracts linked (`ast_contract`); renewals calendar populated | contract report | Contract manager |
| ☐ | POs/receipts reconciled to entitlements; procurement import errors closed | procurement report | Procurement |
| ☐ | Upgrades/step-ups/downgrades/cross-grade documented and linked | model relations | SAM manager |
| ☐ | Allocations valid: user **or** device; quantity ≤ rights; host/VM/cluster rules respected | allocation report | SAM admin |
| ☐ | Override licence costs set where true-up must be financial (created at zero) | cost report | Finance |

## Phase 5 — Normalisation and models

| ☐ | Gate | Evidence | G |
|---|---|---|---|
| ☐ | ≥90% of discovery models `Normalized` + `Manually Normalized` (**P**) | status report | SAM admin |
| ☐ | 0 `New` rows older than 48h (**P**) | status report | SAM admin |
| ☐ | `Match Not Found` backlog has named owner and weekly burn-down | backlog report | SAM analyst |
| ☐ | Pattern/custom-product/PPN fixes applied for recurring misses | rule inventory | SAM admin |
| ☐ | Content Service decision executed; CDS `Current count` = `Expected count` | CDS status | SAM admin |
| ☐ | Every licensable software model has `License under management` + metric | model audit | SAM manager |
| ☐ | Discovery-model→software-model matching reviewed; manual overrides have `Automatically matched=false` | match audit | SAM admin |
| ☐ | Dedup rule per high-volume product; version level chosen deliberately; stale threshold set | dedup report | SAM admin |

## Phase 6 — Reconciliation and position

| ☐ | Gate | Evidence | G |
|---|---|---|---|
| ☐ | T1–T10 controlled scenarios reproduce expected numbers | test evidence | SAM manager |
| ☐ | Product → Software Model → License Metric results populated | results export | SAM admin |
| ☐ | License Position shows Compliant/Not Compliant with non-blank true-up | report | SAM manager |
| ☐ | Rights algebra explained for every Not Compliant pilot model | reconciliation review | SAM manager |
| ☐ | No failed `SAM*` jobs in 7 days; `samp_job_log` clean | job report | SAM admin |
| ☐ | Reconciliation cadence agreed (weekly default + on demand) and communicated | calendar | Programme lead |
| ☐ | Historical Results retention confirmed | audit check | Audit |

## Phase 7 — Reporting, remediation, reclamation

| ☐ | Gate | Evidence | G |
|---|---|---|---|
| ☐ | Named owners use Software asset overview + License usage | access/usage log | Programme lead |
| ☐ | Normalization and content dashboard reviewed weekly | cadence minutes | SAM admin |
| ☐ | Success portal goals + maturity items set | goal records | Programme lead |
| ☐ | Health Check scan run; findings assigned | Scan Findings | SAM admin |
| ☐ | Reclamation rules for pilot publishers; suite logic verified | rule inventory | SAM admin |
| ☐ | Removal candidates reviewed and actioned with service owners | candidate report | Service owner |
| ☐ | Reclaim catalog request tested end to end | request record | Service desk |
| ☐ | Renewals calendar used for upcoming expiries | calendar review | Contract manager |

## Phase 8 — Security, change control, audit

| ☐ | Gate | Evidence | G |
|---|---|---|---|
| ☐ | ACLs reviewed on `alm_license`, `cmdb_software_product_model`, `cmdb_sam_sw_discovery_model`, `samp_license_metric_result` (commercial + workforce data) | ACL export | Security |
| ☐ | Least-privilege verified by role test (read-only cannot edit) | test evidence | Security |
| ☐ | Change control covers: models, metrics, discovery maps, normalisation rules, dedup rules, published list, recon grouping, exclusion flag | change process | Programme lead |
| ☐ | Before/after reconciliation snapshot required for compliance-affecting changes | change template | SAM manager |
| ☐ | Evidence chain retained: PO → `ast_contract` → `alm_license` → allocation → install → result | audit sample | Audit |
| ☐ | Rollback/exception playbook published (misclassified model, wrong metric, duplicate feed, revert limits) | runbook | SAM manager |
| ☐ | Domain separation configured if in scope (properties, published products, PA) | config review | Platform |

## Phase 9 — Testing, cutover, adoption

| ☐ | Gate | Evidence | G |
|---|---|---|---|
| ☐ | Data validation, integration, workflow, reconciliation, security, performance, UAT, regression executed | test summary | QA lead |
| ☐ | UAT signed by procurement, asset, finance, service owners | sign-off | Programme lead |
| ☐ | Migration: extract/cleanse/transform/validate complete; parallel run explained | cutover report | SAM manager |
| ☐ | Go/no-go criteria met; rollback trigger documented | cutover decision | Sponsor |
| ☐ | Definition of "migration complete" met (validated entitlements + normalised inventory + successful recon + accepted reports) | evidence pack | SAM manager |
| ☐ | Role-based training delivered; quick guides published | training log | Change lead |
| ☐ | Stakeholder/comms plan executed; go-live announced | comms log | Change lead |
| ☐ | Hypercare 2–4 weeks staffed; issue log live | hypercare plan | Programme lead |
| ☐ | Support model L1/L2/L3 agreed | support doc | Service manager |
| ☐ | Post-go-live KPI monitoring dashboard live | dashboard | SAM manager |

---

## Final production-readiness statement

SAM is production-ready only when **all** of the following are evidenced:

1. Entitlements complete and contract-linked for the pilot publishers.
2. Inventory producing installs linked to CIs, with owned error paths.
3. Software models/metrics approved by accountable owners.
4. Normalisation coverage gate met and exception workflow staffed.
5. Reconciliation reproduces controlled expected results.
6. SaaS consumption/renewal included where in scope.
7. Named business owners use reports and remediation.
8. Data-quality and reconciliation KPIs monitored after go-live.
9. Rollback, change control, and audit evidence in place.

Anything less is a configured module, not a trusted SAM programme.
