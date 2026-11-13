# Bidirectional delta — swarm GitHub ↔ SAM guide ↔ Learning protocol

**Agent:** `grok-4.6__xai__kilo` · **WT5** · 2026-11-13

| Corpus | URL |
|---|---|
| Swarm | https://github.com/eltonaguiar/ALT_PARALLELSWARM_SAM (G/B/R/K finals) |
| SAM guide (webpage) | https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/sam/sam-guide/ |
| Module protocol | https://eltonaguiar.github.io/ServiceNow_Learning/ (`docs/00-methodology.md` 5-gate loop, `08-SAM-SETUP.md`) |

Do **not** copy LG sample BRs that write `u_` fields as if OOB. Prefer Brazil/Australia product names over LG aliases.

---

## A. In swarm GitHub, **not** on the SAM guide page → **add to sam-guide**

These are product-doc facts the webpage still lacks or gets wrong.

| # | Add to sam-guide | Swarm source | Why |
|---|---|---|---|
| A1 | **Four paths:** catalog publish vs create-before-discovery vs discover-and-link vs block/exclude | G §10 | Guide collapses catalog into “Request and Procure” |
| A2 | Product Catalog nav + roles `model_manager` / `catalog_admin`; `glide.model.catalog_item_currency` | G §10A | Requestable item ≠ software model |
| A3 | Foundation `com.snc.sams` vs Pro `com.sn_samp_master_ws` / `com.snc.samp`; SaaS `sn_sam_saas_int`; upgrade **irreversible** | G §1 | Guide lumps `com.snc.sams` as Foundation/Pro |
| A4 | Recon **weekly or on-demand**, **three tiers** (Product / Software Model / `samp_license_metric_result`) | G §12, B, R | Guide says nightly + `sam_sw_reconciliation_result` |
| A5 | Usage table **`samp_sw_usage`** (product-level) | G S40 | Guide `cmdb_sam_sw_usage` |
| A6 | Named jobs: Normalize DMAPs; DMAP→software-model matching; Deduplicate Install Table; Adjust Installs for excluded CIs | G §14 | Guide has teaching jobs, not OOB names |
| A7 | Install BR: publisher+product+version → DMAP (cannot create DMAP manually; skip “Security Update”) | G §7, B | Guide sample BR uses `current.software_model` |
| A8 | Properties: `automaticsmrcreation` **off in Crawl**, `exclude_device_flag`, `manage.published.products`, wide-net/ML defaults | G §17, §20 | Guide silent |
| A9 | SA/Maintenance **not reconciled** unless linked to perpetual | G S42 | Guide says maintenance ≠ license but not the link rule |
| A10 | Uninstalls **not** auto-deleted; 3rd-party Table API DELETE; Retired/Stolen CI **does** delete installs | G §6, S40 | Guide says exclude retired, not delete-vs-keep |
| A11 | 3rd-party IRE: `com.snc.samp.ire.datasource.integration` + payload keys | G §6 | Guide lists Intune/Jamf as if native SAM |
| A12 | Dedup Exact / Major / Any; IBM Discovery preferred | G §7 | Guide: “duplicate-suppression rule” unnamed |
| A13 | Workspace vs classic-only leftover menus (Brazil) | G §5 | Guide classic-only breadcrumbs |
| A14 | Content Service default **off**; statuses New/Partial/Publisher/Match Not Found/Manual; pattern vs wide-net vs ML | G §8 | Guide “SUMN” jargon |
| A15 | PPN import match/relax/auto-create / multiple-model error | G §9 | Guide: entitle, no import engine |
| A16 | Crawl/Walk/Run + published-products freeze + Success portal | G §20 | Guide has lifecycle mermaid, not vendor maturity UI |
| A17 | No `glide.cmdb.sam.*` family | G §22 | Prevents cargo-cult properties |
| A18 | Entitlement **build → Publish → in use** | G §11 | Guide skips publish gate |

**Fix-in-place on the webpage** (same section, wrong string): weekly not nightly; plugin split; `samp_sw_usage`; drop SUMN as product name; do-not-teach `alm_software`.

---

## B. On the SAM guide page, **not** (or thin) in swarm GitHub → **add to Learning protocol**

These are *module-learning* patterns. Put them in https://github.com/eltonaguiar/ServiceNow_Learning (`00-methodology` / module brief template / `08-SAM-SETUP`), not only in sam-guide.

| # | Guide has | Swarm | Add to protocol as |
|---|---|---|---|
| B1 | CIS-SAM domain weights + quiz + 7-step lab + teach-back | Thin (WT3 cheat sheet only) | Every module brief: **exam map + quiz + break-it lab** (already the 95-min loop; SAM-guide lab is the gold specimen) |
| B2 | Compliance positions: Unknown ≠ compliant; over/under/unlicensed as *meanings* | Swarm has Compliant/Not Compliant dots only | Module protocol: **computed result ≠ business language**; always map UI status → financial action |
| B3 | Publisher-trap table (MS cores, Oracle server-not-VM, IBM PVU+ILMT, SAP named user, Adobe VIP) | Swarm names packs/properties, not audit traps | Protocol: **vendor-rule appendix** required for any money module (SAM, HAM, SPM) |
| B4 | “Never overwrite quantity; one entitlement per contract line” | Mentioned in G anti-patterns, not as hygiene law | Protocol: **immutable financial records** (true-up = new row) |
| B5 | 60–90 day reclaim practice | Swarm: rule types + 30-day flow timeout | Protocol: **practice window vs platform default** — label both |
| B6 | Assigned seats ≠ sign-in; dead connector = fake “no waste” | Missing | Protocol: **integration health is a KPI** |
| B7 | HAM vs SAM vs ITAM comparison table | Thin | Protocol: **sibling-module contrast** in every Orient gate |
| B8 | Key fields people forget + day-one reports | Swarm field lists are install-centric | Protocol: **mandatory vs critical vs optional** (already `04-fields.md`) applied per module record |
| B9 | Mermaid lifecycle / recon / SaaS flows | Swarm is tables | Protocol: **one diagram per gate** (already infographics) |
| B10 | Reusable code (BR/CS/SI) marked verify | Swarm forbids inventing OOB | Protocol: **teaching scripts ≠ OOB**; stamp `verify` / `not OOB` |
| B11 | Official video path (Ask a Ranger, clinics) | Missing | Protocol: `11-video-guide` already; SAM-guide URLs should be **copied into** Learning video index |
| B12 | KPI table with numeric targets (95% recon freshness, etc.) | Community 85/95% only | Protocol: **indicative targets vs SLA** |
| B13 | Finance partner / joint ownership | Path to Value T | Protocol: **RACI in Model gate**, not only admin roles |
| B14 | `ast_contract` / `alm_asset` hierarchy | Named in R, thin in G | Protocol: **shared platform tables** across modules |
| B15 | 5-gate loop, probe.json, LAB-03 break-it, foundation-data load order | **Not in swarm at all** | Swarm is a config encyclopedia. Protocol already wins here — **do not replace the loop with swarm dumps** |

---

## C. What **not** to move either way

| Item | Reason |
|---|---|
| LG sample BR on `u_normalization_status` | Not OOB; contradicts install→DMAP BR |
| LG `sam_sw_reconciliation_result` in Script Include | Unverified table |
| sam-buffy `alm_software` / `sam_license_manager` | Wrong |
| Swarm 299-topic khub dumps | Too raw for a learning page |
| Private rubrics | Stay outside git |

---

## D. Suggested protocol patch (`ServiceNow_Learning` `00-methodology` or module template)

Add one subsection **“Closed-loop modules (SAM, HAM, SPM…)”**:

1. Success ≠ row insert. Success = **two independent truths reconcilable** (owned vs observed).
2. Four object types if a catalog exists (requestable vs master data vs observed vs computed).
3. Pin **plugin IDs** Foundation vs Pro; mark irreversible upgrades.
4. Properties + **named scheduled jobs** in Practise gate.
5. Numeric test: 1 right + 2 observations → shortfall 1.
6. Teaching code stamped not-OOB.
7. Sibling-module contrast (HAM/SAM) in Orient.

SAM-guide page should take **A1–A18**. Learning protocol should take **B1–B15** as reusable gates, using SAM as the worked example already in `08-SAM-SETUP.md` + `LAB-03`.
