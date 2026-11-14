# Cross-Reference Matrix

**Purpose:** every material claim in `finalv2/` traced to (a) an official ServiceNow page, (b) the repo's v1 work, and (c) a status. This is the "cross-reference your work" artifact required by the methodology.

**v1 references** (paths resolve from the published `finalv2/` folder; `../final/` exists in the repo):

- `v1-MOD` = `final/FINAL_SAM_MODULE_REFERENCE.md` (beam, Australia)
- `v1-CFG` = `final/FINAL_SAM_CONFIG_REFERENCE.md` (grok/sam-research, mixed releases)
- `v1-DS` = `final/FINAL_deepseek-flash__deepseek__kilo.md` and `agents/deepseek-flash__deepseek__kilo/05_FINAL/*`
- `v1-BIDIR` = `final/FINAL_BIDIRECTIONAL_GAP_ANALYSIS.md`
- `v1-COV` = `final/FINAL_CROSS_REFERENCE_COVERAGE_ANALYSIS.md`
- `guide` = public SAM guide (2026-11-12)

**Status:** **V** official; **C** corroborated; **U** unverified; **P** practice.

---

## A. Module and data model

| ID | Claim in v2 | Official source | v1 cross-ref | Status |
|---|---|---|---|---|
| A1 | SAM feature areas: dashboards, licensing, discovery/normalization, reconciliation, optimization, downgrade rights | Brazil *SAM overview* | v1-MOD §1 | **V** |
| A2 | Brazil master plugin is `com.sn_samp_master_ws`; `com.sn_samp_master` is pre-Brazil; `com.snc.samp` is core; `com.snc.sams` is Foundation | Brazil *Components installed with SAM Professional*; *Software reconciliation for compliance* | v1-CFG §3.1; v1-DS GUIDE §3 C-04 | **V** |
| A3 | `sam_admin` contains `sam_user`, `sam_spend_import`, `asset`, `model_manager`, `contract_manager` | Brazil *Components* | v1-CFG §3.2 | **V** |
| A4 | `cmdb_sam_sw_install` is the source of truth for current software data once SAM is active | Brazil *SAM overview*; *Components* | v1-MOD §1.1 | **V** |
| A5 | Discovery models are auto-created and cannot be created manually | Brazil *Discovery models and software installations* | v1-MOD §5.1 | **V** |
| A6 | Discovery-model primary key is **Publisher + Display Name + Version** | Brazil *Discovery models and software installations* | v1-MOD §3.2 says Publisher+Product+Version+Edition → **corrected** | **V** |
| A7 | Version matching is exact first, then rounds down to major (`8.0.4` → `8.0`) | Brazil *Discovery models and software installations* | v1-MOD §3.2 | **V** |
| A8 | A business rule matches/creates the discovery model when installs are written | Brazil *Software discovery* | v1-MOD §3.1 | **V** |
| A9 | The install references the **discovery model**, not the software model | Brazil *Software installation fields* | guide conflict; v1-DS C-06 | **V** |
| A9b | Usage is product-level (`samp_sw_usage`) and references publisher/product + CI + user, not the install record | Brazil *View or create software usage* | guide conflict → **corrected** | **V** |
| A10 | Six normalization statuses: New, Match Not Found, Publisher Normalized, Partially Normalized, Normalized, Manually Normalized | Brazil *Discovery models fields* | v1-MOD §6.4 lists five; v1-DS claims six | **V** |
| A11 | Manual normalization allowed for Partially Normalized, Publisher Normalized, Match Not Found | Brazil *Software normalization* | v1-MOD §5.2 | **V** |
| A12 | Revert allowed for Normalized/Partially/Publisher → Match Not Found; not for Manually Normalized or pattern-normalized | Brazil *Software normalization*; *Discovery models…* | v1-MOD §5.2 | **V** |
| A13 | Rule families: Product Map, Package Map, Pattern, Enhanced Pattern, Wide-net; ML optional | Brazil *Software normalization* | v1-MOD §6.5; v1-CFG §3.5 | **V** |
| A14 | Normalization jobs run daily; overview widget needs the two daily jobs | Brazil *Software normalization*; *Software asset overview* | v1-MOD §6.3 | **V** |
| A15 | Content Service is opt-in; custom products can be excluded from sharing | Brazil *Discovery models fields*; v1-CFG | v1-CFG §3.5 | **V/C** |
| A16 | Auto-model creation is controlled by `automaticsmrcreation`, `automaticsmcreation`, `unlicensed_smr_creation` | Brazil *Automatic creation of software models* | v1-CFG §3.8 | **V** |
| A17 | Dedup levels: Exact, Major (default), Any | Brazil *Software install deduplication* | not in v1-MOD (Australia); v1-DS mentions Brazil | **V** |
| A18 | Primary selection: source reliability → completeness → latest version | Brazil *Software install deduplication* | v1-DS §5 | **V** |
| A19 | Custom dedup rules live in `sam_sw_dedup_rule`; product must be normalized | Brazil *Create a custom deduplication rule* | v1-DS §5 | **V** |
| A20 | Uninstalled installs are deleted via REST Table API; role `sam_developer` | Brazil *Delete uninstalled software…* | v1-MOD §7.2 | **V** |
| A21 | Exclude CI via boolean column + `com.snc.samp.exclude_device_flag` + `SAM — Adjust Installs for excluded CIs` | Brazil *Exclude software assets on CIs* | v1-BIDIR A3 | **V** |
| A22 | Retired/stolen CI deletes related installs | Brazil *View or create software usage* | v1-DS A10 | **V** |
| A23 | Product type must be Licensable for reconciliation; changing it sets `Manually Normalized` | Brazil *Discovery models fields* | v1-DS | **V** |
| A24 | Model matching is performed by `SAM – Discovery Model to Software Model matching`: normalized publisher+product, most specific first, generic fallback; install-condition models are not a match; manual override is not overwritten | Brazil *Software model relationship to software installation* | v1-MOD's Display Name strategy is **C/U**, not V | **V** |
| A25 | Classic UI support becomes limited from Brazil; after `com.sn_samp_master_ws`, classic is inaccessible | Brazil *Exploring SAM* | v1-MOD says Australia → **corrected** | **V** |
| A26 | Step-up license type: license-types page says All; import page says Microsoft only | Brazil *Impact of license types*; *Software models and entitlements* | not in v1 | **C/U** |
| A27 | Documented result fields are rights owned/used/needed/available, Software model status, unlicensed installs, true-up cost; not `compliance_state` | Brazil *License Position report*; *Reconciliation results* | guide conflict → **corrected** | **V** |

## B. Reconciliation and reporting

| ID | Claim in v2 | Official source | v1 cross-ref | Status |
|---|---|---|---|---|
| B1 | Reconciliation runs weekly by default, or on demand for publishers/groups/subgroups | Brazil *Software reconciliation for compliance* | v1-CFG says weekly Mon 02:00; guide says nightly | **V** |
| B2 | Group/subgroup dimensions: country, department, company, region, cost center | Brazil *Software reconciliation for compliance*; *SAM properties* | v1-CFG §3.8 | **V** |
| B3 | Three tiers: `samp_product_result` → Software Model Results → `samp_license_metric_result` | Brazil *Software reconciliation results* | v1-DS; guide uses a single table → **corrected** | **V** |
| B4 | Product results are generated for licensable products even without a software model | Brazil *Software reconciliation results* | v1-DS | **V** |
| B5 | Software model results are created only when a model or entitlement exists | Brazil *Software reconciliation results* | v1-DS | **V** |
| B6 | Rights algebra: owned, used, available, allocated in use, not allocated in use, allocated not in use, not allocated, allocations needed | Brazil *Software model results license metric results fields* | v1-DS | **V** |
| B7 | Automatic remediation options appear when not-allocated-in-use or allocated-not-in-use > 0 | Brazil *LMR fields* | v1-DS | **V** |
| B8 | Product status field is Compliant / Not Compliant; the six-state vocabulary is interpretive | Brazil *License Position report*; *Software reconciliation results* | guide conflict; v1-DS C-17 | **V/P** |
| B9 | License Position report fields (rights owned/used/needed/available, true-up, savings, over-licensed) | Brazil *Software license compliance position* | v1-DS | **V** |
| B10 | Two license-position reports when perpetual-SA and subscription coexist; unlicensed installs/subscriptions generate reports | Brazil *Software license compliance position* | v1-DS | **V** |
| B11 | License types and their reconciliation impact (perpetual, SA, subscription, maintenance, upgrade, step-up, add-on, From SA) | Brazil *Impact of different license types…* | v1-DS | **V** |
| B12 | PPN resolution scenarios (blank/provided × standard/MLS × auto-create) | Brazil *Software models and software entitlements* | v1-DS | **V** |
| B13 | Usage table is `samp_sw_usage`; usage is tracked at product level, not version/edition | Brazil *View or create software usage* | v1-DS; guide uses `cmdb_sam_sw_usage` → **corrected** | **V** |
| B14 | Health Check categories and weekly `SAM - Trigger Full Scan` | Brazil *SAM health check* | v1-DS | **V** |
| B15 | Reporting map: product results, LMR, reclamation candidate, discovery model, lifecycle, `alm_license`, `samp_reconciliation_result`, `samp_job_log`, `samp_entitlement_import` | Brazil *Software asset overview* | v1-DS | **V** |
| B16 | `sam_reclamation_flow_error_timeout` = 30 days; engineering peak = 30 days; Citrix app license period = 90 days | Brazil *SAM properties* | v1-DS | **V** |

## C. CMDB / IRE

| ID | Claim in v2 | Official source | v1 cross-ref | Status |
|---|---|---|---|---|
| C1 | IRE uses identification, reconciliation, and IRE data source rules when processing incoming data | Australia *IRE overview*; *Components* | sibling Discovery corpus | **V** |
| C2 | Identification answers insert vs update; no match → create; match → update | Australia *IRE overview* | sibling | **V** |
| C3 | Reconciliation is required only for update; not applied on insert | Australia *Components* | sibling | **V** |
| C4 | Static reconciliation rules set source priority per attribute; child overrides parent; specific attribute beats "all attributes" | Australia *Reconciliation rules*; *Create a CI reconciliation rule* | sibling | **V** |
| C5 | Dynamic reconciliation rules use CMDB 360 and take precedence over static | Australia *Reconciliation rules* | sibling | **V** |
| C6 | Data refresh rules define effective duration; stale values can be updated by a lower-priority source | Australia *Reconciliation rules*; *Create a CI reconciliation rule* | sibling | **V** |
| C7 | IRE data source rules block **inserts** only; updates remain allowed | Australia *Create an IRE data source rule* | sibling | **V** |
| C8 | Blocked insert with `createOrUpdateCI()` fails the whole payload; Enhanced stores a partial payload | Australia *Create an IRE data source rule* | sibling | **V** |
| C9 | IRE data source rules have no impact when dynamic reconciliation rules are in effect | Australia *Create an IRE data source rule* | sibling | **V** |
| C10 | IRE identification can use `source_name` + `source_native_key` or criterion attributes | Australia *IRE overview* | sibling | **V** |
| C11 | Partial payloads are stored and retried; incomplete payloads are logged and never retried; 90-day purge | Australia *IRE overview* | sibling | **V** |
| C12 | SAM does **not** use IRE to match installs to discovery models; that is a business rule + primary key | Brazil *Software discovery*; Australia *IRE overview* | v1-MOD §3.2 says "no IRE-style" | **V** |
| C13 | IRE property defaults (skip_duplicates, override.null, dynamic_ire_enabled, etc.) | Australia *Properties for Identification and Reconciliation* (`ire_properties.txt`) | sibling corroborates | **V** |
| C14 | Exact data-refresh definition table name | not stated in fetched pages | — | **U** |

## D. Guide cross-reference

| ID | Claim in v2 | Official source | v1 cross-ref | Status |
|---|---|---|---|---|
| D1 | Guide's `cmdb_sam_sw_usage` is wrong → `samp_sw_usage` | Brazil *View or create software usage* | v1-DS C-01 | **V** |
| D2 | Guide's single result table is wrong → three tiers | Brazil *Software reconciliation results* | v1-DS C-02 | **V** |
| D3 | Guide's "nightly" is wrong → weekly default | Brazil *Software reconciliation for compliance* | v1-DS C-03 | **V** |
| D4 | Guide's `com.snc.iam` is not the SAM plugin | Brazil *Components* | v1-DS C-04 | **V** |
| D5 | Guide's "SUMN" is not the official term in the fetched pages | Brazil *Software normalization* | v1-DS C-05 | **V/U** |
| D6 | Guide's install→software_model link is wrong → install→discovery model | Brazil *Software installation fields* | v1-DS C-06 | **V** |
| D7 | Guide's `normalized_software_model` → documented label "Software model"; column **U** | Brazil *Discovery models fields* | v1-DS C-07 | **V/U** |
| D8 | Guide's custom `u_*` fields are custom, not OOB | Brazil pages | v1-DS C-09 | **V** |
| D9 | Guide's "Unknown" is not a product status field | Brazil *License Position report* | v1-DS C-17 | **V/P** |
| D10 | Guide's "Oracle 10% rule" is not documented | Brazil pages | v1-DS C-11 | **U** |
| D11 | Guide's "audit package export" is not documented | Brazil pages | v1-DS C-12 | **U** |
| D12 | Guide's 5–15% savings and 60–90-day reclaim are practice | — | v1-DS C-14/C-15 | **P** |

---

## Summary

| Status | Approx. count |
|---|---|
| **V** | 65+ |
| **C** | 3 |
| **U** | 5 |
| **P** | 4 |

The **U** rows above are the claims that could not be settled without an instance or an additional official page: the data-refresh definition table, exact column API names, publisher-specific rules, the Software Model Results table name, and Intune/Jamf Service Graph connector support in the Brazil SAM pages. The deep docs contain additional **U** items (vendor tables, job cadences, `installed_on`); all are collected in `04_QA/QA.md` §4.
