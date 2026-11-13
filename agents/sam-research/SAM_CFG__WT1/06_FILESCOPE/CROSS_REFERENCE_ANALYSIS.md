# Cross-Reference Analysis: SAM Documentation vs. Identified Gaps

**Date:** 2026-11-13  
**Documents analyzed:**
1. `final/FINAL_SAM_CONFIG_REFERENCE.md` (18-section master reference)
2. `agents/sam-research/SAM_CFG__WT1/06_FILESCOPE/FILESCOPE.md` (artifact inventory)
3. `agents/sam-research/SAM_CFG__WT1/06_FILESCOPE/TSOM_SAM_GUIDE_ENHANCEMENTS.md` (8 enhancement concepts)

**Against:** User's comprehensive gap analysis from GitHub repo review

---

## Coverage Matrix

### Legend
| Symbol | Meaning |
|--------|---------|
| ✅ **COVERED** | Explicitly documented with evidence citations |
| 🟡 **PARTIAL** | Mentioned but lacks depth/detail requested |
| ❌ **MISSING** | Not addressed in any of the three documents |
| 🔄 **IN ENHANCEMENTS** | Covered in TSOM enhancement concepts but not in main reference |

---

## 1. Biggest Gaps from Gap Analysis

| Gap Area | Gap Analysis Requirement | Coverage in My Documents | Status |
|----------|-------------------------|--------------------------|--------|
| **Entitlement ingestion** | Purchase records, license metrics, quantities, PO/contract terms, maintenance, upgrade/downgrade rights, allocations, import formats, PPN matching, source-system contracts | Ref §3.6 (Entitlement management), §9 (Entitlement management), §9.1 (critical fields), §9.2 (hygiene rules) | 🟡 PARTIAL — Fields and hygiene covered; **import formats, PPN matching, source-system contracts MISSING** |
| **Software model strategy** | Publisher/product/version/edition, discovery maps, suite relationships, upgrade/downgrade relationships, Content Library / PPN auto-population vs manual creation | Ref §2 (Data model), §8 (Normalization engine), §8.2 (rule types), §12.5 (suite component over-count) | 🟡 PARTIAL — Models and normalization covered; **PPN auto-population vs manual strategy MISSING** |
| **License metrics** | Per-device, per-user, named-user, per-core, processor, vendor-specific metric groups, wrong metric consequences | Ref §3.7 (Licence metrics table), §10 (License metrics config/pitfalls), §10.2 (common pitfalls), §12.4 (consumption logic) | ✅ COVERED — Comprehensive metric groups, publisher-specific, pitfalls, consumption logic |
| **SaaS subscriptions** | Seat/usage ingestion, subscription records, renewal dates, consumption summaries, Store plugin operationalization | Ref §3.1 (SaaS License Management plugin), §3.4 (SaaS Direct Integrations table), §7.3 (SaaS connectors), §10 (Consumption/SaaS metrics), §15.2 (SaaS seat utilization KPI) | 🟡 PARTIAL — Connectors and metrics covered; **operational details (renewal tracking, consumption summaries, custom integration boundary) MISSING** |
| **Content Library / PPN dependency** | PPN-based software-model matching, content updates, fallback manual modeling | Ref §3.5 (Content Library status), §8 (Normalization engine), §8.1 (process), §8.2 (rule types), §14 (Content Service opt-in) | 🟡 PARTIAL — Content Library covered; **PPN-based matching explicitly MISSING** |
| **Operational governance** | Data ownership, source-system contracts, role separation, audit trail, change control, optimization/reclamation workflows | Ref §6 (Roles/ACLs), §14 (Remediation workflow), §15.2 (dashboards with owners), §16 (Anti-patterns #9, #14), TSOM Enh #7 (Exception taxonomy with owners) | 🟡 PARTIAL — Roles and some workflows covered; **source-system contracts, formal change control, audit trail evidence MISSING** |
| **Validation & pilot criteria** | Concrete test cases ("1 per-device entitlement + 2 installs → shortfall 1"), data-quality thresholds, expected License Workbench outcomes | Ref §15.3 (Readiness Scorecard - 10 checks, 3 hard gates), §8.4 (Normalization >85% KPI), TSOM Enh #6 (KPI gate logic) | 🟡 PARTIAL — Readiness probe and KPI gate covered; **concrete reconciliation test cases with expected results MISSING** |

---

## 2. Setup Sequence Gates (Under-emphasized in Docs)

| Setup Gate | Gap Analysis Requirement | Coverage in My Documents | Status |
|------------|-------------------------|--------------------------|--------|
| **Plugin/subscription + roles verified** | Confirm SAM Professional entitlement/plugin + required roles (sam_admin, sam_user, model_manager, asset, procurement_user, contract_manager) | Ref §3.1 (Plugin activation table), §3.2 (Roles table), §5 (Plugin activation steps), §6 (Roles/ACLs) | ✅ COVERED — Plugins and core roles; **model_manager, procurement_user, contract_manager roles NOT listed** |
| **Define data model first** | Inventory sources, entitlement sources, contracts, users/devices, SaaS — before technical implementation | Ref §4A (Setup sequence step 6: Foundation data), §7 (Discovery/connector feeds) | 🟡 PARTIAL — Foundation data step exists; **explicit "define data model first" as prerequisite MISSING** |
| **Select/validate inventory sources** | Discovery, Service Graph SCCM, Jamf, Intune — confirm they populate cmdb_sam_sw_install | Ref §3.4 (Discovery/Connector feeds), §7 (Discovery/connector feeds detail), §4A step 7 | ✅ COVERED — Sources listed with config paths |
| **Import/create entitlements before reconciliation** | Load entitlements (ideally with PPN matching) before relying on reconciliation | Ref §4A steps 11, 13 (Entitlements then Reconciliation), §9 (Entitlement management) | ✅ COVERED — Order specified in setup sequence |
| **Create/match software models for high-value publishers** | Assign correct metric groups/metrics; validate discovery maps | Ref §4A steps 10, 12 (Normalisation then Licence metrics), §8 (Normalization), §10 (Metrics) | 🟡 PARTIAL — Steps exist; **"high-value publishers first" prioritization MISSING** |
| **Run normalization, handle exceptions, then on-demand reconciliation** | Inspect shortfall/surplus in License Workbench | Ref §4A steps 10, 13, §8.4 (KPI gate), §11 (Reconciliation outputs), §15.2 (License Workbench implied) | 🟡 PARTIAL — Sequence covered; **License Workbench explicit inspection step MISSING** |
| **Pilot limited product set with success criteria** | Clear success criteria before scaling | Ref §4A step 7 ("pilot scope"), §16 (Anti-pattern #1) | 🟡 PARTIAL — Pilot mentioned; **explicit success criteria/go-no-go gates MISSING** |
| **Define ownership, access model, audit evidence, change control** | For model/metric/normalization changes | Ref §6 (Roles), §14 (Remediation owners), §16 (Anti-patterns), TSOM Enh #7 (Exception taxonomy with owners) | 🟡 PARTIAL — Some ownership; **formal change control process, audit evidence linking MISSING** |

---

## 3. CMDB Assumptions to Challenge

| Assumption | Gap Analysis Requirement | Coverage in My Documents | Status |
|------------|-------------------------|--------------------------|--------|
| **CI-to-install linkage quality** | Per-device and per-user metrics fail without correct CI linkage | Ref §1.1 (Mental model - 3 gates), §2 (cmdb_ci_computer table), §12.2 (Install recognition flow), §13.3 (Decommissioned devices excluded) | 🟡 PARTIAL — Referenced; **explicit linkage quality requirement for metrics MISSING** |
| **Explicit IRE usage for non-Discovery sources** | Prevent uncontrolled duplicate CIs/install records | Ref §1.1 (Layer 1: CI Identification Rules), §13.1 (Duplicate CI vs Install distinction), §13.3 (Cross-source suppression) | 🟡 PARTIAL — IRE mentioned; **explicit requirement for non-Discovery sources to use IRE MISSING** |
| **Suite, bundle, upgrade, downgrade rights modeling** | Not just CI attributes | Ref §9.1 (Downgrade rights field), §10.2 (Microsoft/Oracle pitfalls), §12.5 (Suite component over-count), §17 (Open Q#10: Suite roll-up behavior) | 🟡 PARTIAL — Referenced in multiple places; **explicit modeling guidance MISSING** |
| **Vendor-specific metric groups vs generic "Common"** | When generic metrics are insufficient | Ref §3.7 (Metric groups table with publisher-specific), §10.1 (Metric group controls), §10.2 (Publisher pitfalls), §17 (Open Q#2, #10) | ✅ COVERED — Publisher-specific groups documented with warnings |

---

## 4. General Module Implementation Plan Items (from 2nd analysis)

| Category | Gap Analysis Requirement | Coverage in My Documents | Status |
|----------|-------------------------|--------------------------|--------|
| **Scope, success criteria, value** | In-scope/out-of-scope, measurable criteria, baseline, phased rollout with gates | Ref §15.2 (Dashboard targets), §16 (Anti-patterns), §4A (Setup sequence) | ❌ MISSING — No explicit scope doc, success criteria, baseline measurements, phased rollout plan |
| **Prerequisites & dependency map** | Plugin entitlements, roles, dependent modules, instance version pin, content services | Ref §3.1 (Plugins), §3.2 (Roles), §5 (Activation steps), §17 (Open Q#4: table names per edition) | 🟡 PARTIAL — Plugins/roles covered; **dependent modules, version pin, content services dependency map MISSING** |
| **Data model & source-system contracts** | Authoritative sources, required fields, update frequency, error handling, ownership, import approach, deduplication, CI relation/IRE | Ref §2 (Data model tables), §3.4/§7 (Sources), §9.1 (Entitlement fields), §12.3 (Duplicate handling), §13.3 (Cross-source) | 🟡 PARTIAL — Data model and sources covered; **source-system contracts (frequency, error handling, ownership) MISSING** |
| **Process design** | End-to-end flows, exception handling, approval/change control, operational cadences, reclamation workflows, business owners | Ref §4B (Runtime reconciliation sequence), §14 (Remediation workflow), §15.2 (Cadences), §16 (Anti-patterns) | 🟡 PARTIAL — Reconciliation flow and reclamation covered; **full process flows, approval gates, change control MISSING** |
| **Governance, ownership, access** | Data/process owners, role-based access, audit trail, change control for model/metric/rule changes | Ref §6 (Roles/ACLs), §14 (Owners per exception), §15.2 (Dashboard owners), §16 (Anti-pattern #9, #14) | 🟡 PARTIAL — Roles and some owners; **formal data ownership model, audit trail requirements, change control process MISSING** |
| **Validation, testing, acceptance** | Concrete test cases with expected results, data-quality thresholds, reconciliation validation, UAT criteria, performance | Ref §15.3 (Readiness Scorecard), §8.4 (Normalization KPI), §17 (Open questions) | 🟡 PARTIAL — Readiness probe and KPI; **concrete test cases with expected results, UAT criteria, performance MISSING** |
| **Reporting, dashboards, consumption** | Primary reports/workspaces, key metrics calculation, alerting/distribution, training/runbooks | Ref §3.3 (Guided Setup/Workspaces), §11.2 (Reconciliation outputs), §15.1 (Health Dashboard), §15.2 (Key dashboards) | 🟡 PARTIAL — Dashboards listed; **metrics calculation detail, alerting, training/runbooks MISSING** |
| **Cutover, hypercare, operations** | Migration steps, hypercare model, content/library updates, monitoring, rollback/exception procedures | Ref §27 (Scheduled jobs), §8.5 (Apply content changes), §17 (Open Q#7: connector monitoring) | ❌ MISSING — No cutover, hypercare, rollback, or ongoing ops procedures |

---

## 5. Recommended Addition: SAM_IMPLEMENTATION_CHECKLIST.md

| Checklist Item | Gap Analysis | Coverage in My Documents | Status |
|----------------|-------------|--------------------------|--------|
| Plugin/subscription and roles verified | ✅ Required | Ref §3.1, §3.2, §5, §6 | ✅ COVERED (partial - missing some roles) |
| Inventory source(s) selected and validated | ✅ Required | Ref §3.4, §7, §4A step 7 | ✅ COVERED |
| Entitlement source, fields, import approach (PPN/Content Library) | ✅ Required | Ref §3.6, §9, §4A steps 11, 13 | 🟡 PARTIAL — **PPN/Content Library import approach MISSING** |
| Software-model and license-metric matrix for priority publishers | ✅ Required | Ref §3.7, §10, §4A steps 10, 12 | 🟡 PARTIAL — **Matrix format for priority publishers MISSING** |
| Normalization exception workflow | ✅ Required | Ref §8.3, §8.4, §13.2, TSOM Enh #6 | ✅ COVERED (KPI gate + remediation workflow) |
| Reconciliation test cases with expected results | ✅ Required | Ref §15.3 (Readiness probe) | ❌ MISSING — **No concrete test cases with expected results** |
| SaaS subscription and usage plan | ✅ Required | Ref §3.1, §3.4, §7.3, §10, §15.2 | 🟡 PARTIAL — **Operational plan (renewals, custom integration boundary) MISSING** |
| Data ownership, access model, audit trail | ✅ Required | Ref §6, §14, §15.2, §16, TSOM Enh #7 | 🟡 PARTIAL — **Formal ownership model, audit trail evidence linking MISSING** |
| Pilot scope, success metrics, production rollout criteria | ✅ Required | Ref §4A step 7, §16 | ❌ MISSING — **No explicit pilot gates or rollout criteria** |

---

## 6. What My Documents Cover WELL (Strengths)

| Area | Evidence |
|------|----------|
| **Discovery → Install → Discovery Model → Normalization → Reconciliation path** | Ref §1.1, §2, §4B, §8, §11, §12 — Comprehensive with flow diagrams |
| **Three-layer insert-vs-update (Install Recognition → Entitlement Consumption → Reconciliation Exceptions)** | Ref §12.1 — Core differentiator from CMDB |
| **Five identification layers (IRE, HAM, Normalisation, Metric, Reconciliation)** | Ref §1.1, §13.1, TSOM Enh #8 — Clear conceptual separation |
| **Normalization engine detail** | Ref §8.1-8.5 — Rule types, statuses, KPI gate, pattern rule form |
| **License metrics with publisher-specific groups and pitfalls** | Ref §3.7, §10.1-10.3, §12.4 — Comprehensive consumption logic |
| **Reconciliation outputs and Oracle specifics** | Ref §11.1-11.5 — Three tiers, properties, Oracle config |
| **Scheduled job dependency chain** | Ref §3.9, §4B, TSOM Enh #4 — Sequential daily → weekly visual |
| **Anti-patterns with fixes** | Ref §16 — 14 patterns with consequence/fix |
| **Readiness probe with hard gates** | Ref §15.3 — 10 checks, 3 hard gates (schema, assets, CMDB) |
| **Evidence discipline** | All claims cited to 32 release-pinned sources; UNVERIFIED explicit |

---

## 7. Critical Missing Artifacts (Not in Any Document)

| Missing Artifact | Why Needed | Gap Analysis Reference |
|------------------|------------|------------------------|
| **SAM_IMPLEMENTATION_CHECKLIST.md** | Gate document for implementation | Explicitly recommended in both analyses |
| **Source-System Contract Templates** | Define update frequency, fields, error handling, ownership for each feed | "Source-system contracts" gap |
| **Concrete Reconciliation Test Cases** | "1 per-device entitlement + 2 installs → shortfall 1" examples | "Validation & pilot criteria" gap |
| **Data Ownership Matrix** | RACI for entitlements, contracts, models, normalization, reconciliation | "Operational governance" gap |
| **Change Control Process for Model/Metric/Rule Changes** | Controlled release because changes alter compliance results | "Change control" gap |
| **Audit Evidence Linkage Specification** | Entitlement → PO → Contract → Reconciliation result chain | "Auditability" gap |
| **Phased Rollout Plan with Go/No-Go Gates** | Pilot publishers → expand with criteria | "Scope, success criteria" gap |
| **Cutover/Hypercare Procedures** | Migration from legacy, ongoing ops | "Cutover, hypercare" gap |
| **Performance/Volume Considerations** | Large install/entitlement volumes | "Validation, testing" gap |
| **SaaS Custom Integration Boundary Doc** | When OOB connectors insufficient | "SaaS-specific process" gap |

---

## 8. Recommendation: Priority Actions

| Priority | Action | Document to Update/Create |
|----------|--------|---------------------------|
| **P0** | Create `SAM_IMPLEMENTATION_CHECKLIST.md` with all 9 gates | New file in `final/` |
| **P0** | Add concrete reconciliation test cases to Reference §15 or new §19 | `FINAL_SAM_CONFIG_REFERENCE.md` |
| **P1** | Add source-system contract template section | `FINAL_SAM_CONFIG_REFERENCE.md` (new §19) |
| **P1** | Add data ownership/RACI matrix | `FINAL_SAM_CONFIG_REFERENCE.md` (new §19) |
| **P1** | Add change control process for model/metric/rule changes | `FINAL_SAM_CONFIG_REFERENCE.md` (new §19) |
| **P1** | Document PPN/Content Library import approach for entitlements | `FINAL_SAM_CONFIG_REFERENCE.md` §9 or new § |
| **P2** | Add SaaS operational plan (renewals, custom integration boundary) | `FINAL_SAM_CONFIG_REFERENCE.md` §7.3 expansion |
| **P2** | Add phased rollout plan with pilot gates | `FINAL_SAM_CONFIG_REFERENCE.md` §4A expansion |
| **P2** | Add cutover/hypercare/ongoing ops section | `FINAL_SAM_CONFIG_REFERENCE.md` (new §) |
| **P3** | Create source-system contract templates as separate artifacts | New files in `agents/sam-research/SAM_CFG__WT1/templates/` |

---

## Summary

| Coverage Dimension | % Covered | Notes |
|--------------------|-----------|-------|
| **Technical Configuration (Discovery → Normalization → Reconciliation)** | 90% | Core strength — comprehensive, evidence-backed |
| **Entitlement & Software Model Strategy** | 60% | Fields/hygiene covered; import formats, PPN strategy, priority publisher matrix missing |
| **SaaS Operationalization** | 40% | Connectors listed; renewal tracking, consumption summaries, custom integration boundary missing |
| **Operational Governance** | 35% | Roles and some workflows; source contracts, change control, audit trail, ownership model missing |
| **Validation & Pilot Criteria** | 40% | Readiness probe + KPI gate; concrete test cases, UAT, go/no-go gates missing |
| **General Module Lifecycle (Scope → Cutover → Ops)** | 20% | Setup sequence only; scope, rollout, cutover, hypercare, performance missing |

**Bottom line:** The reference excels at the **technical configuration contract** (what SAM adds to CMDB/Discovery) but under-delivers on the **implementation lifecycle** (how to successfully deploy and operate SAM). The missing pieces are predominantly process, governance, and validation artifacts — not technical configuration gaps.

---

*Generated 2026-11-13 by cross-referencing three deliverables against user's gap analysis*