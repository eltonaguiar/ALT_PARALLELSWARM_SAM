# Source Notes and Evidence Policy

> This file records what was read, how it was read, and what remains unverified. It is deliberately boring: it is the audit trail for the documentation.

---

## 1. Release pins

| Area | Release | Page update range |
|---|---|---|
| SAM | **Brazil** | 2025-07-31 → 2026-10-19 |
| IRE / CMDB | **Australia** | 2026-03-12 → 2026-03-24 |
| Public SAM guide | `ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM` | 2026-11-12 |

**Do not assume** a Brazil statement is true in Australia or vice versa. Where the two are mixed, the release is stated in the claim.

---

## 2. How the official SAM pages were fetched

The docs site is a single-page application; a headless browser is redirected to an ad tracker and renders an empty shell. The pages were read through the same public khub API the docs SPA uses:

```text
https://www.servicenow.com/docs/api/khub/maps/<map>/topics/<content_id>/content?target=DESIGNED_READER
```

- SAM map id: **`PMOYmdGTPDs40EbYh10h4g`** (Brazil). **V**
- Raw text extracts are retained in the repository's v1 research folder:
  `agents/grok-4.6__xai__kilo/SNC_SAM__WT1/research/raw/*.txt`
- The `_meta.json` in that folder maps each slug to its topic id and API URL. **V**
- IRE text extracts are retained in the sibling Discovery corpus:
  `/home/eaguiar2015/ALT_PARALLELSWARM/research/servicenow-discovery/sources/*.txt` (Australia). **V**

This pass did **not** re-fetch every page; it read the retained official extracts and cross-checked the disputed claims against the official page text embedded in them. That is sufficient for a documentary reference, not for an instance-level configuration audit. **U**

---

## 3. Official SAM pages used

Titles are the page titles in the Brazil map. Slugs are the retained extract names.

| Page title | Slug | Used for |
|---|---|---|
| Software Asset Management overview | `sam_overview` | Feature areas, normalization, reconciliation, optimization, downgrade rights |
| Components installed with Software Asset Management Professional | `components_installed_sam_pro` | Plugins, roles, jobs |
| Software Asset Management properties | `sam_properties` | Property inventory and defaults |
| Software discovery | `software_discovery` | Discovery → install → discovery-model business rule; SCCM plugins |
| Discovery models and software installations | `discovery_models_and_installs` | Primary key, version rounding, normalization statuses, revert |
| Discovery models fields | `discovery_models_fields` | Six statuses, product type, normalized fields |
| Software installation fields | `software_installation_fields` | Install → discovery model; edition override; suite fields |
| Software normalization | `software_normalization` | Normalization process, benefits, jobs, rule families |
| Software models and software entitlements | `software_models_and_entitlements` | Model vs entitlement; PPN resolution scenarios |
| Automatic creation of software models | `automatic_creation_of_software_models` | Auto-create properties and matching |
| Software license metrics | `software_license_metrics` | Metric groups and metrics |
| Impact of different license types on software reconciliation | `impact_license_types_on_recon` | License type behavior |
| Software reconciliation for compliance | `software_reconciliation_for_compliance` | Weekly default; grouping; upgrade note |
| Software reconciliation results | `software_reconciliation_results` | Three result tiers and related lists |
| Software license usage (License Workbench) | `software_license_usage` | Workbench tabs, rights buckets, calculations |
| Software model results license metric results fields | `software_model_results_lmr_fields` | Rights algebra, related lists |
| Software license compliance position | `license_compliance_position` | License Position report fields |
| Software install deduplication | `software_install_deduplication` | Dedup levels, primary selection |
| Create a custom deduplication rule | `create_custom_dedup_rule` | Dedup rule fields, `sam_sw_dedup_rule` |
| Delete uninstalled software from the Software Installation table | `remove_uninstalled_software` | REST Table API procedure; `sam_developer` |
| Exclude software assets on CIs | `exclude_software_assets_on_cis` | Exclude-CI column, property, job |
| View or create software usage | `view_or_create_software_usage` | `samp_sw_usage`; retired/stolen CI behavior |
| Software asset overview | `software_asset_overview` | Widget → source table map; alerts; `samp_reconciliation_result` |
| Software Asset Management health check | `sam_health_check` | Health Check categories; `SAM - Trigger Full Scan` |
| Maturity stages of your Software Asset Management program | `maturity_stages_sam` | Crawl / Walk / Run |
| Manage phase-wise Software Asset Management implementation | `phase_wise_implementation` | Published-products scope |
| Request Software Asset Management (and related) | `request_software_asset_management` | Store request context |
| Software Asset Management installation methods | `sam_installation_methods` | Installation context |

**V** for the titles and content used. Some pages were used only for a single claim; that is noted in the claim's status marker.

---

## 4. Official IRE pages used

| Page title | Used for |
|---|---|
| Identification and Reconciliation Engine (IRE) | IRE purpose, rule families, identifier keys, partial payloads, timestamps |
| Components and process of Identification and Reconciliation | Identification vs reconciliation, APIs, dedup/reclassification tasks |
| Discovery identifiers | Identifier rules, evaluation order, duplicate properties |
| How Discovery identifiers work | Identity probe → identifier → match/create |
| Reconciliation rules | Static vs dynamic, precedence, child override, domain separation |
| Create a CI reconciliation rule | Rule fields, priorities, null handling, filter conditions |
| Create an IRE data source rule | Insert gate, partial payload behavior, `INSERT_NOT_ALLOWED_FOR_SOURCE` |
| Properties for Identification and Reconciliation | IRE property defaults (`ire_properties.txt`) used in `02 §9` and matrix C13 |

**V** for the page content. The IRE pages are Australia; the SAM pages are Brazil. A release mismatch is possible and is called out in the text where it matters.

---

## 5. Secondary sources (corroboration only)

| Source | Used for | Status |
|---|---|---|
| `ALT_PARALLELSWARM` IRE applicability matrix (`results/.../IRE_RULE_APPLICABILITY_MATRIX.md`) | Truth table and permutation examples | **C** — corroborates the official pages; property defaults are cited to the official `ire_properties.txt` instead |
| v1 `final/FINAL_SAM_MODULE_REFERENCE.md` | Discovery → SAM flow, CI related list, manual normalization paths | **C** — Australia-pinned |
| v1 `final/FINAL_SAM_CONFIG_REFERENCE.md` | Plugin/role/job inventory, properties, reporting | **C** — mixed releases |
| v1 `agents/deepseek-flash__deepseek__kilo/05_FINAL/GUIDE_VS_REPO_DELTA.md` | Guide conflict list | **C** — re-verified where possible |
| Public SAM guide | Pedagogy, guide cross-reference | **C/P** — see corrections in `../GUIDE_CROSS_REFERENCE.md` |
| `direction-a-gaps.md` | Repo-vs-guide gap inventory | **C/P** |

The public guide is a learning asset, not an official source. Where it conflicts with the Brazil pages, the official page wins. The corrections are listed in [`../GUIDE_CROSS_REFERENCE.md`](../GUIDE_CROSS_REFERENCE.md).

---

## 6. Evidence policy

| Mark | Meaning |
|---|---|
| **V** | Directly stated in an official ServiceNow page read for this pass |
| **C** | Corroborated by a second independent source, or stated in a v1 doc that cites official pages; not re-read line by line |
| **U** | Unverified, instance-dependent, or release-dependent; a verification query or path is provided |
| **P** | Recommended practice or programme decision; not a product constraint |

**Rules:**

1. A label is not a column name. If only the UI label is documented, the API column is **U**.
2. A job cadence is not a schedule time. "Daily" does not mean 02:00.
3. A community term (for example "SUMN") is not an official term unless a fetched page uses it.
4. A custom `u_*` field is never presented as OOB.
5. A publisher rule is contract-specific until the publisher pack page says otherwise.

---

## 7. Known limits of this pass

- **No live instance.** Business-rule names, ACLs, UI actions, `sys_id`s, and exact column API names are **U**.
- **No re-fetch of every page.** Retained official extracts were used; the docs API was not re-crawled end to end.
- **Release mixing.** SAM is Brazil; IRE is Australia. Where behavior differs, the text states the release.
- **Publisher depth.** Oracle core factors, IBM PVU tables, SAP indirect access, and Microsoft virtualization rules are summarized, not reproduced. They are contract- and pack-specific. **U**
- **Container/Kubernetes licensing** is an explicit exclusion, not a solved capability. **U**
- **Private rubric.** The private grading rubric was not read. The QA in `../04_QA/QA.md` scores against the public plan, not the private rubric.

---

## 8. Reproduce the evidence

```bash
# List the official SAM extracts
ls agents/grok-4.6__xai__kilo/SNC_SAM__WT1/research/raw/

# Inspect the topic id / API URL map
cat agents/grok-4.6__xai__kilo/SNC_SAM__WT1/research/_meta.json

# Inspect the IRE extracts
ls /home/eaguiar2015/ALT_PARALLELSWARM/research/servicenow-discovery/sources/
```

**V** for the paths in this workspace; adjust for your clone.
