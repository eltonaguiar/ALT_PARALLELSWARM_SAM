# Bidirectional Gap Analysis: Webpage SAM Guide ↔ Research Documents

**Date:** 2026-11-13  
**Sources compared:**
- **Webpage/Local:** `https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-.../sam-guide/` (≈1074 lines, same as local `sam-guide.md`)
- **Research:** `FINAL_SAM_CONFIG_REFERENCE.md` + `TSOM_SAM_GUIDE_ENHANCEMENTS.md` + `CROSS_REFERENCE_ANALYSIS.md`

---

## PART A: Items on Webpage/Local SAM Guide NOT in Research Documents
*These should be added to the learning protocol (e.g., ServiceNow_Learning repo patterns)*

| # | Webpage Section / Item | Why Valuable for Learning Protocol | Research Coverage |
|---|------------------------|-----------------------------------|-------------------|
| 1 | **CIS-SAM Exam Alignment Table** (Domain weights, guide section mapping, prep courses) | Standardized exam-prep framework for all module guides | ❌ Not in research |
| 2 | **SAM Lifecycle Diagram** (Mermaid stateDiagram with 6 states + notes) | Visual learning anchor; reusable template for other modules | ❌ Not in research |
| 3 | **Three Record Types Comparison Table** (6 rows: Software Model, Discovery Model, Installation, Usage, Entitlement, Reconciliation Result) | Core mental model; "verify in your release" disclaimer is excellent practice | 🟡 Partial in research §1.1, §2 |
| 4 | **Normalization Workflow (5 steps)** | Clear procedural steps: collect → match → queue → manual map → reconcile | 🟡 Partial in research §8.1 |
| 5 | **Reconciliation "What Breaks It" Symptom Table** (6 symptoms → root causes) | Troubleshooting reference; pattern for other modules | ❌ Not in research |
| 6 | **4 Mermaid Diagrams in Reconciliation Section** (Flow, Compliance States, Publisher Rules, SaaS Flow) | Visual learning standards; diagram templates for module guides | ❌ Not in research |
| 7 | **Compliance Positions Explained Table** (6 positions: Compliant, Over, Under, Unlicensed, Not Counted, Unknown) | Standardized compliance vocabulary; financial meaning + typical action | 🟡 Partial in research §12.5 |
| 8 | **Discovery & Data Sources Table** (6 source types with examples + feeds) | Data architecture reference; "data quality rules" subsection | 🟡 Partial in research §3.4, §7 |
| 9 | **SaaS vs On-Premise Comparison Table** (5-row comparison) | Clear differentiation; reusable for other cloud modules | 🟡 Partial in research §3.4, §7.3 |
| 10 | **Optimization Priority List** (6 ordered items) | Operational playbook; priority ordering methodology | 🟡 Partial in research §14 |
| 11 | **Reclamation Workflow** (6-step ASCII flow) | Standardized workflow notation; "never reclaim on single night" rule | 🟡 Partial in research §14.1 |
| 12 | **Publisher-Specific Traps Table** (6 publishers with licensing traps) | Audit defence reference; exam-critical publisher knowledge | 🟡 Partial in research §10.2, §17 |
| 13 | **5 Re-usable Code Snippets** (Business Rule, Scheduled Job, Script Include, Client Script, Reports) | Copy-paste library; metadata patterns for module guides | ❌ Not in research |
| 14 | **Out-of-Box Features Table** (11 features with descriptions) | Feature inventory; "what ships" vs "what you build" | 🟡 Partial in research §3.1 |
| 15 | **Key Table Hierarchy** (ASCII tree with 6 tables + relationships) | Data model visualization standard | 🟡 Partial in research §2 |
| 16 | **Integrations Table** (14 rows: direction, system, protocol, purpose) | Integration architecture reference | 🟡 Partial in research §3.4, §7 |
| 17 | **Key Fields: Essential + Forgotten** (2 tables, 18 fields with "why it matters") | Field-level reference; "fields people forget" is high-value | 🟡 Partial in research §9.1, §10.2 |
| 18 | **Goals/Metrics Table** (8 goals with metrics + healthy targets) | KPI framework; "business case in one line" | 🟡 Partial in research §15.2 |
| 19 | **Common Mistakes Table** (12 mistakes with consequence + fix) | Anti-pattern format with actionable fixes | 🟡 Partial in research §16 (14 anti-patterns) |
| 20 | **7-Step Lab Exercise** (with verify steps for each) | Hands-on learning template; "teach back" step | ❌ Not in research |
| 21 | **SLAs, Dashboards & Workspaces** (3 tables: workspaces, dashboards, SLA targets) | Operational standards; SLA-style targets template | 🟡 Partial in research §15.2 |
| 22 | **Quiz (8 Q&A)** with hidden answers | Knowledge check template; exam prep | ❌ Not in research |
| 23 | **Official Learning Resources** (Now Learning, Product Docs, Official Videos with playlists) | Curated resource list template | ❌ Not in research |
| 24 | **Memory Aids & Mnemonics** (BAA, LOCS, UI Policy vs Data Policy, IRE, ARM, Retire Before Delete, Order vs Priority, Coalesce, Debugging) | Cross-cutting learning aids; reusable across modules | ❌ Not in research |
| 25 | **Related Guides** cross-references | Module ecosystem navigation | ❌ Not in research |
| 26 | **"Verify in your release" disclaimers** throughout | Version-awareness practice; critical for ServiceNow | ❌ Not in research |
| 27 | **"Exam focus" / "Exam-critical" callouts** | Certification alignment markers | ❌ Not in research |
| 28 | **"ELI5" explanations** (e.g., M365 example in Purpose) | Accessible entry points for complex topics | ❌ Not in research |
| 29 | **"Tip" / "Note" callout boxes** | Information hierarchy patterns | ❌ Not in research |

---

## PART B: Items in Research Documents NOT on Webpage/Local SAM Guide
*These should be added to the SAM guide page (via PR to ServiceNow_Learning_TSOM repo)*

| # | Research Item | Source Document/Section | Value for SAM Guide | Priority |
|---|---------------|------------------------|---------------------|----------|
| 1 | **Evidence Policy + Release Scope** (32 sources, release-pinned, [S<n>] citations) | REF §0 | Source transparency; reproducibility | P1 |
| 2 | **Three Hard Gates Mental Model** (Schema+Entitlement, CMDB+IRE, Discovery Feed) | REF §1 | Prerequisite clarity before configuration | P1 |
| 3 | **Five Identification Layers** (IRE, HAM, Normalisation, Metric, Reconciliation) | REF §1.1, §13.1, TSOM Enh #8 | Conceptual clarity; #1 confusion point | P1 |
| 4 | **Complete Plugin Activation Table** (11 plugins with IDs, entitlement gates, notes) | REF §3.1 | Comprehensive plugin inventory | P1 |
| 5 | **Roles Table** (4 roles with capabilities + ACL notes) | REF §3.2, §6 | Role-based access clarity | P1 |
| 6 | **Guided Setup / Configuration Console Entry Points** (4 paths with roles required) | REF §3.3 | "Where to click" operational guidance | P1 |
| 7 | **Discovery/Connector Feeds Detail** (Legacy vs Modern vs SaaS, 11 sources with config paths) | REF §3.4, §7 | Source selection guidance | P1 |
| 8 | **Normalization Engine Deep Dive** (Process, 4 rule types, 6 statuses, KPI >85%, Pattern rule form) | REF §8 | Normalization operational detail | P1 |
| 9 | **Entitlement Critical Fields + Hygiene Rules** (7 fields with verdict, 4 hygiene rules) | REF §9 | Entitlement data quality | P1 |
| 10 | **License Metrics: Complete Publisher Groups** (10 groups, 30+ metrics, Common vs Publisher-specific) | REF §3.7, §10 | Metric selection reference | P1 |
| 11 | **License Metric Pitfalls Table** (5 pitfalls with consequence + fix) | REF §10.2 | Silent failure prevention | P1 |
| 12 | **Custom License Metrics** (scripted, Resource Value table, property) | REF §10.3 | Advanced configuration | P2 |
| 13 | **Reconciliation Detail** (3 output tiers, remediation actions, Oracle properties, 8 system properties) | REF §11 | Reconciliation configuration | P1 |
| 14 | **Three-Layer Insert-vs-Update Decision Table** (Install Recognition, Entitlement Consumption, Reconciliation Exceptions) | REF §12.1, TSOM Enh #1 | **Core SAM differentiator from CMDB** | P1 |
| 15 | **Software Install Recognition Flow** (ASCII flow: Discovery → Install → BR → Match/No Match) | REF §12.2 | Technical flow clarity | P1 |
| 16 | **Duplicate Installation Handling** (No duplicate_of, cross-source, REST API remediation) | REF §12.3 | Duplicate management | P1 |
| 17 | **Entitlement Consumption Logic per Metric** (9 metrics with calculation formulas) | REF §12.4 | Consumption transparency | P1 |
| 18 | **Reconciliation Exception Types** (5 types with meaning + typical cause) | REF §12.5 | Exception taxonomy | P1 |
| 19 | **Duplicate Prevention: SAM vs CMDB** (3 duplicate types, mechanisms, resolutions) | REF §13 | Cross-module duplicate clarity | P1 |
| 20 | **Remediation Actions by Exception Type** (6 exceptions with action + owner) | REF §14 | Operational ownership | P1 |
| 21 | **Reclamation Workflow with Grace Period** (60-90 days, owner sign-off) | REF §14.1 | Safe reclamation practice | P1 |
| 22 | **SAM Health Dashboard** (ITAM Health Check from Store) | REF §15.1 | Health assessment tool | P2 |
| 23 | **Key Dashboards/Indicators** (7 dashboards with healthy targets) | REF §15.2 | Dashboard inventory | P1 |
| 24 | **SAM Readiness Scorecard** (10 checks, 3 hard gates, probe-based) | REF §15.3 | Pre-deployment validation | P1 |
| 24 | **Anti-Patterns** (14 patterns with consequence + fix) | REF §16 | Failure mode library | P1 |
| 25 | **Open Questions (10 UNVERIFIED)** | REF §17 | Intellectual honesty; research gaps | P2 |
| 26 | **Source Ledger** (32 sources with type, release label, URL) | REF §18 | Citation discipline | P2 |
| 27 | **OOTB Automation Inventory** (9 automations: BRs, scheduled jobs, tables, triggers, purpose) | TSOM Enh #2 | "What ships active" verification | P1 |
| 28 | **Pattern Normalization Precedence** (6-level inferred order, operational rule, UNVERIFIED flag) | TSOM Enh #3 | Configuration conflict prevention | P1 |
| 29 | **Scheduled Job Dependency Chain** (Mermaid: 5 daily sequential → 1 weekly, debugging rule) | TSOM Enh #4 | Debugging accelerator | P1 |
| 30 | **Foundation vs Professional Feature Matrix** (11 features × 3 editions × release labels) | TSOM Enh #5 | Edition clarity | P1 |
| 31 | **Normalization Coverage KPI Gate** (Formula, probe check, remediation workflow) | TSOM Enh #6 | Hard gate enforcement | P1 |
| 32 | **Reconciliation Exception Taxonomy** (5 exceptions: meaning, financial impact, cause, owner, NEVER DO) | TSOM Enh #7 | Audit defence | P1 |
| 33 | **SAM_IMPLEMENTATION_CHECKLIST** (9 gates) | CROSS_REF §5 | Implementation gate document | P1 |
| 34 | **Source-System Contract Templates** | CROSS_REF §7 | Data feed governance | P2 |
| 35 | **Concrete Reconciliation Test Cases** | CROSS_REF §7 | Validation examples | P1 |
| 36 | **Data Ownership/RACI Matrix** | CROSS_REF §7 | Governance | P2 |
| 37 | **Change Control Process for Model/Metric/Rule Changes** | CROSS_REF §7 | Compliance integrity | P2 |
| 38 | **Audit Evidence Linkage Specification** | CROSS_REF §7 | Audit trail | P2 |
| 39 | **Phased Rollout Plan with Go/No-Go Gates** | CROSS_REF §7 | Deployment strategy | P2 |
| 40 | **Cutover/Hypercare/Ongoing Ops** | CROSS_REF §7 | Lifecycle operations | P2 |
| 41 | **SaaS Custom Integration Boundary Doc** | CROSS_REF §7 | Integration limits | P2 |
| 42 | **PPN/Content Library Entitlement Import Approach** | CROSS_REF §7 | Entitlement automation | P2 |

---

## PART C: Overlap (Covered in Both)

| Topic | Webpage Treatment | Research Treatment |
|-------|-------------------|-------------------|
| SAM vs HAM vs ITAM | Comparison table (6 aspects) | Mental model table (5 layers) — deeper |
| Three Record Types | 6-row table with "verify in release" | 4-layer table (IRE, HAM, Normalisation, Metric, Recon) — more layers |
| Normalization | 5-step workflow, Content Library mention | 4 rule types, 6 statuses, KPI gate, precedence — deeper |
| Entitlements | 11 attributes table, 4 hygiene rules | 7 critical fields (verdict), 4 hygiene rules — similar |
| Reconciliation | 7 steps, symptom table, 4 diagrams | 3 output tiers, Oracle, 8 properties, exception types — deeper |
| Compliance Positions | 6 positions table | 5 exception types table — similar |
| Discovery Sources | 6 source types table | 11 sources with config paths — deeper |
| SaaS vs On-Prem | 5-row comparison table | Connectors table + metrics — deeper |
| Optimization | 6 priority items | Remediation workflow — similar |
| Publisher Traps | 6 publishers table | 5 publishers in pitfalls + Oracle specifics — similar |
| Out-of-Box Features | 11 features table | Plugin table + scheduled jobs — different angle |
| Table Hierarchy | ASCII tree (6 tables) | 15-row table with purpose/notes — deeper |
| Integrations | 14-row table | Connector detail — similar |
| Key Fields | Essential (10) + Forgotten (5) | Critical fields (7) + pitfalls — different angle |
| Goals/Metrics | 8 goals with targets | 7 dashboards with targets — similar |
| Common Mistakes | 12 mistakes table | 14 anti-patterns — similar |

---

## PART D: Recommended Actions

### For Learning Protocol (ServiceNow_Learning repo) — Add from Webpage
1. **Standardize module guide template** with: Exam Alignment, Lifecycle Diagram, Three Record Types, Normalization Workflow, Reconciliation Diagrams, Compliance Positions, Discovery Sources, SaaS Comparison, Optimization Priority, Reclamation Workflow, Publisher Traps, Code Snippets, Out-of-Box Features, Table Hierarchy, Integrations, Key Fields, Goals/Metrics, Common Mistakes, Lab Exercise, SLAs/Dashboards, Quiz, Learning Resources, Memory Aids, Related Guides
2. **Adopt conventions**: "Verify in your release" disclaimers, "Exam focus" callouts, "ELI5" explanations, "Tip/Note" boxes, hidden-answer quizzes
3. **Create cross-cutting memory aids** (BAA, LOCS, IRE, ARM, etc.) as shared assets

### For SAM Guide Page (ServiceNow_Learning_TSOM repo) — Add from Research
**P1 (High Impact, Low Effort):**
1. Add **Evidence Policy + Release Scope** section at top
2. Add **Three Hard Gates** prerequisite section before "Where to Find It"
3. Add **Five Identification Layers** callout in "SAM vs HAM vs ITAM" or new Architecture section
4. Add **Complete Plugin Activation Table** in "Where to Find It" or new Prerequisites section
5. Add **Roles with Capabilities + ACLs** table
6. Add **Guided Setup/Configuration Console entry points** with required roles
7. Add **Discovery/Connector Feeds** detail (Legacy vs Modern vs SaaS)
8. Add **Normalization Engine Deep Dive** (rule types, statuses, KPI gate, pattern rule form)
9. Add **Entitlement Critical Fields + Hygiene Rules** (expand existing)
10. Add **License Metrics: Complete Publisher Groups** (expand existing table)
11. Add **License Metric Pitfalls Table** (new)
12. Add **Reconciliation Detail** (output tiers, Oracle, system properties)
13. Add **Three-Layer Insert-vs-Update Decision Table** (new section — core differentiator)
14. Add **Software Install Recognition Flow** (ASCII flow)
15. Add **Duplicate Installation Handling** (no duplicate_of, REST remediation)
16. Add **Entitlement Consumption Logic per Metric** (9 metrics with formulas)
17. Add **Duplicate Prevention: SAM vs CMDB** (3 duplicate types table)
18. Add **Remediation Actions by Exception Type** (with owners)
19. Add **SAM Readiness Scorecard** (10 checks, 3 hard gates)
20. Add **Anti-Patterns** (14, expand existing 12)
21. Add **OOTB Automation Inventory** (9 automations table)
22. Add **Pattern Normalization Precedence** (inferred order + UNVERIFIED flag)
23. Add **Scheduled Job Dependency Chain** (Mermaid + debugging rule)
24. Add **Foundation vs Professional Feature Matrix** (11 features × 3 editions)
25. Add **Normalization Coverage KPI Gate** (formula + remediation workflow)
26. Add **Reconciliation Exception Taxonomy** (NEVER DO column)
27. Add **SAM_IMPLEMENTATION_CHECKLIST** (9 gates)

**P2 (Medium Impact):**
28. Add **Open Questions (10 UNVERIFIED)** as "Known Gaps" section
29. Add **Source Ledger** (32 sources) as appendix
30. Add **Custom License Metrics** detail
31. Add **Source-System Contract Templates** concept
32. Add **Concrete Reconciliation Test Cases** concept
33. Add **Data Ownership/RACI Matrix** concept
34. Add **Change Control Process** concept
35. Add **Audit Evidence Linkage** concept
36. Add **Phased Rollout Plan** concept
37. Add **Cutover/Hypercare/Ops** concept
38. Add **SaaS Custom Integration Boundary** concept
39. Add **PPN/Content Library Import** concept

---

## Summary Statistics

| Direction | Items Identified | P1 Items | P2 Items |
|-----------|-----------------|----------|----------|
| Webpage → Learning Protocol | 29 | N/A (template work) | N/A |
| Research → SAM Guide Page | 42 | 27 | 15 |

**Net insight:** The webpage guide excels at **learning/pedagogical patterns** (diagrams, quizzes, mnemonics, exam alignment, labs). The research excels at **operational/implementation depth** (evidence, configuration detail, decision tables, dependency chains, governance). The ideal module guide combines both.

---

*Generated 2026-11-13 by systematic bidirectional comparison*