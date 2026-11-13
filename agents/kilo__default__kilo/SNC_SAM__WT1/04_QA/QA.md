# QA.md — ServiceNow SAM QA Self-Check

- **Compiled by:** `kilo` / provider **kilo** / harness **default** (`kilo__default__kilo`)
- **Date:** 2026-11-13
- **Purpose:** Self-check validations for each phase of the SAM implementation, mirroring the QA.md pattern from `ALT_PARALLELSWARM` (`final/QA.md`).

---

## 0. Provenance & method

Sources were fetched from the ServiceNow khub API (Australia maps) on 2026-11-13 and retained as raw text in this agent's `research/` folder. Where two sources disagreed, the discrepancy is flagged rather than silently resolved.

---

## 1. Phase 1 QA self-check

### 1.1 CMDB health prerequisites
- [ ] CMDB hardware/computer CIs have `installed_on` field populated (sufficient identity for Discovery/SCCM).
- [ ] Owners set on CIs if reconciliation grouping will be used.
- [ ] Location/department/cost center/company/country/region set on CIs if grouping by them.
- [ ] User records exist for per-user allocation or SaaS seat reclamation.
- [ ] Discovery actually covers the estate (Discovery and/or SCCM/SG connector), not a spreadsheet.
- [ ] Entitlement source of truth ready (contracts, PPN, Microsoft MLS).
- [ ] In-scope publisher list documented (packs cost money and complexity).
- [ ] Exclude-SAM device decision documented (leased, out of scope, phase-1 location only).

### 1.2 Baseline metrics captured
- [ ] Discovery-model count by normalization status.
- [ ] Install count vs unique products vs unique software models.
- [ ] Unlicensed product-result count.
- [ ] % CIs with owner/location.
- [ ] SaaS assigned vs used (after connector).
- [ ] Time of last successful recon.
- [ ] Published-product count if phase-wise.

### 1.3 Phase 1 gate pass/fail
- PASS: All 8 prerequisites verified + all 8 baseline metrics captured.
- FAIL: Any prerequisite unverified OR any baseline metric missing.

---

## 2. Phase 2 QA self-check

### 2.1 SAM activation
- [ ] Plugin `com.sn_samp_master_ws` activated.
- [ ] SAM tables created (`cmdb_sam_sw_install`, `cmdb_sam_sw_discovery_model`, etc.).
- [ ] CI related-list: `Software Installations` tab on CI records.
- [ ] Discovery running post-SAM; `cmdb_sam_sw_install` populated.
- [ ] Entitlements loaded and verifiable.
- [ ] Content Service opt-in decision documented (opt-in or defer).

### 2.2 Phase 2 gate pass/fail
- PASS: SAM activated; CI related-list working; Discovery post-SAM populating tables; entitlements loaded.
- FAIL: Plugin activation failed; CI related-list not configured; Discovery not populating SAM tables; entitlements not loaded.

---

## 3. Phase 3 QA self-check

### 3.1 Normalization running
- [ ] Daily job `SAM - Normalize discovery models using content library rules` running.
- [ ] Daily job `SAM - Discovery Model Normalization job` running.
- [ ] Normalization status distribution measurable across 5 statuses.

### 3.2 Reconciliation running
- [ ] Weekly reconciliation running on schedule.
- [ ] Three-tier results accessible (Product, Software Model, License Metric).
- [ ] Dedup job has run; primary vs duplicate installs marked.
- [ ] IBM special case: Discovery rows stay Active; authorized-provider duplicates inactivated.

### 3.3 Reclamation rules
- [ ] Reclamation rules flagging unused rights.
- [ ] SaaS/SSO integration auto-created rule reviewed.
- [ ] Timeout property `sam_reclamation_flow_error_timeout` = 30 days.

### 3.4 Phase 3 gate pass/fail
- PASS: Normalization running; reconciliation running; dedup working; reclamation active.
- FAIL: Normalization not assigning statuses; reconciliation not running; dedup not marking; reclamation rules not flagging.

---

## 4. Phase 4 QA self-check

### 4.1 Discovery Status
- [ ] Devices reach `Identified CI`; not `Active, couldn't classify`.
- [ ] Per-device states flow verified.
- [ ] Discovery Timeline reviewed; no stalled devices.

### 4.2 CMDB Health KPIs
- [ ] Correctness, completeness, compliance KPIs captured/improving.
- [ ] Duplicate metric reviewed (narrow conditions — only CIs with identification rules and empty discovery source or active de-dup task).

### 4.3 Anti-pattern checklist
- [ ] Zero active anti-patterns from the 10 documented.
- [ ] Discovery models not treated as catalog items.
- [ ] Entitlements loaded before discovery (if PPN-driven).
- [ ] `automaticsmrcreation` off in Crawl.
- [ ] Phase-wise publisher rollout, not day-one all.
- [ ] Content Service opt-in not skipped.
- [ ] Not using deprecated SCCM 2012/2016 usage plugins.
- [ ] Not overlaying unnamed install→discovery-model BR.
- [ ] Not mixing `model_manager` vs `catalog_admin` in catalog publish.
- [ ] Not assuming Workspace leaves classic SAM navigation.

### 4.4 Data quality
- [ ] Normalization hit-rate measurable (~85%+ OOTB, ~95%+ after Content Service).
- [ ] Reconciliation weekly cadence confirmed.
- [ ] Dedup templates configured; inclusion rules/skip-duplicates set.
- [ ] Reclamation unused rights flagged; timeout verified.
- [ ] Phase-wise scope freeze: `com.snc.samp.manage.published.products` enabled; products published; recon re-run.
- [ ] Success portal goals completed; savings tracked; health checks passed.

### 4.5 Phase 4 gate pass/fail
- PASS: All Phase 4 QA items verified.
- FAIL: Any QA item unverified; remediate and re-loop.

---

## 5. Overall SAM implementation QA

### 5.1 End-to-end validation
- [ ] Full cycle: CMDB health → SAM activation → Discovery → Normalization → Reconciliation → Reclamation → Success portal.
- [ ] All phases gate-passed (Phase 1 → Phase 2 → Phase 3 → Phase 4).
- [ ] Baseline metrics captured before go-live and tracked after go-live.
- [ ] Success portal tracking completed goals, actual vs projected savings, health checks passed, value-builder tasks.
- [ ] CMDB health KPIs (correctness, completeness, compliance) assessed.

### 5.2 Final go/no-go
- GO: All phase gates passed; baseline captured; success portal active; KPIs improving.
- NO-GO: Any phase gate failed; remediate and re-loop through failed phases.