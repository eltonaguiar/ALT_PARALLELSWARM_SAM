# phase3_research_done.md — ServiceNow SAM Phase 3: Normalization & Reconciliation Running

- **Compiled by:** `kilo` / provider **kilo** / harness **default** (`kilo__default__kilo`)
- **Date:** 2026-11-13
- **Status:** Phase 3 in progress — Normalization running, reconciliation executed, compliance results visible

---

## 1. Phase 3 objectives

### 1.1 Normalization running daily
- [ ] Daily scheduled job `SAM - Normalize discovery models using content library rules` is running and assigning normalization statuses.
- [ ] Daily scheduled job `SAM - Discovery Model Normalization job` is running and updating normalization trend charts.
- [ ] Normalization status distribution measurable across `cmdb_sam_sw_discovery_model`:
  - `Normalized`
  - `Partially Normalized`
  - `Publisher Normalized`
  - `Match Not Found`
  - `Manually Normalized`
- [ ] If ML Normalization plugin active: ML-based normalization augmenting content library rules.

### 1.2 Reconciliation running weekly
- [ ] Weekly reconciliation running by default, or on demand for specific publishers/groups/subgroups.
- [ ] Group/subgroup dimensions configured (country, department, company, region, cost center).
- [ ] Default group/subgroup set via `Software Asset > Administration > Properties` if desired.
- [ ] Reconciliation results accessible in Core UI and Software Asset Workspace.
- [ ] Three-tier results visible:
  1. Product results — compliance status, true-up cost, potential savings.
  2. Software Model results — per-model detail including License Metric Results and Unlicensed Installs.
  3. License Metric Results — rights owned, rights used, allocation breakdown.

### 1.3 Dedup job running
- [ ] `SAM - Deduplicate Install Table` job has run and marked primary vs duplicate installs.
- [ ] IBM special case: ServiceNow Discovery rows stay Active; authorized-provider duplicates inactivated by dedup job.
- [ ] Custom dedup rules in `sam_sw_dedup_rule` table if needed.

### 1.4 Reclamation rules active
- [ ] Reclamation rules flagging unused rights over time (hours/latest date).
- [ ] Suite parent pulling components automatically; filter on parent applies to children.
- [ ] SaaS/SSO integration auto-creates a reclamation rule — reviewed and confirmed.

---

## 2. Phase 3 activities (week 7–12)

| Activity | Owner | Deliverable |
|---|---|---|
| Daily normalization jobs verification | `sam_user` | Confirm jobs running; status distribution captured |
| First reconciliation run | `sam_admin` | Reconciliation results visible; three-tier compliance data |
| Dedup job verification | `sam_admin` | Primary vs duplicate installs marked; IBM case confirmed |
| Reclamation rules review | `sam_admin` | Unused rights flagged; SaaS rule reviewed |
| Content Service opt-in if deferred | `sam_admin` | Opt in to Content Service; normalization hit-rate measurable |
| Published-product list phase-wise | `sam_admin` | Enable `com.snc.samp.manage.published.products`; add licensable products; re-run recon |

---

## 3. Phase 3 gate review

**Go to Phase 4 when:**
- Daily normalization jobs running and assigning statuses.
- Weekly reconciliation running and producing three-tier results.
- Dedup job has marked primary vs duplicate installs.
- Reclamation rules active and unused rights flagged.
- Content Service opt-in confirmed (if deferring from Phase 2) and normalization hit-rate measurable.
- Published-product list phase-wise enabled and re-conciliated.

**Stay in Phase 3 if:**
- Normalization not running or statuses not assigning.
- Reconciliation not running or results incomplete.
- Dedup job not marking installs correctly.
- Reclamation rules not flagging unused rights.