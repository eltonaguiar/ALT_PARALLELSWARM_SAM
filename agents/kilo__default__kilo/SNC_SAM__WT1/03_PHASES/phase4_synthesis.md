# phase4_synthesis.md — ServiceNow SAM Phase 4: QA & Stabilization

- **Compiled by:** `kilo` / provider **kilo** / harness **default** (`kilo__default__kilo`)
- **Date:** 2026-11-13
- **Status:** Phase 4 in progress — QA validation, anti-pattern check, and stabilization

---

## 1. Phase 4 objectives

### 1.1 QA validation checklist

#### 1.1.1 Discovery Status verification
- [ ] `Discovery → Status` — confirm devices reach `Identified CI`, not `Active, couldn't classify`.
- [ ] Per-device states flow: `Alive, not active, not classified` → `Active` → `Classified` / `Active, couldn't classify` → `Identified CI` / `Identified, ignored extra IP` → `Updated CI`.
- [ ] Show Discovery Timeline — confirm every probe/sensor/pattern with queueing vs processing time and ECC queue records; fastest way to see where a device stalled.

#### 1.1.2 CMDB CI audit
- [ ] `cmdb_ci_computer` list — filter `duplicate_of is not empty` for the class just scanned.
- [ ] CI Class Manager → class → Identifiers: confirm exactly one rule, and that its entries match the attributes your pattern actually returns.
- [ ] CI form → CI Health widget: if duplicate score says *not applicable*, you have no identification rule at that class or its ancestors.

#### 1.1.3 SAM-specific QA
- [ ] Normalization and content dashboard — status distribution measurable.
- [ ] License position / true-up cost articles — baseline captured.
- [ ] Health check scan — run and pass.
- [ ] Success portal widgets: SAM maturity, completed goals, savings, health checks passed, value builder tasks.
- [ ] Software model list — `Created source` column verified.
- [ ] Install Active flag after dedup — confirmed.

#### 1.1.4 Anti-pattern validation
- [ ] NOT treating a discovery model as a catalog item, or a catalog item as a license.
- [ ] NOT discovering before entitlements if PPN-driven models wanted.
- [ ] NOT customizing OOB recon jobs instead of properties / custom metrics.
- [ ] NOT enabling `automaticsmrcreation` in Crawl (keeps software-model table curated).
- [ ] NOT rolling out all publishers on day one instead of phase-wise.
- [ ] NOT skipping Content Service opt-in then drowning in Match Not Found.
- [ ] NOT new SCCM work on deprecated 2012/2016 usage plugins.
- [ ] NOT overlaying the unnamed install→discovery-model business rule.
- [ ] NOT publishing to software catalog with `model_manager` vs `catalog_admin` mixed up.
- [ ] NOT assuming Workspace activation still leaves classic SAM navigation.

### 1.2 Data quality checks

#### 1.2.1 Normalization hit-rate
- [ ] Measurable hit-rate: ~85%+ OOTB on SCCM-class sources, ~95%+ after Content Service opt-in.
- [ ] Treat as Path-to-Value figure, not an SLA.

#### 1.2.2 Reconciliation cadence
- [ ] Weekly reconciliation running on schedule.
- [ ] Reconciliation results accessible and reviewable.

#### 1.2.3 Dedup integrity
- [ ] Duplicate sets properly resolved (main CI + N duplicates with `duplicate_of`).
- [ ] No new duplicates re-created on next scan (inclusion rules / skip-duplicates configured).

#### 1.2.4 Reclamation validity
- [ ] Reclamation rules flagging unused rights over the defined time period.
- [ ] Timeout property `sam_reclamation_flow_error_timeout` default 30 days then Closed/canceled.

### 1.3 Stabilization checks

#### 1.3.1 Phase-wise scope freeze
- [ ] `com.snc.samp.manage.published.products` enabled.
- [ ] Licensable products added under License operations → SAM Implementation → Published products.
- [ ] Reconciliation re-run to update published-product scope.
- [ ] Suite publish warns to include parent/children.

#### 1.3.2 Success portal goals
- [ ] Completed goals tracking actual vs projected savings.
- [ ] Health checks passed.
- [ ] Value-builder tasks assigned.

#### 1.3.3 Maturity model assessment
- [ ] Crawl → Walk → Run maturity assessed and documented.
- [ ] Phase-wise plan progress visible.

---

## 2. Phase 4 activities (week 13–16)

| Activity | Owner | Deliverable |
|---|---|---|
| Discovery Status walkthrough | `discovery_admin` | Devices reach `Identified CI`; Timeline reviewed |
| CMDB Health KPIs | `cmdb_admin` | Correctness, completeness, compliance KPIs captured/improving |
| SAM Anti-pattern review | `sam_admin` | All 10 anti-patterns checked; none active |
| Normalization hit-rate measurement | `sam_user` | Hit-rate ~85%+ OOTB or ~95%+ after Content Service |
| Reconciliation QA | `sam_admin` | Weekly cadence confirmed; three-tier results reviewable |
| Dedup template check | `sam_admin` | Duplicate sets resolved; inclusion rules/skip-duplicates configured |
| Reclamation review | `sam_admin` | Unused rights flagged; timeout property verified |
| Phase-wise scope freeze | `sam_admin` | `com.snc.samp.manage.published.products` enabled; products published; recon re-run |
| Success portal goals | `sam_user` | Goals created; completed; savings tracked |

---

## 3. Phase 4 gate review

**Go to Phase 5 when:**
- Discovery Status: devices reach `Identified CI`; no `Active, couldn't classify` failures.
- CMDB Health KPIs: correctness/completeness/compliance improving or stable.
- Anti-patterns: zero active anti-patterns from the 10 documented.
- Normalization hit-rate: measurable (~85%+ OOTB, ~95%+ after Content Service).
- Reconciliation: weekly cadence; three-tier results reviewable.
- Dedup: duplicates resolved; inclusion rules/skip-duplicates configured.
- Reclamation: unused rights flagged; timeout verified.
- Phase-wise scope freeze: `com.snc.samp.manage.published.products` enabled; products published; recon re-run.
- Success portal: goals completed; savings tracked; health checks passed.

**Remediate and re-loop if:**
- Any QA checklist item fails.
- Anti-patterns identified and need remediation.
- Normalization hit-rate below thresholds.