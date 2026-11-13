# SAM configuration reference — Brazil (SNC_SAM__WT1)

**Agent:** `grok-4.6__xai__kilo` · **Model:** `grok-4.6` · **Provider:** xAI · **Harness:** Kilo
**Release pin:** ServiceNow docs **Brazil** ITAM map `PMOYmdGTPDs40EbYh10h4g` (pages labelled *Updated Sep 10, 2026* unless noted).
**Evidence policy:** every non-obvious claim has `[S<n>]` → §23. No instance was available. OOB business-rule *sys_ids* are **UNVERIFIED**.

This is the SAM analog of the Discovery/CMDB swarm reference: options, order of operations, workspace breadcrumbs, insert-vs-update, plus catalog-vs-discovery paths and implementation-success.

---

## 0. Evidence policy + release scope

- Primary corpus: 45+ Brazil ITAM articles fetched via khub content API (same unlock as Discovery).
- Zurich / Yokohama ITAM maps exist (`1zMxrAxr2iK81FYv03BwFA`, `EdiPWhlSAqBiE0AMK4k9bQ`) and were **not** used as the pin.
- Community / Customer Success Center pages named by docs but not fetched here are tagged UNVERIFIED.
- `[verify on instance]` = needs a live `sam_admin` session.

---

## 1. Mental model

SAM is **not** Discovery and **not** the Service Catalog. Four records sit in a pipeline `[S14][S16]`:

```
Discovery / SCCM / SG connector / SaaS
        │  writes
        ▼
Software Installation  cmdb_sam_sw_install
        │  BR matches publisher+product+version  [S16]
        ▼
Discovery Model        cmdb_sam_sw_discovery_model   (primary key: Publisher, Display Name, Version)  [S14]
        │  normalize vs Content Library  [S8]
        ▼
Software Model         cmdb_software_product_model   (what you purchased / manage)
        │  entitlements  [S9]
        ▼
License position / reclamation / (optional) software catalog item
```

| Thing | What it is | What it is not |
|---|---|---|
| Software **installation** | One discovered copy on one CI | A license, a catalog item |
| Software **discovery model** | Deduped *discovered string* (publisher/display/version) | A purchasable model; **cannot be created manually** `[S14]` |
| Software **model** | Profile of software you purchased/manage (publisher, version criteria, discovery map) `[S9]` | A catalog item (until you *publish* it) |
| Software **catalog item** | Requestable item in the **service catalog** (Product Catalog) `[S27][S28]` | Automatic result of discovery |
| Entitlement | Rights you bought, linked to a software model `[S9]` | An install |

Foundation vs Professional vs SaaS LM `[S1][S38]`:
- **Professional:** Brazil/Australia installer `com.sn_samp_master_ws` (loads `com.sn_samp_master` + Workspace `sn_sam_workspace`). Pre-Australia: `com.sn_samp_master` → `com.snc.samp` + packs + `com.sn_samp_workbench`. Core plugin `com.snc.samp` is activated by ServiceNow personnel and may not appear in the plugin list.
- **Foundation / Basic (ITSM):** `com.snc.sams` (Australia UI: “Basic Software Asset Management”). Legacy Jakarta- `com.snc.software_asset_management`; upgrade to Pro is **irreversible**. Foundation normalization statuses are only **Manually Normalized** and **New** (no Content Library auto-norm).
- **SaaS LM:** Store `sn_sam_saas_int` (requires `com.snc.samp`). Creates **subscriptions**, not classic installs.

Brazil: classic SAM UI is limited-support; activating Workspace **hides** classic menus that moved, but several admin menus stay classic-only `[S18]`.

---

## 2. Data model / tables you will touch

| Table | Role |
|---|---|
| `cmdb_sam_sw_install` | Software installations `[S14][S16]` |
| `cmdb_sam_sw_discovery_model` | Discovery models. **Not** `samp_discovered_model` `[S8][S14][S38]` |
| `cmdb_software_product_model` | Software models (dedup rules require a normalized row here) `[S12]` |
| `alm_license` | Entitlements. **Not** `samp_sw_entitlement` `[S9][S38]` |
| `samp_license_metric_result` | License metric results (third recon tier) `[S38][S39]` |
| `samp_sw_usage` | Software usage (product level, not version/edition). **Not** `cmdb_sam_sw_usage` `[S40]` |
| `samp_sw_product` / `samp_sw_publisher` | Product / publisher (`samp_sw_publisher` must relate to `core_company`) `[S38]` |
| `alm_entitlement_user` / `alm_entitlement_asset` | User vs device allocations `[S38]` |
| `samp_dmap_downgrade_model` / `samp_sw_downgrade_model` | Content vs populated downgrade rights `[S9][S38]` |
| `sam_sw_dedup_rule` | Custom deduplication rules `[S13]` |
| `cmdb_ci_hardware` | Optional boolean column to exclude device from SAM `[S7][S4]` |
| `cmdb_ci_spkg` | Legacy Discovery-without-SAM packages; Foundation migrate copies → `cmdb_sam_sw_install` `[S38]` |
| Content Library / discovery maps / PPNs | Content Service `[S17]` |

Discovery models are **not** created when the install name contains `Security Update` `[S14]`.

---

## 3. Configuration surface (by where you set it)

| Where | What |
|---|---|
| Product Hub or Store | Install SAM `[S20]` |
| Plugin `com.sn_samp_master_ws` | Professional + Workspace in one step (Brazil) `[S1][S18]` |
| `All > Software Asset > Administration > Properties` | SAM properties (also Configuration Console) `[S4]` |
| Software Asset Workspace | Day-to-day: license ops, content, custom products, recon, published products `[S18][S22]` |
| Classic leftover menus | Properties, Content Service Setup, Pattern Normalization Rules, Reclamation Rules, Custom Products/PPNs/metrics, SaaS profiles, SAP connections `[S18]` |
| `All > Product Catalog > …` | Publish/link software **catalog** items (this is HAM/Product Catalog, role `model_manager` / `catalog_admin`) `[S27][S28][S29]` |
| Hardware table + property `com.snc.samp.exclude_device_flag` | Exclude CIs `[S7]` |
| Content Service Setup | Opt-in, data-type toggles, exclude-from-content-service flags `[S17]` |
| Publisher pack plugins | Adobe, Citrix, IBM, Microsoft, Oracle, SAP, VMware, Engineering `[S1]` |

---

## 4. Order of operations

### 4A. Setup sequence (implementation)

1. Healthy **CMDB** + discovery coverage (maturity Crawl: “establish a healthy CMDB, identify tools to discover data, establish processes and roles”) `[S21]`.
2. Install SAM (Product Hub first-time / Store otherwise) `[S20]`.
3. Activate Professional + Workspace plugin `[S1][S18]`. Request SaaS LM / Spend Detection / publisher packs only if in scope `[S1]`.
4. Opt in to **Content Service** (default is **not** opted in) `[S17]`.
5. Wire discovery sources (Discovery plugin + patterns; SCCM or Service Graph connector for SCCM — 2012/2016 usage plugins deprecated toward Tokyo) `[S16][S1]`.
6. Load **entitlements** (bulk import / PPN matching) `[S9][S16]` — docs explicitly say discover *after* entitlements for the Discovery/SCCM path `[S16]`.
7. Let daily jobs normalize discovery models `[S8]`.
8. Create custom products / pattern rules / manual normalize for Match Not Found `[S8][S10]`.
9. First **reconciliation**. Enable auto software-model creation properties only if you want unlicensed models created `[S5][S4]`.
10. Optionally enable `com.snc.samp.manage.published.products` and publish a **small product set** (phase-wise) `[S22][S4]`.
11. Reclamation rules, then catalog publish for requestable software (Run-stage: “standard catalog and onboarding process”) `[S21][S15]`.
12. Success portal: goals, health check, maturity items `[S23]`.

### 4B. Runtime pipeline (one install)

1. Source writes a row to `cmdb_sam_sw_install` `[S16]`.
2. **Business rule** (unnamed in docs): if publisher+product+version exists on a discovery model, set the reference; else insert a discovery model and set the reference `[S16]`.
3. Daily `SAM - Normalize discovery models using content library rules` assigns a normalization status `[S8]`. Fallback: wide-net (`com.snc.samp.wide_net_normalization.enabled`, default on) then ML (`com.snc.samp.enable.ml_normalization`, default on) `[S4]`.
4. Job **SAM – Discovery Model to Software Model matching** writes the software model onto the discovery model (most specific match wins; manual set ⇒ Automatically matched = false, job will not override) `[S38]`.
5. Reconciliation matches installs → software models → entitlements; may auto-create software models if properties allow `[S5]`.
6. Dedup job marks primary vs duplicate installs `[S11][S12]`. IBM special case: `SAM - Deduplicate Install Table` prefers ServiceNow Discovery over authorized provider for IBM `[S11]`.
7. Reclamation rules flag unused rights `[S15]`.
8. `SAM — Adjust Installs for excluded CIs` honors the exclude-device flag `[S7]`.

---

## 5. Breadcrumbs

**Workspace:** `Workspaces > Software Asset Workspace` `[S18]` or `All → Software asset → Software Asset Workspace` `[S38]`. Views: Software asset overview, License usage, License operations, Software asset analytics, Success portal, Renewals calendar, Overlapping usage, Content Library portal `[S38]`.

| View | Path / contents |
|---|---|
| License operations | Custom software products: `Content > Custom software products` `[S10]` |
| License operations | Dedup rules: `Administration > Deduplication rules` `[S13]` |
| License operations | Published products: `SAM Implementation > Published products` `[S22]` |
| Success portal | `Software Asset Workspace > Success portal` `[S23]` |
| Classic properties | `All > Software Asset > Administration > Properties` `[S4]` |

**Classic-only even after Workspace** `[S18]`: Custom Products, Custom part Numbers, Custom License Metrics, Pattern Normalization Rules, Reclamation Rules, Job Results, Content Service Setup, Properties, SaaS integration profiles, SAP connections.

**Software catalog (not SAM workspace):**
- `All > Product Catalog > Catalog Definition > Vendor Items` — Publish / Link to Software Catalog (`model_manager`) `[S27][S28]`
- `All > Product Catalog > Product Model > All Models` — Publish to Software Catalog (`catalog_admin`) `[S29]`

---

## 6. Discovery sources that feed SAM

- ServiceNow **Discovery** (plugin required); base patterns cited: Citrix XenApp/XenDesktop, VMware vCenter, Microsoft SQL Server, Microsoft Exchange Server, Oracle Database `[S16]`.
- **SCCM** 2012 v2 / 2016 integration + usage plugins; docs push **Service Graph connector for Microsoft SCCM** for new work; 2012/2016 usage plugins deprecated in Tokyo `[S1][S16]`.
- Other third-party via CMDB / Store apps; “add it manually” points at Customer Success Center **UNVERIFIED** (not fetched) `[S16]`.
- SaaS: Store plugin `sn_sam_saas_int`; creating a direct integration profile **auto-creates a reclamation rule** `[S1][S15]`.
- File Signature Normalization plugin `com.snc.file_signature_normalization` (also with File-based Discovery `com.snc.discovery.file_based_discovery`); matched files write `cmdb_sam_sw_install`. Library file-signature rules **beat** custom file rules `[S1][S38]`.
- **ILMT / BigFix Inventory** via IBM pack; new integrations use **v2** APIs `[S38]`.
- Generic 3rd-party: IRE REST related `cmdb_sam_sw_install` on a computer CI; enable `com.snc.samp.ire.datasource.integration`; role `sam_developer`. Payload keys: `publisher`, `version`, `display_name` (+ optional edition); parent CI identified by `name`; send `sys_class_name` so the CI is not reclassified `[S38]`.
- Uninstalls are **not** auto-deleted from `cmdb_sam_sw_install`; 3rd-party must DELETE via Table API (`installed_on` query) `[S38]`.
- Intune / Jamf are Service Graph CMDB connectors; SAM discovery pages do **not** list them as native SAM install sources `[S38]`.
- Agent Client Collector / GRC / APM / Contract Management Pro are named as companion products, not sourced in depth here.

---

## 7. Installations + discovery models — insert vs update

**Discovery model primary key:** Publisher + Display Name + Version `[S14]`.

Version matching: exact version first, else round down to major (e.g. 8.0.4 → 8.0) `[S14]`.

**Install insert path:** Discovery writes `cmdb_sam_sw_install`; BR looks up discovery model; insert model if missing `[S16]`. Discovery models **cannot** be created in the UI `[S14]`.

**Install fields that matter** `[S30]`: Display name, Discovery model, Publisher, Version, Edition Override (editable when edition not discovered — needed for recon), Installed on, Install location/date, Instance key.

**Duplicates:** same publisher/product/version/edition from **multiple sources** create multiple install rows `[S11]`. Brazil dedup: detect by version-matching level, then pick primary by (1) discovery-source reliability (2) information completeness (3) latest version `[S12]`. Custom rule table `sam_sw_dedup_rule`; product must already be a **normalized software model**; default version level **Major** `[S12][S13]`.

IBM: ServiceNow Discovery rows stay Active; authorized-provider duplicates inactivated by `SAM - Deduplicate Install Table` `[S11]`.

---

## 8. Normalization / Content Service / pattern rules / custom products

**Statuses named in docs** `[S8][S17][S38]`: Normalized (publisher+product+version; or publisher+product if type Not Licensable/Child/Driver/Patch), Partially Normalized (publisher+product, version editable), Publisher Normalized (publisher only), Match Not Found, Manually Normalized, **New** (not yet run). Partial/publisher-normalized are **not** later filled to a full version. Recon only considers product type **Licensable**, and **License under management** must be selected `[S38]`.

Daily job: `SAM - Normalize discovery models using content library rules`. Dashboard job: `SAM - Discovery Model Normalization job` `[S8]`.

Rule families (SAM analog of IRE’s four) `[S8]`:
1. Product Map / Package Map (Content Service; one rule per distinct discovery model)
2. Pattern normalization (one rule, many models)
3. Enhanced pattern normalization (edition/version variants, include/exclude terms)
4. Wide-net normalization (eligible products only; property default enabled)

Plus ML normalization plugin `com.sn_sam_ml_normalization` `[S8]`.

Manual normalize allowed when Partially / Publisher / Match Not Found `[S8]`. **Cannot revert** Manually Normalized or pattern-normalized models `[S8]`.

**Custom product** (before Content Library has it): Workspace `License operations > Content > Custom software products`, role `sam_admin`. Product types: Child (not licensable), Driver, Licensable, Not Licensable, Patch, Unknown `[S10]`. `Exclude from content service` keeps it local; otherwise a content request is sent and a **product suggestion** is generated to consolidate `[S10]`.

Content Service **default off**. Sharing discovery models with statuses Match not found / Publisher normalized / Partially / Manually / (Normalized with empty version) `[S17]`. Property typo in docs: `com.snc.samp.ml.overrride_ml_model_version` (three r’s) `[S17]` — quote both if an instance shows a different spelling.

---

## 9. Software models, products, entitlements

Software model = purchased/available profile; many discovery models can map to one model via version criteria (“Starts with 10”) `[S14][S9]`.

Auto-create during recon `[S5][S4]`:
| Property | Default | Effect |
|---|---|---|
| `com.snc.samp.automaticsmrcreation` | (enable to use) | Auto software model for **licensable** unlicensed product results |
| `com.snc.samp.automaticsmcreation` | No | Auto software model for **not licensable** (APM) |
| `com.snc.samp.unlicensed_smr_creation` | False | Software *model results* for unlicensed models |

Match attributes before create: version, edition, language, platform, install condition. Model is created **across versions** for a specific edition; **never against a specific version** `[S5]`. `Created source = System property` in list view flags auto-created `[S5]`. Discovery map attached only if Content Library has one `[S5]`.

Entitlement import: PPN → Content Library → software model. Blank PPN: exact then relaxed (any platform/language) match; else auto-create if property on `[S9]`. Multiple models for one PPN → error, user must choose `[S9]`.

---

## 10. Four paths (do not collapse)

### Path A — Add software to the **service / software catalog** (requestable)

This is Product Catalog, not normalization.

1. Create/open a **product model** (`catalog_admin`): `All > Product Catalog > Product Model > All Models` → Related Link **Publish to Software Catalog** → pick category. Currency: `glide.model.catalog_item_currency` default `false` = user session currency `[S29]`.
2. Or from a **vendor catalog item** (`model_manager`): add a software (or consumable) model to Product Model, leave Product Catalog Item blank → **Publish to Software Catalog** `[S28]` or **Link to Software Catalog Item** `[S27]`. After publish, the publish link disappears; vendor-item edits sync to the catalog `[S28]`.

Maturity **Run** expects this as the standard onboarding/purchasing path `[S21]`.

### Path B — Create software in SAM **before any discovery**

Use when the contract exists but nothing is installed yet (SaaS, future deploy, entitlement-first).

1. If the product is not in Content Library: **custom software product** `[S10]`.
2. Create **software model** (workspace or classic) `[S9]`.
3. Create/import **entitlement** (PPN if you have one) `[S9]`.
4. Discovery later attaches installs → discovery models → this software model.

Do **not** wait for auto-create (`automaticsmrcreation`) if you need downgrade rights / discovery maps / catalog publish first.

### Path C — Discovered software **linked** to a SAM model (and maybe catalog)

1. Install row written `[S16]`.
2. Discovery model keyed by Publisher + Display Name + Version `[S14]`.
3. Normalize (content / pattern / wide-net / ML / manual) `[S8]`.
4. Reconciliation associates discovery models to software models by version/edition criteria `[S14][S5]`.
5. Optional: publish that software model to the software catalog (Path A). Linking to catalog is **not** automatic from discovery.

### Path D — Block / exclude / do not manage

| Mechanism | What it blocks | Where |
|---|---|---|
| Hardware boolean + `com.snc.samp.exclude_device_flag` + job `SAM — Adjust Installs for excluded CIs` | All software on that CI from SAM compliance | Properties + `cmdb_ci_hardware` `[S7][S4]` |
| Phase-wise published products (`com.snc.samp.manage.published.products`, default **false**) | Reports/dashboards to *unpublished* products (overview + license usage) | Workspace Published products `[S22][S4]` |
| Custom product `Exclude from content service` | Sharing that product with ServiceNow | Custom product form `[S10][S17]` |
| Discovery model / custom PPN exclude-from-content-service | Sharing that row | Content Service `[S17]` |
| Deactivate Normalization Library content version | That content version’s rules | Content Service `[S17]` |
| Name contains `Security Update` | Discovery model never created | Hard-coded `[S14]` |
| Leave `automaticsmrcreation` off | No auto software model for licensable unlicensed installs | Properties `[S5]` |
| Dedup marking Active=false | Duplicate install excluded from recon | Dedup job `[S11]` |
| Pattern rule / ignore UNVERIFIED | Docs do not describe a global “block this publisher from insert” IRE-style data source rule | — |

---

## 11. Entitlements, allocations, license metrics

Entitlement records rights on **`alm_license`**; allocations are `alm_entitlement_user` or `alm_entitlement_asset` (metric picks one list, not both). Total allocation qty cannot exceed entitlement rights `[S9][S38]`. Role `sam_admin` required to import entitlements `[S1]`. State **build** until **Publish** → **in use** (eligible for recon) `[S38]`.

License types `[S38]`: Perpetual, Perpetual+SA, SA, Subscription, Step-up, Subscription Step-up, Add-on, From SA. SaaS default type Subscription, metric User Subscription. Enterprise/ULA/ELA/ETLA/SCE stay **Compliant** even with unlicensed installs.

Reclamation rule types `[S38]`: Total Usage Time (default), Last Used Date, Peak Concurrent Usage (eng apps), Active Transaction Codes (SAP). Role `sam_admin`. Removal candidates: classic `All → Software Asset → Removal Candidates`; role `sam_user`.

Microsoft-specific: License Duration Contractual needs start/end; step-up license type **Microsoft only** `[S9]`.

License metrics: large publisher-specific catalog in `software_license_metrics` topic `[S31]` (IBM PVU/RVU, Oracle, SAP named user, Citrix, unlimited licenses, etc.). Full metric enum is **not** copied here; see `[S31]`.

Allocation management is its own 8k article `[S32]` — treat as a follow-on worktree if depth is needed.

---

## 12. License reconciliation

Recon runs **weekly or on demand**. Results are **three tiers**, not a single `sam_sw_reconciliation_result` table (that curriculum name is UNVERIFIED) `[S39]`:

| Tier | What it covers | Nav |
|---|---|---|
| Product Results | All models/installs for a product+publisher; true-up, over-licensed, potential savings. Generated for licensable products even without software models | Classic: `All > Software Asset > Reconciliation > Historical Results`. Workspace: `License usage` → publisher card `[S39]` |
| Software Model Results | One row per software model **only if** a software model or entitlement exists | Related list on Product Results `[S39]` |
| License Metric Results | One row per metric on that model (`samp_license_metric_result`). Two LMRs / two license-position reports if perpetual-SA + subscription on the same model | Related list on Software Model Results `[S39][S41]` |

License Position report software-model status is **Compliant** (green) or **Not Compliant** (red) `[S35]`. Curriculum “Unknown / Over-licensed / Unlicensed” are *interpretations* of rights needed / unlicensed installs / over-licensed amount — not extra status dots on this form.

Rights breakdown on LMR `[S41]`: allocated in use, not allocated in use (remediation: Create Allocations / Remove Unallocated Installs), allocated not in use (Remove Allocations), not allocated, allocations needed (Per Named User/Device only).

**Maintenance ≠ license:** SAM does **not** reconcile Software Assurance or Maintenance entitlements unless they are linked to a base perpetual license `[S42]`. Perpetual alone has no upgrade/BYOL/SA benefits until SA/maintenance is associated.

Properties `[S4]`:
- `com.snc.samp.recon.group` / `com.snc.samp.recon.subgroup` — default None; Company/Cost Center/Country/Department/Region; group ≠ subgroup
- `com.snc.samp.recon.enablecustommetrics` — default Yes
- `com.snc.samp.debug` — default No (perf hit)
- `com.snc.samp.recon.max_workers` — parallel publisher jobs
- Oracle pack: `com.snc.samp.oracle.reconlevel` (ESX / **ESX cluster default** / vCenter(s)); `com.snc.samp.oracle.hostaffinityenabled`

Run recon after changing published-product list or the manage-published-products property `[S22]`.

---

## 13. Reclamation + request flows

Reclamation rules aggregate usage over time (hours / latest date) `[S15]`. Suite parent pulls components automatically; filter on parent applies to children `[S15]`. SaaS/SSO integration **auto-creates** a reclamation rule — review it `[S15]`.

Usage evidence lives on **`samp_sw_usage`** (product-level). Role `sam_admin` or `sam_user`. Workspace: `License operations > Discovery > Software usage`. Reclamation type Total Usage Time (month/year/count/seconds) or Last Used Date. If the CI Hardware/CI Status becomes **Retired or Stolen**, related **installs are deleted** `[S40]`.

Timeout property: `sam_reclamation_flow_error_timeout` default **30 days** then Closed canceled `[S4]`.

Classic leftover: Reclamation Rules menu `[S18]`. Workspace: create removal candidates; catalog request to reclaim `[S33]`. Software request workflow is a separate 7.9k article `[S34]`.

Orchestration Client Software Distribution plugin: SAM Pro license covers **uninstall/reclamation only**; install/distribution needs extra license `[S1]`.

---

## 14. OOB components (roles, plugins, jobs — not a full BR dump)

“Components installed with Software Asset Management Professional” lists **roles, plugins, scheduled jobs, demo data**. It does **not** enumerate business rules, UI policies, or client scripts `[S1]`. Named platform objects from other articles:

**Roles** `[S1]`: `sam_admin` (contains `sam_user`, `sam_spend_import`, `asset`, `model_manager`, `contract_manager`); `sam_user`; `sam_developer` (script privileges; must be trained admin); `sam_integrator` (SaaS profiles; `connection_admin`, `flow_operator`); `sam_spend_import`.

**Find jobs:** Scheduled jobs filter `Name starts with SAM` `[S1]`. Jobs named in this corpus:
- `SAM - Normalize discovery models using content library rules` (daily) `[S8]`
- `SAM - Discovery Model Normalization job` (daily, dashboard) `[S8]`
- `SAM – Discovery Model to Software Model matching` `[S38]`
- `SAM- Create downgrades/upgrades for a software entitlement` (weekly) `[S38]`
- `Download software content: Downgrade Rights` (weekly) `[S38]`
- `SAM - Deduplicate Install Table` `[S11]`
- `SAM — Adjust Installs for excluded CIs` `[S7]`
- `SAM - Label Spend Transactions` (spend prediction; `samp.spend_prediction_service.max_label_attempts` default 3) `[S4]`
- Weekly reconciliation (default; also on-demand) `[S4][S38]`

**Documented business rule (unnamed):** on insert to `cmdb_sam_sw_install`, match or create discovery model by publisher+product+version `[S16]`.

**Flows:** reclamation flow (error timeout property) `[S4]`; software request workflow `[S34]`; reclaim catalog request `[S33]`. Individual flow names/sys_ids **UNVERIFIED**.

**UI policies / client scripts:** not listed in the components article → **UNVERIFIED**. `[verify on instance]` `sys_ui_policy` / `sys_script` filtered by `sam` / `samp`.

**Extension points (safe to add, not overlay OOB):** custom products, pattern normalization rules, custom license metrics, custom PPNs, custom dedup rules, reclamation rules, published-product list.

---

## 15. Duplicate-prevention playbook + insert-vs-update table

| Incoming | Match key | Insert if | Update if | Control that can stop insert |
|---|---|---|---|---|
| Software install | source-specific; dups allowed across sources `[S11]` | new row always possible | same source refresh **UNVERIFIED** | exclude-device flag `[S7]`; dedup sets Active=false `[S11]` |
| Discovery model | Publisher + Display Name + Version `[S14]` | BR finds no model `[S16]` | BR finds model, sets reference `[S16]` | name contains Security Update `[S14]`; cannot create manually `[S14]` |
| Software model | version/edition/language/platform/install condition `[S5]` | no match and auto-create property on `[S5]` | recon uses existing | leave auto-create **off**; phase-wise doesn’t block create, only reporting `[S22]` |
| Entitlement | PPN or publisher+product+version+edition+platform+language `[S9]` | import creates | PPN maps to existing model | PPN errors; MLS blank-PPN won’t invent a model `[S9]` |
| Catalog item | vendor item / model publish `[S27][S28][S29]` | publish/link | vendor-item sync after publish `[S28]` | don’t publish |

Causes of “second install / second model” `[S11][S12][S5]`:
1. Two discovery sources, no dedup yet
2. Version-level Exact vs Major mismatch
3. Auto-create software models while a close-but-not-exact model already exists
4. Custom product not consolidated with Content Library suggestion `[S10]`
5. Security Update skipped (missing model, not a duplicate)

---

## 16. Types inventory

| Kind | Values sourced |
|---|---|
| Normalization status | Normalized, Partially Normalized, Publisher Normalized, Match Not Found, Manually Normalized `[S8]` |
| Custom product type | Child, Driver, Licensable, Not Licensable, Patch, Unknown `[S10]` |
| Dedup version level | Exact / Major (default) / Any `[S12][S13]` |
| Recon group | None, Company, Cost Center, Country, Department, Region `[S4]` |
| Oracle recon aggregation | ESX, ESX cluster (default), vCenter(s) `[S4]` |
| Maturity | Crawl, Walk, Run `[S21]` |
| Success goal status | Draft, In Progress, Pending Review, Completed, Canceled `[S23]` |
| Publisher packs | Adobe, Citrix, IBM, Microsoft, Oracle, SAP, VMware, Engineering Apps `[S1]` |
| Content Service data types | Discovery models, lifecycles, part numbers/discovery maps, processor names, product license exception rules `[S17]` |

License metric types: see `[S31]` (too large to duplicate; do not invent names).

---

## 17. System properties (named + default where documented)

Nav: `All > Software Asset > Administration > Properties` `[S4]`.

| Property | Default (docs) | Effect |
|---|---|---|
| `com.snc.samp.recon.group` | None | Weekly recon grouping |
| `com.snc.samp.recon.subgroup` | None | Secondary grouping |
| `com.snc.samp.recon.enablecustommetrics` | Yes | Apply custom metrics |
| `com.snc.samp.debug` | No | Recon + on-prem import debug |
| `com.snc.samp.automaticsmrcreation` | (opt-in) | Auto SM for licensable unlicensed |
| `com.snc.samp.unlicensed_smr_creation` | False | SMR rows for unlicensed |
| `com.snc.samp.automaticsmcreation` | No | Auto SM for not-licensable |
| `com.snc.samp.exclude_device_flag` | (empty) | Hardware boolean column name |
| `com.snc.sam.auto_suite_inference` | false | Map installs to suite entitlement |
| `sn_sam_workspace.sam_license_operations_list_count` | 5000000 | List count cap |
| `com.snc.samp.citrix.app.license.period` | 90 | Citrix pack |
| `sam_reclamation_flow_error_timeout` | 30 | Reclamation flow cancel |
| `com.snc.samp.eng.app.peak.usage.period` | 30 | Engineering pack |
| `com.snc.samp.recon.max_workers` | (unset in snippet) | Parallel recon jobs |
| `com.snc.samp.wide_net_normalization.enabled` | enabled | Wide-net fallback |
| `com.snc.samp.enable.ml_normalization` | enabled | ML fallback |
| `com.snc.samp.sam_ci_billing_threshold` | 30 | Cloud Insights billing age |
| `com.snc.samp.windowserver.license.threshold` | 4.59 | MS Windows Server pack |
| `sn_samp_ibm_lic.default_region` | North America and South America | IBM pack |
| `sn_samp_ibm_lic.ilmt_api_version` | (version picker) | ILMT/BigFix API |
| `com.snc.samp.sqlserver.standard_sa.to.enterprise_sa.cost.ratio` | 0.25 | SQL pack |
| `com.snc.samp.ms.sa.to.nonsa.cost.ratio` | 1.25 | SQL SA pack |
| `com.snc.samp.use_lifecycle_approximation` | enabled | Lifecycle report |
| `com.snc.samp.generate.calculated.lifecycles` | (opt-in) | Calculated EOS/EOES/EOL |
| `com.snc.samp.manage.published.products` | false | Phase-wise published products |
| `samp.spend_prediction_service.max_label_attempts` | 3 | Spend labelling |
| `glide.model.catalog_item_currency` | false | Catalog item currency from model vs session `[S29]` |
| `com.snc.samp.ml.overrride_ml_model_version` | (override) | ML model version; spelling as in docs `[S17]` |
| `com.snc.samp.oracle.reconlevel` | ESX cluster | Oracle pack |
| `com.snc.samp.oracle.hostaffinityenabled` | (opt-in) | Oracle pack |

RHEL Virtual Datacenters threshold default **3.2** (property display name in docs; programmatic name not printed in the fetched table) `[S4]` — UNVERIFIED name.

---

## 18. Verification

- Normalization and content dashboard `[S8]`
- License position / true-up cost articles `[S35][S36]`
- Health check scan `[S23]`
- Success portal widgets: SAM maturity, completed goals, savings, health checks passed, value builder tasks `[S23]`
- Software model list `Created source` column `[S5]`
- Install Active flag after dedup `[S11]`
- `[verify on instance]` Scheduled jobs `Name starts with SAM`

---

## 19. Anti-patterns

- Treating a **discovery model** as a catalog item, or a **catalog item** as a license `[S14][S27]`
- Discovering before entitlements if you wanted PPN-driven models first `[S16][S9]`
- Customizing OOB recon jobs instead of properties / custom metrics
- Enabling `automaticsmrcreation` then wondering why extra software models appeared `[S5]`
- Rolling out all publishers on day one instead of published-products phase-wise `[S22][S21]`
- Skipping Content Service opt-in then drowning in Match Not Found `[S17]`
- New SCCM work on deprecated 2012/2016 usage plugins `[S1]`
- Overlaying the unnamed install→discovery-model business rule `[S16]`
- Publishing to software catalog with `model_manager` vs `catalog_admin` mixed up `[S27][S29]`
- Assuming Workspace activation still leaves classic SAM navigation `[S18]`

---

## 20. META — successful SAM implementation

### Foundational data (Crawl) `[S21][S16][S7]`

Must already be true, or SAM reports garbage:

1. **CMDB hardware/computer CIs** with enough identity for Discovery/SCCM to land installs (`installed_on`).
2. **Owners / location / department / cost center / company / country / region** on those CIs if you will group recon by them `[S4]`.
3. **User records** if you allocate per-user or reclaim SaaS seats.
4. **Discovery actually covering the estate** (Discovery and/or SCCM/SG connector), not a spreadsheet `[S16]`.
5. **Entitlement source of truth** (contracts, PPN, Microsoft MLS) ready to import `[S9]`.
6. **In-scope publisher list** (packs cost money and complexity) `[S1]`.
7. Decision on **exclude-from-SAM** devices (leased, out of scope, phase-1 location only) `[S7]`.

### Baseline metrics to capture *before* go-live

Docs do not publish numeric SLO targets. Capture these on day 0 so Success portal / health check have a before/after `[S23][S8]`:

| Metric | Why |
|---|---|
| Discovery-model count by normalization status | Content Service value `[S8][S17]` |
| Install count vs unique products vs unique software models | Dedup / auto-create health `[S12][S5]` |
| Unlicensed product-result count | True-up `[S5][S36]` |
| % CIs with owner/location | Recon grouping `[S4]` |
| SaaS assigned vs used (after connector) | Reclamation `[S15]` |
| Time of last successful recon | Operating cadence |
| Published-product count if phase-wise | Scope freeze `[S22]` |

After go-live, Success portal tracks completed goals, actual vs projected savings, health checks passed, value-builder tasks, Crawl/Walk/Run maturity items `[S23]`.

### Phase-wise plan (official)

Maturity `[S21]`:
- **Crawl:** healthy CMDB, discovery tools, processes/roles; start with end-user computing or simple SaaS.
- **Walk:** automate Crawl processes; datacenter / BYOL / more SaaS; metering, reclamation, overlapping software, rightsizing from compliance results.
- **Run:** standardized catalog + onboarding in purchasing; automated on-demand software; regular SAM goals.

Product-scope freeze: enable `com.snc.samp.manage.published.products`, add licensable products under License operations → SAM Implementation → Published products, **re-run recon** `[S22]`. Suite publish warns to include parent/children `[S22]`.

Guided path: Product Hub install → Workspace → Content Service → discovery → entitlements → recon → success portal `[S20][S19][S23]`.

### Operating model

Roles: `sam_admin` for imports/recon/content/reclamation; `sam_user` for analysis; `sam_integrator` for SaaS; `sam_developer` only for trained script work `[S1]`. Success goals assign to owner/group with email on assign / pending review `[S23]`.

### Path to Value / Office Hours (community corroboration, not Brazil product docs) `[S37]`

- **80% process and governance, 20% tool.** Configuring plugins without RACI is the main failure mode.
- Sequence: CMDB health → EUC discovery (Service Graph: SCCM/MECM, Intune, Jamf, Tanium) → normalize → entitlements → recon as a *data-quality loop*, not a true-up invoice.
- Normalization hit-rate claimed **~85%+** OOTB on SCCM-class sources, **95%+** after Content Service opt-in. Treat as a Path-to-Value figure, not an SLA.
- **Leave `com.snc.samp.automaticsmrcreation` off in Crawl** so the software-model table stays curated (Office Hours). This matches §10 Path B vs auto-create.
- Do **not** attach both SSO and a direct SaaS integration to the same app.
- ~80% of spend sits in a few publishers (Microsoft, VMware, Adobe, Oracle, IBM, SAP, Salesforce) — that is the MVP freeze list.
- Datacenter / publisher packs are **Walk**, not day one. Acting on first recon as a purchase order is an anti-pattern.
- Partners: Now Create SAM Success Pack (login-gated; not fetched).

---

## 21. META — successful ServiceNow module implementation in general

SAM’s Crawl/Walk/Run is the vendor’s module-success pattern `[S21]`. Applied generally:

1. **Process and roles before plugins.** Crawl text starts with CMDB + processes + roles, not “turn on every pack” `[S21]`.
2. **Data foundations.** Every ITOM/ITAM module writes through CMDB; SAM’s exclude-CI and recon grouping are useless without CI attributes `[S7][S4]`.
3. **Baseline KPIs before configuration.** Success portal is pointless without a before-state `[S23]`.
4. **Scope freeze / MVP.** Published products are the SAM instance of “do not boil the ocean” `[S22]`.
5. **Know OOB vs extension points.** Use properties, custom products, pattern rules, dedup rules; do not overlay the install BR `[S16][S1]`.
6. **Hypercare jobs.** Know the scheduled-job filter (`Name starts with SAM`) on day 1 `[S1]`.
7. **Catalog last, not first.** Run-stage catalog onboarding comes after discovery/recon work `[S21]`. Path A is a purchasing UX, not a license database.

---

## 22. Open questions (UNVERIFIED)

1. Exact *name* of the install→discovery-model business rule and any UI policies on `cmdb_sam_sw_install`.
2. Remaining `samp.*` properties not on the Properties page table `[S4]`. **`glide.cmdb.sam.*` is not an official family** (Australia properties page) `[S38]`.
3. IRE identifier attributes for `cmdb_sam_sw_install` itself (serial / `instance_key` / `discovery_source` as uniqueness). ISO serial is a form field, not a documented match key `[S38]`.
4. Discovery-source reliability ranking used by dedup primary selection `[S12]`.
5. Exact table names for removal candidates / reclamation rules (UI modules only) `[S38]`.
6. Entitlement unique index (PPN + metric + company, etc.) — docs warn on PPN mismatch, no published unique key `[S38]`.
7. RHEL threshold property *internal name* `[S4]`.
8. Whether `com.snc.samp.ml.overrride_ml_model_version` is a docs typo `[S17]`.
9. Now Create / Success Checklist PDFs (login-gated).
10. Zurich/Yokohama deltas vs this Brazil pin. A **role named “analyst”** is not documented; use `sam_user` `[S38]`.

---

## 23. Source ledger

Brazil ITAM map `PMOYmdGTPDs40EbYh10h4g`. Content URL pattern:
`https://www.servicenow.com/docs/api/khub/maps/PMOYmdGTPDs40EbYh10h4g/topics/<id>/content?target=DESIGNED_READER`

| ID | Topic | Local file |
|---|---|---|
| S1 | `s5fH~A1sUUyDzngPzlKmoA` Components installed with SAM Professional | `research/raw/components_installed_sam_pro.txt` |
| S4 | `wlowLFRyzTKG~aYlKoWGrQ` SAM properties | `research/raw/sam_properties.txt` |
| S5 | `YdVZA9~1YsBKai3GydfjJA` Automatic creation of software models | `research/raw/automatic_creation_of_software_models.txt` |
| S7 | `R~CU_~6K11G9N63vdhdQWg` Exclude software assets on CIs | `research/raw/exclude_software_assets_on_cis.txt` |
| S8 | `GAqHdgqn0gug8rl5B76dyg` Software normalization | `research/raw/software_normalization.txt` |
| S9 | `zi3EfIdp~5LlvSHt7BRxKw` Software models and entitlements | `research/raw/software_models_and_entitlements.txt` |
| S10 | `yUYtBYnrAlpWRL9jsnCm~g` Add custom software products in workspace | `research/raw/add_custom_software_products_workspace.txt` |
| S11 | `zFgm8oWPo81mqLn7665rlA` Duplicate software installations | `research/raw/duplicate_software_installations.txt` |
| S12 | `g2vJ_yZvxLks~NfUSm6NCw` Software install deduplication | `research/raw/software_install_deduplication.txt` |
| S13 | `dZMVh50f2PI16cqrLVlo9A` Create a custom deduplication rule | `research/raw/create_custom_dedup_rule.txt` |
| S14 | `dQyVDoW8zEmzF_zQvv_7dg` Discovery models and software installations | `research/raw/discovery_models_and_installs.txt` |
| S15 | `G_ROnN2e7dWK~A768krQWQ` Software reclamation rules | `research/raw/software_reclamation_rules.txt` |
| S16 | `14CNM8vUS0aV7EE9TGFLeQ` Software discovery | `research/raw/software_discovery.txt` |
| S17 | `WwxD09ptVyD8cbEzLYjEmg` SAM Content Service | `research/raw/sam_content_service.txt` |
| S18 | `z5dNeUywZUMF8aknX1Rl3g` Exploring SAM | `research/raw/exploring_sam.txt` |
| S19 | `DRViqEpnohcgiWnVqbYzYQ` Configuring SAM | `research/raw/configuring_sam.txt` |
| S20 | `U70gtq8ZRqZT3ELF2Ty8xA` SAM installation methods | `research/raw/sam_installation_methods.txt` |
| S21 | `5i6qYMLaESV6cbIeDDKSVQ` Maturity stages | `research/raw/maturity_stages_sam.txt` |
| S22 | `dHEwwQ8O9pwIEz5MEEeFWg` Publish a specific set of products | `research/raw/publish_specific_set_of_products.txt` |
| S23 | `5Zth~lyu8PmPCG7eB5RPbg` Success portal | `research/raw/success_portal.txt` |
| S27 | `2DX4es9VZnTWDqtlxd_Lzw` Link an item to the software catalog | `research/raw/link_item_to_software_catalog.txt` |
| S28 | `3UK~zVq_kaxr05U6NxIj_g` Publish an item to the software catalog | `research/raw/publish_item_to_software_catalog.txt` |
| S29 | `iM9JQ58LKQmtwkR8IKi_vA` Publish models to HW or SW catalog | `research/raw/publish_models_to_hw_or_sw_catalog.txt` |
| S30 | `ABprxDQ~V1MOP2hP0odeMQ` Software installation fields | `research/raw/software_installation_fields.txt` |
| S31 | `hA25DFvIh8F2QUGYaqk0Gw` Software license metrics | `research/raw/software_license_metrics.txt` |
| S32 | `mHTmD2kNfjmeq6ksQCUSOQ` Allocation management | `research/raw/allocation_management.txt` |
| S33 | `OYewkvjy6lR2jJcPmLZN0g` Catalog request to reclaim | `research/raw/catalog_request_to_reclaim.txt` |
| S34 | `qVOtwtGQrYVLxP4inhYWXA` Software request workflow | `research/raw/software_request_workflow.txt` |
| S35 | `NkFF6uEfaBVCY2EASAorGA` License compliance position | `research/raw/license_compliance_position.txt` |
| S36 | `vvheubQ7n2nV1Nh15QIilA` True-up cost | `research/raw/true_up_cost.txt` |
| S37 | Path to Value / Quick Start / Office Hours / Starter Kit / Measuring Outcomes (ServiceNow employee Community) | `research/IMPLEMENTATION_SUCCESS.md` |
| S38 | Australia-family config inventory (tables `alm_license` / `cmdb_sam_sw_discovery_model`, Foundation `com.snc.sams`, matching job, IRE 3rd-party, recon-only Licensable) | `research/CONFIG_INVENTORY_AUSTRALIA.md` |
| S39 | `0L9Tjj4Eybnwnmt5tTu8fg` Software reconciliation results (three tiers) | `research/raw/software_reconciliation_results.txt` |
| S40 | `grzQLxfnAfqnJM0bO8WA5g` View or create software usage (`samp_sw_usage`) | `research/raw/view_or_create_software_usage.txt` |
| S41 | `9RI9Xq7062LW5Iqy7n52iw` Software model results LMR fields | `research/raw/software_model_results_lmr_fields.txt` |
| S42 | `7jeRdsPcmLzk6ET2NaQFWw` Impact of license types on reconciliation | `research/raw/impact_license_types_on_recon.txt` |

Topic index: `research/topics_brazil_itam_sam.json` (299 titles).
