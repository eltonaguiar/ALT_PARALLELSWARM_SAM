# phase1_started.md — ServiceNow SAM Phase 1: Foundations Started

- **Compiled by:** `kilo` / provider **kilo** / harness **default** (`kilo__default__kilo`)
- **Date:** 2026-11-13
- **Status:** Phase 1 initiated — CMDB health assessment and prerequisite validation

---

## 1. Phase 1 objectives

### 1.1 CMDB health validation
- [ ] Verify CMDB hardware/computer CIs have sufficient identity for Discovery/SCCM to land installs (`installed_on` field populated).
- [ ] Confirm owners, location, department, cost center, company, country, region are set on CIs if reconciliation grouping will be used.
- [ ] Validate user records exist for per-user allocation or SaaS seat reclamation.
- [ ] Confirm Discovery coverage of the estate (Discovery and/or SCCM/SG connector), not relying on a spreadsheet.
- [ ] Verify entitlement source of truth is ready (contracts, PPN, Microsoft MLS).
- [ ] Document in-scope publisher list (packs cost money and complexity).
- [ ] Document exclude-SAM device decision (leased, out of scope, phase-1 location only).

### 1.2 Baseline metrics capture
- [ ] Discovery-model count by normalization status (Content Service value when opted in).
- [ ] Install count vs unique products vs unique software models (Dedup / auto-create health).
- [ ] Unlicensed product-result count (True-up baseline).
- [ ] % CIs with owner/location (Recon grouping baseline).
- [ ] SaaS assigned vs used (after connector) (Reclamation baseline).
- [ ] Time of last successful recon (Operating cadence baseline).
- [ ] Published-product count if phase-wise (Scope freeze baseline).

### 1.3 Phase 1 exit criteria
- [ ] CMDB CIs with identity for Discovery landing confirmed.
- [ ] Entitlement source of truth ready and importable.
- [ ] In-scope publisher list documented.
- [ ] Exclude-SAM device decision documented.
- [ ] Baseline metrics captured before go-live.

---

## 2. Phase 1 activities (week 1–2)

| Activity | Owner | Deliverable |
|---|---|---|
| CMDB CI audit | `sn_cmdb_admin` | List of CIs with `installed_on` + owner/location data |
| Entitlement inventory | `sam_admin` | PPN/ contract inventory ready for import |
| Publisher scope definition | `sam_admin` | Documented in-scope publisher list |
| Exclude-SAM device list | `sam_admin` | CIs/devices to exclude from SAM |
| Baseline metric capture | `sam_user` | Spreadsheet or dashboard snapshot of 8 core metrics |
| Discovery coverage validation | `discovery_admin` | Confirm Discovery/SCCM covers target estate |

---

## 3. Phase 1 gate review

**Go to Phase 2 when:**
- All CMDB CI identity checks pass.
- Entitlement source of truth verified.
- Publisher scope documented and approved.
- Exclude-SAM device list documented.
- All 8 baseline metrics captured.

**Stay in Phase 1 if:**
- Any CI lacks `installed_on` or owner data.
- Entitlement contracts not yet available.
- Publisher scope undefined or too broad.
- Discovery does not cover the target estate.