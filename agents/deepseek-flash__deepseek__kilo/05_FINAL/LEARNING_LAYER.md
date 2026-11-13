# LEARNING LAYER — pedagogical assets from the SAM guide, corrected and added to the repo

**Agent:** `deepseek-flash__deepseek__kilo` · **Date:** 2026-11-13
**Why this file exists:** the live SAM guide is a better *teacher* than the research repo, but several of its table/field names are wrong or non-OOB. This file preserves the teaching value and corrects the facts. It is the "guide → repo" half of `GUIDE_VS_REPO_DELTA.md`.

Marks: **V** Brazil-documented · **C** corroborated · **P** programme practice · **U** verify on instance.

---

## 1. CIS-SAM exam alignment

| Domain | ~Weight | What it covers |
|---|---|---|
| 1. SAM overview & fundamentals | 15% | ITAM/SAM positioning, lifecycle, roles, value case |
| 2. Data integrity — models, normalisation, Content Library | 25% | Software models, discovery models, normalisation, publisher packs, suites |
| 3. Entitlements, licences, reconciliation | 30% | Licence metrics, entitlement records, reconciliation logic, compliance states |
| 4. Optimisation, reclamation, audit defence | 20% | Reclamation, true-up, publisher rules, audit workflow |
| 5. Reporting, dashboards, operational integration | 10% | Workspace, dashboards, KPIs, integrations |

Weights are the guide's; confirm against the current Now Learning blueprint. Prep path: Welcome to ServiceNow → Administration Fundamentals → SAM Fundamentals → SAM Professional/Implementation → CIS-SAM Exam Prep.

---

## 2. ELI5

You own **1,000** Microsoft 365 E3 rights. Discovery finds **1,180** installs and **1,090** active users. Reconciliation says you are **90 users under-licensed**. You either buy 90 (true-up) or reclaim 90 unused accounts before the publisher audits you. Everything else in SAM — optimisation, reclamation, renewal, audit defence — is downstream of that calculation.

---

## 3. SAM vs HAM vs ITAM

| Aspect | HAM | SAM | ITAM |
|---|---|---|---|
| Tracks | Physical hardware assets | Software rights, installs, usage | Both |
| Primary question | What do we own, where, who has it? | Are we compliant? Over/under-licensed? | Full portfolio cost & risk |
| Core record | `alm_asset` / `alm_hardware` | Software model + entitlement + install | `alm_asset` hierarchy |
| Key engine | Asset lifecycle, hardware normalisation | **Reconciliation** | Both |
| Key risk | Lost/stolen/stale assets, depreciation | Audit fines, wasted licence spend | Both |
| Shared tables | `alm_asset`, `alm_model`, `ast_contract` | `alm_asset` (licences), `ast_contract` | all |

**Exam-critical:** SAM adds the `software model → discovery model → installation → usage → entitlement → reconciliation result` chain. HAM has no reconciliation equivalent.

---

## 4. SAM lifecycle

```
Request → Procure → Entitle → Discover/Normalise → Reconcile → Remediate/Optimise → Renew/Retire
                  ↑                                                        │
                  └──────────────────── continuous loop ───────────────────┘
```

The loop is continuous: reclamation feeds reconciliation; renewal decisions use the resulting position.

---

## 5. Five record types (expanded from the guide's "three")

**Mnemonic:** *Model = what it is. Entitlement = what you may use. Installation = what exists. Usage = what is used. Reconciliation = the difference.*

| Record | Table | Meaning | Created by |
|---|---|---|---|
| **Software model** | `cmdb_software_product_model` **V** | Canonical, purchasable/managed product profile | Content Library or SAM admin |
| **Discovery model** | `cmdb_sam_sw_discovery_model` **V** | Raw observed fingerprint, deduped per publisher/product/version | Discovery/SCCM/import (cannot be created manually) |
| **Installation** | `cmdb_sam_sw_install` **V** | One concrete install on one CI | Discovery/import |
| **Usage** | `samp_sw_usage` **V** (not `cmdb_sam_sw_usage`) | Evidence of use, product level | Usage connectors/manual |
| **Entitlement** | `alm_license` **V** | Right to use N units under a metric | SAM admin/import |
| **Result** | `samp_product_result` → Software Model Result → `samp_license_metric_result` **V** | Computed compliance, three tiers | Reconciliation job |

Supporting reference data the guide omits: vendor (`core_company`), publisher (`samp_sw_publisher`), PPN (`samp_sw_product_definition`), catalog item (`sc_cat_item`). See `SAM_MODULE_REFERENCE.md` §2.4.

**Chain correction:** an installation references `discovery_model`; the `software_model` reference is on the **discovery model**, set by the matching job.

---

## 6. Compliance-position vocabulary (with the product caveat)

| Position | Meaning | Financial meaning | Action |
|---|---|---|---|
| Compliant | Rights ≥ demand | Neutral | Monitor; harvest reclaimed rights |
| Over-licensed | Rights > demand | Money already spent, wasted | Reclaim, reduce renewal, renegotiate |
| Under-licensed | Rights < demand | Audit exposure / unbudgeted true-up | True-up or reclaim/remove |
| Unlicensed | Installs with no entitlement | Highest audit risk | Remove, purchase, or reclassify freeware/OSS |
| Not counted | Excluded by rule (excluded CI, ignore list) | Excluded from risk | Review annually — exclusions creep |
| Unknown | Insufficient data (unmatched model, missing feed) | Unknown risk | Fix normalisation/feed; **never report as compliant** |

**Caveat (V):** the product's License Position "Software model status" is only **Compliant** or **Not Compliant**. Over/Under/Unlicensed/Unknown are *interpretations* of rights needed, unlicensed installs, and missing data — not extra status dots on the form. Teach the vocabulary, but report from the fields.

---

## 7. Publisher audit traps (**P/U** — confirm against the contract)

| Publisher | Trap |
|---|---|
| Microsoft | SQL Server per-core (physical cores + core factor, minimum 4 cores/socket); virtualisation rules; M365 suite overlap; downgrade rights must be documented; SA must be linked to perpetual to count |
| Oracle | Core-factor table per processor family; server-level licensing unless certified hard partitioning; Oracle LMS scripts are the audit instrument; Named User Plus minimums; `reconlevel`/host affinity are SAM settings, not the contract |
| IBM | PVU table per processor model; sub-capacity requires ILMT/BigFix evidence; region must be set |
| SAP | Named-user type classification; indirect/digital access is the live audit battleground |
| Adobe | VIP/ETLA named user; shared-device licensing differs; Creative Cloud suite roll-up |
| ServiceNow | Subscription by product line and fulfilled user; over-consumption is billed, not audited — a cost-control problem |

The guide's Oracle "10% rule" and "audit package export" are **U** — not verified in the Brazil pages.

---

## 8. What breaks reconciliation (symptom → cause)

| Symptom | Likely cause |
|---|---|
| Everything "unlicensed" | No entitlement for the model, or metric mismatch |
| Huge duplicate install count | Two sources without dedup (`Active` flag) |
| Installs appear then vanish | Source rotation or normalisation remap |
| Compliance fluctuates weekly | Intermittent usage feed |
| One publisher wildly over-licensed | Suite roll-up missing; components counted separately |
| Oracle numbers impossible | Oracle options/core-factor settings not configured (`samp_oracle_options`, `reconlevel`) |
| Newly discovered software never counts | Discovery model stuck in `Match Not Found` / no `Licensable` product type / `License under management` unset |
| Rights used drops without a purchase | CI retired/stolen deletes related installs **V** |

**Reconciliation is a report, not a correction.** Fix the model, entitlement, normalisation, or feed — never edit the result row.

---

## 9. Fields people forget

- Licence metric on the entitlement **and** the model's metric group/metric attributes — mismatch is the #1 silent reconciliation failure.
- Suite membership on the software model — without it, components over-count.
- `installed_on` pointing at a retired CI — phantom demand forever.
- Entitlement `end_date` — expired rights still look compliant if not filtered.
- Virtualisation/hosting flags on the CI — required for Microsoft/Oracle per-host rules.
- `License under management` — a model can exist and never reconcile.
- `Automatically matched` on the discovery model — tells you whether a human overrode the job.

---

## 10. Day-one reports (corrected to real tables)

| Report | Table | Grouping | Why |
|---|---|---|---|
| Entitlements expiring in 90 days | `alm_license` | publisher, end date | Renewal pipeline |
| Under-licensed models | `samp_product_result` / `samp_license_metric_result` | publisher, model | Audit triage |
| Unmatched discovery models | `cmdb_sam_sw_discovery_model` (status `Match Not Found`) | publisher | Normalisation backlog |
| Installs with no usage 90 days | `cmdb_sam_sw_install` + `samp_sw_usage` | software model | Reclamation pipeline |
| Cost of over-licensing | `samp_product_result` / `samp_license_metric_result` | publisher | CFO conversation |
| Normalisation status mix | `cmdb_sam_sw_discovery_model` | status | Data-quality KPI |
| Failed SAM jobs | `samp_job_log` | job | Ops health |
| CDS download status | Central Data Service Download Status | table | Content freshness |

Do **not** build on `sam_sw_reconciliation_result` (not documented).

---

## 11. Guided lab (7 steps)

Use a sub-production instance.

1. **Pick a model** in `cmdb_software_product_model` with publisher, version, metric group, suite membership. Record the sys_id.
2. **Create an entitlement** in `alm_license`: same model and metric, rights **1**, start today, end +1 year. Publish → In use.
3. **Confirm installs** in `cmdb_sam_sw_install` for that model's discovery model; note count `n > 1`.
4. **Reconcile**; open the result. Expect rights owned 1, used `n`, unlicensed `n−1` (or negative available), **Not Compliant**.
5. **Prove the fix:** add rights (or a true-up entitlement) to `n+5`; re-run; expect Compliant. Historical results remain.
6. **Prove normalisation:** find a `Match Not Found` discovery model in the same publisher family, normalise it, re-run, observe demand change.
7. **Teach back:** five sentences — model, entitlement, install, reconciliation, position.

**Numeric companion:** T0–T10 in `ROUND2_GAP_ANALYSIS.md` §4.5. The simplest is T0: 1 right, 2 installs on 2 devices → 1 unlicensed; the same 2 installs on 1 device with `Major`/`Any` dedup → 1 used.

---

## 12. Quiz

1. Difference between software model, discovery model, installation?
2. Three inputs reconciliation compares?
3. Why must the entitlement metric match the model's counting basis?
4. What does "unknown" mean, and why is it not compliant?
5. Why configure suite membership?
6. Correct way to fix under-licensing caused by a wrong quantity?
7. Why a sustained inactivity window before reclaiming?
8. Two publisher rules that cause audit findings?

**Answers:** 1. Canonical product / raw observed fingerprint / one install on one CI. 2. Entitlement rights, normalised install demand, usage evidence (+ publisher rules). 3. A mismatch compares different counting bases and produces a plausible but meaningless number. 4. Missing data (unmatched model or feed) — reporting it as compliant hides exposure. 5. Otherwise components count individually and inflate demand. 6. Create a true-up/adjustment entitlement; never overwrite the original quantity. 7. Usage feeds have gaps; absence of evidence is not evidence of absence. 8. Microsoft SQL core/virtualisation; Oracle core factor/server licensing; IBM PVU sub-capacity; SAP indirect access.

---

## 13. Mnemonics

- **Five records:** *It is · You may · It exists · It is used · The difference.*
- **Normalisation:** *New → Match → Publisher → Partial → Full → Manual.*
- **Rights:** *Owned − Used = Available; Used = Allocated-in-use + Not-allocated-in-use.*
- **Recon:** *Report, never correct.*
- **Maintenance:** *No perpetual, no rights.*
- **Unknown:** *Unknown ≠ Compliant.*
- Cross-module mnemonics (BAA, LOCS, IRE, ARM, Retire-before-Delete, Order-vs-Priority, Coalesce, Log-first) belong in the generic learning protocol, not the SAM reference.

---

## 14. SLA-style targets (**P** — programme choices, not product SLOs)

| Commitment | Target |
|---|---|
| New discovery model normalised | within 5 business days |
| Reconciliation run | weekly (Brazil default) or agreed cadence; results < 8 days old |
| Under-licensed finding triaged | within 5 business days |
| Renewal review before expiry | 60 days |
| Reclamation candidate validated | within 10 business days |
| `New` status older than 48h | zero |

The guide's "nightly, <24h" conflicts with the documented weekly default; choose deliberately.

---

## 15. SaaS waste pattern + connector health

**Pattern:** 1,000 assigned M365 E5 seats, 260 never signed in for 90+ days → ~26% of spend recoverable with no user impact — *if* connector data is trustworthy and reclaim has an owner.

**Connector essentials:** least-privilege API credentials; refresh cadence matched to API limits; a named owner; **dead-connector alerting** (a dead connector looks exactly like "no waste"). Reclamation rule is auto-created with a direct integration profile — review it **V**. Do not attach SSO **and** a direct profile to the same app **C**. Unmatched subscriptions land in `samp_sw_unrecognized_subscription_identifier` **V**.

---

## 16. Optimisation priority order + workflow

1. Reclaim dormant SaaS/named-user seats (fastest, lowest risk).
2. Uninstall unused installs (servers with per-core licensing first).
3. Right-size editions (Enterprise → Standard, E5 → E3).
4. Consolidate overlapping tools.
5. Align renewal quantities to reconciled demand.
6. Gate new requests on existing entitlement.

**Workflow:** identify → validate with owner → notify → grace period → reclaim/remove → re-run reconciliation → record savings. Never reclaim on one night of data; require a sustained window (60–90 days, **P**) and owner sign-off.

---

## 17. Safe reusable patterns (custom, not OOB)

The guide's samples are useful teaching code but use non-OOB fields and a non-existent result table. Safe replacements:

**A. Read-only normalisation check (no field write).**
```javascript
// Scheduled job / fix script (read-only). Verify table/field names first.
var gr = new GlideRecord('cmdb_sam_sw_discovery_model');
gr.addQuery('norm_status', 'in', 'match_not_found,partially_normalized,publisher_normalized'); // U: verify choice values
gr.addQuery('sys_updated_on', '<', gs.daysAgoStart(5));
gr.setLimit(500);
gr.query();
while (gr.next()) {
  gs.warn('[SAM] Stale unnormalised discovery model ' + gr.getDisplayValue('display_name'));
}
```

**B. Entitlement expiry report (no state mutation).**
```javascript
var gr = new GlideRecord('alm_license');
gr.addQuery('end_date', '<', gs.nowDateTime());
gr.addQuery('active', true); // verify field
gr.query();
while (gr.next()) {
  gs.info('[SAM] Expired entitlement ' + gr.number + ' ' + gr.getDisplayValue('end_date'));
}
```

**C. Compliance aggregate (three-tier table, not `sam_sw_reconciliation_result`).**
```javascript
var agg = new GlideAggregate('samp_license_metric_result'); // verify
agg.addAggregate('SUM', 'rights_owned');   // U: verify column
agg.addAggregate('SUM', 'rights_used');    // U: verify column
agg.groupBy('license_metric');
agg.query();
```

**D. Metric warning on entitlement (client-side, no custom field).**
```javascript
function onChange(control, oldValue, newValue, isLoading) {
  if (isLoading || !newValue) return;
  if (!g_form.getValue('license_metric')) { // U: verify field
    g_form.showFieldMsg('license_metric', 'Metric mismatch silently breaks reconciliation.', 'warning');
  }
}
```

All four are **examples**; confirm table/field names with `sys_dictionary`/`sys_db_object` before use. Do not overlay OOB jobs or the install→discovery-model business rule.

---

## 18. Official learning resources

- Now Learning: SAM Fundamentals, SAM Professional/Implementation, CIS-SAM Exam Prep.
- Product documentation: `docs.servicenow.com` → IT Asset Management → Software Asset Management.
- Now Support KB for reconciliation/normalisation errors.
- ServiceNow Community Path to Value / Office Hours (practice, not product docs).
