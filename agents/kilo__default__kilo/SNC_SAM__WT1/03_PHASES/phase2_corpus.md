# phase2_corpus.md — ServiceNow SAM Phase 2: Activation & Corpus Built

- **Compiled by:** `kilo` / provider **kilo** / harness **default** (`kilo__default__kilo`)
- **Date:** 2026-11-13
- **Status:** Phase 2 in progress — SAM plugin activation, data model setup, and initial configuration

---

## 1. Phase 2 objectives

### 1.1 SAM plugin activation
- [ ] Install/activate Software Asset Management (`com.sn_samp_master_ws`).
- [ ] Optionally activate ML Normalization plugin (`com.sn_sam_ml_normalization`).
- [ ] Outcome: SAM tables created (`cmdb_sam_sw_install`, `cmdb_sam_sw_discovery_model`, etc.) and Discovery behaviour changes on the next run.

### 1.2 Roles and entry points assignment
- [ ] Assign `sam_admin` role to configuration administrators.
- [ ] Assign `sam_user` role to analysts who view/review configurations.
- [ ] Assign `admin` / `sn_cmdb_admin` for CI form related-list and property configuration.
- [ ] Verify entry points are accessible:
  - `All > Software Asset > …` (core UI)
  - `All > Software asset > Software Asset Workspace > License operations > Discovery models` (new workspace)
  - `All > Configuration > Servers > All` / `cmdb_ci_computer.list` (SAM related list)
  - `All > Software Asset > Administration > Application Properties`
  - `All > Software Asset > Administration > Job Results`

### 1.3 Discovery sources configuration
- [ ] Configure Discovery schedules (per Discovery reference §5) for software scanning.
- [ ] If using SCCM: activate the integration plugin for your SCCM version and the software-usage plugin if usage data desired.
- [ ] Prefer Service Graph connector for Microsoft SCCM; legacy 2012/2016 usage plugins deprecated toward Tokyo.
- [ ] Set `Discover` schedule type and credentials as appropriate in Discovery.

### 1.4 CI form configuration
- [ ] Navigate to `All > Configuration > Servers > All` (or `cmdb_ci_computer.list`), open a computer CI.
- [ ] Right-click header → `Configure > Related Lists`.
- [ ] From `Available`, add `Software Installation -> Installed on` to `Selected` → `Save`.
- [ ] Verify the `Software Installations` tab appears on the computer CI's related-list section.

### 1.5 Entitlement loading (critical timing)
- [ ] **Load entitlements AFTER discovery is configured** (docs explicitly say discover after entitlements for the Discovery/SCCM path).
- [ ] Bulk import / PPN matching for software models.
- [ ] Verify entitlements are loaded before running the first reconciliation.

---

## 2. Phase 2 activities (week 3–6)

| Activity | Owner | Deliverable |
|---|---|---|
| SAM plugin activation | `sam_admin` | Plugin `com.sn_samp_master_ws` activated; SAM tables created |
| ML Normalization (optional) | `sam_admin` | Plugin `com.sn_sam_ml_normalization` activated if required |
| CI related-list setup | `sam_admin` / `admin` | `Software Installations` tab on CI records |
| Discovery schedule configuration | `discovery_admin` | Software discovery schedules with credentials and ranges |
| Entitlement import | `sam_admin` | PPN/ contract data loaded into SAM |
| Content Service opt-in decision | `sam_admin` | Documented: opt in now or defer to Phase 3 |
| First Discovery run post-SAM | `discovery_admin` | Confirm `cmdb_sam_sw_install` populated; Business rule fires |

---

## 3. Phase 2 gate review

**Go to Phase 3 when:**
- SAM plugin activated and SAM tables created.
- CI related-list configured and showing SAM installs.
- Discovery running post-SAM; `cmdb_sam_sw_install` populated.
- Entitlements loaded and verifiable.
- Content Service opt-in decision documented (opt-in or defer).

**Stay in Phase 2 if:**
- SAM plugin activation fails or tables not created.
- CI related-list not configured or showing legacy `cmdb_ci_spkg`.
- Discovery not populating SAM tables.
- Entitlements not yet loaded.