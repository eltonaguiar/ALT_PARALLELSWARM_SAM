# Normalization and Deduplication

> **Status legend:** **V** verified; **C** corroborated; **U** unverified/instance-dependent; **P** practice.
> **Release pin:** **Brazil** (updated 2025-07-31 → 2026-10-19).

---

## 1. Why normalization exists

Discovery reports the same product under many fingerprints: `Microsoft Corp`, `Microsoft Corporation`, `MS`, `Office16`, `O365ProPlus`, and so on. Normalization compares the discovered **publisher, product, version, and edition** against the **SAM Content Library** and writes standardized values to the normalized columns on `cmdb_sam_sw_discovery_model`. **V**

Those normalized values are then used by:

- reconciliation of entitlements vs installs, **V**
- license position calculation, **V**
- software lifecycle management. **V**

Example: discovered publisher `Microsoft Corp` can normalize to `Microsoft`. **V**

Without normalization, counts are wrong, audit evidence is weak, and the same product is split across multiple software models. **V/P**

---

## 2. The fields that matter

On `cmdb_sam_sw_discovery_model`: **V**

| Field | Meaning |
|---|---|
| **Display name** | Generated automatically from discovered publisher, discovered product, and discovered version |
| **Normalization status** | Current state of the normalization process |
| **Publisher / Product / Version / Edition / Full version** | **Normalized** values written by normalization |
| **Discovered publisher / product / version** | Raw observed values |
| **Product type** | `Child`, `Driver`, `Licensable`, `Not Licensable`, `Patch`, `Unknown` |
| **Platform / Language** | Normalized platform and language |
| **Exclude from content service** | Excludes this model's details from Content Service sharing (custom products, when opted in) |

**Reconciliation only considers licensable discovery models.** **V**

---

## 3. Six normalization statuses (verified)

| Status | What it means | Manual normalization allowed? | Revert allowed? |
|---|---|---|---|
| **New** | Newly created; normalization has not completed | No (wait for the job) | No |
| **Match Not Found** | No Content Library match | **Yes** | No (it is already the fallback) |
| **Publisher Normalized** | Publisher matched; product/version incomplete | **Yes** | **Yes** → `Match Not Found` |
| **Partially Normalized** | Some fields matched | **Yes** | **Yes** → `Match Not Found` |
| **Normalized** | Full match | No | **Yes** → `Match Not Found` |
| **Manually Normalized** | An operator set values | No | **No** |

**V** for the six values (Brazil discovery-model fields page). **V** for manual eligibility (`Partially Normalized`, `Publisher Normalized`, `Match Not Found`). **V** for revert (`Normalized`, `Partially Normalized`, `Publisher Normalized` → `Match Not Found`; `Manually Normalized` and pattern-normalized models cannot be reverted). The plain-English descriptions in the second column are **inferred (U)**; the official page documents the value names, not the definitions.

> **This corrects two earlier simplifications:** (a) the status field is not a binary "normalized / unmatched"; (b) `New` is a real documented value, not an unverified invention. The earlier v1 pass was right to flag it; the Brazil fields page settles it. See [`../CONFLICT_LOG.md`](../CONFLICT_LOG.md) C-05.

---

## 4. Rule families

The Content Library uses these normalization rule families: **V**

| Rule family | How it works | Typical use |
|---|---|---|
| **Product Map** | One rule per distinct discovery model | Precise mapping of a known fingerprint |
| **Package Map** | One rule per distinct package fingerprint | Installer/package-level mapping |
| **Pattern normalization** | One rule covers many models matching a data pattern | `Microsoft Office 2019*` → `Microsoft Office` |
| **Enhanced pattern normalization** | Handles complex variations in product, edition, and version; supports conditional include/exclude terms | Edition aliases (`standard`, `STD`, `stand`) → `Standard` |
| **Wide-net normalization** | Groups similar discovered values to reduce one-off rules; only eligible products | Long-tail titles |
| **Machine learning normalization** | ML matches unrecognized software (optional plugin) | Real-time improvement |

**V** for the first four and wide-net; **V** for ML plugin/property. Eligibility for wide-net is determined by the Content Service. **V**

---

## 5. Scheduled jobs

| Job | Cadence | Purpose |
|---|---|---|
| **`SAM - Normalize discovery models using content library rules`** | Daily | Normalize discovery models and assign status |
| **`SAM - Daily Job`** | Daily | Required for the overview normalization widget |
| **`SAM - Discovery Model Normalization job`** | Daily | Update normalization trend charts on the Normalization and content dashboard |
| **`SAM - Central Data Service Download Status`** | Daily | Update the Central Data Service Download Status related list |
| **`SAM - Trigger Full Scan`** | Weekly (health check) | Run health-check KPIs |

**V** for the job names and cadences above.

- **Software asset overview** normalization widget: populated only after `SAM - Normalize discovery models using content library rules` **and** `SAM - Daily Job` have run. **V**
- **Normalization and content dashboard** trend charts: updated daily by `SAM - Discovery Model Normalization job`. **V**
- The dashboard's normalization-status widget also depends on `SAM - Normalize discovery models using content library rules`, `SAM - Daily Job`, and `Central Data Service Download Status`. **V**

---

## 6. Manual normalization

### 6.1 Workspace path

**Software Asset Workspace → License operations → Discovery models** → select a record → **Normalize** → set values → status becomes `Manually Normalized`. **V** (The exact action label may be `Normalize`; the v1 reference uses this wording. **C**)

### 6.2 Classic path

`All > Software asset > Discovery > Discovery models` → open a record with an eligible status → set Publisher / Product / Version → save. The legacy form also exposes the **Software model** field and the **Approved** check box. **C**

### 6.3 Revert

Use **Revert Normalization**. Normalized fields return to their original unnormalized values. The revert rules are in §3. **V**

### 6.4 Suggestions

Normalization suggestions are generated for manually normalized discovery models. They suggest **Publisher, Product, Version, Edition, Platform, and Language** from the Content Service. You can accept or reject each suggestion. **V**

- Accepting a suggestion copies the suggested values to the discovery model, changes the status from `Manually Normalized` to `Normalized`, and sets the suggestion status to `Accepted`. **V**
- Rejecting keeps the manual values and `Manually Normalized` status. **V**
- The property `com.snc.samp.auto_accept_normalization_suggestion` (enabled by default) auto-accepts suggestions when there is no difference from the manually normalized values. **V**
- Records are stored in **`samp_normalization_suggestion`** (singular) **V**. The overview page labels the list `samp_normalization_suggestions` **C**. Verify the exact table name in your release **U**.

A caution icon next to the status field indicates a suggestion exists. **V**

---

## 7. Machine learning and wide-net

- Activate `com.sn_sam_ml_normalization` to add ML normalization. **V**
- Property `com.snc.samp.enable.ml_normalization` is enabled by default; ML is applied only to models that content rules could not normalize. **V**
- Property `com.snc.samp.wide_net_normalization.enabled` is enabled by default; wide-net is applied only to models that regular package normalization could not handle. **V**
- Only an admin can modify those two properties. **V**

---

## 8. Content Service

Content Service is an opt-in feedback loop: unnormalized discovery-model data can be shared with ServiceNow to improve the Content Library. **V**

- Opt-in is done through the **Configuration Console for Software Asset Management** (or the classic **Content Service Setup** menu). You are **not opted in by default**. **V**
- Software discovery models, custom software products, and custom publisher part numbers can be excluded via **Exclude from content service**. **V**
- In NSC DOD IL5 deployments, data can flow **only from ServiceNow to your organization**, not the reverse; you must create a content request manually. **V**
- Content Service is not a substitute for local normalization governance; it improves matching over time. **P**

---

## 9. Discovery model → software model matching

After normalization, the scheduled job **`SAM – Discovery Model to Software Model matching`** associates discovery models to software models:

- For each **normalized publisher + normalized product** pair, it finds software models with matching publisher and product. **V**
- It matches the **most specific** model first, then the **most generic** if no specific model exists. **V**
- A model with an **install condition** (or subscription condition / DB option) is not a match; if auto-create is enabled, a new model without an install condition is created. **V**
- On a match, the software-model reference is written to the **Software model** column on the discovery model. **V**
- A manual override unchecks **Automatically matched**; the job does not overwrite it. **V**

Version matching in the broader model relationship is exact first, then rounds down to the major version (`8.0.4` → `8.0`). **V**

A software model can cover multiple discovery models (for example, `Version starts with 10` covers 10.1 and 10.2). **V**

> **Correction:** the older "Display Name + Publisher + Version" fallback strategy is **C/U** — it is not in the Brazil pages. Use the job behavior above. See [`../CONFLICT_LOG.md`](../CONFLICT_LOG.md) C-21.

**Automatic model creation** is controlled by:

- `com.snc.samp.automaticsmrcreation` (licensable),
- `com.snc.samp.automaticsmcreation` (not licensable),
- `com.snc.samp.unlicensed_smr_creation` (unlicensed results). **V**

If a generic match exists, no model is created even when auto-create is enabled. If the properties are disabled, the job only matches. A model is created across versions and for the specific edition, if available, but **never against a specific version**. **V**

---

## 10. Normalization quality gates

Use these as onboarding gates, not SLAs:

| Gate | Target | Evidence |
|---|---|---|
| Top 10 titles normalized | 100% map to exactly one software model | Discovery-model status + software-model link |
| Overall normalization rate | ≥ 85% for SCCM-class sources before scaling | Normalization dashboard |
| After Content Service opt-in | ≥ 95% (Path-to-Value figure) | Trend over 2–4 weeks |
| `Match Not Found` backlog | Trending down | Status count by week |
| Manual normalization backlog | Owned and reviewed weekly | Queue age |

The 85%/95% figures are **P** (Path-to-Value), not product guarantees. **P**

---

## 11. Deduplication (summary)

Full detail is in [`03_DISCOVERY_TO_SAM_PIPELINE.md`](03_DISCOVERY_TO_SAM_PIPELINE.md) §5. Key facts:

- Dedup is per product and per device. **V**
- Levels: **Exact**, **Major** (default), **Any**. **V**
- Primary selection: source reliability → completeness → latest version. **V**
- Custom rules live in `sam_sw_dedup_rule`; the product must be normalized first. **V**
- Dedup fixes duplicate **installs**, not duplicate **CIs** or duplicate **software models**. **P**

---

## 12. Verification queries

```text
# Normalization status distribution
cmdb_sam_sw_discovery_model.list  (group by normalization_status)

# Models with no software model link
cmdb_sam_sw_discovery_model.list  (software_model is empty)

# Product type distribution
cmdb_sam_sw_discovery_model.list  (group by product_type)

# Dedup rules
sam_sw_dedup_rule.list

# Normalization suggestions
samp_normalization_suggestion.list

# Job health
samp_job_log.list  (filter Name starts with SAM)
sysauto_script.list (filter Name starts with SAM)
```

**V** for table names where stated; **U** for exact column API names in your release.

---

## 13. Common traps

| Trap | Effect | Fix |
|---|---|---|
| Enabling auto-model creation before normalization is stable | Many bad models | Wait for the normalization gate |
| Editing normalized fields on a `Normalized` model | Status flips to `Manually Normalized`; cannot revert | Use manual normalization deliberately |
| Assuming Edition is part of the discovery-model key | Wrong duplicate logic | Key is Publisher + Display Name + Version |
| Treating `New` as "normalized" | It is not manually eligible; wait for the job. Reconciliation gates on product type `Licensable`, not on this status | Wait for the normalization job |
| Leaving `Match Not Found` in the backlog | Under-counted demand | Manual normalize / pattern rule / Content Service |
| Pattern rule too broad | Wrong product mapping across titles | Sample-test before enabling; change control |
| Confusing vendor, publisher, PPN, model, catalog item | Wrong model links | See the six-layer model in the configuration reference |

**V/P.**
