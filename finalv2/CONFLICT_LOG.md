# Conflict Log

**Rule:** official ServiceNow page for the pinned release wins. If two official pages differ by release, the release is stated. Secondary sources and the public guide lose to official pages. Practices stay **P**. Unresolved items stay **U** — they are not smoothed over.

> **ID map to `GUIDE_CROSS_REFERENCE.md`:**
>
> | CONFLICT_LOG | GUIDE | Topic |
> |---|---|---|
> | C-01 | C-04 | Plugin IDs |
> | C-02 | C-02, C-12 | Result tiers / run record |
> | C-03 | — | Discovery-model key |
> | C-04 | C-06, C-07 | Install / model field |
> | C-05 | — | Six statuses |
> | C-06 | — | IRE engine order |
> | C-07 | C-03, C-16 | Reconciliation cadence |
> | C-08 | C-01 | Usage table |
> | C-09 | C-21 (and C-08 partial) | Entitlement table / metric columns |
> | C-10 | C-05 | "SUMN" |
> | C-11 | C-17 | Compliance state |
> | C-12 | C-02 | Run vs analysis |
> | C-13..C-16 | C-13..C-16 | 1:1 |
> | C-17 | C-11, C-12 | Oracle 10% / audit export |
> | C-18 | C-19 | Record-chain heading |
> | C-19 | C-18 | Classic UI / breadcrumbs |
> | C-20 | — | Step-up conflict |
> | C-21 | — | Model-matching job |
> | C-22 | G-27 | Usage granularity |
> | C-23 | G-30 | Result fields |

---

## C-01 — Which plugin is "SAM"?

| Position | Claim | Evidence |
|---|---|---|
| v1-MOD | `com.sn_samp_master_ws` | Australia config |
| v1-CFG | `com.sn_samp_master_ws` (Xanadu+) / `com.snc.samp` (pre-Xanadu) / `com.snc.sams` (Foundation) | Mixed releases |
| guide | `com.snc.sams` "Foundation/Pro" + `com.snc.iam` | Community framing |
| **Official Brazil** | `com.sn_samp_master_ws` loads `com.sn_samp_master` + `sn_sam_workspace`; `com.sn_samp_master` is pre-Brazil; `com.snc.samp` is the core plugin; `com.snc.sams` is Foundation | *Components installed with SAM Professional*; *Software reconciliation for compliance* |

**Resolution:** document all four with release labels; **`com.snc.iam` is not the SAM plugin** and is removed as a SAM identifier. **V**

---

## C-02 — Is there a single reconciliation result table?

| Position | Claim |
|---|---|
| guide | `sam_sw_reconciliation_result` with `compliance_state` |
| v1-DS | Three tiers: `samp_product_result` → Software Model Results → `samp_license_metric_result`; no single documented result table |
| **Official Brazil** | Three tiers are documented; the run record is `samp_reconciliation_result` (source of the "last reconciliation" alert) |

**Resolution:** use the three tiers for analysis (**V**); use `samp_reconciliation_result` for the **run** (**V**). There is no documented `sam_sw_reconciliation_result` analysis table (**C** — absence in the fetched pages).

---

## C-03 — Discovery-model primary key: is Edition included?

| Position | Claim |
|---|---|
| v1-MOD | Publisher + Product + Version + **Edition** |
| **Official Brazil** | **Publisher + Display Name + Version**; Display Name is generated from discovered publisher, product, and version |
| Official Brazil (software discovery) | Business rule checks discovered publisher, discovered product, discovered version |

**Resolution:** the documented primary key is **Publisher + Display Name + Version**. Edition is a normalized field, not part of the key. **V**

---

## C-04 — Does the install reference the software model or the discovery model?

| Position | Claim |
|---|---|
| guide | `cmdb_sam_sw_install.software_model` |
| **Official Brazil** | Software Installation has a **Discovery model** field; the software-model reference lives on the discovery model |
| v1-DS | Same correction |

**Resolution:** install → discovery model → software model. **V**

---

## C-05 — How many normalization statuses?

| Position | Claim |
|---|---|
| v1-MOD | Five (Normalized, Partially, Publisher, Match Not Found, Manually) |
| v1-DS | Six (adds `New`), but flagged the column name **U** |
| guide | Binary "queue"/"unmatched" |
| **Official Brazil** | **Six**: New, Normalized, Partially Normalized, Publisher Normalized, Match Not Found, Manually Normalized |

**Resolution:** six. The field is labeled **Normalization status**; the API column name remains **U** until verified in `sys_dictionary`. **V**

---

## C-06 — Where does the IRE data source rule sit in the processing order?

| Position | Claim |
|---|---|
| Run diagram | Identification → reconciliation → data refresh → **IRE data source rule** (visually last) |
| **Official IRE** | On **insert**, after identification finds no match, the data source rule gates the insert; reconciliation and data refresh are **update-only** |

**Resolution:** the diagram is a conceptual ordering of the four families; the engine order is **identify → (match? update gates : insert gate)**. Document both, and state which is which. **V**

---

## C-07 — Weekly, nightly, or Monday 02:00?

| Position | Claim |
|---|---|
| Official Brazil | **Weekly default** + on demand |
| guide | "default nightly" |
| v1-CFG | Weekly (Mon 02:00) |

**Resolution:** **weekly default** is the only official cadence. Monday 02:00 is a schedule configuration detail, not a documented default; mark it **U** unless the instance's schedule confirms it. **V/U** The guide's "nightly" is wrong; the v1 "Mon 02:00" is unconfirmed at the documentation level.

---

## C-08 — Usage table name

| Position | Claim |
|---|---|
| guide | `cmdb_sam_sw_usage` |
| **Official Brazil** | `samp_sw_usage` (Software Usage); tracks product level, not version/edition |
| v1-DS | `samp_sw_usage` |

**Resolution:** `samp_sw_usage`. **V**

---

## C-09 — Entitlement table name

| Position | Claim |
|---|---|
| v1-CFG | `cmdb_sam_entitlement` / `samp_entitlement` (Professional); `alm_license` (Foundation) |
| **Official Brazil** | Software Entitlement is `alm_license` in the overview and reports; no `samp_entitlement` page was found in the fetched set |

**Resolution:** use `alm_license` as the documented table. `samp_entitlement` / `cmdb_sam_entitlement` are **not documented for Brazil**; do not use them in new work. Verify only if migrating from an older release. **V/U**

---

## C-10 — Is "SUMN" an official term?

| Position | Claim |
|---|---|
| guide | "ServiceNow calls this Software Usage and Normalization Mapping (SUMN)" |
| **Official Brazil** | The fetched pages use **normalization** and **Content Library**; SUMN is not used |

**Resolution:** use **Content Library normalization**; mention SUMN once as a community/legacy label. **V/U**

---

## C-11 — Is "Unknown" a compliance state?

| Position | Claim |
|---|---|
| guide | Six compliance positions including Unknown |
| v1-DS | Product status is Compliant / Not Compliant; Unknown is an interpretation |
| **Official Brazil** | License Position report has **Software model status**: Compliant / Not Compliant |

**Resolution:** document the six-state vocabulary as **teaching/interpretation** and the product field as binary. **V/P**

---

## C-12 — Is "reconciliation result" the run or the analysis?

| Position | Claim |
|---|---|
| guide | One result record per model with a compliance state |
| **Official Brazil** | `samp_reconciliation_result` is the run; the analysis is product/model/metric tiers |

**Resolution:** separate the **run** from the **analysis**. **V**

---

## C-13 — "One entitlement per contract line"

| Position | Claim |
|---|---|
| guide | Stated as a rule |
| Official docs | Not stated as a product constraint; it is audit-evidence practice |

**Resolution:** mark **P**. **P**

---

## C-14 — 60–90-day reclamation window

| Position | Claim |
|---|---|
| guide | 60–90 days |
| Official Brazil | `sam_reclamation_flow_error_timeout` = 30 days (error timeout, not a usage window) |

**Resolution:** keep 60–90 days as **P**; distinguish the 30-day error timeout as **V**. **V/P**

---

## C-15 — "SAM returns 5–15% of spend"

| Position | Claim |
|---|---|
| guide | 5–15% in year one |
| Official docs | Not a product SLO |

**Resolution:** mark **P**; do not use as a commitment. **P**

---

## C-16 — "Nightly reconciliation, results < 24h" SLA

| Position | Claim |
|---|---|
| guide | SLA target |
| Official Brazil | Weekly default |

**Resolution:** change to "weekly or agreed cadence; results within one cadence + slack" as a programme choice. **V/P**

---

## C-17 — Oracle "10% rule" and "audit package export"

| Position | Claim |
|---|---|
| guide | Both presented as product capabilities |
| Official Brazil | Not found in the fetched pages |

**Resolution:** mark **U**; verify in the instance / publisher contract / Store before use. **U**

---

## C-18 — "Three record types"

| Position | Claim |
|---|---|
| guide | Three record types |
| v2 | Five/six records in the operational chain |

**Resolution:** keep the mnemonic, expand the chain. **C/P**

---

## C-19 — When does classic UI support become limited?

| Position | Claim |
|---|---|
| v1-MOD | "Classic UI has limited support from Australia" |
| **Official Brazil** | Limited support begins with **Brazil**; after activating `com.sn_samp_master_ws`, the classic UI is **inaccessible** |
| v1-DS | Repeats the Australia error |

**Resolution:** Brazil, not Australia. Add the master-plugin lockout. **V**

---

## C-20 — Step-up license type: all publishers or Microsoft only?

| Position | Claim |
|---|---|
| Official *Impact of license types on reconciliation* | Publisher applicability: **All** |
| Official *Software models and software entitlements* | Step-up is available **only if the publisher is Microsoft**; another publisher errors |
| guide | Presents step-up generically |

**Resolution:** record both official statements; mark the practical answer **C/U** and verify in your release. Do not silently pick one.

---

## C-21 — How does a discovery model find a software model?

| Position | Claim |
|---|---|
| v1-MOD | Display Name + Publisher + Version; fallbacks; version rounding |
| **Official Brazil** | Scheduled job `SAM – Discovery Model to Software Model matching`; normalized publisher + product; most specific first, most generic fallback; models with install conditions are not a match; manual override unchecks `Automatically matched` |
| v2 draft | Initially repeated the v1 strategy as **V** — corrected |

**Resolution:** use the official job behavior. Keep the v1 fallback description as **C/U** only. **V**

---

## C-22 — Is usage install-level or product-level?

| Position | Claim |
|---|---|
| guide | Usage = evidence the install was run (install-level framing) |
| **Official Brazil** | `samp_sw_usage` tracks usage at the **product** level, not version/edition; records reference publisher/product + CI + user |
| v2 draft | Initially drew `samp_sw_usage → install` — corrected |

**Resolution:** usage is product-level; do not join it to a specific install record. **V**

---

## C-23 — What fields does a reconciliation result have?

| Position | Claim |
|---|---|
| guide | `entitlement_count`, `install_count`, `usage_count`, `compliance_state` |
| **Official Brazil** | Product/Software Model/License Metric tiers; rights owned/used/needed/available; Software model status; unlicensed installs; true-up cost; etc.; `compliance_state` is not a documented field |
| v1-DS | Three tiers |

**Resolution:** use the documented tier fields; treat the guide's field list as custom/illustrative. **V**

---

## Unresolved (kept as U)

| Item | Why unresolved | Verification |
|---|---|---|
| Exact data-refresh definition table/field names | Not stated in fetched IRE pages | CI Class Manager → Reconciliation Rules → Add |
| Exact column API names (`normalization_status`, `software_model`, `license_metric`) | Docs expose labels, not columns | `sys_dictionary.list` |
| Publisher-specific rules (Oracle core factors, IBM PVU, SAP indirect access) | Contract- and pack-specific | Publisher agreement + pack docs |
| Exact job schedule/time zone | Weekly/daily documented; hour is configuration | `sysauto_script` / Scheduled Jobs |
| `samp_entitlement` / `cmdb_sam_entitlement` existence | v1 claims; not in fetched Brazil set | `sys_db_object` |

---

## Resolution summary

| Conflict | Resolution |
|---|---|
| C-01 | Four plugin IDs, release-labeled; drop `com.snc.iam` |
| C-02 | Three tiers + run record |
| C-03 | Publisher + Display Name + Version |
| C-04 | Install → discovery model |
| C-05 | Six statuses |
| C-06 | Conceptual vs engine order |
| C-07 | Weekly default |
| C-08 | `samp_sw_usage` |
| C-09 | `alm_license` (verify alternatives) |
| C-10 | Content Library normalization |
| C-11 | Binary field + six-state teaching |
| C-12 | Run vs analysis |
| C-13 | Practice |
| C-14 | Practice + 30-day property |
| C-15 | Practice |
| C-16 | Cadence choice |
| C-17 | Unverified |
| C-18 | Expanded chain / heading reframe |
| C-19 | Classic UI: Brazil + master-plugin lockout |
| C-20 | Step-up conflict: record both |
| C-21 | Official model-matching job |
| C-22 | Usage is product-level |
| C-23 | Documented result fields |
