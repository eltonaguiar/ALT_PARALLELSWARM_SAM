# FILESCOPE — SAM Configuration Reference Artifact Inventory

**Generated:** 2026-11-13  
**Worktree:** `SAM_CFG__WT1`  
**Scope:** All files produced or consumed by the SAM configuration reference build

---

## 05_FINAL — Canonical output

| File | Status | Description |
|---|---|---|
| `SAM_CONFIG_REFERENCE.md` | ✅ Created | 18-section master reference (this document's source) |
| `FINAL_SAM_MODULE_REFERENCE.md` | ✅ Created | Deployed to `~/alt_parallelswarm_SAM/final/` |

---

## 01_PLAN — Execution plan

| File | Status | Description |
|---|---|---|
| `PLAN.md` | ✅ Created | 18-section output structure + 5-phase methodology mirroring CMDB reference |

---

## 00_PREREQ — Prerequisites

| File | Status | Description |
|---|---|---|
| `PREREQ.md` | ✅ Created | Token budgets, tool chain, release scope, probe requirements |

---

## 02_CLARIFICATIONS — Open questions resolved

| File | Status | Description |
|---|---|---|
| `CLARIFY.md` | ✅ Created | 12 clarifications resolved (Foundation vs Pro, CMDB vs SAM identification, etc.) |

---

## 03_PHASES — Phase execution log

| File | Status | Description |
|---|---|---|
| `PHASE_LOG.md` | ✅ Created | Timestamped phase transitions: 0→1→2→3→4→5 |

---

## 04_QA — Quality gates

| File | Status | Description |
|---|---|---|
| (none yet) | ⏳ Pending | Evidence-coverage check, cross-ref validation, release-pin audit |

---

## research — Evidence corpus

| File | Status | Description |
|---|---|---|
| `EVIDENCE_DIGEST.md` | ✅ Created | 32 sources, verbatim quotes, release-pinned citations |
| `source_index.json` | ⏳ Pending | Machine-readable index for automation |

---

## agents/sam-research — Agent identity

| File | Status | Description |
|---|---|---|
| `AGENT_CARD.md` | ✅ Created | Agent identity, capabilities, comms protocol |

---

## External dependencies (read-only)

| Path | Purpose |
|---|---|
| `~/alt_parallelswarm/final/DISCOVERY_INSERT_VS_UPDATE_GUIDE.md` | CMDB/Discovery reference methodology template |
| `~/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/sam/sam-guide.md` | Target for enhancement concepts |
| `~/ServiceNow_Learning/docs/08-SAM-SETUP.md` | Source [S28] — implementation runbook |
| `~/ServiceNow_Learning/scripts/sam_readiness.py` | Source [S31] — readiness probe |
| `~/ServiceNow_Learning/scripts/sn_probe.js` | Source [S32] — schema probe |

---

## Deployment targets

| Target | Action |
|---|---|
| `~/alt_parallelswarm_SAM/final/FINAL_SAM_MODULE_REFERENCE.md` | ✅ Written (this replaces/enhances beam/grok version) |
| `~/ServiceNow_Learning_TSOM-.../docs/modules/sam/sam-guide.md` | ⏳ Enhancement concepts documented below |

---

## Enhancement concepts for TSOM repo `sam-guide.md`

The existing `sam-guide.md` in the TSOM repo is a **field-mapping / breadcrumb reference** (what tables/fields exist). The research produced **operational configuration knowledge** (how to configure, what order, what breaks). Recommended enhancements:

### 1. Three-layer Insert-vs-Update Decision Table (NEW SECTION)
Add after the field mapping tables:
- **Software Install Recognition** → Discovery source + native key dedup
- **Entitlement Consumption** → Metric-gated right consumption
- **Reconciliation Exceptions** → Priority rules for over/under/unlicensed
This is the SAM equivalent of the CMDB guide's insert-vs-update table but with three distinct layers.

### 2. OOTB Business Rules / Flows / UI Policies Inventory (NEW SECTION)
Document the **active automation** SAM ships:
| Automation | Table | Trigger | Purpose |
|---|---|---|---|
| `SAM: Install Normalization` | `cmdb_sam_sw_install` | After insert/update | Creates/updates discovery model, kicks normalization |
| `SAM: Discovery Model Normalization` | `cmdb_sam_sw_discovery_model` | Scheduled daily | Content Library matching, status assignment |
| `SAM: Reconciliation Worker` | `samp_reconciliation_result` | Weekly (Mon 02:00) | Main compliance calculation |
| `SAM: Deduplicate Install Table` | `cmdb_sam_sw_install` | Daily | Cross-source duplicate suppression |
| `SAM: Populate Licensing Data` | `cmdb_ci_computer` | Daily | CI licensing related-list data |

### 3. Pattern Normalization Rule Precedence vs Content Library (CLARIFICATION)
Current docs say "Content Library takes precedence over custom file signature rules" but are silent on **Pattern Normalization Rules**. Add explicit callout:
> **Precedence (inferred from behavior):** Content Library exact match → Pattern Normalization (manual) → Enhanced Pattern → Wide-net → ML Normalization (if plugin active) → Match Not Found.
> **Rule:** Do not create Pattern Normalization Rules for publishers already covered by Content Library — they create conflicts.

### 4. Scheduled Job Dependency Chain (VISUAL)
```
┌─────────────────────────────────────────────────────────────┐
│  DAILY (sequential, not parallel)                           │
├─────────────────────────────────────────────────────────────┤
│  1. SAM - Normalize discovery models using content library  │
│     └─► Must complete before install counts are accurate    │
│  2. SAM - Discovery Model to Software Model matching        │
│     └─► Depends on #1 normalization statuses                │
│  3. SAM - Get install count for software model              │
│     └─► Aggregates installs per normalized model            │
│  4. SAM/CI - Populate Licensing Data                        │
│     └─► Populates CI related lists for dashboards           │
│  5. SAM - Deduplicate Install Table                         │
│     └─► Cleanup after all normalization done                │
├─────────────────────────────────────────────────────────────┤
│  WEEKLY (Mon 02:00)                                         │
│  6. SAM - Software License Reconciliation                   │
│     └─► Consumes outputs of #1-#5; parallel workers=4       │
└─────────────────────────────────────────────────────────────┘
```

### 5. Foundation vs Professional Feature Matrix with Release Labels (NEW TABLE)
| Feature | Foundation (Pre-Xanadu `com.snc.samp`) | Professional (Xanadu+ `com.sn_samp_master_ws`) | Release label |
|---|---|---|---|
| Core SAM tables | ✅ `alm_license`, `cmdb_sam_*` | ✅ `samp_*`, `cmdb_sam_*` | All |
| Publisher Packs (Microsoft, Oracle, IBM, Adobe, SAP, VMware, Citrix) | ❌ | ✅ | Xanadu+ |
| Software Asset Workspace (new UI) | ❌ | ✅ | Xanadu+ |
| ML Normalization | ❌ | ✅ | Yokohama+ |
| SaaS License Management (M365, Salesforce, Adobe, Zoom) | ❌ | ✅ (Store) | Xanadu+ |
| Spend Detection | ❌ | ✅ | Xanadu+ |
| Engineering Apps (OpenLM, Open iT) | ❌ | ✅ | Xanadu+ |
| Guided Experiences / Product Setups | ❌ | ✅ | Yokohama+ |
| Configuration Console | ❌ | ✅ (via `sn_samp_admin` Store) | Xanadu+ |
| Entitlement Playbook | ❌ | ✅ (Store) | Yokohama+ |
| ITAM Health Check | ❌ | ✅ (Store) | All |

### 6. Normalization Coverage KPI with Gate Logic (ADD TO SETUP SECTION)
> **Hard gate:** Do not run first reconciliation until **normalization coverage > 85%**.
> **Measurement:** `(Normalized + Partially Normalized + Publisher Normalized) / Total Discovery Models`
> **Probe:** `sam_readiness.py` check #4 (normalization coverage)
> **Remediation:** Pattern Normalization Rules for top-20 unmatched models by install count.

### 7. Reconciliation Exception Taxonomy (ADD TO TROUBLESHOOTING)
| Exception | Meaning | Never do this |
|---|---|---|
| Under-licensed | Rights < demand | Report as compliant |
| Over-licensed | Rights > demand | Ignore (wasted spend) |
| Unlicensed | Installs, no entitlement | Leave in place "for now" |
| Not counted | Excluded by rule | Assume covered |
| **Unknown** | Insufficient data (unmatched model, no usage) | **Report as compliant** |

### 8. Three Distinct "Identification" Layers Callout (ADD TO ARCHITECTURE)
> **Do not conflate:**
> 1. **CI Identification Rules (IRE)** → CMDB level, all CIs, `duplicate_of` field
> 2. **Asset↔CI Reconciliation (HAM)** → Serial number match, hardware assets
> 3. **Software Normalisation (SAM)** → Content Library + Pattern Rules, software titles
> 4. **License Metric** → Commercial decision (per core/user/device)
> 5. **License Reconciliation** → Rights vs installs → the number you defend

---

## Checksums (for drift detection)

| File | SHA256 (first 16 chars) |
|---|---|
| `05_FINAL/SAM_CONFIG_REFERENCE.md` | (compute on commit) |
| `final/FINAL_SAM_MODULE_REFERENCE.md` | (compute on commit) |
| `research/EVIDENCE_DIGEST.md` | (compute on commit) |

---

*End of FILESCOPE*