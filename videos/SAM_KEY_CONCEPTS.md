# ServiceNow SAM (Software Asset Management) - Key Concepts for Video Series

**Source References:**
- https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/sam/sam-guide/
- https://github.com/eltonaguiar/alt_parallelswarm_SAM
- CIS-SAM Exam Blueprint

---

## CORE CONCEPT (One Sentence)
**SAM reconciles what you own (entitlements) against what exists and is used (normalized installs + usage) per software model and license metric, and turns the difference into a compliance position.**

---

## THE CHAIN (Memorize This Order)
```
CI (CMDB/IRE)
  └─ cmdb_sam_sw_install            # one install on one device
       └─ cmdb_sam_sw_discovery_model  # raw fingerprint, normalized
            └─ cmdb_software_product_model  # purchased product profile
                 └─ alm_license             # rights + metric + dates
                      └─ reconciliation     # rights vs demand
                           ├─ samp_product_result
                           ├─ Software Model Results
                           └─ samp_license_metric_result
```

**Install → discovery model → software model → entitlement → result.**

---

## 1. THREE RECORD TYPES YOU MUST NEVER CONFUSE

| Record | Table | Plain-English Meaning | Who Creates It |
|--------|-------|----------------------|----------------|
| **Software Model** | `cmdb_software_product_model` | Canonical normalized product definition | Content Library (auto) or SAM admin (manual) |
| **Discovery Model** | `cmdb_sam_sw_discovery_model` | Raw fingerprint observed in field | Discovery / SCCM / Intune import (auto) |
| **Installation** | `cmdb_sam_sw_install` | One concrete install on one device | Discovery import |
| **Usage** | `cmdb_sam_sw_usage` / `samp_sw_usage` | Evidence install was actually run | Usage connectors |
| **Entitlement** | `alm_license` | Right to use N units under specific metric | SAM admin |
| **Reconciliation Result** | `sam_sw_reconciliation_result` / `samp_*_result` | Computed per-model compliance verdict | Reconciliation job (auto) |

**Rule:** *Software model = what it is. Entitlement = what you may use. Installation = what exists. Usage = what is used. Reconciliation = the difference.*

---

## 2. SAM vs HAM vs ITAM

| Aspect | HAM | SAM | ITAM |
|--------|-----|-----|------|
| **Tracks** | Physical hardware | Software entitlements, installs, usage | Both |
| **Primary Question** | What do we own, where, who has it? | Are we compliant, over/under-licensed? | Full asset portfolio cost & risk |
| **Core Record** | `alm_asset` / `alm_hardware` | Software model + entitlement + install | `alm_asset` hierarchy |
| **Key Engine** | Asset lifecycle | **Reconciliation** | Both engines |
| **Key Risk** | Lost/stolen assets | Publisher audit fines, wasted spend | Both |
| **Exam Critical:** HAM and SAM share ITAM app and `alm_*` tables, but SAM adds the **software model → discovery model → installation → usage → entitlement → reconciliation result** chain. HAM has no equivalent of reconciliation. |

---

## 3. SOFTWARE MODELS & NORMALIZATION (SUMN)

**Normalization** converts messy raw discovery fingerprints into publisher-sanctioned software models.

**Why it matters:** Without normalization, Discovery reports 40 variants of "Microsoft Office". Reconciliation against one Office entitlement would show catastrophic under-licensing.

**Normalization Workflow:**
1. Discovery/SUMN collects raw fingerprints → creates **Discovery Model**
2. SUMN matches discovery model to **Software Model** in Content Library (publisher packs)
3. Unmatched models land in **normalization queue** for manual review
4. SAM admin maps unmatched models manually (`Normalize` action) or ignores them
5. Normalized installs participate in reconciliation

**Six Normalization Statuses:**
| Status | Manual Normalize? | Revert? |
|--------|------------------|---------|
| New | No | No |
| Match Not Found | Yes | No |
| Publisher Normalized | Yes | Yes |
| Partially Normalized | Yes | Yes |
| Normalized | No | Yes |
| Manually Normalized | No | No |

---

## 4. ENTITLEMENTS — THE CONTRACT SIDE

**Must-have attributes:**
- Software model (must match normalized model)
- Publisher (drives publisher-specific counting rules)
- **License metric** (per user / per device / per core / per processor / subscription)
- Purchased quantity
- License type (perpetual vs subscription vs maintenance)
- Contract + PO reference
- Start / end date
- Unit cost
- Owned by / cost center
- Downgrade / upgrade rights

**Entitlement Hygiene Rules:**
- One entitlement per **contract line**, not per PO
- Never overwrite quantity — create adjustment/true-up record
- **Maintenance ≠ license** — maintenance-only records must not count as usage rights
- **Metric mismatch is silent** — per-device entitlement vs per-user usage produces meaningless number

---

## 5. RECONCILIATION — THE CORE ENGINE

**Scheduled job (default nightly/weekly)** that computes:
```
Compliance position = f(entitlement quantity, normalized installs, usage evidence, metric, rules)
```

**Step by step:**
1. Gather entitlements for software model (filtered by date validity)
2. Gather normalized installs, de-duplicated per device
3. Apply usage evidence (for reclamation and "not in use" classification)
4. Apply publisher rules and exclusions (ignore lists, VM rules, suite roll-ups, downgrade rights)
5. Calculate position per model and per metric
6. Persist reconciliation result record
7. Roll up to publisher and portfolio dashboards

**Three Reconciliation Tiers:**
| Tier | Table | Answers |
|------|-------|---------|
| Product | `samp_product_result` | Is the product compliant? Cost/savings? |
| Software Model | Software Model Results | Which model is the problem? |
| License Metric | `samp_license_metric_result` | Rights owned vs used vs available, by metric |

**Run record:** `samp_reconciliation_result`

---

## 6. COMPLIANCE POSITIONS

| Position | Meaning | Financial Meaning | Typical Action |
|----------|---------|-------------------|----------------|
| **Compliant** | Entitlements ≥ demand | Neutral | Monitor; harvest reclaimed licenses |
| **Over-licensed** | Entitlements > demand | Money wasted | Reclaim, reduce renewal, renegotiate |
| **Under-licensed** | Entitlements < demand | Audit exposure | True-up purchase, or reclaim installs |
| **Unlicensed** | Installs exist, no entitlement | Highest audit risk | Remove, purchase, or reclassify |
| **Not counted** | Excluded by rule | Excluded from risk | Review annually |
| **Unknown / Unallocated** | Insufficient data | Unknown risk | Fix normalization or data feed |

**Exam Critical:** "Unknown" is NOT "compliant". A SAM program reporting unknown as compliant causes surprise audit penalties.

---

## 7. PUBLISHER-SPECIFIC TRAPS (Exam Favorites)

| Publisher | Licensing Trap |
|-----------|----------------|
| **Microsoft** | Per-core SQL Server (physical cores, core factor, min 4 cores/socket); virtualization rules; M365 suite overlap; downgrade rights exist but must document |
| **Oracle** | Core-factor table per processor; licensing the **server** (not VM) unless hard partitioning certified; LMS scripts are audit instrument; "named user plus" minimums |
| **IBM** | PVU tables per processor model; sub-capacity licensing requires ILMT evidence |
| **SAP** | Named-user classification by usage type; indirect/digital access = audit battleground |
| **Adobe** | VIP/ETLA named-user; shared-device licensing differs; Creative Cloud suite roll-up |
| **ServiceNow** | Subscription by product line + fulfilled user/approved requester; over-consumption billed not audited |

---

## 8. OPTIMIZATION & RECLAMATION (Where SAM Pays for Itself)

**Priority Order:**
1. **Reclaim dormant seats** — SaaS and named-user models first; largest, fastest, lowest-risk
2. **Uninstall unused installs** — especially servers with per-core licensing (Oracle, SQL Server)
3. **Right-size editions** — Enterprise → Standard, E5 → E3 where justified
4. **Consolidate overlapping tools** — duplicate PDF/archiving/monitoring post-merger
5. **Align renewal quantities to actual demand** — negotiate using reconciled number
6. **Enforce process** — new requests gated by approval checking existing entitlement

**Reclamation Workflow:**
```
Identify (reconciliation + usage) → Validate with owner → Notify user → Grace period
→ Reclaim/remove → Re-run reconciliation → Confirm savings recorded
```
**Never reclaim on single night's data.** Require 60-90 day inactivity window + business owner sign-off.

---

## 9. SAAS LICENSE MANAGEMENT (SAM Pro)

| On-premise SAM | SaaS License Management |
|----------------|------------------------|
| Discovery finds installs | Connector pulls **subscriptions + assigned seats** from vendor API |
| Metric: per device/core | Metric: **per user / named user** |
| Usage = launch metering | Usage = **last activity / sign-in** |
| Reconciliation vs installs | Reconciliation vs **assigned but inactive seats** |
| Optimization = uninstall | Optimization = **reclaim dormant seats** |

**Classic SaaS Waste Pattern:** 1,000 assigned M365 E5 seats, 260 never signed in 90+ days = 26% spend recoverable.

---

## 10. KEY TABLES REFERENCE

| Table | What It Is |
|-------|------------|
| `cmdb_sam_sw_install` | Installs (source of truth) |
| `cmdb_sam_sw_discovery_model` | Raw fingerprints + normalized fields + status |
| `cmdb_software_product_model` | Purchased product profile |
| `alm_license` | Entitlement |
| `samp_sw_usage` | Usage evidence (product-level, references publisher/product + CI + user) |
| `samp_product_result` | Product compliance/cost |
| `samp_license_metric_result` | Rights per metric |
| `samp_reconciliation_result` | Reconciliation run |
| `samp_sw_reclamation_candidate` | Reclamation candidates |
| `sam_sw_dedup_rule` | Custom dedup rules |

---

## 11. KEY PROPERTIES

| Property | What It Does |
|----------|--------------|
| `com.snc.samp.recon.group` / `.subgroup` | Weekly reconciliation grouping |
| `com.snc.samp.automaticsmrcreation` | Auto-create models for licensable products |
| `com.snc.samp.exclude_device_flag` | Exclude CIs from SAM |
| `com.snc.samp.manage.published.products` | Phase-wise scope |
| `com.snc.samp.oracle.reconlevel` | Oracle VMware aggregation |
| `com.snc.samp.enable.ml_normalization` | ML normalization |
| `com.snc.samp.wide_net_normalization.enabled` | Wide-net normalization |

---

## 12. KEY JOBS

| Job | Cadence |
|-----|---------|
| Normalize discovery models using content library rules | Daily |
| Discovery Model Normalization job | Daily |
| SAM - Daily Job | Daily |
| Trigger Full Scan | Weekly |
| Adjust Installs for excluded CIs | Not documented |
| Software License Reconciliation | Weekly default |
| Discovery Model to Software Model matching | Not documented |

---

## 13. TOP 8 TRAPS (Memorize for Interviews)

1. **Metric mismatch** between model and entitlement → silently meaningless result
2. **Duplicate installs** from multiple sources → inflated demand; configure dedup
3. **Unnormalized titles** → unlicensed/unknown; normalize before auto-create
4. **Maintenance treated as a license** → false compliance
5. **Leftover installs on out-of-scope devices** → phantom demand
6. **First reconciliation treated as an invoice** → wrong true-up; use as data-quality loop
7. **Dead SaaS connector** → "no waste" illusion; monitor health
8. **Confusing vendor / publisher / PPN / model / discovery model / catalog item** → wrong links

---

## 14. RIGHTS ALGEBRA

- **Rights owned** = active entitlements sharing the metric
- **Rights used** = allocated in use + not allocated in use + installed
- **Rights available** = owned − used
- **Allocated not in use** = wasted rights → remove allocations
- **Not allocated in use** = unallocated consumption → create allocations or remove unallocated installs

---

## 15. CIS-SAM EXAM DOMAINS

| Domain | Weight | Key Topics |
|--------|--------|------------|
| 1: SAM Overview & Fundamentals | ~15% | ITAM/SAM positioning, lifecycle, roles, value case |
| 2: Data Integrity — Models, Normalization, Content Library | ~25% | Software models, SUMN, publisher packs, suites, discovery models |
| 3: Entitlements, Licenses, Reconciliation | ~30% | License metrics, entitlement records, reconciliation logic, compliance states |
| 4: Optimization, Reclamation, Audit Defence | ~20% | Reclamation, true-up, publisher-specific rules, audit workflow |
| 5: Reporting, Dashboards, Operational Integration | ~10% | SAM Workspace, dashboards, KPIs, integrations |

---

## 16. INTERVIEW-READY SOUNDBITES

> **"SAM is the only IT practice that directly prevents seven-figure audit penalties while simultaneously finding 5-15% waste in software spend."**

> **"The reconciliation engine is just arithmetic: entitlements minus installs minus usage, but the complexity is in the normalization pipeline and publisher rules."**

> **"A compliance position of 'Unknown' is not 'Compliant' — it's a data quality failure that hides audit exposure."**

> **"Reclamation without a 60-90 day inactivity window is not SAM — it's guessing."**

> **"Suite roll-up is the difference between counting 500 Office installs vs 500 Word + 500 Excel + 500 PowerPoint as 1,500 separate licenses."**

---

## 17. LAB: ENTITLEMENT → RECONCILIATION → COMPLIANCE

1. **Choose software model** with publisher, version, license metric, suite membership
2. **Create entitlement** with quantity = 1 (far below demand)
3. **Confirm installs exist** (install count > 1)
4. **Run reconciliation** → should show under-licensed/unlicensed
5. **Fix:** Update entitlement quantity to exceed installs → re-run → compliant
6. **Prove normalization matters:** Find unmatched discovery model → normalize → re-run → demand changes
7. **Teach back:** Write 5 sentences covering the chain

---

## VIDEO SERIES STRUCTURE (Phase 1: Visual Only)

| Video | Title | Duration | Core Concepts |
|-------|-------|----------|---------------|
| 1 | SAM in 60 Seconds | 1 min | One-sentence definition, SAM vs HAM |
| 2 | The Chain: Install → Discovery → Model → Entitlement → Result | 3 min | Six record types, never confuse them |
| 3 | Normalization (SUMN) Deep Dive | 4 min | Content Library, publisher packs, 6 statuses |
| 4 | Entitlements: Contracts, Metrics, Hygiene | 4 min | License metrics, true-up, maintenance trap |
| 5 | Reconciliation Engine Explained | 4 min | Three tiers, step-by-step, what breaks it |
| 6 | Compliance Positions & What They Mean | 3 min | 6 positions, Unknown ≠ Compliant |
| 7 | Publisher Traps: Microsoft, Oracle, IBM, SAP, Adobe | 5 min | Core factor, PVU, per-core, indirect access |
| 8 | SaaS License Management | 3 min | Assigned seats vs usage, reclamation pattern |
| 9 | Optimization & Reclamation Workflow | 3 min | Priority order, 60-90 day rule |
| 10 | Top 8 SAM Traps (Exam & Real World) | 3 min | Metric mismatch, duplicate installs, dead connectors |
| 11 | CIS-SAM Exam Map & Study Strategy | 3 min | 5 domains, weights, what to memorize |
| 12 | Lab Walkthrough: Entitlement → Compliance | 4 min | Step-by-step proof of the chain |

---

## KEY MNEMONICS FOR MEMORIZATION

| Concept | Mnemonic |
|---------|----------|
| Business Rule Types | **BAA** (Before, After, Async) |
| Client Script Types | **LOCS** (onLoad, onChange, onSubmit, onCellEdit) |
| UI Policy vs Data Policy vs Client Script | **UDC** (UI = client, Data = server, Client = both) |
| Identification Before Reconciliation | **IRE** |
| Update Set Conflicts | **ARM** (Accept, Reject, Merge) |
| CMDB | **Retire Before Delete** |
| Order vs Priority | **Lower = First** |
| Transform Script | **Coalesce = Match** |
| Debugging | **Log First, Then Debug** |
| SAM Chain | **I-D-S-E-R** (Install, Discovery, Software model, Entitlement, Reconciliation) |
| Compliance Positions | **CUOUU** (Compliant, Under, Over, Unlicensed, Unknown) |

---

## PHASE 2 PREPARATION (Audio + Video)

**TTS Options to Evaluate:**
- **Local (ASUS GX10):** Coqui TTS, Piper, MeloTTS, StyleTTS2, Bark
- **Cloud Free Tier:** ElevenLabs (free tier), PlayHT, Speechify, Microsoft Edge TTS, Google Cloud TTS (free tier), AWS Polly (free tier)
- **Open Source Models:** XTTS v2, VALL-E X, Tortoise TTS, RVC (Retrieval-based Voice Conversion)

**Video Generation Tools:**
- **Local:** MoviePy, Manim, Stable Video Diffusion, AnimateDiff, Deforum
- **Cloud Free:** Runway Gen-2 (free credits), Pika Labs, Kaiber, HeyGen (free tier), D-ID (free tier)
- **Hybrid:** Generate slides locally → cloud TTS → combine with FFmpeg