# Subagent Cross-Check Record

**Purpose:** the user asked for subagents to cross-check the work, then to cross-reference again against the public SAM guide. This file records the dispatch, the findings, and what changed.

**Method:** four read-only `explore` subagents in round 1, each with a narrow checklist and exact evidence paths. They were told **not to edit**. Round 2 was a consistency reviewer after the corrections.

---

## Round 1 — four parallel checks

| # | Scope | Subagent session | Verdict |
|---|---|---|---|
| 1 | Data model + pipeline + normalization (`01`, `03`, `04`) | `ses_e27074744ffelE4w95dC6gRbdW` | pass-with-corrections |
| 2 | CMDB/IRE governance (`02`) | `ses_e27073ebaffedbsRX6mYMQzXa0` | pass-with-corrections |
| 3 | Entitlements/reconciliation + config (`05`, `06`) | `ses_e27073452ffe4lFSD9Lh832rtQ` | pass-with-corrections |
| 4 | Guide delta (`GUIDE_CROSS_REFERENCE`, `CONFLICT_LOG`) | `ses_e27072a67ffeG0ICNsYG3JqKMD` | pass-with-corrections |

All four agreed on the core architecture and found no fabricated product mechanism. The defects were confidence-marker inflation, a few over-broad statements, one stale release fact, one wrong guide attribution, and material omissions.

---

## 1. Data model / pipeline findings

### Accepted and fixed

| Finding | Fix |
|---|---|
| Discovery-model key is Publisher + Display Name + Version; Edition is out | Already correct; retained **V** |
| Install references the discovery model | Already correct; retained **V** |
| Six statuses; manual/revert rules | Already correct; retained **V**; descriptions marked **U** |
| Dedup levels and primary selection | Already correct; added Exact = normalized version + edition, Major skips unparseable |
| Software-model matching is a scheduled job, not the v1 Display Name strategy | Rewrote `03 §7` and `04 §9`; marked the v1 strategy **C/U**; added job semantics |
| Diagram conflated normalization status with model association | Rewrote the branch to "matching job → auto-create / manual" |
| Retired/Stolen CI deletes installs; exclude-CI is for leased/phase rollout | Fixed `01 §13`; kept the **V** in `03 §10.2` |
| Usage is product-level, not install-level | Fixed the chain edge and the record table; added a note in the README |
| Classic UI limited support starts **Brazil**, and classic is inaccessible after `com.sn_samp_master_ws` | Fixed `01 §9`, `06 §7`, guide C-18 |
| Overview widget depends on normalize + `SAM - Daily Job`; the Normalization job updates trend charts | Fixed `04 §5` and added the CDS job |
| Suggestions table is `samp_normalization_suggestion` (singular) | Fixed `04 §6.4`/`§12`, `05 §13`, and `06 §3.1`; added the overview's plural-label caveat |
| `New` is not manually eligible; reconciliation gates on `Licensable`, not status | Fixed `04 §13` |
| SAM dedup, not IRE, selects the primary record | Fixed `03 §5.2` |
| Intune/Jamf Service Graph connectors are not in the Brazil SAM pages | Marked **U** in `03 §1` |
| `cmdb_ci_spkg` migration advice is v1-only | Marked **U/C** |
| SCCM deprecation is future ("will be deprecated in Tokyo") | Fixed `01 §3` and `06 §1` |
| Content Service is opt-in via Configuration Console; default not opted in; discovery models/custom products/custom PNs excludable | Fixed `04 §8` |
| Missing: matching job, `SAM - Daily Job`, dedup role, exclude-CI role/default, usage fields, Edition Override, suggestions detail, install count cap | Added where material |

### Rejected (with reason)

| Finding | Decision |
|---|---|
| "SAM Foundation `com.snc.sams` is not in the Brazil extracts" | **Rejected.** `software_reconciliation_for_compliance.txt` explicitly says "Software Asset Management Foundation (`com.snc.sams`)". Keep **V**. |
| "Discovery models are not documented as impossible to create manually" | **Rejected.** `discovery_models_and_installs.txt` says "Software discovery models cannot be created manually." Keep **V**. |
| "Maturity exit criteria should be P" | **Accepted**; fixed. |
| "CI identification step should be C" | **Accepted**; fixed. |

---

## 2. IRE findings

### Accepted and fixed

| Finding | Fix |
|---|---|
| The "four families" is a synthesis, not an official enumeration | Marked framing **C**; each family remains **V** |
| Data refresh is evaluated **with** reconciliation, not as a separate later step | Fixed the order statement; marked the separate-step framing **C** |
| Missing first-writer exception | Added: lower-priority source allowed if first writer or stale |
| Duplicate handling defaults are official (`true` / `5`) | Changed **C/U** → **V**; deterministic oldest + `duplicate_of` |
| Dynamic precedence is same-class-level; child static can override parent dynamic | Added |
| `enable_reconciliation_filter_before_update` default is official | Changed **C** → **V** |
| Property defaults table should cite the official properties page, not the sibling matrix | Re-labeled all **V**; replaced attribution |
| `installed_on` API column is not documented | Marked **U**; kept the label |
| Identification/data-refresh paths are reconstructed | Marked **C/U** |
| `task.list` filter is not documented | Marked **U** |
| Fifth control (dynamic IRE) is not wholly **C** | Split: instance-wide switch **V**; per-class exclusion **C/U** |
| Typo "ajust" | Fixed |
| Missing `cmdb_ire_partial_payloads_index` | Added |
| Missing `last_discovered`/`discovery_source` always updated | Added |
| Missing partial-payload max size | Added |
| Missing `last_scan` properties and dynamic fallback | Added |

### Residual

- `cmdb_dynamic_ire_skip_class` remains **U**; it appears only in secondary evidence.
- The exact data-refresh definition table name remains **U**.

---

## 3. Licensing / reconciliation / config findings

### Accepted and fixed

| Finding | Fix |
|---|---|
| Classic UI limited support is Brazil, not Australia | Fixed `01 §9`, `06 §7` |
| Step-up license type conflicts between two official pages | Marked **C/U**, recorded both positions |
| "Product status" vs "Software model status" | Corrected the wording; product-level compliance is Product Results |
| True-up cost is based on the **least** rights needed | Fixed |
| `unlicensed_smr_creation` wording reversed | Fixed: False disables; True creates |
| `exclude_device_flag` default not stated; column default false | Fixed |
| `recon.max_workers` no default | Fixed |
| `oracle.hostaffinityenabled` no default; only at vCenter level | Fixed |
| `generate.calculated.lifecycles` no default | Fixed |
| PPN auto-create requires a standard (custom) import | Added |
| `cmdb_dynamic_ire_skip_class` is U | Fixed |
| `samp_vmware_license_key`, `samp_oracle_options`, `cmdb_ci_spkg` are U | Fixed |
| `samp_entitlement` / `cmdb_sam_entitlement` are not documented for Brazil | Firmly marked; `alm_license` is the table |
| Job cadence wording overstates "documented" | Renamed the section; marked undocumented cadences |
| Missing Rights Used By and LMR form fields | Added |
| Content Library path is U | Fixed |
| Software Model Results table name is undocumented | Added a caveat |
| `recon.subgroup` must differ from group | Added to `06 §5` |

### Missing material added

`com.sn_itam_samp`, `com.sn_samp_workbench`, `samp_sw_resource_value`, CrowdStrike metrics, Concurrent Licenses, Nontransferable/Legacy fields, cost-ratio properties, `SAM - Central Data Service Download Status`, `SAM - Label Spend Transactions`, `samp_bulk_import`, `asset_job_log`, SAP Licensed Installs caveat, IBM RVU Rights Used By caveat, Brazil reclamation upgrade note.

### Residual

- Software Model Results table name: **U**.
- Publisher-specific rules: **U** (contract-specific).

---

## 4. Guide-delta findings

### Accepted and fixed

| Finding | Fix |
|---|---|
| C-10 is not a guide correction; the guide already labels the expire job as custom code | Rewritten as **not a correction**; safety note only |
| C-19 is partial; the guide's table already lists six records; only the heading is wrong | Reframed as a heading rename |
| Correction-ID collision between the delta and the conflict log | Added a mapping table to both files |
| Missed guide claims (workspace name, SaaS plugin, normalization hierarchy, edition labels, install fields, usage granularity, publisher assertions, unsafe code, result fields, "bundle") | Added G-22–G-31 |
| Internal pointer said C-07 for the record chain; should be C-19 | Fixed |
| Guide's Carry-Over Addendum already fixes part of C-01/C-04 | Added a scope note: main body vs addendum |
| `license_metric_type` four-way inconsistency | Added a resolution note |
| C-03 should mention the "Monday 02:00" claim | Added |
| Guide-only assets under-credited | Added exam table, study plans, platform mnemonics |
| "Link, don't merge" needs a nuance | Added: high-risk corrections must land in the guide; the addendum is precedent |

### Rejected (with reason)

| Finding | Decision |
|---|---|
| "The guide's table only has three rows" | **Rejected.** The guide's table lists six records; the defect is the heading. C-19 is now correctly scoped. |

---

## Round 2 — consistency check

**Subagent:** `ses_e2701f961ffe7pLp4aLHID0SVV` (final consistency reviewer).

Checks:

- cross-file consistency of the corrected claims,
- link integrity,
- confidence marks not contradicting each other,
- guide-delta numbering and mapping,
- residual **U** items listed in one place.

**Verdict:** fail on first pass (missing QA/FILESCOPE artifacts plus mark/mapping inconsistencies). All blockers were fixed: `04_QA/QA.md` and `06_FILESCOPE/FILESCOPE.md` were created, the GUIDE↔LOG map was rebuilt, the confidence marks were normalized, the SUBAGENT record was corrected, and the v1 links were verified against the published repo layout. The final QA verdict is in `04_QA/QA.md` §5.

---

## Net effect

- **0 fabricated product mechanisms** survived round 1.
- **1 release fact** corrected (classic UI: Brazil, not Australia).
- **1 guide attribution** corrected (C-10 is not an OOB claim).
- **1 major matching mechanism** corrected (job semantics, not the v1 fallback).
- **1 usage-granularity** correction (product-level, not install-level).
- **IRE property defaults** corrected from **C** to **V** (official properties page), and several claims corrected from **V** to **U/C** where the evidence was not in the fetched pages (data-refresh table, `installed_on`, job cadences, vendor-specific tables).
- **10+ material omissions** added.
