# Operations Runbook

> **Status legend:** **V** verified; **C** corroborated; **U** unverified/instance-dependent; **P** practice.
> **Audience:** SAM administrator, platform owner, change manager.
> **Rule:** this runbook is for a **sub-production instance first**. No step in this document was executed against a live instance in this pass.

---

## 1. Pre-flight (do not skip)

| # | Check | Pass evidence |
|---|---|---|
| 1 | Edition and plugin confirmed | `com.sn_samp_master_ws` (or your edition's plugin) active; `samp_*` / `cmdb_sam_*` tables exist **V** |
| 2 | Roles assigned | `sam_admin` and `sam_user` populated; `sam_developer` restricted **V** |
| 3 | Foundation data loaded | Companies, locations, departments, cost centers, users **P** |
| 4 | One discovery source configured | A sample CI has a current `discovery_source` and at least one install **P** |
| 5 | CI identification verified | No duplicate CI tasks for the pilot class; identifier rules reviewed **V** |
| 6 | Content Library reachable | Download job succeeded; publisher packs present **V** |
| 7 | Reconciliation result table present | `samp_reconciliation_result` exists **V** |
| 8 | Change record opened | Scope, rollback, and owner recorded **P** |

If any check fails, stop. A later step cannot compensate for a missing gate.

---

## 2. Setup runbook

### Step 1 — Activate the correct master plugin

- Confirm edition (Foundation vs Professional).
- Activate the release-correct master (`com.sn_samp_master_ws` in Brazil). **V**
- Wait for plugin activation to complete; verify tables.

**Pass:** plugin active, tables present, no failed activation jobs. **V**

### Step 2 — Install scope plugins

- Publisher packs for in-scope publishers. **V**
- Optional: ML normalization, SaaS, Spend, Engineering. **V**
- Do **not** install every pack "just in case"; each adds configuration surface. **P**

**Pass:** only in-scope packs active; licence entitlements confirmed. **V**

### Step 3 — Roles and integration users

- `sam_admin` for administrators. **V**
- `sam_user` for analysts. **V**
- `sam_developer` only for trained script authors. **V**
- `sam_integrator` for SaaS profiles. **V**

**Pass:** least-privilege review signed off. **P**

### Step 4 — Foundation data

- Companies, locations (with time zones), departments, cost centers, users, groups. **P**
- Ensure the cost-center and department fields used for reconciliation grouping are populated and standardized. **P**

**Pass:** grouping dimensions resolve for a sample of entitlements. **P**

### Step 5 — Configure one discovery source

- Choose one: Service Graph SCCM, Intune, Jamf, Discovery, or ACC. **V**
- Pilot a small scope. **P**
- Verify installs land in `cmdb_sam_sw_install` with a discovery model reference. **V**

**Pass:** sample CI shows installs; discovery models created; no mass `Match Not Found` spike. **V/P**

### Step 6 — Verify CI identity

- Review identifier rules for the pilot class. **V**
- Check duplicate and reclassification tasks. **V**
- Confirm reconciliation rules authorize the intended sources. **V**

**Pass:** no unexplained duplicate CIs; the intended source can update the intended fields. **V**

### Step 7 — Normalization

- Confirm the daily normalization job runs. **V**
- Review status distribution. **V**
- Resolve the top titles before scaling. **P**
- Do not enable auto-model creation until the normalization gate passes. **P**

**Pass:** top titles map to one software model each; `Match Not Found` backlog owned. **V/P**

### Step 8 — Entitlements

- Import or create entitlements from contracts/POs. **V**
- Link every entitlement to a software model and a metric. **V**
- Use PPN where available to improve model resolution. **V**
- Never overwrite quantity; create true-up/adjustment records. **P**

**Pass:** zero entitlements with no model or metric; every entitlement traceable to a contract/PO. **V/P**

### Step 9 — First reconciliation

- Run reconciliation for the pilot scope. **V**
- Treat the result as a **data-quality loop**, not a true-up invoice. **P**
- Triage the top three gaps: normalization, missing entitlement, duplicate install, metric mismatch. **P**

**Pass:** top three gaps explained and assigned; no unexplained `Unknown`. **P**

### Step 10 — Reporting and ownership

- Configure the Software Asset Overview, License Position report, normalization dashboard, and Health Check. **V**
- Assign an owner for SAM, each connector, and each publisher. **P**
- Define the weekly review. **P**

**Pass:** named owner; dashboard refreshed; health check scheduled. **V/P**

### Step 11 — Scope freeze (optional, phase-wise)

- Enable `com.snc.samp.manage.published.products`. **V**
- Publish only the products in the pilot. **V**
- Re-run reconciliation so the published set is the reporting surface. **P**

**Pass:** reports reflect only published products; unpublished products excluded intentionally. **V/P**

---

## 3. First reconciliation is a data-quality loop

Use this sequence every time before trusting a number:

1. **Normalization:** are the top titles mapped? **V**
2. **Duplicates:** are duplicate installs suppressed? **V**
3. **Metric match:** does the entitlement metric match the model metric? **P**
4. **Dates:** are entitlements active for the period? **V**
5. **Scope:** are retired/leased CIs excluded? **V**
6. **Usage:** is the usage feed current? **P**
7. **Only then:** read the compliance position. **P**

**Anti-pattern:** buying or reclaiming licenses to "fix" a data-quality artifact. **P**

---

## 4. Operating cadence

| Cadence | Task | Owner |
|---|---|---|
| Daily | Check SAM job log (`Name starts with SAM`); normalization status trend | SAM admin |
| Weekly | Review reconciliation results and Health Check; triage top gaps | SAM admin + publisher owners |
| Weekly | Review `Match Not Found` and normalization suggestions | Normalization owner |
| Weekly | Review connector health (SaaS and inventory) | Integration owner |
| Monthly | Review entitlements expiring in 90 days; renewals | Procurement + SAM |
| Monthly | Review over-licensed and reclamation candidates | SAM + finance |
| Quarterly | Re-baseline scope, metrics, and ownership | ITAM manager |
| On change | Re-run reconciliation after any model/metric/rule change | Change owner |

**P**, with **V** job/health-check references.

---

## 5. Health checks and KPIs

| KPI | Definition | Healthy signal |
|---|---|---|
| Normalization rate | Normalized / total discovery models | ≥ 85% before scaling; ≥ 95% after Content Service **P** |
| `Match Not Found` backlog | Count and age | Trending down |
| Duplicate install rate | Duplicates / installs | Stable after dedup rules |
| Entitlements with model+metric | % of entitlements | 100% **P** |
| Reconciliation freshness | Age of latest successful run | Within the agreed cadence **P** |
| Unlicensed installs | Count by publisher | Trending down in pilot |
| Over-licensed amount | Cost of unused rights | Trending down |
| Connector freshness | Last successful sync per connector | Within agreed SLA **P** |
| Failed SAM jobs | Count per day | Zero or explained **V** |

Health Check categories: SQL Server Config/CMDB, Windows Server Config/CMDB, Oracle Database, Java-Oracle, WebLogic-Oracle, Microsoft 365, General. **V**

---

## 6. Troubleshooting

| Symptom | Likely cause | Verify | Fix |
|---|---|---|---|
| Everything looks unlicensed | No entitlement for the model, or metric mismatch | `alm_license` for the model; metric on both sides | Add/correct entitlement; align metric |
| Install count doubles | Two discovery sources; dedup not configured | Group installs by `discovery_source` | Configure dedup; consolidate source |
| Normalization stuck at `Match Not Found` | Content Library miss; pattern gap | Status distribution; sample models | Manual normalize / pattern rule / Content Service |
| `Unknown`-looking results | Missing model link or feed | Orphan installs; model links | Fix normalization/model mapping |
| Oracle count implausible | Core factor / virtualization aggregation | `com.snc.samp.oracle.reconlevel`; host affinity | Correct property; validate with publisher rules |
| Suite components over-counted | Suite roll-up missing | Suite membership; inferred suite | Configure suite; verify `Omit from suites` |
| Retired devices still count | Installs not removed/excluded | Installs on retired CIs | Delete installs; exclude CI; wait for job |
| Reconciliation did not run | Job failure | `samp_job_log`; `samp_reconciliation_result` | Fix job; re-run |
| Entitlement import errors | PPN/model not found; metric invalid | `samp_entitlement_import` | Correct PPN/model/metric |
| SaaS shows no waste | Dead connector | Last successful sync | Restore connector; assign owner |
| Source cannot update a CI field | IRE reconciliation rule missing | `cmdb_reconciliation_definition` | Add specific-attribute rule |
| Trusted source cannot create CIs | IRE data source rule blocks insert | `cmdb_ire_data_source_rule` | Narrow/disable rule |

**V/P.**

---

## 7. Rollback and change control

### 7.1 Rollback patterns

| Change | Rollback |
|---|---|
| Wrong metric on an entitlement | Create a corrected entitlement/true-up record; retire the old; keep both auditable **P** |
| Bad normalization rule | Disable the rule; re-run matching; inspect `Match Not Found` delta; document in CR **P** |
| Wrong software model | Create a corrected model; re-run reconciliation; deprecate (do not delete) the old **P** |
| Bad third-party feed | Disable the connector/property; stop the feed; do not delete raw installs ad hoc **P** |
| Published-products scope error | Adjust published set; re-run reconciliation **P** |
| IRE rule error | Disable the rule; restore previous priority; re-run affected payloads **P** |

### 7.2 Change-control blast radius

| Change | Blast radius | CAB |
|---|---|---|
| Manual normalize one model | Low | No |
| Pattern/wide-net rule | Medium | Sample-test |
| Software model create/match | Medium | High-spend review |
| License metric change | **High** | Yes |
| Reconciliation grouping | **High** | Yes |
| IRE identifier attributes | **High** | Yes |
| SaaS connector disable | **High** | Yes |
| Published-products scope | Medium/High | Yes |

**P**

---

## 8. Audit evidence chain

For each material entitlement, retain:

1. Contract (`ast_contract`) → PO/invoice → entitlement (`alm_license`). **V/P**
2. Software model → license metric → quantity and dates. **V**
3. Normalized installs → discovery model → `discovery_source` and last-seen. **V**
4. Usage evidence where the metric depends on use. **V**
5. Reconciliation run result and the inputs used. **V**
6. Change record for any model/metric/rule change. **P**

**Rule:** never overwrite history to make a report look right. Create a new record and explain it. **P**

---

## 9. Go/no-go gates

| Gate | Go criteria | No-go action |
|---|---|---|
| **G1 Schema** | Correct edition/plugin; tables present | Stop; fix activation |
| **G2 Identity** | No unexplained duplicate CIs; rules reviewed | Fix IRE before loading more |
| **G3 Feed** | One trusted source; installs and models created | Fix connector |
| **G4 Normalization** | Top titles mapped; backlog owned | Do not enable auto-create |
| **G5 Entitlements** | 100% have model + metric + evidence | Fix imports |
| **G6 Reconciliation** | Run completes; top gaps explained | Treat as data-quality loop |
| **G7 Operations** | Owner, cadence, health check, rollback | Do not declare live |

**P**

---

## 10. Open items (instance-only verification)

- Exact plugin IDs and role containment in your release. **U**
- Exact scheduled job names, cadence, and time zone. **U**
- Exact table/field API names (`normalization_status`, `software_model`, `license_metric`). **U**
- Whether your instance uses static or dynamic IRE. **U**
- Publisher-specific rules and contract terms (Oracle, IBM, SAP, Microsoft, Adobe). **U**
- SaaS connector inventory and health. **U**
- Any custom `u_*` fields the guide or local code references — they are **custom**, not OOB. **U**
