# Enhancement Concepts for TSOM Repo `sam-guide.md`

**Source:** `SAM_CFG__WT1` research (32 release-pinned sources)  
**Target:** `/home/eaguiar2015/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/sam/sam-guide.md`  
**Date:** 2026-11-13  
**Purpose:** Operational configuration knowledge to complement the existing field-mapping/breadcrumb reference

---

## Current State Assessment

The existing `sam-guide.md` is excellent at:
- Field mappings and table hierarchies (Sections "Key Table Hierarchy", "Key Fields")
- Breadcrumb navigation (Section "Where to Find It")
- Exam-aligned concept explanations (Sections "SAM Lifecycle", "Three Record Types")
- Re-usable code snippets (Business Rules, Script Includes, Client Scripts)
- Lab exercises (Section "Lab: Entitlement → Reconciliation → Compliance")
- Memory aids and official resources

**Gap:** It is a **reference manual** (what tables/fields exist) but lacks **operational configuration guidance** (how to configure, in what order, what breaks, precedence rules, dependency chains).

---

## 8 Recommended Enhancements

### 1. Three-Layer Insert-vs-Update Decision Table (NEW SECTION)

**Placement:** After "The Three Record Types You Must Never Confuse" (around line 225)

**Content:**
```markdown
## Three-Layer Insert-vs-Update Decision Table

SAM has three distinct "insert vs update" gates — do not conflate them:

| Layer | Insert Trigger | Update Trigger | Blocking Rules | Probe Check |
|-------|----------------|----------------|----------------|-------------|
| **Software Install Recognition** (`cmdb_sam_sw_install`) | New discovered install (source + native key) | Same install re-discovered (version change, last seen update) | Duplicate detection via source+native key; Normalisation status | `sam_readiness.py` #4 |
| **Entitlement Consumption** | First install of a normalised product consumes entitlement | Install count changes, version upgrade/downgrade, metric change | Metric definition, entitlement quantity, licence type | `sam_readiness.py` #6 |
| **Reconciliation Exceptions** | New exception detected (over-consumption, metric mismatch) | Exception resolved or changed severity | Reconciliation scope, exception thresholds, priority rules | `sam_readiness.py` #10 |

**Why this matters:** The CMDB guide has one insert-vs-update table for CIs. SAM has THREE because the recognition, consumption, and exception layers are distinct processes with different owners and failure modes.
```

---

### 2. OOTB Business Rules / Flows / UI Policies Inventory (NEW SECTION)

**Placement:** After "Out-of-Box Features" (around line 667)

**Content:**
```markdown
## OOTB Automation Inventory (Active Business Rules, Flows, Scheduled Jobs)

These are the automations SAM ships — verify they are **Active** in your instance before building custom ones:

| Automation | Type | Table | Trigger | Purpose | Probe |
|------------|------|-------|---------|---------|-------|
| `SAM: Install Normalization` | Business Rule (before) | `cmdb_sam_sw_install` | After insert/update | Creates/updates discovery model, kicks normalization | ✅ |
| `SAM: Discovery Model Normalization` | Scheduled Job (Daily) | `cmdb_sam_sw_discovery_model` | Scheduled | Content Library matching, status assignment | ✅ |
| `SAM: Reconciliation Worker` | Scheduled Job (Weekly Mon 02:00) | `samp_reconciliation_result` | Scheduled | Main compliance calculation | ✅ |
| `SAM: Deduplicate Install Table` | Scheduled Job (Daily) | `cmdb_sam_sw_install` | Scheduled | Cross-source duplicate suppression | ✅ |
| `SAM: Populate Licensing Data` | Scheduled Job (Daily) | `cmdb_ci_computer` | Scheduled | CI licensing related-list data | ✅ |
| `SAM: Get install count for software model` | Scheduled Job (Daily) | `cmdb_software_product_model` | Scheduled | Install count aggregation | ✅ |
| `SAM: Discovery Model to Software Model matching` | Scheduled Job (Daily) | `cmdb_sam_sw_discovery_model` | Scheduled | Map discovery → software models | ✅ |
| `SAM - Subscription Maintenance` | Scheduled Job (Daily) | `alm_license` | Scheduled | Renewed/subscription license handling | ✅ |
| `SAM - Apply latest content changes` | Scheduled Job (On Demand) | `cmdb_sam_sw_discovery_model` | Manual | Content library updates | ⏳ |

**Tip:** Use `sys_hub_flow.list` + filter `name CONTAINS SAM` for Flow Designer automations.
```
```

---

### 3. Pattern Normalization Rule Precedence vs Content Library (CLARIFICATION)

**Placement:** In "Software Models & Normalization (SUMN)" section (around line 238)

**Content:**
```markdown
### ⚠️ Normalization Rule Precedence (Inferred — Not Fully Documented)

ServiceNow docs state: *"Content Library takes precedence over custom file signature rules"* but are silent on **Pattern Normalization Rules** vs Content Library.

**Observed precedence order (from community corroboration + behavior):**

1. **Content Library exact match** (publisher pack rules) — highest
2. **Pattern Normalization Rules** (manual, substring match) — second
3. **Enhanced Pattern Normalization** (conditional mapping) — third
4. **Wide-net Normalization** (grouping similar values, selective) — fourth
5. **ML Normalization** (if `com.sn_sam_ml_normalization` plugin active) — fifth
6. **Match Not Found** → manual normalization queue — lowest

**Operational rule:** Do not create Pattern Normalization Rules for publishers already covered by Content Library (Microsoft, Oracle, Adobe, IBM, SAP, VMware, Citrix). They create conflicts and the Content Library match will win anyway.

**Evidence gap:** [S16] demonstrates Pattern Normalization fixing "Match Not Found" but does not show precedence vs Content Library exact matches. This is **UNVERIFIED** — see Open Question #2 in the full reference.
```
```

---

### 4. Scheduled Job Dependency Chain (VISUAL)

**Placement:** After "Reconciliation — The Core Engine" (around line 307)

**Content:**
```markdown
### Scheduled Job Dependency Chain (Critical for Debugging)

Jobs run **sequentially, not in parallel**. A failure in an early job cascades to reconciliation.

```mermaid
flowchart TD
    subgraph DAILY[DAILY — Sequential Chain]
        J1[1. Normalize discovery models<br/>using content library]
        J2[2. Discovery Model →<br/>Software Model matching]
        J3[3. Get install count<br/>for software model]
        J4[4. SAM/CI - Populate<br/>Licensing Data]
        J5[5. Deduplicate<br/>Install Table]
    end

    subgraph WEEKLY[WEEKLY — Mon 02:00]
        J6[6. Software License<br/>Reconciliation<br/>(max_workers=4)]
    end

    J1 --> J2 --> J3 --> J4 --> J5 --> J6

    style J1 fill:#ff6b6b,color:#fff
    style J6 fill:#6bcb77,color:#fff
```

**Debugging rule:** If reconciliation numbers look wrong, check job logs in this order:
1. Job #1 completed? (normalization statuses assigned)
2. Job #2 completed? (models mapped)
3. Job #3 completed? (install counts aggregated)
4. Job #5 completed? (duplicates removed)
5. Then check Job #6 (reconciliation)

**Property controls:** `com.snc.samp.recon.max_workers` (default 4) [S24][S26]
```
```

---

### 5. Foundation vs Professional Feature Matrix with Release Labels (NEW TABLE)

**Placement:** In "Where to Find It" or new "SAM Editions" section (around line 131)

**Content:**
```markdown
## SAM Editions: Foundation vs Professional vs Pro — Feature Matrix

| Feature | Foundation<br/>(Pre-Xanadu<br/>`com.snc.samp`) | Professional<br/>(Xanadu+<br/>`com.sn_samp_master_ws`) | Pro / Advanced<br/>(Store apps) | Release |
|---------|-----------------------------------------------|--------------------------------------------------------|--------------------------------|---------|
| Core SAM tables | ✅ `alm_license`, `cmdb_sam_*` | ✅ `samp_*`, `cmdb_sam_*` | ✅ | All |
| Publisher Packs (Microsoft, Oracle, IBM, Adobe, SAP, VMware, Citrix) | ❌ | ✅ | ✅ | Xanadu+ |
| Software Asset Workspace (new UI) | ❌ | ✅ | ✅ | Xanadu+ |
| ML Normalization | ❌ | ✅ | ✅ | Yokohama+ |
| SaaS License Management (M365, Salesforce, Adobe, Zoom) | ❌ | ✅ | ✅ (Store) | Xanadu+ |
| Spend Detection | ❌ | ✅ | ✅ | Xanadu+ |
| Engineering Apps (OpenLM, Open iT concurrent) | ❌ | ✅ | ✅ | Xanadu+ |
| Guided Experiences / Product Setups | ❌ | ✅ | ✅ | Yokohama+ |
| Configuration Console | ❌ | ✅ | ✅ (via `sn_samp_admin` Store) | Xanadu+ |
| Entitlement Playbook | ❌ | ✅ | ✅ (Store) | Yokohama+ |
| ITAM Health Check | ❌ | ✅ | ✅ (Store) | All |

**Migration note:** `cmdb_ci_spkg` (legacy Software CI) → `cmdb_sam_sw_install` migration script runs on plugin activation. Verify in `sys_script` [S7].
```
```

---

### 6. Normalization Coverage KPI with Gate Logic (ADD TO SETUP)

**Placement:** In "Software Models & Normalization (SUMN)" after normalization workflow (around line 240)

**Content:**
```markdown
### 🔴 Hard Gate: Normalization Coverage > 85% Before First Reconciliation

> **Community-corroborated KPI** [S6]: "Reconciliation doesn't run unless normalization is clean. Unnormalized installs simply don't get picked up. Always check the normalization coverage % before your first reconciliation run and set a KPI (typically targeting >85%)."

**Measurement:**
```
Normalization Coverage % = 
  (Normalized + Partially Normalized + Publisher Normalized) 
  / Total Discovery Models 
  × 100
```

**Probe check:** `sam_readiness.py` check #4 — queries `cmdb_sam_sw_discovery_model` for status distribution.

**Remediation workflow for <85%:**
1. Sort unmatched discovery models by `install_count` desc
2. Top 20 = Pattern Normalization Rule candidates
3. Create rules via **All > Software Asset > Administration > Pattern Normalization Rules** [S15]
4. Re-run Job #1 (Normalize), verify coverage
5. Only then run first reconciliation
```
```

---

### 7. Reconciliation Exception Taxonomy (ADD TO TROUBLESHOOTING)

**Placement:** In "Compliance Positions Explained" (around line 457)

**Content:**
```markdown
### Reconciliation Exception Taxonomy — What Each State Means for Action

| Exception | Meaning | Financial Impact | Typical Cause | Owner | Never Do This |
|-----------|---------|------------------|---------------|-------|---------------|
| **Under-licensed** | Entitlements < demand | Audit exposure / unbudgeted true-up | True-up needed or reclaim | SAM admin + Procurement | Report as compliant |
| **Over-licensed** | Entitlements > demand | Money wasted on unused licenses | Over-purchase, no reclamation | SAM admin + Finance | Ignore (compounds at renewal) |
| **Unlicensed** | Installs exist, no matching entitlement | Highest audit risk | Missing entitlement, wrong model | SAM admin + IT Ops | Leave in place "for now" |
| **Not counted** | Excluded by rule (ignore list, excluded CI/publisher) | Excluded from risk | Intentional exclusion | SAM admin | Assume covered — review annually |
| **Unknown** | Insufficient data (unmatched model, no usage feed) | **Unknown risk** | Normalization backlog, dead connector | SAM admin | **Report as compliant** — hides exposure |

**Exam-critical:** "Unknown" is not "compliant". A SAM program that reports unknown as compliant is the reason audit penalties appear out of nowhere. [S28]
```
```

---

### 8. Three Distinct "Identification" Layers Callout (ADD TO ARCHITECTURE)

**Placement:** In "SAM vs HAM vs ITAM" or new "Architecture" section (around line 107)

**Content:**
```markdown
### ⚠️ Do Not Conflate These Five "Identification" Layers

| Layer | Question | Configured In | Scope | Mechanism |
|-------|----------|---------------|-------|-----------|
| **1. CI Identification Rules (IRE)** | Is this CI new or the one I already have? | CI Class Manager / CI Identifiers, per CI class | **CMDB** — all CIs (servers, laptops, network gear) | `duplicate_of` field; de-duplication tasks |
| **2. Asset↔CI Reconciliation (HAM)** | Which asset record is this CI? | HAM asset sync | Hardware assets ↔ CIs | Serial number match |
| **3. Software Normalisation (SAM)** | Are these two software titles the same product? | SAM normalisation, Content Library, publisher packs | **SAM** — software titles | Pattern rules, Content Library matching |
| **4. Licence Metric** | Per user, device, or core? | Entitlement record | **Commercial decision** | Contract terms |
| **5. Licence Reconciliation** | Rights vs installs → compliance | SAM reconciliation | **SAM** — the number you defend | Weekly job, per model + metric |

**Rule of thumb:** 
- Deduplicating **a machine** → CMDB/IRE (Layer 1)
- Deduplicating **a software title** → Normalisation in SAM (Layer 3)  
- Deduplicating **a quantity of rights** → Licence metric (Layer 4) + Reconciliation (Layer 5)

**Source:** [S28] — this distinction is the #1 confusion point in implementations.
```
```

---

## Implementation Priority

| Priority | Enhancement | Effort | Value |
|----------|-------------|--------|-------|
| 1 | Three-Layer Insert-vs-Update Table | Low | High — fills CMDB-parity gap |
| 2 | Normalization Coverage KPI Gate | Low | High — prevents silent reconciliation failures |
| 3 | Scheduled Job Dependency Chain | Low | High — debugging accelerator |
| 4 | Foundation vs Pro Feature Matrix | Medium | High — edition clarity |
| 5 | OOTB Automation Inventory | Medium | Medium — prevents duplicate automation |
| 6 | Pattern Normalization Precedence | Medium | Medium — configuration clarity |
| 7 | Exception Taxonomy | Low | High — audit defence |
| 8 | Five-Layer Identification Callout | Low | High — conceptual clarity |

---

## Notes for Integration

- All enhancements reference `[S<n>]` evidence from `SAM_CFG__WT1/research/EVIDENCE_DIGEST.md`
- UNVERIFIED items explicitly flagged (precedence order, exact table names per edition)
- Follow existing `sam-guide.md` style: tables, mermaid diagrams, ELI5 summaries, "Exam focus" callouts
- Preserve existing section numbering; insert as subsections
- Update "Official Exam Alignment" table if new sections map to CIS-SAM domains

---

*End of Enhancement Concepts*