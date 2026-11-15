# ServiceNow SAM Video Series — Complete Curriculum

**CIS-SAM Interview Preparation & Technical Mastery**
**Wiki-style study hub compiled from a multi-agent fleet (deepseek-flash, grok-4.6, beam, kilo)**

This series covers the complete ServiceNow Software Asset Management (SAM) landscape, organized into logical study sections. Each video maps directly to the **CIS-SAM exam domains** and real-world SAM administrator responsibilities. The **Summary Section** at the bottom consolidates the key concepts across every video into a single, longer-form study companion.

---

## 📁 Video Index (GitHub Pages)

All videos are served from this page. The full playlist files are in the `videos/` subfolder of this directory.

| # | Video File | Title | Duration |
|---|------------|-------|----------|
| 1 | [video_01.mp4](./videos/video_01_clean.mp4) | SAM in 60 Seconds (Intro) | 40s |
| 1f | [video_01_clean.mp4](./videos/video_01_clean.mp4) | SAM in 60 Seconds (Full) | 65s |
| 2 | [video_02.mp4](./videos/video_02_clean.mp4) | The Chain: Install → Discovery → Model → Entitlement → Result | 40s |
| 3 | [video_03.mp4](./videos/video_03_clean.mp4) | Normalization (SUMN) Deep Dive | 40s |
| 4 | [video_04.mp4](./videos/video_04_clean.mp4) | Entitlements: Contracts, Metrics, Hygiene | 40s |
| 5 | [video_05.mp4](./videos/video_05_clean.mp4) | Reconciliation Engine Explained | 45s |
| 6 | [video_06.mp4](./videos/video_06_clean.mp4) | Compliance Positions — 6 States, Unknown ≠ Compliant | 40s |
| 7 | [video_07.mp4](./videos/video_07_clean.mp4) | Publisher Traps — Microsoft, Oracle, IBM, SAP, Adobe | 50s |
| 8 | [video_08.mp4](./videos/video_08_clean.mp4) | SaaS License Management | 40s |
| 9 | [video_09.mp4](./videos/video_09_clean.mp4) | Optimization & Reclamation — Where SAM Pays for Itself | 45s |
| 10 | [video_10.mp4](./videos/video_10_clean.mp4) | Top 8 SAM Traps — Exam & Real World | 60s |
| 11 | [video_11.mp4](./videos/video_11_clean.mp4) | CIS-SAM Exam Map & Study Strategy | 45s |
| 12 | [video_12.mp4](./videos/video_12_clean.mp4) | Lab Walkthrough: Entitlement → Reconciliation → Compliance | 65s |

> **Phase 2 versions (narration + burned-in subtitles):** `video_01_final.mp4` and `video_02_final.mp4` are also available in the parent folder with aligned SRT subtitles (`subtitles/video_01.srt`, `subtitles/video_02.srt`).

---

## 📚 Study Sections (Organized Curriculum)

The 12 videos are grouped into **5 thematic sections** that mirror the CIS-SAM blueprint progression. Study in this order for interview readiness.

### Section 1 — SAM Foundations (Videos 1–2)
**Blueprint Domains 1 & 3 (Overview, Fundamentals, Chain)**

| Video | Key Concepts |
|-------|--------------|
| **1. SAM in 60 Seconds** | One-sentence definition · SAM vs HAM vs ITAM · The reconciliation engine as the differentiator |
| **2. The Chain** | `Install → Discovery Model → Software Model → Entitlement → Reconciliation → Result` · I-D-S-E-R mnemonic · The three record types never to confuse |

**Memorize:**
> *"SAM reconciles what you own (entitlements) against what exists and is used (normalized installs + usage) per software model and license metric, and turns the difference into a compliance position."*

---

### Section 2 — Data Integrity & Normalization (Videos 3–4)
**Blueprint Domain 2 (Data Integrity — Models, Normalization, Content Library)**

| Video | Key Concepts |
|-------|--------------|
| **3. Normalization (SUMN) Deep Dive** | SUMN pipeline (Discovery → Normalization → Reconciliation) · Content Library & Publisher Packs · **6 normalization statuses** (New, Match Not Found, Publisher Normalized, Partially Normalized, Normalized, Manually Normalized) · Suite roll-up |
| **4. Entitlements** | Must-have attributes (software model, publisher, license metric, quantity, contract/PO, dates, unit cost) · License metric types · Entitlement hygiene (one per contract line, never overwrite quantity, maintenance ≠ license, metric mismatch is silent) |

**The 6 Normalization Statuses:**
| Status | Manual Normalize? | Revert? |
|--------|-------------------|---------|
| New | No | No |
| Match Not Found | Yes | No |
| Publisher Normalized | Yes | Yes |
| Partially Normalized | Yes | Yes |
| Normalized | No | Yes |
| Manually Normalized | No | No |

**Key rule:** All reverts go to **Match Not Found**. Pattern-normalized models cannot be reverted.

---

### Section 3 — Reconciliation & Compliance (Videos 5–6)
**Blueprint Domain 3 (Entitlements, Licenses, Reconciliation — highest weight ~30%)**

| Video | Key Concepts |
|-------|--------------|
| **5. Reconciliation Engine Explained** | Formula: `Compliance = f(entitlement quantity, normalized installs, usage evidence, metric, rules)` · 7-step reconciliation · **Three tiers**: product (`samp_product_result`), software model, license metric (`samp_license_metric_result`) · What breaks reconciliation |
| **6. Compliance Positions** | **6 states**: Compliant, Over-licensed, Under-licensed, Unlicensed, Not counted, Unknown · Financial meaning · **"Unknown is NOT Compliant"** |

**Rights Algebra (core math):**
```
Rights Owned = active entitlements sharing the metric
Rights Used = allocated in use + not allocated in use + installed
Rights Available = Owned − Used
Allocated Not In Use = wasted rights → remove allocations
Not Allocated In Use = unallocated consumption → create allocations or remove unallocated installs
```

---

### Section 4 — Publisher-Specific & SaaS (Videos 7–8)
**Blueprint Domain 4 (Optimization, Reclamation, Audit Defence)**

| Video | Key Concepts |
|-------|--------------|
| **7. Publisher Traps** | **Microsoft**: SQL Server per-core (physical cores × core factor, min 4/socket), virtualization rules, M365 bundle splitting, downgrade rights · **Oracle**: core-factor table, license the *server* not VM unless certified hard partitioning, LMS scripts, named-user-plus minimums · **IBM**: PVU tables, sub-capacity needs ILMT · **SAP**: named-user by usage type, indirect/digital access · **Adobe**: VIP/ETLA named-user, suite roll-up · **ServiceNow**: billed over-consumption |
| **8. SaaS License Management** | On-prem vs SaaS (installs vs seats, device/core vs per-user, launch metering vs last sign-in) · Connectors (M365, Google Workspace, Salesforce, Zoom, Slack, Box… ) · Classic waste pattern (1,000 seats, 260 inactive = 26% recoverable) · Dead-connector trap |

---

### Section 5 — Optimization, Exam & Lab (Videos 9–12)
**Blueprint Domain 4 & 5 (Optimization, Reporting, Integration)**

| Video | Key Concepts |
|-------|--------------|
| **9. Optimization & Reclamation** | Priority order: reclaim dormant seats → uninstall unused installs → right-size editions → consolidate tools → align renewal quantities → enforce process · Reclamation workflow · **60–90 day inactivity rule** + owner sign-off |
| **10. Top 8 SAM Traps** | Metric mismatch (silent) · Duplicate installs · Unnormalized titles · Maintenance as license · Leftover installs on out-of-scope devices · First reconciliation as invoice · Dead SaaS connector · Confusing vendor/publisher/PPN/model/catalog |
| **11. CIS-SAM Exam Map** | 5 domains + weights (1: ~15%, 2: ~25%, 3: ~30%, 4: ~20%, 5: ~10%) · official prep courses · what to memorize |
| **12. Lab Walkthrough** | 7-step proof of the chain: choose model → entitlement far below demand → confirm installs → run reconciliation (under-licensed) → fix (compliant) → prove normalization changes answer → teach back |

---

# 🎬 SUMMARY SECTION — The "Master Class" Longer-Form Companion

This is the consolidated, longer-form study companion. It synthesizes the core concepts from **all** videos and all peer work into one master narrative. Read it after watching the videos, or use it as a rapid refresher before an interview.

## The One-Sentence Thesis

> **SAM reconciles what you own (entitlements) against what exists and is used (normalized installs + usage) per software model and license metric, and turns the difference into a compliance position.**

## The Master Chain (I-D-S-E-R)

```
CI (CMDB/IRE)
  └─ cmdb_sam_sw_install            # one install on one device
       └─ cmdb_sam_sw_discovery_model  # raw fingerprint → normalized
            └─ cmdb_software_product_model  # purchased product profile
                 └─ alm_license             # rights + metric + dates
                      └─ reconciliation     # rights vs demand
                           ├─ samp_product_result
                           ├─ Software Model Results
                           └─ samp_license_metric_result
```

**"Software model = what it IS. Entitlement = what you MAY USE. Installation = what EXISTS. Usage = what is USED. Reconciliation = the DIFFERENCE."**

## The Four Gates (Prerequisites for SAM to Work)

| Gate | Pass Condition |
|------|----------------|
| Schema + edition | Correct plugin; SAM tables present |
| CMDB + CI identity | One CI per device; IRE rules reviewed |
| Discovery feed | One trusted source populating installs |
| Normalization + entitlements | Models normalize; every entitlement has model + metric |

## The Reconciliation Engine

**Formula:** `Compliance position = f(entitlement quantity, normalized installs, usage evidence, metric, rules)`

**Step-by-step:**
1. Gather entitlements (filtered by date validity)
2. Gather normalized installs, de-duplicated per device
3. Apply usage evidence (for reclamation / not-in-use)
4. Apply publisher rules and exclusions (ignore lists, VM rules, suite roll-ups, downgrade rights)
5. Calculate position per model and metric
6. Persist a timestamped reconciliation result record
7. Roll up to publisher and portfolio dashboards

> **"Reconciliation is a report, not a correction. Fix the model, entitlement, or normalization — never edit the result."**

## Compliance Positions & Their Meaning

| Position | Meaning | Action |
|----------|---------|--------|
| Compliant | Owned ≥ demand | Monitor |
| Over-licensed | Owned > demand | Reclaim / renegotiate |
| Under-licensed | Owned < demand | True-up or reclaim |
| Unlicensed | No entitlement | Remove / purchase |
| Not counted | Excluded by rule | Review annually |
| Unknown | Insufficient data | Fix data — NOT compliant |

> **"Unknown" is NOT "Compliant". A SAM program that reports unknown as compliant is why audit penalties appear out of nowhere.**

## Publisher-Specific Traps (Exam Favorites)

- **Microsoft:** SQL Server per-core (physical cores × core factor, min 4/socket); M365 suite overlap; downgrade rights documented.
- **Oracle:** Core-factor per processor; license the **server** not the VM unless hardened partitioning; LMS scripts are the audit instrument; named-user-plus minimums.
- **IBM:** PVU tables; sub-capacity needs ILMT evidence.
- **SAP:** Named-user by usage type; indirect/digital access is a live battleground.
- **Adobe:** VIP/ETLA named-user; shared-device differs; suite roll-up.
- **ServiceNow:** Billed over-consumption (cost-control, not audit).

## The Rights Algebra

```
Rights Owned = active entitlements sharing the metric
Rights Used = allocated in use + not allocated in use + installed
Rights Available = Owned − Used
Allocated Not In Use = wasted rights → remove allocations
Not Allocated In Use = unallocated consumption → create allocations or remove unallocated installs
```

## SaaS License Management

- On-prem: Discovery finds installs, per-device/core metric, launch metering, vs installs, uninstall.
- SaaS: Connector pulls subscriptions + assigned seats, per-user metric, last sign-in, vs assigned inactive seats, reclaim dormant seats.
- **Classic waste:** 1,000 assigned M365 E5 seats, 260 never signed in 90+ days = 26% recoverable.
- **Dead connector trap:** a silent connector looks exactly like "no waste" — monitor health.

## Optimization & Reclamation (Where SAM Pays for Itself)

Priority order:
1. Reclaim dormant seats (SaaS / named-user first)
2. Uninstall unused installs (per-core servers)
3. Right-size editions (E5 → E3, Ent → Std)
4. Consolidate overlapping tools (post-merger)
5. Align renewal quantities to actual demand
6. Gate new requests on existing entitlement

> **Never reclaim on one night's data — require the 60–90 day inactivity window and business owner sign-off.**

## Top 8 Traps (Memorize)

1. **Metric mismatch** — silently meaningless result
2. **Duplicate installs** — inflated demand; configure dedup
3. **Unnormalized titles** — unlicensed/unknown; normalize before auto-create
4. **Maintenance treated as a license** — false compliance
5. **Leftover installs on out-of-scope devices** — phantom demand
6. **First reconciliation treated as an invoice** — wrong true-up
7. **Dead SaaS connector** — "no waste" illusion
8. **Confusing vendor/publisher/PPN/model/discovery model/catalog** — wrong links

## CIS-SAM Exam Blueprint (Domain Weights)

| Domain | Weight | Focus |
|--------|--------|-------|
| 1: Overview & Fundamentals | ~15% | Positioning, lifecycle, roles, value case |
| 2: Data Integrity (Models, Normalization) | ~25% | Software models, SUMN, publisher packs, suites |
| 3: Entitlements, Licenses, Reconciliation | ~30% | License metrics, entitlement records, reconciliation logic, compliance states |
| 4: Optimization, Reclamation, Audit Defence | ~20% | Reclamation, true-up, publisher rules, audit workflow |
| 5: Reporting, Dashboards, Integration | ~10% | SAM Workspace, dashboards, KPIs |

## Key Tables to Know

| Table | Purpose |
|-------|---------|
| `cmdb_sam_sw_install` | Installs (source of truth for current software) |
| `cmdb_sam_sw_discovery_model` | Raw fingerprints + normalized fields + status |
| `cmdb_software_product_model` | Purchased product profile |
| `alm_license` | Entitlement |
| `samp_sw_usage` | Usage evidence (product-level) |
| `samp_product_result` | Product compliance/cost |
| `samp_license_metric_result` | Rights per metric |
| `samp_reconciliation_result` | Reconciliation run record |
| `samp_sw_reclamation_candidate` | Reclamation candidates |
| `sam_sw_dedup_rule` | Custom dedup rules |

## Key Mnemonics

- **I-D-S-E-R** — Install, Discovery, Software model, Entitlement, Reconciliation (the chain)
- **BAA** — Business Rules: Before, After, Async
- **LOCS** — Client Scripts: onLoad, onChange, onSubmit, onCellEdit
- **IRE** — Identification Before Reconciliation (CMDB)
- **Retire Before Delete** — CMDB lifecycle
- **Lower = First** — Order vs Priority
- **Coalesce = Match** — Transform scripts
- **Log First, Then Debug** — Debugging discipline

## Interview-Ready Soundbites

> *"SAM is the only IT practice that directly prevents seven-figure audit penalties while simultaneously finding 5-15% waste in software spend."*

> *"The reconciliation engine is just arithmetic: entitlements minus installs minus usage, but the complexity is in the normalization pipeline and publisher rules."*

> *"A compliance position of 'Unknown' is not 'Compliant' — it's a data quality failure that hides audit exposure."*

> *"Reclamation without a 60-90 day inactivity window is not SAM — it's guessing."*

> *"Suite roll-up is the difference between counting 500 Office installs vs 500 Word + 500 Excel + 500 PowerPoint as 1,500 separate licenses."*

---

## 🔗 Source & Reference Material

- **Live SAM Guide:** https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/sam/sam-guide/
- **Consolidated Key Concepts:** [SAM_KEY_CONCEPTS.md](../../videos/SAM_KEY_CONCEPTS.md)
- **Condensed Summary:** [SAM_KEY_CONCEPTS_SUMMARY.md](../../videos/SAM_KEY_CONCEPTS_SUMMARY.md)
- **Video Generation Tool Analysis:** [VIDEO_GENERATION_TOOLS_ANALYSIS.md](../../videos/VIDEO_GENERATION_TOOLS_ANALYSIS.md)

## 📋 Provenance & Metadata

| Field | Value |
|-------|-------|
| Repository | alt_parallelswarm_SAM |
| Source Folder | docs/sam-videos/ |
| Video Folder | docs/sam-videos/videos/ |
| Worktree | samvideos-v4 (peers: samvideos, samvideos-v2, samvideos-v3) |
| Generated | 2026-11-14/15 |
| Pipeline | YAML → PPTX → PNG → FFmpeg (libx264), 1920×1080, 30fps |
| Narration | edge-tts (en-US-AriaNeural) |
| Subtitles | Slide-aligned SRT (no overlapping captions) |

---

## 💬 Interview Q&A — How ServiceNow Measures Software Entitlements

**Q:** How does ServiceNow measure software entitlement — by contract start/end date, by quantity, or both?

**A:** ServiceNow measures and evaluates software entitlements using **both quantity and start/end dates**, depending on whether it is measuring compliance (license exhaustion) or temporal validity (active/expired status).

**1. By Quantity (License Counts & Rights)**
- **Purchased / Active Rights:** tracks how many licenses, packs, or concurrent user limits you bought (e.g., 100 installed/purchased rights).
- **Reconciliation & Consumption:** during SAM reconciliation, ServiceNow compares discovered/installed quantity against the available purchased-rights quantity.
- If installations exceed purchased quantity → flags **non-compliance** or triggers an **overallocation / true-up alert**.

**2. By Start Date and End Date (Time & Duration)**
- **License Duration:** either **Perpetual** (continuous, no expiration) or **Subscription** (valid for a specific time frame).
- **Validity Dates:** start and end dates dictate when the entitlement is active.
- **Automated State Changes:**
  - **In Use** when current date falls between start and end dates.
  - **Retired/expired** when the date passes the end date (and active rights hit zero).
  - **On Order** if the start date is in the future.

**Summary:** ServiceNow uses **quantity** to determine how many installations are covered vs how many you own, and **start/end dates** to determine when those rights are valid/active. Both work together during SAM compliance calculations.
