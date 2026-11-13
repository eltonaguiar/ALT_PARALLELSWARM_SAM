# 01_PLAN — ServiceNow SAM Module Implementation Plan

- **Compiled by:** `kilo` / provider **kilo** / harness **default** (`kilo__default__kilo`)
- **Date:** 2026-11-13
- **Release basis:** ServiceNow docs Australia (2026-03-12 → 2026-09-30 per pages).
- **Purpose:** Deterministic 5-phase workflow for planning, executing, and delivering a ServiceNow SAM (Software Asset Management) implementation, mirroring the phased approach of `ALT_PARALLELSWARM` (`final/FINAL_deepseek-v4-pro.md`).

---

## 0. Provenance & method

Sources were fetched from the ServiceNow khub API (Australia maps) on 2026-11-13 and retained as raw text in this agent's `research/` folder. Where two sources disagreed, the discrepancy is flagged in §"Known gaps" rather than silently resolved.

Primary sources used:
- `Configuring Software Asset Management` (Australia)
- `Software Asset Management administration` (Australia)
- `Basic Software Asset Management discovery models and software installations` (Australia)
- `Basic Software Asset Management software discovery and normalization` (Australia)
- `Software discovery models` (legacy plugin) (Australia)
- `Software normalization` (Australia)
- `Software discovery and normalization` (Australia)
- `Manually normalize a software model …` / `Manually normalize a software discovery model …` (Australia)
- `Software reconciliation for compliance` + `Software reconciliation results` (Australia)
- `Delete uninstalled software from the Software Installation table` (Australia)
- `Configure a CI to display Software Asset Management data` (Australia)
- `Configure SCCM for Software Asset Management` (Australia)
- Domain separation Oracle reconciliation properties page (Australia)
- `Maturity stages` (Australia) — Crawl/Walk/Run framework
- `Path to Value / Quick Start / Office Hours / Starter Kit / Measuring Outcomes` (ServiceNow Community) (Australia)
- `SAM Configuration Reference` (Australia) — FINAL_SAM_MODULE_REFERENCE.md

---

## 1. Phase 1 — Foundations (Crawl)

### 1.1 CMDB health prerequisites
- Healthy CMDB hardware/computer CIs with enough identity for Discovery/SCCM to land installs (`installed_on`).
- Owners / location / department / cost center / company / country / region on those CIs if grouping reconciliation by them.
- User records if allocating per-user or reclaiming SaaS seats.
- Discovery actually covering the estate (Discovery and/or SCCM/SG connector), not a spreadsheet.
- Entitlement source of truth (contracts, PPN, Microsoft MLS) ready to import.
- In-scope publisher list (packs cost money and complexity).
- Decision on exclude-SAM devices (leased, out of scope, phase-1 location only).

### 1.2 Baseline metrics to capture *before* go-live
| Metric | Why |
|---|---|
| Discovery-model count by normalization status | Content Service value |
| Install count vs unique products vs unique software models | Dedup / auto-create health |
| Unlicensed product-result count | True-up |
| % CIs with owner/location | Recon grouping |
| SaaS assigned vs used (after connector) | Reclamation |
| Time of last successful recon | Operating cadence |
| Published-product count if phase-wise | Scope freeze |

### 1.3 Phase-gate exit criteria (Crawl → Walk)
- CMDB CIs with identity for Discovery landing confirmed.
- Entitlement source of truth ready.
- In-scope publisher list documented.
- Exclude-SAM device decision documented.
- Baseline metrics captured before go-live.

---

## 2. Phase 2 — Walk (Automation & Expansion)

### 2.1 SAM activation sequence
1. Healthy CMDB + discovery coverage (establish processes and roles).
2. Install SAM (Product Hub first-time / Store otherwise).
3. Activate Professional + Workspace plugin (Brazil: `com.sn_samp_master_ws`).
4. Opt in to Content Service (default is **not** opted in).
5. Wire discovery sources (Discovery plugin + patterns; SCCM or Service Graph connector for SCCM — 2012/2016 usage plugins deprecated toward Tokyo).
6. Load entitlements (bulk import / PPN matching) — docs explicitly say discover *after* entitlements for the Discovery/SCCM path.
7. Let daily jobs normalize discovery models.
8. Create custom products / pattern rules / manual normalize for Match Not Found.
9. First reconciliation. Enable auto software-model creation properties only if you want unlicensed models created.
10. Optionally enable `com.snc.samp.manage.published.products` and publish a **small product set** (phase-wise).
11. Reclamation rules, then catalog publish for requestable software (Run-stage: "standard catalog and onboarding process").
12. Success portal: goals, health check, maturity items.

### 2.2 Phase-gate exit criteria (Walk → Run)
- Content Service opt-in confirmed and normalization hit-rate measurable.
- Entitlements loaded and reconciliation running weekly.
- Published-product list phase-wise enabled and re-conciliated.
- Reclamation rules active and reviewable.
- Success portal goals and health checks passing.

### 2.3 Scope freeze
- Enable `com.snc.samp.manage.published.products`.
- Add licensable products under License operations → SAM Implementation → Published products.
- Re-run recon to update published-product scope.

---

## 3. Phase 3 — Run (Standardized operations)

### 3.1 Ongoing runtime pipeline (one install)
1. Source writes a row to `cmdb_sam_sw_install`.
2. **Business rule** (unnamed in docs): if publisher+product+version exists on a discovery model, set the reference; else insert a discovery model and set the reference.
3. Daily `SAM - Normalize discovery models using content library rules` assigns a normalization status. Fallback: wide-net (`com.snc.samp.wide_net_normalization.enabled`, default on) then ML (`com.snc.samp.enable.ml_normalization`, default on).
4. Reconciliation matches installs → software models → entitlements; may auto-create software models if properties allow.
5. Dedup job marks primary vs duplicate installs. IBM special case: `SAM - Deduplicate Install Table` prefers ServiceNow Discovery over authorized provider for IBM.
6. Reclamation rules flag unused rights.
7. `SAM — Adjust Installs for excluded CIs` honors the exclude-device flag.

### 3.2 Phase-gate exit criteria (Run stabilization)
- Normalization status distribution measurable (hit-rate ~85%+ OOTB on SCCM-class sources, ~95%+ after Content Service opt-in).
- Reconciliation running on scheduled cadence (weekly).
- Dedup job marking primary vs duplicate installs correctly.
- Reclamation rules flagging unused rights.
- Excluded CIs adjusted flag working.

### 3.3 Maturity model — Run phase
- Standardized catalog + onboarding in purchasing.
- Automated on-demand software.
- Regular SAM goals.
- Success portal tracks completed goals, actual vs projected savings, health checks passed, value-builder tasks.

---

## 4. Risks and mitigation

| Risk | Mitigation |
|---|---|
| Treating a **discovery model** as a catalog item, or a **catalog item** as a license | Keep distinct: discovery models = deduped discovered strings; catalog items = requestable service catalog entries |
| Discovering before entitlements if PPN-driven models wanted | Load entitlements *before* or *concurrently* with discovery for PPN-driven models |
| Customizing OOB recon jobs instead of properties / custom metrics | Use properties, custom products, pattern rules, dedup rules; do not overlay the install BR |
| Enabling `automaticsmrcreation` then wondering why extra software models appeared | Leave `automaticsmrcreation` off in Crawl so the software-model table stays curated |
| Rolling out all publishers on day one instead of phase-wise | Enable `com.snc.samp.manage.published.products`, add licensable products under License operations → SAM Implementation → Published products, re-run recon |
| Skipping Content Service opt-in then drowning in Match Not Found | Opt in to Content Service early; sharing discovery models with statuses Match not found / Publisher normalized / Partially / Manual improves matching |
| New SCCM work on deprecated 2012/2016 usage plugins | Use Service Graph connector for Microsoft SCCM; legacy plugins deprecated in Tokyo |
| Overlaying the unnamed install→discovery-model business rule | Customization review required on upgrade (Yokohama+); use properties for tuning, not BR overrides |
| Publishing to software catalog with `model_manager` vs `catalog_admin` mixed up | Use `catalog_admin` to publish models to HW or SW catalog; `model_manager` for vendor catalog items |
| Assuming Workspace activation still leaves classic SAM navigation | Workspace activation hides classic menus that moved; several admin menus stay classic-only |

---

## 5. Success criteria

- Content Service opt-in confirmed.
- Normalization hit-rate measurable (~85%+ OOTB, ~95%+ after Content Service).
- Reconciliation running weekly on schedule.
- Published-product list phase-wise enabled and scoped.
- Reclamation rules active and reviewable.
- Success portal goals and health checks passing.
- Baseline metrics captured before go-live and tracked after go-live.
- CMDB health KPIs (correctness, completeness, compliance) improving or stable.

---

## 6. Phase-wise plan (official)

Maturity `[S21]`:
- **Crawl:** healthy CMDB, discovery tools, processes/roles; start with end-user computing or simple SaaS.
- **Walk:** automate Crawl processes; datacenter / BYOL / more SaaS; metering, reclamation, overlapping software, rightsizing from compliance results.
- **Run:** standardized catalog + onboarding in purchasing; automated on-demand software; regular SAM goals.

Product-scope freeze: enable `com.snc.samp.manage.published.products`, add licensable products under License operations → SAM Implementation → Published products, **re-run recon** `[S22]`. Suite publish warns to include parent/children `[S22]`.

Guided path: Product Hub install → Workspace → Content Service → discovery → entitlements → recon → success portal `[S20][S19][S23]`.