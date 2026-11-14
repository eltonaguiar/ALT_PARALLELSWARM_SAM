# Cross-Reference — v2 Reference vs the Public SAM Guide

**Guide:** <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/sam/sam-guide/>
**Guide source:** `ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/sam/sam-guide.md` (agent `opencode`, 2026-11-12).
**Reference:** this `finalv2/` set, pinned to Brazil (SAM) and Australia (IRE).
**Verdict:** the guide is the better **teacher**; this reference is the better **configuration and operations source**. The guide carries several table/field/cadence claims that conflict with the official Brazil pages. Keep the guide's voice; link here for depth; correct the specific claims below before using it as an implementation source.

> **Correction-ID map (GUIDE ↔ CONFLICT_LOG):**
>
> | GUIDE | CONFLICT_LOG | Topic |
> |---|---|---|
> | C-01 | C-08 | Usage table |
> | C-02 | C-02, C-12 | Result tiers / run record |
> | C-03 | C-07, C-16 | Reconciliation cadence |
> | C-04 | C-01 | Plugin IDs |
> | C-05 | C-10 | "SUMN" |
> | C-06 | C-04 | Install → discovery model |
> | C-07 | C-04 | Software model field |
> | C-08 | C-09 (partial) | Metric / entitlement columns |
> | C-09 | — | Custom `u_*` fields |
> | C-10 | — | Not a correction |
> | C-11, C-12 | C-17 | Oracle 10% / audit export |
> | C-13..C-16 | C-13..C-16 | 1:1 |
> | C-17 | C-11 | Compliance state |
> | C-18 | C-19 | Classic UI / breadcrumbs |
> | C-19 | C-18 | Record-chain heading |
> | C-20 | — | Model inheritance |
> | C-21 | C-09 | `alm_license` label |
>
> IDs are kept stable for traceability; use this map when cross-referencing the two files.
>
> **Scope note:** the guide's **Carry-Over Addendum** already uses the correct master plugin IDs, roles, `sn_sam_saas_int`, and `samp_sw_usage`. The corrections below apply to the **main body**; where the addendum already fixes a claim, say so rather than implying the whole page is wrong.

---

## 1. Section-by-section map

| Guide section | What the guide does well | v2 counterpart | Notes |
|---|---|---|---|
| Purpose | One-paragraph value case + ELI5 | [`05_FINAL/01_SAM_MODULE_GUIDE.md`](05_FINAL/01_SAM_MODULE_GUIDE.md) §1 | Keep the ELI5 |
| SAM vs HAM vs ITAM | Clear ownership/record comparison | §2 | Keep; add the record-chain gate |
| Where to Find It | Practical breadcrumbs | §9 + [`06_CONFIGURATION_REFERENCE.md`](05_FINAL/06_CONFIGURATION_REFERENCE.md) §7 | Workspace-first paths; classic limited |
| CIS-SAM exam alignment | Domain weights and prep courses | — | Guide-only pedagogy; keep |
| SAM lifecycle | Request → procure → entitle → discover → reconcile → optimize → renew | §7 | v2 adds the runtime sequence |
| Three record types | Memorable mnemonic | §4 (five/six records) | Reframe the heading; the table already lists six records; see correction C-19 |
| Software models & normalization (SUMN) | SUMN narrative, suite emphasis | [`04_NORMALIZATION_AND_DEDUP.md`](05_FINAL/04_NORMALIZATION_AND_DEDUP.md) | v2 adds six statuses, rule families, jobs, revert |
| Entitlements | Contract-side checklist | [`05_ENTITLEMENTS_METRICS_RECONCILIATION.md`](05_FINAL/05_ENTITLEMENTS_METRICS_RECONCILIATION.md) §2–3 | v2 adds PPN resolution and license types |
| Reconciliation | Step-by-step + "what breaks" | §6–9 | v2 adds three tiers and rights algebra |
| Compliance positions | Six-state vocabulary | §9 | Keep, with the binary-field caveat |
| Discovery & data sources | Source inventory and data-quality rules | [`03_DISCOVERY_TO_SAM_PIPELINE.md`](05_FINAL/03_DISCOVERY_TO_SAM_PIPELINE.md) | v2 adds the business rule, dedup, exclude-CI |
| SaaS License Management | Waste pattern and connector basics | §12 | v2 adds the record/plugin detail |
| Optimization & reclamation | Priority order + 60–90-day practice | §11 | Keep as practice |
| Publisher-specific traps | Strong audit-prep table | §5 metrics + publisher packs | Keep; contract-specific |
| Re-usable code | Teaching patterns | [`07_OPERATIONS_RUNBOOK.md`](05_FINAL/07_OPERATIONS_RUNBOOK.md) + this doc §5 | Code is custom, not OOB |
| Out-of-Box features | Feature inventory | `06_CONFIGURATION_REFERENCE.md` | v2 adds tables/jobs/properties |
| Key table hierarchy | Visual hierarchy | §4 / `06` §3 | Correct the install→model link |
| Integrations | Protocol-level table | `06` §8 | v2 adds plugin IDs and deprecations |
| Key fields | Field hygiene | `05` §2 / `06` §3 | v2 separates label vs column |
| Goals / metrics | KPI targets | `07` §5 | Treat targets as P |
| Common mistakes | Excellent anti-pattern list | `01` §13 / `07` §6 | Keep |
| Lab | 7-step proof path | `07` §2–3 | Align expected numbers with your data |
| SLAs / dashboards | Operating cadence | `07` §4–5 | Fix "nightly" |
| Quiz / mnemonics | Retrieval practice | — | Guide-only pedagogy; keep |
| Official resources | Study path | `08_SOURCE_NOTES.md` | v2 cites product docs |

---

## 2. Corrections to the guide (verified where possible)

| # | Guide claim | Official evidence | Correction | Status |
|---|---|---|---|---|
| C-01 | Usage table is `cmdb_sam_sw_usage` | Brazil **View or create software usage** names `samp_sw_usage` | Use `samp_sw_usage`; table tracks product level, not version/edition | **V** |
| C-02 | Result table is `sam_sw_reconciliation_result` with `compliance_state` | Brazil **Software reconciliation results** documents three tiers: `samp_product_result` → Software Model Results → `samp_license_metric_result`; the run record is `samp_reconciliation_result` | Replace the single-table model with the three tiers; use `samp_reconciliation_result` for the run | **V** (tiers/run); **C** (no single analysis table) |
| C-03 | Reconciliation default is **nightly** | Brazil **Software reconciliation for compliance** says **weekly default + on demand** | Change to weekly default; nightly is an optional schedule choice. v1's "Monday 02:00" is a schedule configuration, not a documented default (**U**) | **V/U** |
| C-04 | Plugin is `com.snc.sams` + `com.snc.iam` | Brazil **Components installed with SAM Professional** names `com.sn_samp_master_ws` (Brazil master), `com.sn_samp_master` (pre-Brazil), `com.snc.samp` (core), `com.snc.sams` (Foundation); `com.snc.iam` is not the SAM plugin | Split Foundation vs Professional; remove `com.snc.iam` as the SAM plugin | **V** |
| C-05 | "ServiceNow calls this SUMN" | The fetched Brazil pages use **normalization** + **Content Library**; SUMN is not used in those pages | Use "Content Library normalization"; mention SUMN as a community/legacy label | **V/U** |
| C-06 | Install has `software_model` | Brazil **Software installation fields** shows the install references the **Discovery model**; the software-model reference is on the discovery model | Fix the hierarchy and code samples | **V** |
| C-07 | Discovery model field `normalized_software_model` | Brazil **Discovery models fields** documents the field as **Software model** | Rename to the documented label; API column is **U** | **V/U** |
| C-08 | `license_metric_type` on both model and entitlement | Brazil pages show a **License metric** on the entitlement and **Metric Attributes** on the model; exact columns are not exposed in the fetched pages | Use labels; mark exact columns **U** | **V/U** |
| C-09 | Custom code writes `u_normalization_status`, `u_sam_status`, `u_license_metric_notes` | These are custom fields; normalization status lives on the discovery model | Label as custom examples; do not imply OOB | **V** |
| C-10 | **Not a guide correction.** The guide presents an "Expire entitlements" scheduled job under **Re-usable Code / Metadata**, not as an OOB capability | The code block is explicitly a custom example; there is no OOB claim to correct | If reused, label it custom and verify `sysauto_script`; do not attribute an OOB claim to the guide | **P** |
| C-11 | Oracle "10% rule" | Not a Brazil-documented SAM rule; Oracle virtualization rules are contract-specific | Mark **U** / publisher rule; verify contract | **U** |
| C-12 | "Audit package export" is OOB | Not found in the fetched Brazil pages | Mark **U**; verify in instance/Store | **U** |
| C-13 | "One entitlement per contract line" | Practice, not a product constraint | Mark **P** | **P** |
| C-14 | 60–90-day reclaim window | Practice; product timeout `sam_reclamation_flow_error_timeout` = 30 days | Keep 60–90 as **P**; distinguish the property | **P/V** |
| C-15 | "SAM typically returns 5–15% of spend" | Community/practice, not a product SLO | Mark **P** | **P** |
| C-16 | SLA "reconciliation nightly, results < 24h" | Conflicts with weekly default | Change to "weekly or agreed cadence; results < 8 days" or make it a programme choice | **V/P** |
| C-17 | "Unknown" is a compliance position | The product field is Compliant / Not Compliant; Unknown is an interpretation of missing data | Keep the concept; add the caveat | **V/P** |
| C-18 | Breadcrumbs `All > Software Asset Management > …` | Brazil uses `All > Software asset` and workspace-first paths; classic support becomes limited from Brazil, and after activating the master plugin the classic UI is inaccessible | Add workspace-first paths and "your release may differ" | **V** |
| C-19 | Heading says "Three Record Types" | The table under the heading already lists six records (Software Model, Discovery Model, Installation, Usage, Entitlement, Reconciliation Result) | Rename the heading to "The record chain" and keep the mnemonic; the table itself is already six rows | **C/P** |
| C-20 | `cmdb_software_product_model` extends `cmdb_model` | Not verified in the fetched pages | Mark **U** or verify in `sys_db_object` | **U** |
| C-21 | `alm_license` label "License" | Brazil overview uses **Software Entitlement [alm_license]** | Label may differ by release/module; use `alm_license` + "Software Entitlement" | **V/C** |

**On `license_metric_type` (four-way inconsistency):** the guide says the metric must match on model and entitlement; `direction-a-gaps.md` says a mismatch flips the result to `Unknown`; the product's status field is binary Compliant / Not Compliant. **Resolution:** treat metric matching as a **P** data-quality rule; the exact columns are **U**; do not present `Unknown` as a product field. The guide's "silent, meaningless number" warning is the safest formulation.

### 2.1 Additional guide claims not covered by C-01..C-21

| # | Guide claim | Issue | Correction | Status |
|---|---|---|---|---|
| G-22 | "SAM Workspace" | Official product name is **Software Asset Workspace** (`sn_sam_workspace`) | Rename; "SAM Workspace" is a colloquial shorthand | **V** |
| G-23 | "SAM Pro (and later) extends SAM to cloud subscriptions" | `sn_sam_saas_int` is a separate Store plugin that **requires SAM Professional** | Say "SaaS License Management is a separate Store plugin requiring SAM Professional" | **V** |
| G-24 | Key table hierarchy puts "normalization rules ← Content Library publisher pack" under `cmdb_software_product_model` | Normalization compares **discovery models** to the Content Library; the matching job then sets the software model | Move the rules under the discovery model / normalization layer | **V** |
| G-25 | "SAM Pro" / "SAM Foundation/Pro" | Brazil pages use **SAM Foundation** and **SAM Professional**; "SAM Pro" is not an official edition label in the fetched set | Use the official edition labels; keep "Pro" as shorthand only | **V** |
| G-26 | Install fields `discovery_source`, `last_seen` | The official Software Installation form lists Discovery model, Publisher, Version, Edition Override, Installed on, etc.; those two fields are not in the form list | Mark **U** and verify in `sys_dictionary` | **U** |
| G-27 | Usage = "evidence the install was actually run" | Official usage is **product-level** (publisher/product + CI + user), not install-level | Correct the granularity; do not join usage to a specific install record | **V** |
| G-28 | "Oracle and IBM do not permit downgrades"; "server (not the VM) unless hard partitioning is certified" | Contract-specific claims, not in the Brazil SAM pages | Mark **U**; verify against the publisher agreement | **U** |
| G-29 | Code samples query `cmdb_ci` synchronously per install, write `u_exclude_from_reconciliation`, use `alm_license.number`, `getDisplayValue('software_model')`, `addHaving`, and `showFieldMsg` on a possibly missing `u_*` field | Custom fields/columns; the synchronous query is a performance hazard on a high-volume table | Label all `u_*` fields custom; batch/asynchronous query; verify every column before use | **P/U** |
| G-30 | Result fields `entitlement_count`, `install_count`, `usage_count`, `compliance_state` | The documented result fields are Rights owned / used / needed / available, Software model status, Unlicensed installs, True-up cost, etc. | Replace the field list with the documented License Position/result fields | **V** |
| G-31 | Software models can be "standalone, part of a suite, or a bundle" | Suite inference is documented; "bundle" is not in the fetched pages | Mark "bundle" **U**; keep suite | **U** |

> **`C-10` is not a correction.** The guide presents the "expire entitlements" job as reusable custom code, not as OOB. The safety note is: label it custom if you reuse it.

---

## 3. What v2 adds that the guide lacks

Ordered by implementation risk if omitted:

1. **Six normalization statuses** with manual/revert rules. **V**
2. **Correct table chain** and the install → discovery-model link. **V**
3. **Three-tier reconciliation results** and rights algebra. **V**
4. **Property inventory** with defaults and blast radius. **V**
5. **Dedup framework** (Exact/Major/Any, primary selection, `sam_sw_dedup_rule`). **V**
6. **PPN resolution** (blank/provided × standard/MLS × auto-create). **V**
7. **IRE governance** (identification, reconciliation, data refresh, data source rules, insert/update applicability). **V**
8. **Insert/update matrix** across the pipeline. **V/P**
9. **Reporting map** (widget → table). **V**
10. **Plugin/role matrix** with release-correct IDs. **V**
11. **Operational runbook** (pre-flight, gates, troubleshooting, rollback, audit chain). **P**
12. **Verification queries** and confidence marks. **V/U**

---

## 4. What the guide adds that v2 intentionally does not replace

Keep these in the guide:

- ELI5 (1,000 rights vs 1,180 installs vs 1,090 users).
- SAM vs HAM vs ITAM narrative.
- Lifecycle diagram and the "two independent truths" framing.
- The "what it is / what you may use / what exists / what is used / the difference" mnemonic.
- Six-state compliance vocabulary (with the binary-field caveat).
- Publisher audit-trap table.
- "What breaks reconciliation" and "fields people forget".
- The 7-step lab.
- Quiz, mnemonics, official learning resources.
- CIS-SAM exam-alignment table.
- 30/60/90-day study plans.
- Platform mnemonics (BAA, LOCS, ARM, IRE).

**Do not paste this reference into the guide wholesale.** The guide is a learning path; this is a configuration reference. Link, don't merge.

**Nuance:** the high-risk factual corrections (C-01, C-02, C-03, C-04, C-06, C-16, C-17, G-22–G-24, G-27, G-30) should land in the guide itself — a link will not be followed before someone runs the lab. The guide's existing **Carry-Over Addendum** is the accepted "link + curated carry-over" pattern; use it as precedent rather than duplicating the reference.

---

## 5. Safe code-pattern policy

The guide's code samples are useful teaching patterns but use non-OOB fields. If you adapt them:

1. Replace `cmdb_sam_sw_usage` with `samp_sw_usage`. **V**
2. Replace `sam_sw_reconciliation_result` with the three-tier tables. **V**
3. Treat `u_*` fields as custom; create them deliberately. **V**
4. Query `sys_dictionary` / `sys_db_object` before relying on a field name. **V**
5. Do not run a custom "expire entitlements" job without change control. **P**

---

## 6. Terminology reconciliation

| Concept | Guide term | v2 term | Use |
|---|---|---|---|
| Normalization framework | SUMN | Content Library normalization | **Content Library**; SUMN as a note |
| Records | Three record types | Install, discovery model, software model, entitlement, result (+ usage) | Five/six, with the mnemonic |
| Compliance | Compliant / Over / Under / Unlicensed / Not counted / Unknown | Product field is Compliant / Not Compliant; richer states are interpretive | Teach the six states, caveat the field |
| Results | Reconciliation result | Three tiers | **Three tiers** |
| Statuses | "queue"/"unmatched" | Six statuses | **Six statuses** |
| Edition | `com.snc.sams` "Foundation/Pro" + `com.snc.iam` | Foundation `com.snc.sams`; Pro `com.sn_samp_master_ws` / `com.snc.samp` | Split editions; drop `com.snc.iam` as SAM |

---

## 7. Recommended edits to the guide (additive, safe)

| Order | Change | Effort |
|---|---|---|
| 1 | Fix C-01, C-02, C-03, C-04, C-06, C-16, C-17 | 1–2 h |
| 2 | Expand "three record types" to five/six with the install→discovery-model link | 1 h |
| 3 | Add six-status table + transitions | 1 h |
| 4 | Add three-tier results + rights algebra | 2 h |
| 5 | Add property inventory (must-consider + full) | 2 h |
| 6 | Add dedup, PPN, Content Service, exclude-CI, published products | 2 h |
| 7 | Add OOB jobs/BRs with customise-vs-leave | 1 h |
| 8 | Add widget→table reporting map | 1 h |
| 9 | Add integration plugin IDs + deprecations | 1 h |
| 10 | Add operating model appendix (RACI, gates, rollback, change, audit) | 2 h |
| 11 | Add confidence legend + verification queries | 30 m |

**P**

---

## 8. Bottom line

- **Use the guide to learn.** Its pedagogy is stronger than anything a reference can provide.
- **Use this reference to configure and operate.** It separates verified product behavior from practice and names what remains unverified.
- **Correct the guide before implementation.** The table, cadence, and plugin claims in §2 are the ones most likely to cause real errors.
- **Audit result:** of the 21 numbered corrections, 18 are confirmed, C-19 is a partial (heading, not missing rows), and C-10 is not a correction (the guide already labels the code as custom). The additional claims G-22–G-31 cover what the numbered list missed.
