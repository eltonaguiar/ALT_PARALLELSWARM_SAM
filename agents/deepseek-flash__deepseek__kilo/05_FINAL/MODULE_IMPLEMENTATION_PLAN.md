# MODULE IMPLEMENTATION PLAN — ServiceNow module (generic) with SAM instantiation

**Agent:** `deepseek-flash__deepseek__kilo` · **Model:** `deepseek/deepseek-flash` · **Provider:** DeepSeek · **Harness:** Kilo CLI
**Date:** 2026-11-13
**Purpose:** the programme-level counterpart to `SAM_MODULE_REFERENCE.md`. That file answers *how to configure SAM*; this file answers *how the organisation will operate, govern, trust, and improve it*. Use it for any ServiceNow module; the SAM column is the worked example.

**Relationship to the rest of the repo**

| Artefact | Answers |
|---|---|
| `SAM_MODULE_REFERENCE.md` | tables, fields, statuses, jobs, properties, insert/update |
| `ROUND2_GAP_ANALYSIS.md` | critique verification, races, missing operational controls |
| **this file** | business case → scope → ownership → data → integration → security → release → test → cutover → adoption → hypercare |
| `SAM_IMPLEMENTATION_CHECKLIST.md` | the go/no-go gates extracted from this file |

Marks: **V** = ServiceNow-documented; **P** = programme practice (not a product SLO); **U** = verify on instance.

---

## 1. Business case, outcomes, and KPIs

### 1.1 What to define

- The decisions the module must improve (not the screens it will have).
- Current-state baseline, target state, and the measurement window.
- Financial benefit, risk benefit, cost, effort, and executive sponsor.
- A value-realisation review cadence after go-live.
- **Explicit definitions** for every headline term, so reports cannot be argued about.

### 1.2 SAM instantiation

| Element | Definition to agree | Evidence source |
|---|---|---|
| **Compliant** | Software model status = `Compliant` (green) on the License Position; rights owned ≥ rights used **V** | License Position / `samp_license_metric_result` |
| **Under-licensed** | `Unlicensed installs` > 0 or rights available < 0; status `Not Compliant` **V** | LMR |
| **Over-licensed** | `Over-licensed amount` > 0; rights owned > used **V** | LMR / Product Result |
| **Reclaimable** | Removal candidate with justification, active, state ready **V** | `samp_sw_reclamation_candidate` |
| **Normalisation coverage** | % installs whose discovery model is `Normalized` or `Manually Normalized` | `cmdb_sam_sw_discovery_model` |
| **Reconciliation accuracy** | Controlled test scenarios (§12) reproduce expected rights algebra | test evidence |
| **True-up exposure** | Sum of true-up cost for Not Compliant models, selected publishers **V** | Product Results |
| **Audit findings** | Open findings attributable to SAM data | audit log |
| **Renewal savings** | Avoided spend from reclamation/downgrade/consolidation | reclamation + contracts |
| **Software spend** | Total cost of non-retired entitlements **V** | `samp_license_metric_result` |

**Baseline before go-live (P):** discovery-model count by status; installs vs unique products vs models; unlicensed product-result count; % CIs with owner/location; published-product count if phase-wise; time of last successful reconciliation. Without a baseline, the Success portal has nothing to compare against.

**Value cadence (P):** monthly for the first quarter (data quality + compliance), quarterly thereafter (savings, renewals, audit posture).

### 1.3 Common failure

Configuring every publisher because the licence allows it, without agreeing which decisions (true-up? audit? renewal? reclamation?) the programme exists to improve.

---

## 2. Scope, assumptions, constraints, exclusions

### 2.1 What to define

In-scope **processes, publishers, data domains, regions, business units, environments, integrations**; out-of-scope items as a written list; assumptions and constraints (licence tier, headcount, source availability).

### 2.2 SAM instantiation

| Axis | Example in-scope | Example out-of-scope (write it down) |
|---|---|---|
| Publishers | Microsoft, Oracle, IBM, SAP, Adobe, VMware | Niche engineering tools with no entitlement data |
| Process | Request → procure → entitlement → discover → normalise → reconcile → remediate → renew | Software packaging/deployment engineering |
| Data | `cmdb_sam_sw_install`, `cmdb_sam_sw_discovery_model`, `cmdb_software_product_model`, `alm_license`, `samp_sw_usage` | Non-software hardware asset lifecycle (HAM) |
| Regions | Named countries/domains | Entities with no contract visibility |
| Environments | Production + pre-prod | Lab devices excluded via the exclude flag |
| Integrations | Discovery, SCCM/SGC, procurement, contracts, SaaS | Unapproved third-party scanners |
| Editions | Pro (`com.sn_samp_master_ws`) | Foundation `com.snc.sams` pilot instances |

**Phase-wise scope (V):** `com.snc.samp.manage.published.products` + Published products list freezes reporting to the MVP set; re-run reconciliation after every change **V**. Suite publish warns to include parent and children **V**.

### 2.3 Common failure

"All software" as one undifferentiated scope. Start with the few publishers that hold most spend (typically Microsoft, Oracle, IBM, SAP, Adobe, VMware — **P**), and with end-user computing or simple SaaS (Crawl, **V**).

---

## 3. Stakeholders, RACI, and governance

### 3.1 What to define

Process owner, data owner, technical owner, product owner, escalation path, steering cadence, decision rights, and the separation between the person who can normalise and the person who can change models/metrics.

### 3.2 SAM instantiation

Use the RACI in `ROUND2_GAP_ANALYSIS.md` §4.3. Minimum roles:

| Role | Accountability |
|---|---|
| Executive sponsor | Budget, scope, escalation |
| SAM programme lead / product owner | Outcomes, roadmap, published-product scope |
| SAM manager | Entitlements, models, reconciliation sign-off |
| SAM admin | Configuration, imports, normalisation |
| SAM analyst (`sam_user`) | Review, manual normalise, removal candidates |
| CMDB owner | CI coverage and quality |
| Discovery admin | Schedules, credentials, source health |
| Procurement | POs, supplier data |
| Contract manager | `ast_contract`, renewals |
| Finance | Cost, true-up, savings validation |
| Audit / risk | Evidence, controls |
| Publisher owners | Confirm metric/contract interpretation |

**Governance forums (P):** weekly data-quality stand-up (normalisation, failed jobs, dedup); monthly compliance review (position + remediation); quarterly value review (savings, renewals, audit); annual publisher strategy.

**Decision rights:** metric changes, model changes, normalisation rule changes, dedup rules, published-product scope, and exclusion flags are **change-controlled** (§10/§15).

### 3.3 Common failure

No accountable owner after go-live. The module becomes a reporting museum.

---

## 4. Current-state assessment and gap analysis

### 4.1 What to define

Inventory of existing sources, data quality, contracts, entitlements, skills, and process maturity; quantified gaps; remediation backlog with owners.

### 4.2 SAM instantiation

| Assessment | Evidence |
|---|---|
| Discovery coverage | % CIs with installs; % installs with `installed_on` |
| Normalisation quality | status distribution; top `Match Not Found` publishers |
| Entitlement completeness | % with PPN/model, metric, rights, dates |
| Contract coverage | contracts linked to entitlements (`ast_contract`) |
| Reconciliation history | any prior results; failed jobs |
| Dedup state | active installs per device/product/edition |
| Roles | who holds `sam_admin`, `sam_user`, `sam_developer` |
| Maturity | Crawl / Walk / Run self-assessment **V** |

### 4.3 Common failure

Treating a green plugin as a current-state assessment.

---

## 5. Target process design (end to end)

Document the process **before** tables and flows.

```
Request ─► Approval ─► Procurement / PO ─► Contract capture
   ─► Entitlement (alm_license) + allocation
   ─► Deployment ─► Discovery / SGC / SaaS ingest ─► cmdb_sam_sw_install
   ─► Normalisation (discovery model status)
   ─► Model matching (software model)
   ─► Reconciliation (three tiers)
   ─► Compliance review ─► Remediate (buy / remove / allocate / reclaim)
   ─► Renewal / true-up / retirement ─► Audit support
```

| Stage | Owner | System object | Exit criterion |
|---|---|---|---|
| Request/approval | Service owner | `sc_request` / `sc_req_item` | approved, assigned |
| Procurement | Procurement | PO, receipt | PO line has PPN/qty/price |
| Contract | Contract manager | `ast_contract` | term, vendor, rights |
| Entitlement | SAM manager | `alm_license` | Published/In use, metric, rights |
| Deployment | Endpoint/app team | CI | software installed |
| Discovery | Discovery admin | `cmdb_sam_sw_install` | install linked to CI |
| Normalisation | SAM analyst | `cmdb_sam_sw_discovery_model` | Normalized/Manually |
| Matching | SAM admin | model reference | `software_model` set |
| Reconciliation | SAM manager | results | explainable position |
| Remediation | Service owner | allocations/removal candidates | action closed |
| Renewal | Contract + SAM | `alm_license`, `ast_contract` | renewal decision recorded |
| Audit | Audit | evidence chain | sample passes |

**Common failure:** treating SAM as reporting and never designing upstream procurement/contract or downstream remediation. The position is only actionable if both ends exist.

---

## 6. Data model, reference data, and data-quality rules

### 6.1 What to define

A data dictionary and entity-relationship view, mandatory fields, reference-data standards, ownership, quality thresholds, retention, and archival.

### 6.2 SAM instantiation

Entity chain: `core_company`/`samp_sw_publisher` → `cmdb_software_product_model` → `cmdb_sam_sw_discovery_model` → `cmdb_sam_sw_install` → `alm_license` / `alm_entitlement_user|asset` → `samp_license_metric_result`. See `SAM_MODULE_REFERENCE.md` §2 and `ROUND2_GAP_ANALYSIS.md` §4.1.

**Reference-data standards (P):**

- Publisher: canonical `samp_sw_publisher`, linked to `core_company`; no free-text variants.
- Product: Content Library name where it exists; custom product only when it does not.
- Version: normalised major.minor; exact-match-first, then major (V).
- Edition: canonical edition; `Edition Override` only where discovery missed it.
- Language/platform: controlled values (Windows/macOS/UNIX; six documented languages V).
- Product type: Licensable / Not Licensable / Child / Driver / Patch / Unknown (V).
- Entitlement: metric matches contract counting basis (§4.11 of Round 2).
- Suite: parent/child explicit; `auto_suite_inference` decided, not defaulted.

**Mandatory-field rules:** discovery model needs publisher+product+version to be `Normalized`; a licensable model needs `License under management` and a metric; an entitlement needs rights, metric, dates, and model/PPN.

**Retention/archival (P):** installs are not auto-deleted; define a stale threshold and deletion evidence (Table API delete), retain reconciliation history, retain import files and job logs for audit, archive retired entitlements rather than deleting.

### 6.3 Common failure

A list of tables instead of standards. "Publisher = Microsoft" must be enforceable, not aspirational.

---

## 7. Integration architecture and source-system inventory

### 7.1 What to design

Inbound/outbound flows, APIs, middleware, credentials, frequency, latency, error handling, retries, idempotency, reconciliation of counts, and a written feed contract.

### 7.2 SAM instantiation

Use the source-system contract table in `ROUND2_GAP_ANALYSIS.md` §4.4. Architecture rules:

1. CMDB writes go through IRE; do not bypass with direct inserts (Discovery, SGC, imports) **V/C**.
2. Software installs from third parties: `com.snc.samp.ire.datasource.integration`, `sam_developer`, payload keys publisher/version/display_name, parent CI by name, `sys_class_name` present **C**.
3. Uninstall is not propagated by SAM; the source must send an absence signal or the programme must run a controlled delete **V**.
4. Every feed has a **count reconciliation**: source count vs accepted count vs rejected count, with an alert threshold.
5. Credentials are vaulted/rotated; integration users are not `admin`.
6. Retries are idempotent: dedup key = source + publisher + product + version + edition + CI.
7. Error queues are owned: `samp_entitlement_import`, `samp_bulk_import`, `samp_job_log`, SGC/Discovery logs.

### 7.3 Common failure

Integrations listed but not designed: no retry, no rejection queue, no count check, no owner. The position drifts silently.

---

## 8. Security, roles, and compliance design

### 8.1 What to define

Role/group matrix, least privilege, ACLs on sensitive fields, delegated administration, approval boundaries, audit logging, PII handling, credential vaulting, vendor-risk/data-residency.

### 8.2 SAM instantiation

- **Commercial sensitivity:** `alm_license` costs, PPNs, contract terms, and true-up figures are commercially sensitive; restrict read to SAM/finance/audit.
- **Workforce sensitivity:** `alm_entitlement_user` and `samp_sw_usage` reveal who uses what; apply least privilege and privacy review.
- **Role separation:** `sam_admin` ≠ `sam_developer` in production; `sam_user` who normalises should not also approve model/metric changes.
- **ACLs:** audit `sys_security_acl` on `alm_license`, `cmdb_software_product_model`, `cmdb_sam_sw_discovery_model`, `samp_license_metric_result` (`U` — not documented; verify).
- **Delegation:** domain-separated admins get domain-scoped properties, not global.
- **Audit logging:** retain job logs, import results, change records, and reconciliation snapshots.
- **Integration credentials:** vaulted, rotated, least privilege (`sam_developer` only where required).

### 8.3 Common failure

Security added late; broad `sam_admin` for convenience; commercial data readable by all `itil` users.

---

## 9. Configuration versus customization and upgrade strategy

### 9.1 Four categories

| Category | Examples | Upgrade posture |
|---|---|---|
| OOTB configuration | Roles, properties, published list, dedup rules, pattern rules, custom products, custom metrics, custom PPNs | Safe; supported |
| Low-code configuration | Flow Designer for reclaim/request, UI Builder, Virtual Agent, portal | Supported; test on upgrade |
| Customization | Overlaying SAM jobs/BRs, custom script includes, custom tables, custom integrations | Risky; requires regression and may break |
| Vendor-managed content | Content Library, normalisation rules, discovery maps, publisher packs | Do not modify; opt in/out, deactivate versions |

### 9.2 SAM instantiation

- **Extension points (use these):** custom products, pattern normalisation rules, custom license metrics, custom PPNs, custom dedup rules, reclamation rules, published-product list, custom license exception rules **V**.
- **Never overlay:** normalisation job, discovery-model matching job, dedup job, install→discovery-model business rule.
- **Known upgrade break:** reconciliation script includes moved to `com.sn_itam_samp` from Yokohama; migrate customisations **V**.
- **Content:** deactivating a content version is allowed; editing content is not.
- **Revert Customizations** module after install/upgrade **V**.

### 9.3 Common failure

Customising a job to "fix" a data problem; the fix disappears or breaks at the next release.

---

## 10. Environments, source control, and release management

### 10.1 What to define

Dev/test/UAT/prod; instance strategy; update-set/change-set standards; automated or controlled promotion; configuration backup; rollback; release calendar; approval gates; production-readiness criteria.

### 10.2 SAM instantiation

- **Promotion:** properties, custom products, pattern rules, dedup rules, published list, and report definitions move as update sets; **data does not** — re-create or import in each environment.
- **Pre-release export:** `cmdb_software_product_model`, `alm_license`, `cmdb_sam_sw_discovery_model` (sample), `sam_sw_dedup_rule`, pattern rules, published list.
- **Rollback:** compliance-affecting changes need a before/after reconciliation snapshot and a documented reversal; normalisation revert limits apply (§4.7 Round 2).
- **Calendar:** freeze around true-up/audit periods; no compliance-affecting change without a re-run.
- **PRC:** jobs healthy, data gates met (§4.6 Round 2), test scenarios pass, owners sign off.

### 10.3 Common failure

No controlled path from dev to prod; a property change lands during an audit.

---

## 11. Test strategy, UAT, and acceptance criteria

### 11.1 Test types

| Type | Purpose | SAM example | Exit |
|---|---|---|---|
| Data validation | Source data complete/accurate | Entitlement quantity/metric match contract | 100% sampled |
| Integration | Interfaces and error paths | Discovery install lands; failed feed alerts; retry idempotent | All paths exercised |
| Workflow | Approvals/assignments | Reclaim request routes to owner | Approver correct |
| Reconciliation | Business logic | T1–T10 in Round 2 §4.5 | Expected numbers |
| Role/security | Least privilege | Read-only user cannot edit entitlement | No bypass |
| Performance | Scale | Large install volume does not stall reconciliation | Within agreed window |
| UAT | Real scenarios | Procurement/asset/finance sign off | Sign-off |
| Regression | Protect existing | CMDB/Discovery change does not break SAM | No delta |

### 11.2 Acceptance criteria

Use `ROUND2_GAP_ANALYSIS.md` §4.6 (data-quality gates) plus the numeric test cases T1–T10. "Reconciliation ran" is not acceptance; "T1 returned 2 unlicensed installs and the expected true-up" is.

### 11.3 Common failure

Testing configuration screens rather than end-to-end business outcomes.

---

## 12. Data migration and cutover

### 12.1 Runbook

1. Extract: entitlements, contracts, POs, software models, PPNs, existing installs, users/devices.
2. Cleanse: canonical publisher/product/version/edition; dedupe; reconcile quantities to contracts.
3. Transform: map to `alm_license`, `cmdb_software_product_model`, `cmdb_sam_sw_discovery_model`/`cmdb_sam_sw_install` as appropriate.
4. Validate: counts, financial totals, sample reconciliation.
5. Sequence: contracts → entitlements → models → discovery → normalisation → reconciliation.
6. Freeze window: no source changes during cutover; record the freeze.
7. Parallel/shadow run: reconcile migrated data against the legacy calculation; explain deltas.
8. Go/no-go: gates met; owners sign.
9. Hypercare: daily triage for 2–4 weeks.
10. **Definition of "migration complete":** validated entitlements, normalised inventory, successful reconciliation, accepted key reports — **not** "records imported".

### 12.2 SAM-specific

- Basic SAM → Pro is irreversible; migrate `cmdb_ci_spkg` → `cmdb_sam_sw_install` **C**.
- Do not write to `cmdb_ci_spkg` after migration.
- Re-run matching and reconciliation after import.
- Keep the legacy calculation as the parallel-run baseline.

### 12.3 Common failure

Declaring migration complete when the import succeeded.

---

## 13. Training, communications, and adoption

### 13.1 What to define

Stakeholder map, role-based training, quick-reference guides, comms plan, go-live announcement, executive dashboards, recurring governance, support model, known-issue log, feedback loop.

### 13.2 SAM instantiation

| Audience | Training |
|---|---|
| SAM admin | Entitlements, imports, normalisation, reconciliation, properties, change control |
| SAM analyst | Review, manual normalise, removal candidates, reports |
| Procurement | PPN, PO/receipt, MLS, contract linkage |
| Contract manager | `ast_contract`, renewals, maintenance/SA linkage |
| Service owners | Reclamation decisions, request process |
| Finance | True-up, savings validation, spend |
| Executives | Success portal, position, risk |
| End users | Request software, reclamation etiquette |

**Adoption signals (P):** named owners use the dashboards; remediation actions close; normalisation backlog falls; true-up decisions are made from the position, not a spreadsheet.

### 13.3 Common failure

Access granted, process not adopted; the spreadsheet survives.

---

## 14. Hypercare, support model, and continuous improvement

- **Hypercare (P):** 2–4 weeks daily triage of failed jobs, import errors, normalisation spikes, position deltas; named on-call; issue log.
- **Steady state:** weekly data-quality, monthly compliance, quarterly value, annual publisher strategy.
- **Support model:** L1 service desk (access/how-to), L2 SAM admin (data/config), L3 platform/Discovery (integration/IRE), vendor (content/pack defects).
- **Continuous improvement:** normalisation hit-rate, dedup rate, reclamation conversion, reconciliation runtime, audit findings.
- **Known-issue log:** recurring `Match Not Found` publishers, flaky feeds, ambiguous contracts.

---

## 15. Risks, issues, decisions, dependencies

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Entitlement data incomplete | High | Position wrong | Gate: ≥98% completeness before production |
| Normalisation backlog | High | Unlicensed false positives | Content opt-in, pattern rules, owner |
| Duplicate feeds | Medium | Inflated rights used | Feed contracts + dedup rules |
| Wrong metric | Medium | Methodology error | Publisher metric matrix + owner sign-off |
| Over-customisation | Medium | Upgrade break | Extension points only |
| No owner | High | Programme stalls | RACI + governance |
| SaaS not integrated | Medium | Under-reported consumption | Scope decision + connector plan |
| Containers out of scope | High | Blind spot | Explicit exclusion + alternative method |
| Commercial data exposure | Medium | Legal/HR risk | ACLs + least privilege |
| Audit evidence missing | Medium | Findings | Evidence chain + retention |

**Decision log:** record every scope, metric, model, and integration decision with date/owner/rationale. **Dependency log:** plugins, packs, connectors, content sync, procurement, contracts, SaaS, domain separation.

---

## 16. SAM production-readiness gates (summary)

Full checklist in `SAM_IMPLEMENTATION_CHECKLIST.md`. Minimum:

1. Plugin/subscription/roles verified; environment promoted correctly.
2. Inventory source producing installs linked to CIs; error paths owned.
3. Entitlements complete for pilot publishers; metric approved by owner.
4. Software models approved; `License under management` set; suites/downgrades modelled.
5. Normalisation coverage gate met; exception workflow staffed.
6. Reconciliation reproduces T1–T10 expected results.
7. Reports/dashboards used by named owners; remediation workflow exercised.
8. SaaS subscriptions (if in scope) include consumption + renewal.
9. Data-quality and reconciliation KPIs monitored post-go-live.
10. Rollback, change control, and audit evidence in place.

---

## 17. How this maps to ServiceNow's own guidance

| ServiceNow guidance | Where used here |
|---|---|
| Crawl / Walk / Run maturity **V** | §2 scope, §4 assessment, §16 gates |
| Healthy CMDB first **V** | §4, §6, prerequisites |
| Entitlements before discovery/reconciliation **V** | §5 process, §12 cutover |
| Content Library/PPN for model creation **V** | §6 standards, §9 content |
| Content Service opt-in **V** | §6, §9 |
| Published products for phase-wise rollout **V** | §2 scope |
| Success portal / health check / maturity items **V** | §1 KPI, §14 improvement |
| Weekly reconciliation default **V** | §14 cadence |

Everything marked **P** is programme practice, not a ServiceNow product guarantee; adapt thresholds to the estate.
