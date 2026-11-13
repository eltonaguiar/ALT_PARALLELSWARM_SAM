# GUIDE ↔ REPO DELTA — SAM module guide vs `ALT_PARALLELSWARM_SAM`

**Agent:** `deepseek-flash__deepseek__kilo` · **Date:** 2026-11-13
**Compared**
- **GUIDE:** `ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/sam/sam-guide.md` (live page, 1,074 lines, agent `opencode`, 2026-11-12).
- **REPO:** `ALT_PARALLELSWARM_SAM` — `grok-4.6__xai__kilo` WT1–WT4, `beam__kilo__cli` WT1, and this pass (`SAM_MODULE_REFERENCE.md`, `ROUND2_GAP_ANALYSIS.md`, `MODULE_IMPLEMENTATION_PLAN.md`, `SAM_IMPLEMENTATION_CHECKLIST.md`).
- **PROTOCOL:** `ServiceNow_Learning/docs/00-methodology.md` + `docs/08-SAM-SETUP.md` (the generic learning protocol).

**Verdict:** the guide is the better *teacher*; the repo is the better *reference*. The guide has pedagogy the repo lacks (exam map, ELI5, quiz, lab, mnemonics, compliance vocabulary). The repo has the operational truth the guide lacks (six statuses, correct tables, three-tier results, properties, dedup, PPN, OOB jobs, reporting map, programme controls). The guide also carries several incorrect or non-OOB table/field names that must be corrected before it is used as an implementation source.

Companion artefacts:
- `LEARNING_LAYER.md` — the guide-only pedagogical assets, corrected and added to this repo.
- `LEARNING_PROTOCOL_ADDITIONS.md` — the generic module-protocol additions for `ServiceNow_Learning`.

---

## 0. Coverage by CIS-SAM domain

| Domain (guide's weights) | Guide strength | Repo strength | Net |
|---|---|---|---|
| 1 Overview & fundamentals (~15%) | ELI5, HAM vs SAM, lifecycle, exam map, roles in prose | plugin IDs, roles matrix, setup order, prerequisites | **Guide wins pedagogy; repo wins precision** |
| 2 Data integrity: models/normalisation/content (~25%) | SUMN narrative, suite emphasis, "fields people forget" | six statuses, rule families, PPN branches, Content Service, suggestions, revert | **Repo materially deeper** |
| 3 Entitlements/reconciliation (~30%) | compliance-state vocabulary, "what breaks recon", metric-mismatch warning | three-tier results, rights algebra, licence types, full properties, dedup | **Repo deeper; guide better teaching** |
| 4 Optimisation/reclamation/audit (~20%) | priority order, 60–90-day practice, publisher traps, SaaS waste pattern | candidate table, timeout, SaaS lifecycle, vendor metric matrix, audit chain | **Complementary** |
| 5 Reporting/ops (~10%) | day-one report list, SLA-style targets, dashboards | widget→table map, Workspaces, Success portal, Health Check | **Repo deeper; guide more actionable for a beginner** |

---

## 1. In the REPO but missing from the GUIDE → add to the guide

Ordered by implementation risk if omitted. Each row names the guide section to extend.

| # | Repo item | Why it matters | Add to guide section |
|---|---|---|---|
| 1 | **Six normalisation statuses** — `New`, `Match Not Found`, `Publisher Normalized`, `Partially Normalized`, `Normalized`, `Manually Normalized` — with which allow manual normalise and which allow revert | The guide says "normalization queue" and implies a binary; admins cannot triage without the real states | "Software Models & Normalization (SUMN)" |
| 2 | **Correct usage table `samp_sw_usage`** (not `cmdb_sam_sw_usage`) | Wrong table breaks every usage/reclamation report | "Three Record Types", "Key Table Hierarchy" |
| 3 | **Three-tier reconciliation**: `samp_product_result` → Software Model Results → `samp_license_metric_result` (no single `sam_sw_reconciliation_result`) | The guide's single result table does not exist as documented; rights algebra is per-metric | "Reconciliation", "Key Table Hierarchy", code samples |
| 4 | **Full property inventory** (`com.snc.samp.*`, defaults, blast radius) — the guide has zero properties | Recon grouping, auto-create, exclusions, published products, suite inference, Oracle levels are all properties | New "Configuration properties" section |
| 5 | **Dedup rules** `sam_sw_dedup_rule`, levels `Exact`/`Major`/`Any`, primary-selection order, IBM source preference | Duplicate installs are the #1 inflated-demand cause; the guide mentions suppression but not the rule object | "Discovery & Data Sources" / new "Deduplication" |
| 6 | **PPN resolution** (`samp_sw_product_definition`; blank/provided × standard/MLS × auto-create on/off) | The guide says "Content Library" but not how an entitlement becomes a model | "Entitlements" / "Software Models" |
| 7 | **Model vs vendor vs publisher vs PPN vs catalog item** | The guide's "three record types" omits vendor/publisher/PPN entirely; this is the top architecture error | "Three Record Types" → expand to six |
| 8 | **OOB jobs/BRs/flows/UI actions** with customise-vs-leave verdict | The guide lists features, not the objects an admin must not overlay | New "OOB scripts and jobs" |
| 9 | **Reporting widget → source table map** (overview, License Workbench, Normalization and content, Success portal, Health Check, Renewals, Overlapping usage) | The guide lists dashboards but not where the numbers come from | "Dashboards" |
| 10 | **Integrations with plugin IDs** — `com.snc.samp.ire.datasource.integration`, SCCM legacy→SGC, `sn_sam_saas_int`, ILMT API, Procurement, CSD, FBD, OpenLM/Open iT, SAP, Citrix | The guide's integration table is protocol-level; admins need plugin IDs and uninstall semantics | "Integrations" |
| 11 | **Insert/update matrix** across install, discovery model, software model, entitlement, allocation, catalog | The guide explains reconciliation but not what creates/updates each record | New subsection under "Reconciliation" |
| 12 | **`License under management` gate** and product-type `Licensable` requirement | A model can exist and never reconcile; the guide omits the gate | "Software Models" / "Entitlements" |
| 13 | **Content Service** opt-in, shared data types, exclusions, NSC IL5 | The guide treats Content Library as static; content sharing is the normalisation improvement loop | "Software Models & Normalization" |
| 14 | **Exclude-CI control** (`com.snc.samp.exclude_device_flag` + `SAM — Adjust Installs for excluded CIs`) | The guide says "exclude retired CIs" but not the product mechanism | "Discovery & Data Sources" |
| 15 | **Published products** (`com.snc.samp.manage.published.products`) for phase-wise rollout | The guide preaches piloting but not the scope-freeze control | "Goals/Operations" |
| 16 | **Suite inference** (`com.snc.sam.auto_suite_inference`) and reclamation suite behaviour | The guide says suites matter but not the property or parent/child reclamation rule | "Optimization" |
| 17 | **True-up cost source order** + override licence cost created at zero | The guide explains true-up conceptually, not how the number is produced | "Compliance Positions" |
| 18 | **SaaS lifecycle**: `sn_sam_saas_int`, direct profile auto-creates reclamation rule, `samp_sw_unrecognized_subscription_identifier`, SSO vs direct, overlapping usage | The guide has a good waste pattern but not the records/flow | "SaaS License Management" |
| 19 | **Programme layer**: RACI, feed contracts, T0–T10 numeric tests, acceptance gates, rollback, change control, audit chain | The guide has common mistakes and SLAs, not enforceable gates | New "Operating model" + appendix |
| 20 | **Cloud/virtual/container**: Oracle `reconlevel`, host affinity, Microsoft dual-use/edition flexibility/legacy flag, PVU region, container exclusion | The guide's publisher traps are conceptual; these are the switches | "Publisher-Specific Traps" |
| 21 | **Domain separation / upgrade**: `com.glide.domain.msp_extensions.installer`, published-products per domain, Yokohama script-include move, revert customizations | Missing entirely | New "Upgrade and domain separation" |
| 22 | **Confidence/release discipline**: `V/C/U` marks, Brazil pin, `sys_dictionary`/`sys_db_object` verification | The guide says "verify" but not how | Front matter + appendix |

---

## 2. In the GUIDE but missing from the REPO → add to the repo

These are now written (corrected) in `LEARNING_LAYER.md`.

| # | Guide asset | Value | Repo location added |
|---|---|---|---|
| 1 | **CIS-SAM exam alignment** — domains, ~weights, prep courses | Gives learners a target; repo had weights only inside WT2 | `LEARNING_LAYER.md` §1 |
| 2 | **ELI5** — 1,000 M365 rights vs 1,180 installs / 1,090 users | Fastest intuition for reconciliation | `LEARNING_LAYER.md` §2 |
| 3 | **SAM vs HAM vs ITAM** comparison | Prevents "SAM is asset management" confusion | `LEARNING_LAYER.md` §3 |
| 4 | **SAM lifecycle diagram** (request → procure → entitle → discover → reconcile → optimise → renew) | Shows the loop, not a one-pass pipeline | `LEARNING_LAYER.md` §4 |
| 5 | **"Three record types you must never confuse"** mnemonic | Strong teaching device; repo had five types but no mnemonic | `LEARNING_LAYER.md` §5 |
| 6 | **Compliance-position vocabulary** — Compliant / Over-licensed / Under-licensed / Unlicensed / Not counted / Unknown | More useful than the product's binary status, *if* caveated | `LEARNING_LAYER.md` §6 |
| 7 | **Publisher audit-trap table** — Microsoft, Oracle, IBM, SAP, Adobe, ServiceNow | Concise interview/audit prep | `LEARNING_LAYER.md` §7 |
| 8 | **"What breaks reconciliation"** symptom → root cause | Excellent triage table | `LEARNING_LAYER.md` §8 |
| 9 | **"Fields people forget"** | Practical field hygiene | `LEARNING_LAYER.md` §9 |
| 10 | **Day-one report definitions** | Actionable reporting start | `LEARNING_LAYER.md` §10 |
| 11 | **Guided 7-step lab** | Concrete proof path; complements T0–T10 | `LEARNING_LAYER.md` §11 |
| 12 | **Quiz (8 Q&A) + mnemonics** | Retrieval practice | `LEARNING_LAYER.md` §12–§13 |
| 13 | **SLA-style targets** | Operating cadence (mark **P**, fix "nightly") | `LEARNING_LAYER.md` §14 |
| 14 | **SaaS waste pattern + connector health** | Memorable, operational | `LEARNING_LAYER.md` §15 |
| 15 | **Optimisation priority order + reclamation workflow** | Business sequencing | `LEARNING_LAYER.md` §16 |
| 16 | **Reusable code/metadata patterns** | Useful *as examples*, but the guide's field names are non-OOB | `LEARNING_LAYER.md` §17 (corrected, safe) |
| 17 | **Official learning resources** | Study path | `LEARNING_LAYER.md` §18 |

---

## 3. Conflicts and errors in the guide (must fix before reuse)

| # | Guide says | Official / repo evidence | Correct action |
|---|---|---|---|
| 1 | Usage table `cmdb_sam_sw_usage` | `samp_sw_usage` **V** (Brazil "View or create software usage") | Replace all occurrences |
| 2 | Result table `sam_sw_reconciliation_result`, field `compliance_state` | Three tiers: `samp_product_result` → Software Model Result → `samp_license_metric_result` **V**. No single documented result table. Status is "Software model status" Compliant/Not Compliant | Replace table and code samples; explain tiers |
| 3 | Reconciliation "default nightly" | Brazil: **weekly default + on demand** **V** | Change default; keep "nightly" only as an option |
| 4 | ITAM plugin `com.snc.iam` alongside `com.snc.sams` | SAM Pro = `com.sn_samp_master_ws` (loads `com.sn_samp_master` + Workspace); core `com.snc.samp`; Foundation `com.snc.sams` **V/C**. `com.snc.iam` is not the SAM plugin | Qualify or remove |
| 5 | "ServiceNow calls this SUMN" | Brazil docs call it **normalisation** + **Content Library**; SUMN is not an official term in the fetched pages | Rename to Content Library normalisation; keep SUMN as a note |
| 6 | `cmdb_sam_sw_install.software_model` | Install references `discovery_model`; the `software_model` reference lives on `cmdb_sam_sw_discovery_model` **V** | Fix hierarchy diagram and code |
| 7 | Discovery model field `normalized_software_model` | Documented field is `software_model` **C** | Rename |
| 8 | `license_metric_type` on both model and entitlement | Entitlement has a **license metric**; model has **metric attributes / metric group** **V**. Exact columns `U` | Use labels + `U` marker; don't present as exact columns |
| 9 | Custom code writes `u_normalization_status` on `cmdb_sam_sw_install`, `u_sam_status`, `u_license_metric_notes` | These are **custom** fields, not OOB. Normalisation status is on the discovery model | Label "custom example"; do not imply OOB |
| 10 | "Expire entitlements" scheduled job | Not documented as OOB in Brazil pages; the guide presents custom code | Label custom; verify `sysauto_script` |
| 11 | Oracle "10% rule" | Not a Brazil-documented SAM rule; Oracle virtualisation rules are contract-specific | Mark **U** / publisher rule; verify contract |
| 12 | "Audit package export" as OOB | Not found in the Brazil pages fetched | Mark **U**; verify in instance/Store |
| 13 | "One entitlement per contract line" | Practice, not a product constraint | Mark **P** |
| 14 | 60–90-day reclaim window | Practice; product timeout is `sam_reclamation_flow_error_timeout` = 30 days **V** | Keep 60–90 as **P**, distinguish property |
| 15 | "SAM typically returns 5–15% of spend" | Community/practice, not a product SLO | Mark **P** |
| 16 | SLA "reconciliation nightly, results < 24h" | Conflicts with weekly default | Change to "weekly (or agreed cadence); results < 8 days" or make it a programme choice |
| 17 | "Unknown" as a compliance position | License Position status field is only Compliant/Not Compliant; Unknown is an interpretation of missing data | Keep the concept, add the caveat |
| 18 | Breadcrumbs `All > Software Asset Management > …` | Brazil uses `All > Software asset` and Workspaces; classic is limited-support | Add workspace-first paths and "your release may differ" |

---

## 4. Both — terminology reconciliation

| Concept | Guide term | Repo term | Use |
|---|---|---|---|
| Normalisation framework | SUMN | Content Library + normalisation rules | **Content Library**; mention SUMN once as legacy/community |
| Record set | Three record types (six rows) | Five record types + vendor/publisher/PPN | **Five** (install, discovery model, software model, entitlement, result), with vendor/publisher/PPN as supporting reference data |
| Compliance | Compliant / Over / Under / Unlicensed / Not counted / Unknown | Product status Compliant/Not Compliant + rights buckets | Teach the six-state vocabulary, but state the product field is binary and the richer states come from rights/unlicensed columns |
| Result | Reconciliation result | Three tiers | **Three tiers** |
| Normalisation status | "queue"/"unmatched" | Six statuses | **Six statuses** |
| Plugin | `com.snc.sams` "Foundation/Pro" + `com.snc.iam` | Pro `com.sn_samp_master_ws` / `com.snc.samp`; Foundation `com.snc.sams` | **Split Pro vs Foundation** |

---

## 5. Generic learning-protocol additions (from repo-only material)

The repo material that the *learning protocol* currently lacks is listed in `LEARNING_PROTOCOL_ADDITIONS.md`. Summary of the ten protocol artefacts:

1. Record-chain map (owned / observed / computed).
2. Identity & normalisation state machine.
3. Insert/update matrix.
4. Quantity/entitlement algebra (for any module with rights/allocations).
5. OOB object inventory (jobs, BRs, flows, script includes, UI actions).
6. Property inventory split must-consider vs full, with defaults and blast radius.
7. Reporting map (widget → source table).
8. Integration contract (plugin, direction, target, required fields, frequency, error/retry, uninstall/absence).
9. Programme controls (RACI, numeric tests, acceptance gates, rollback, change control, audit chain).
10. Confidence/release discipline (`V/C/U`, release pin, `sys_dictionary`/`sys_db_object` verification).

These slot into the existing `ORIENT → MODEL → PRACTISE → PROVE → TEACH` loop: 1–3 in MODEL, 4–8 in PRACTISE, 9 in PROVE, 10 in every artefact.

---

## 6. Apply plan (guide repo)

| Order | Change | File/anchor | Effort |
|---|---|---|---|
| 1 | Fix the 18 conflicts in §3 (table/field names, nightly, plugin, SUMN, custom `u_*`) | whole guide; priority "Three Record Types", "Reconciliation", "Key Table Hierarchy", code samples | 1–2 h |
| 2 | Replace "three record types" with five + vendor/publisher/PPN | "The Three Record Types…" | 1 h |
| 3 | Add six-status table + transitions | "Software Models & Normalization" | 1 h |
| 4 | Add three-tier results + rights algebra | "Reconciliation" | 2 h |
| 5 | Add property inventory (must + full) | new section after "Where to Find It" | 2 h |
| 6 | Add dedup, PPN, Content Service, exclude-CI, published products | respective sections | 2 h |
| 7 | Add OOB jobs/BRs with customise-vs-leave | new section | 1 h |
| 8 | Add widget→table reporting map | "Dashboards" | 1 h |
| 9 | Add integration plugin IDs + uninstall semantics | "Integrations" | 1 h |
| 10 | Add operating-model appendix (RACI, tests, gates, rollback, change, audit) | new appendix | 2 h |
| 11 | Add confidence legend + verification queries | front matter/appendix | 30 m |

**Do not** paste the repo verbatim: the guide is a learning path, not a reference. Link to the repo for depth and keep the guide's ELI5/quiz/lab voice.

---

## 7. What to keep from the guide unchanged

- ELI5, SAM vs HAM, lifecycle narrative, the "what it is / what you may use / what exists / what is used / the difference" mnemonic.
- Compliance-position vocabulary (with the product-field caveat).
- Publisher audit-trap table (with **P/U** marks).
- "What breaks reconciliation" and "fields people forget".
- The 7-step lab structure (align expected numbers with T0–T10).
- Quiz, mnemonics, official learning resources.
- Optimisation priority order and SaaS waste pattern.

These are the pieces the reference repo cannot replace; they are now preserved in `LEARNING_LAYER.md` so they are not lost when the guide is corrected.

---

## 8. Sibling merge — `grok-4.6__xai__kilo` WT5

WT5 independently produced a 92-line bidirectional delta (`agents/grok-4.6__xai__kilo/SNC_SAM__WT5/05_FINAL/BIDIRECTIONAL_DELTA.md`). It agrees on every conflict and adds seven specifics now folded in:

| WT5 item | Status in this delta | Where |
|---|---|---|
| A1 **Four paths** (catalog publish / create-before-discovery / discover-and-link / block-exclude) | **Added** | `SAM_MODULE_REFERENCE.md` §1.3 |
| A2 Product Catalog nav + `model_manager` / `catalog_admin` + `glide.model.catalog_item_currency` | Already in reference §2.4/§14; now explicit in the path table | reference §1.3 |
| A3 Foundation vs Pro plugins + irreversible upgrade | Already in §3 conflict #4; add the irreversible note | §3 #4 |
| A10 Uninstalls not auto-deleted; Retired/Stolen CI **does** delete installs | Already in reference §2.1/§9; now in the guide correction list | `LEARNING_LAYER.md` §8 |
| A17 No `glide.cmdb.sam.*` family | Already in reference §14.4; keep | reference §14.4 |
| A18 Entitlement **Build → Publish → In use** | Already in reference §2.5/§10; add to guide correction list | `LEARNING_LAYER.md` §17 |
| D **Closed-loop module** framing (two independent truths; four object types; plugin pin; named jobs; 1+2 test; teaching code ≠ OOB; sibling contrast) | **Added** | `LEARNING_PROTOCOL_ADDITIONS.md` §1.11 |

**Where this delta is broader than WT5:** six-status transition/revert matrix, full property catalog, reporting widget→table map, three-tier rights algebra, Content Service data types, dedup primary-selection order, model-matching job, OOB customise-vs-leave inventory, and the programme layer (RACI, feed contracts, T0–T10, gates, rollback, change control, audit, cloud/container). WT5's 18 guide additions and 15 protocol items are a subset plus the seven above.

**Do not merge WT5's "do not move" list** into the guide as content; it is a migration guardrail. The combined canonical is this file + `LEARNING_LAYER.md` + `LEARNING_PROTOCOL_ADDITIONS.md`.
