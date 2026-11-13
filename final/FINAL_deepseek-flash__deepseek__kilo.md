# FINAL — ServiceNow SAM (Brazil) — merged fleet compilation

**Compiled by:** `deepseek-flash__deepseek__kilo` · **Model:** `deepseek/deepseek-flash` · **Provider:** DeepSeek · **Harness:** Kilo CLI
**Date:** 2026-11-13
**Release pin:** ServiceNow docs **Brazil** (ITAM map `PMOYmdGTPDs40EbYh10h4g`), pages *Updated Sep 10 2026* unless noted. Australia-family corroboration marked **C**.

> This file merges the SAM work in this repo — `grok-4.6__xai__kilo` WT1/WT2/WT3, `beam__kilo__cli` WT1, and this pass (`SAM_MODULE_REFERENCE.md`, `ROUND2_GAP_ANALYSIS.md`, `MODULE_IMPLEMENTATION_PLAN.md`, `SAM_IMPLEMENTATION_CHECKLIST.md`). Deep detail stays in those files; this is the single readable compilation.

**Confidence:** **V** printed on a Brazil page · **C** Australia/corroborated · **U** label-only, verify on instance.

---

## 0. Agents merged and conflicts

| Source | Model / provider | Contribution | Conflicts kept explicit |
|---|---|---|---|
| `beam__kilo__cli` WT1 | beam / Kilo | Table contract, Discovery→SAM business rule, CI related-list, migration, Oracle summary | Says normalisation statuses are five; Brazil lists six (adds `New`) |
| `grok-4.6__xai__kilo` WT1 | grok-4.6 / xAI | Brazil-pinned reference: 42 sources, properties, four record paths, dedup, reclamation, implementation success | Reconciliation "weekly" (docs) vs curriculum "nightly" |
| `grok-4.6__xai__kilo` WT2 | grok-4.6 / xAI | Curriculum compare vs CIS-SAM learning guide | `cmdb_sam_sw_usage` vs `samp_sw_usage`; `sam_sw_reconciliation_result` unverified |
| `grok-4.6__xai__kilo` WT3 | grok-4.6 / xAI | CIS-SAM quiz → section map, names curriculum got wrong | SUMN jargon; `alm_software` wrong |
| this pass | deepseek-flash / DeepSeek | Deep module reference, six-status matrix, model-vs-vendor, reporting→table map, integrations, full properties, round-2 gap + programme plan + checklist | — |

**Ambiguity:** the repo index lists agents that have no folder (`deepseek-v4-flash__deepseek__hermes`, etc.). They are not merged; only folders with content are sources.

---

## 1. Mental model — five record types

```
Discovery / SCCM-SGC / FBD / SaaS / ILMT / 3rd-party IRE
        ▼
cmdb_sam_sw_install            one copy of software on one CI
        ▼  BR: Publisher + Display name + Version
cmdb_sam_sw_discovery_model    deduped discovered string; cannot be created manually
        ▼  normalise + match
cmdb_software_product_model    what you purchased/manage
        ▼  entitlements + allocations
alm_license                    rights you own
        ▼  weekly/on-demand recon
samp_product_result → Software Model Result → samp_license_metric_result
```

Non-negotiables:

1. Discovery model ≠ software model ≠ catalog item ≠ entitlement.
2. Only `Licensable` product types reconcile; `License under management` must be set (**C**).
3. Normalisation is the gate; `Match Not Found` is not compliant, it is unknown.
4. SAM does not delete uninstalled software; a retired/stolen CI **does** delete related installs **V**.
5. Reconciliation is **weekly default + on demand** **V**, not nightly.

---

## 2. Setup order (implementation)

1. Healthy CMDB + Discovery coverage.
2. Install SAM (Product Hub first time / Store otherwise).
3. Activate `com.sn_samp_master_ws` (Pro + Workspace). Foundation is `com.snc.sams` (C).
4. Publisher packs only if contracted (Adobe, Citrix, IBM, Microsoft, Oracle, SAP, VMware, Engineering).
5. Content Service opt-in decision (default off).
6. Wire sources (Discovery, SCCM/SGC, FBD, ILMT, SaaS, third-party IRE).
7. Record opt-in/opt-out decisions (Content Service, SaaS LM, Spend Detection) in a decision log.
8. Load entitlements (`alm_license`) **before** reconciliation (docs sequence).
9. Daily normalisation; custom products/pattern rules for misses.
10. First on-demand reconciliation; validate; then scheduled.
11. Enable `com.snc.samp.manage.published.products` and publish a small product set (phase-wise).
12. Reclamation rules → candidates → catalog reclaim.
13. Publish requestable software (catalog).
14. Success portal goals + health check + maturity items.

---

## 3. Tables and fields (compact contract)

| Record | Table | Key fields |
|---|---|---|
| Installation | `cmdb_sam_sw_install` | `display_name`, `discovery_model`, `publisher`, `version`, Edition Override, `installed_on`, `install_location`, `install_date`, `instance_key`, `uninstall_string`, `iso_serial_number`, `active`, `inferred_suite`, `omit_from_suites` |
| Discovery model | `cmdb_sam_sw_discovery_model` | **Normalization status**, Publisher/Product/Version (normalised), Discovered publisher/product/version, Product type, Platform, Language, Edition, Full version, `software_model`, `Automatically matched`, Normalization date, Approved |
| Software model | `cmdb_software_product_model` | publisher, product, version(+condition), edition(+condition), platform, language, install condition, discovery map, suite parent/component, metric attributes/metric group, `created_source`, licence costs, `License under management` |
| Entitlement | `alm_license` | PPN, license type, license metric, rights, start/end, license duration, state (Build/Published/In use), company, cost, licence/+maintenance cost, metric group, subscription period, agreement type, upgraded entitlements |
| Allocations | `alm_entitlement_user` / `alm_entitlement_asset` | user or device, quantity/cores |
| Results | `samp_product_result` → Software Model Result (`U:samp_sw_model_result`) → `samp_license_metric_result` | rights owned/used/available, allocation buckets, unlicensed installs, true-up, over-licensed, savings |
| Usage | `samp_sw_usage` | Publisher, Product, Reclamation type, CI, User, Month/Year, Usage count, Total seconds, Last used |
| Reclamation | `samp_sw_reclamation_candidate` | justification, state, active, savings |
| Dedup | `sam_sw_dedup_rule` | product, active, version level, stale threshold |
| Suggestions | `samp_normalization_suggestion` (also `…suggestions` in one page) | discovered/suggested/normalised values, status |
| Lifetimes | `sam_sw_product_lifecycle`, `sam_custom_sw_product_lifecycle` | EOS/EOES/EOL |
| Content | `samp_sw_product`, `samp_sw_publisher`, `samp_sw_product_definition` | product/publisher/PPN |

Full field-level detail with `U` markers: `SAM_MODULE_REFERENCE.md` §2.

---

## 4. Out-of-box scripts

| Object | Target | Customise? | Risk |
|---|---|---|---|
| `SAM - Normalize discovery models using content library rules` (daily) | discovery model normalised fields + status | **Leave** | Overlay drifts status semantics |
| `SAM - Discovery Model Normalization job` (daily) | dashboard aggregates | Leave | Dashboard lies |
| `SAM – Discovery Model to Software Model matching` | `software_model`, `Automatically matched` | Leave | Manual choices overwritten |
| `SAM - Deduplicate Install Table` | `cmdb_sam_sw_install.active` | Leave; tune rule | Two active installs inflate rights |
| `SAM — Adjust Installs for excluded CIs` | installs on flagged CIs | Leave | Excluded devices leak |
| `SAM - Daily Job` | dashboard | Leave | Stale widgets |
| `SAM - Trigger Full Scan` (weekly) | Health Check KPIs | Leave; add KPIs | Custom KPI collision |
| `SAM - Label Spend Transactions` | spend labels | Leave | Mislabeled spend |
| `SAM- Create downgrades/upgrades…` (weekly) | downgrade tables | Leave | Missing rights |
| `SAM - Central Data Service Download Status` | CDS counts | Leave | Blind content failure |
| Weekly reconciliation jobs | results | Configure via properties | Script includes moved to `com.sn_itam_samp` (Yokohama) |
| Install→discovery-model BR (`U`) | discovery model | **Never** | Duplicate/flooded models |
| Product-type edit→status BR (`U`) | status | Never | Wrong recon eligibility |
| CI retired/stolen→install delete (`U`) | installs | Never | Position jumps without business event |

**Extension points:** custom products, pattern normalisation rules, custom license metrics, custom PPNs, custom dedup rules, reclamation rules, published-product list, custom license exception rules.

---

## 5. Insert/update and dedup

| Incoming | Match key | Insert | Update | Stop control |
|---|---|---|---|---|
| Installation | source-specific; dups allowed | always possible | same-source refresh (`U`) | exclude flag; dedup `active=false` |
| Discovery model | Publisher + Display name + Version **V** | no match | match sets reference | `Security Update` skip; cannot create manually |
| Software model | version/edition/language/platform/install condition | no match + auto-create on | recon reuses | auto-create off |
| Entitlement | PPN, else pub+prod+ver+ed+platform+lang | import creates | PPN maps | PPN errors; MLS blank PPN |
| Allocation | entitlement + user/device | create | re-evaluate | ≤ rights |
| Catalog item | vendor item/model publish | publish | vendor sync | do not publish |

Dedup levels **V**: `Exact` (full version), `Major` default (major version), `Any` (ignore version). Primary selection: source reliability → completeness → latest version **V**. IBM: ServiceNow Discovery wins; provider duplicates set inactive **V**.

---

## 6. Normalisation — six statuses, not four

| Status | Meaning | Manual allowed | Revert |
|---|---|---|---|
| `New` | pre-run | wait | n/a |
| `Match Not Found` | nothing matched | **Yes** | base |
| `Publisher Normalized` | publisher only | **Yes** | **Yes** → Match Not Found |
| `Partially Normalized` | publisher+product | **Yes** | **Yes** → Match Not Found |
| `Normalized` | full | — | **Yes** → Match Not Found |
| `Manually Normalized` | human set | — | **No** |

Rules/fallbacks **V**: Product/Package Map → Pattern → Enhanced Pattern → Wide-net (property default on) → ML (property default on) → manual. Suggestions: `samp_normalization_suggestion`; accept → `Normalized`; reject → stays; auto-accept property `com.snc.samp.auto_accept_normalization_suggestion` default **on**. Content Service opt-in improves hit rate and is default **off**.

**Product type reclassification** (Unknown→Licensable etc.) forces `Manually Normalized` **V**.

---

## 7. Model vs vendor vs publisher vs PPN vs catalog

| Concept | Table | Not |
|---|---|---|
| Vendor/company | `core_company` **C** | Not a product |
| Publisher | `samp_sw_publisher` → `core_company` **C** | Not the contract |
| PPN | `samp_sw_product_definition` **V** | Not an entitlement |
| Software model | `cmdb_software_product_model` **V** | Not a discovered string |
| Discovery model | `cmdb_sam_sw_discovery_model` **V** | Not purchasable |
| Vendor catalog item | `U:pc_vendor_cat_item` | Not a model |
| Catalog item | `sc_cat_item` **C** | Not a licence |
| Entitlement | `alm_license` **V** | Not an install |

Contract vendor lives on `ast_contract`, not on the model. Publishing a model creates a catalog item; it does not create a licence.

---

## 8. Position, true-up, reclamation

**Rights algebra** (all **V**): owned = sum active rights; used = allocated-in-use + not-allocated-in-use; available = owned − used; unlicensed installs; rights needed; over-licensed amount; true-up cost; potential savings; allocations needed (named user/device only); nontransferable rights (Microsoft core packs only).

**Remediation:** not-allocated-in-use → Create Allocations / Remove Unallocated Installs; allocated-not-in-use → Remove Allocations; unlicensed → Purchase Rights / Remove Unlicensed Installs.

**Licence types** **V**: Perpetual, Perpetual+SA, Subscription, Perpetual+Maintenance, Upgrade, SA, Maintenance, Step-up, Subscription Step-up, Add-on, From SA. SA/Maintenance reconcile **only** when linked to a base perpetual. Enterprise agreements stay Compliant **C**.

**True-up cost** = least rights needed × average price; cost from software-model licence/plus-maintenance cost, else average entitlement cost; override licence cost created at zero **V**.

**Reclamation:** `samp_sw_usage` (product level), rule types Total Usage Time (default) / Last Used Date / Peak Concurrent (eng) / Active Transaction Codes (SAP); `samp_sw_reclamation_candidate`; timeout `sam_reclamation_flow_error_timeout` 30 days; CSD uninstall-only licence; SaaS/SSO auto-creates a rule.

---

## 9. Workspaces, dashboards, reports

- **Software Asset Workspace** views **V**: Software asset overview, License usage, License operations, Software asset analytics, Success portal, Renewals calendar, Overlapping usage, Content Library portal.
- **Software asset overview** widgets + sources **V**: publishers/products out of compliance, over-licensed, expiring maintenance/subscription, total/top-5 true-up, potential/actual savings, software spend, installs by normalisation status, EOL products, Activity center.
- **License usage / License Workbench**: All/Out-of-Compliance/Pinned publishers; Product → Model → Metric drill-down; Rights Used By / Rights Needed By / Licensed Installs / Installs Used / Downgrades-Upgrades / Licensed Subscriptions / Cloud Special Rights.
- **Normalization and content** (PA): % normalised, installs by status, CDS Download Status.
- **Software Asset Analytics**: Overview, License Summary, Compliance Summary, Removal Summary; Normalization and Content; publisher analytics (Citrix/IBM/Microsoft/Oracle/SAP/VMware); Office 365/Adobe; SaaS; discovered inventory; optimisation; lifecycle; cloud cost simulator; engineering; normalisation.
- **Success portal**: SAM maturity, completed/total/projected savings, all goals, health checks passed, value-builder tasks, open activities.
- **Health Check**: suites SQL Server Config/CMDB, Windows Server Config/CMDB, Oracle Database, Java-Oracle, WebLogic-Oracle, Microsoft 365, General; Scan Findings; weekly `SAM - Trigger Full Scan`.
- **License Position**, **Renewals calendar**, **Overlapping usage**, **Content Library portal**, **CMDB success advisor for SAM**.

Every widget→table mapping is in `SAM_MODULE_REFERENCE.md` §12.2.

---

## 10. Integrations

Discovery · FBD (`com.snc.discovery.file_based_discovery` + `com.snc.file_signature_normalization`) · SCCM 2012/2016 plugins (deprecated Tokyo) → **Service Graph connector for Microsoft SCCM** · Intune/Jamf/Tanium (SGC, not native SAM) · ILMT/BigFix (IBM pack; `sn_samp_ibm_lic.ilmt_api_version`) · SaaS LM (`sn_sam_saas_int`) · SSO (`samp_sso_application`) · Spend Detection (`com.sn_sam_spend`) · Procurement (`com.snc.procurement`) + `app-itam-procurement-integration` · CSD (`com.snc.orchestration.client_sf_distribution`, uninstall only) · Engineering (OpenLM/Open iT) · SAP pack · Citrix pack · third-party IRE (`com.snc.samp.ire.datasource.integration`) · HAM contracts (`alm_asset`, `ast_contract`) · Content Service/CDS · Otto (`sn_now_assist_sam`).

**Uninstall rule:** SAM never deletes installs on its own; third parties must DELETE via Table API; a Retired/Stolen CI deletes related installs **V**.

---

## 11. Parameter inventory

### Must-consider (top 12)

| Property | Default | Decision |
|---|---|---|
| `com.snc.samp.automaticsmrcreation` | opt-in | Leave **off** in Crawl |
| `com.snc.samp.automaticsmcreation` | No | Off unless APM |
| `com.snc.samp.unlicensed_smr_creation` | False | Only for unlicensed position reporting |
| `com.snc.samp.manage.published.products` | false | Phase-wise scope |
| `com.snc.samp.exclude_device_flag` | empty | Leased/out-of-scope devices |
| `com.snc.samp.recon.group` / `.subgroup` | None | Reporting dimension; group ≠ subgroup |
| `com.snc.samp.wide_net_normalization.enabled` | on | Keep on |
| `com.snc.samp.enable.ml_normalization` | on | Keep on |
| `com.snc.samp.auto_accept_normalization_suggestion` | on | Govern the silent status change |
| `com.snc.samp.auto_suite_inference` | false | Suite over-count control |
| `com.snc.samp.recon.enablecustommetrics` | Yes | Custom metrics |
| `com.snc.samp.oracle.reconlevel` | ESX cluster | Large licence swing |

### Full list

`com.snc.samp.recon.group`, `.subgroup`, `.enablecustommetrics`, `.debug`, `.recon.max_workers`, `.automaticsmrcreation`, `.automaticsmcreation`, `.unlicensed_smr_creation`, `.auto_suite_inference`, `.exclude_device_flag`, `.manage.published.products`, `.wide_net_normalization.enabled`, `.enable.ml_normalization`, `.ml.overrride_ml_model_version`, `.auto_accept_normalization_suggestion`, `.use_lifecycle_approximation`, `.generate.calculated.lifecycles`, `.sam_ci_billing_threshold` (30), `.citrix.app.license.period` (90), `.eng.app.peak.usage.period` (30), `sam_reclamation_flow_error_timeout` (30), `.windowserver.license.threshold` (4.59), RHEL VDC threshold (3.2, `U` name), `.sqlserver.standard_sa.to.enterprise_sa.cost.ratio` (0.25), `.ms.sa.to.nonsa.cost.ratio` (1.25), `.oracle.reconlevel`, `.oracle.hostaffinityenabled`, `sn_samp_ibm_lic.default_region`, `sn_samp_ibm_lic.ilmt_api_version`, `com.snc.samp.ire.datasource.integration` (C), `sn_sam_workspace.sam_license_operations_list_count` (5,000,000), `samp.spend_prediction_service.max_label_attempts` (3), `glide.model.catalog_item_currency` (false).

Discovery-side: `glide.discovery.discover_software`, `.enable.software_filter`, `.software_filter_keys`, `.enable.software_simplify`, `.enable.software_simplify_sccm`, `.software_sccm_managed`, `.populate_software_instance_table`, `.sam_batch_update_size`, `.file_discovery.wildcard.windows`, `.file_discovery.blacklist.windows`, `.enable_file_tracking`, `.file_tracking.*`.

`glide.cmdb.sam.*` is **not** an official family **C**.

---

## 12. Maintenance runbooks

### 12.1 Add a software model

- **PPN path:** PPN in `samp_sw_product_definition` → entitlement import → model assigned/auto-created → `alm_license`; branches: one model / multiple (error, choose) / PPN missing (exact search → auto-create or `PPN and SM not found`).
- **Manual path:** custom product (`core_company`/`samp_sw_publisher`) → `cmdb_software_product_model` (publisher, product, version/edition conditions, platform, language, install condition, discovery map, suite, metric group, costs) → vendor catalog item → downgrade rights (`samp_sw_downgrade_model`, `samp_dmap_downgrade_model`, `samp_downgrade_model`) → lifecycles (`sam_sw_product_lifecycle`, `sam_custom_sw_product_lifecycle`) → publish catalog (`sc_cat_item`) → `alm_license` (PPN, type, metric, rights, dates, state, cost, metric group) → `alm_entitlement_user|asset` → run matching + reconciliation.
- Auto-create is **across versions for a specific edition, never a specific version**; `Created source = System property` **V**.

### 12.2 Normalise a software model

Triage dashboard → daily jobs → pattern rule → manual normalise (Partially/Publisher/Match Not Found) → suggestions (accept/reject/auto) → revert only where allowed → re-match model → re-run recon → reclassify product type if needed → content request for recurring misses. Never edit the normaliser/BR.

---

## 13. Curriculum compare (round 2)

CIS-SAM domains: overview 15%, data integrity 25%, entitlements/recon 30%, optimisation/audit 20%, reporting/ops 10% (weights from the learning guide only).

| Topic | Curriculum | Official (Brazil) | Keep |
|---|---|---|---|
| Usage table | `cmdb_sam_sw_usage` | `samp_sw_usage` **V** | **Official** |
| Recon result | single `sam_sw_reconciliation_result` | three tiers; `samp_license_metric_result` **V** | **Official** |
| Recon cadence | nightly | weekly default + on demand **V** | **Official** |
| Foundation vs Pro | conflated (`com.snc.sams`) | Pro `com.sn_samp_master_ws`; Foundation `com.snc.sams` **C** | **Official** |
| Normalisation name | "SUMN" | Content Library + named jobs **V** | **Official** |
| Install→model link | sample BR writes model | OOB matches publisher+product+version to discovery model **V** | **Official** |
| Reclaim window | 60–90 days | rule-defined usage/date; flow timeout 30 **V** | 60–90 is **practice** |
| Roles | `sam_license_manager`, `sn_sam.admin` | `sam_admin`, `sam_user`, `sam_developer`, `sam_integrator`, `sam_spend_import` **V** | **Official** |
| Tables | `alm_software`, `alm_software_installation` | do not exist for SAM Pro | **Reject** |

Curriculum-only strengths to absorb: "Unknown ≠ compliant", suite over-count, maintenance ≠ licence, publisher traps, don't overwrite entitlement quantity, reclaim evidence via usage.

---

## 14. Programme layer (new in this pass)

`MODULE_IMPLEMENTATION_PLAN.md` covers the 15 implementation dimensions the technical docs do not: business case/KPIs, scope, RACI, current state, process design, data governance, integration architecture, security/ACLs/PII, config-vs-customisation, environments/release/rollback, test strategy, cutover/migration, adoption/training, hypercare/support, risks/decisions/dependencies.

`SAM_IMPLEMENTATION_CHECKLIST.md` turns them into gates across 10 phases (prerequisites → scope → data model → integrations → entitlements → normalisation → reconciliation → reporting → security → testing/cutover/adoption).

Numeric test cases (T1–T10) and acceptance thresholds are in `ROUND2_GAP_ANALYSIS.md` §4.5–§4.6.

---

## 15. Final thoughts + what to add to the public SAM guide

The public guide at `…/docs/modules/sam/sam-guide/` is a learning path, not a config reference. It should absorb the following **concepts**, not this file verbatim:

### 15.1 Chapters to add or rewrite

1. **"Five records, one pipeline"** — install → discovery model → software model → entitlement → result. One diagram; the exam's single most useful mental model.
2. **"Six statuses, not four"** — New, Match Not Found, Publisher Normalized, Partially Normalized, Normalized, Manually Normalized; which allow manual normalise and which allow revert.
3. **"Model vs vendor vs publisher vs PPN vs catalog item"** — a one-page table. This prevents the most common architecture mistake.
4. **"The rights algebra"** — owned/used/available and the five allocation buckets, each with its remediation action. Include the `Not allocated in use` / `Allocated not in use` distinction; it is where most learners lose marks.
5. **"Licence types and why maintenance ≠ licence"** — the SA/maintenance must-link rule; enterprise agreements.
6. **"Insert/update in SAM"** — the one business rule that matches publisher+display name+version; dedup is separate; uninstalls are not propagated.
7. **"Normalisation rules"** — Product/Package Map, Pattern, Enhanced Pattern, Wide-net, ML, manual; fallback order.
8. **"Reporting map"** — each dashboard/widget → table (the current guide lists widgets without sources).
9. **"Integrations"** — Discovery, FGD/FBD, SCCM→SGC, ILMT, SaaS, SSO, Procurement, CSD, third-party IRE.
10. **"Operating model"** — RACI, change control, test cases, rollback limits, audit evidence. This is the missing half of most SAM curricula.

### 15.2 Diagrams

- Pipeline (records + tables).
- Normalisation state machine (six statuses + transitions).
- Rights algebra (owned → allocated/used → buckets).
- Insert/update decision tree (install → discovery model → software model).
- Integration topology (sources → installs → models → entitlements → results).

### 15.3 Labs to add

- Build one software model from a PPN; show the auto-created vs manual paths.
- Import one entitlement qty 1; publish; reconcile against two installs; read the shortfall.
- Normalise a `Match Not Found` model, accept a suggestion, then demonstrate the revert limit.
- Configure a dedup rule at Exact vs Major vs Any on three SQL installs.
- Exclude a leased device and watch the position change.
- Reclaim a seat: usage → candidate → reclaim request.

### 15.4 Corrections to publish prominently

`cmdb_sam_sw_usage` → `samp_sw_usage`; `sam_sw_reconciliation_result` → three tiers (`samp_license_metric_result`); nightly → weekly/on-demand; `alm_software` → do not use; "SUMN" → Content Library; Foundation ≠ Pro.

### 15.5 Final position

SAM is not a discovery module and not a reporting module. It is a **reconciliation contract** between what was purchased, what is installed, and how it may be used. The technical reference makes the contract executable; the programme plan makes it trustworthy. A module without owners, feed contracts, acceptance gates, change control, and audit evidence will produce a number that nobody defends.

---

## 16. Known gaps (`U`)

Business-rule/UI-policy/ACL names and sys_ids; internal columns for label-only fields; exact Software Model Results table; custom-product/pattern-rule/reclamation-rule table names; vendor catalog item table; RHEL threshold property name; instance reconciliation cadence. Queries: `SAM_MODULE_REFERENCE.md` Appendix A.

## 17. Source ledger

Brazil corpus: `agents/grok-4.6__xai__kilo/SNC_SAM__WT1/research/raw/` (58 pages, full list in `SAM_MODULE_REFERENCE.md` Appendix B). Australia: `CONFIG_INVENTORY_AUSTRALIA.md`. Discovery boundary: `ALT_PARALLELSWARM/research/servicenow-discovery/DISCOVERY_END_TO_END_GUIDE.md`.
