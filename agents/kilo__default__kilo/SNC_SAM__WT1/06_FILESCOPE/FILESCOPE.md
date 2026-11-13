# FILESCOPE.md — ServiceNow SAM Module File Scope

- **Compiled by:** `kilo` / provider **kilo** / harness **default** (`kilo__default__kilo`)
- **Date:** 2026-11-13
- **Purpose:** Define the file inventory and scope boundaries for the SAM module documentation worktree, mirroring the FILESCOPE.md pattern from `ALT_PARALLELSWARM` (`final/FILESCOPE.md`).

---

## 0. Worktree identity

- **Worktree:** `SNC_SAM__WT1`
- **Agent:** `kilo` / provider **kilo** / harness **default**
- **Model:** `kilo`
- **Created:** 2026-11-13
- **Purpose:** Document ServiceNow Software Asset Management (SAM) module configuration, discovery rules, CI insertion/update rules, and license/CI management

---

## 1. File inventory

### 1.1 Phase documentation (03_PHASES)

| File | Purpose | Lines | Status |
|---|---|---|---|
| `phase1_started.md` | Phase 1: Foundations started — CMDB health, prerequisite validation, baseline metrics | ~450 | Complete |
| `phase2_corpus.md` | Phase 2: Activation & corpus built — SAM plugin activation, CI config, entitlement loading | ~500 | Complete |
| `phase3_research_done.md` | Phase 3: Normalization & reconciliation running — daily jobs, weekly recon, dedup, reclamation | ~500 | Complete |
| `phase4_synthesis.md` | Phase 4: QA & stabilization — Discovery Status, CMDB Health KPIs, anti-patterns, gate review | ~600 | Complete |

### 1.2 Plan & prerequisites

| File | Purpose | Lines | Status |
|---|---|---|---|
| `00_PREREQ/PREREQ.md` | Platform and role pre-conditions; tables created; order of operations; data flow | ~600 | Complete |
| `01_PLAN/PLAN.md` | 5-phase implementation plan (Crawl→Walk→Run); risks & mitigation; success criteria; phase-wise plan | ~800 | Complete |

### 1.3 Clarifications & edge cases

| File | Purpose | Lines | Status |
|---|---|---|---|
| `02_CLARIFICATIONS/CLARIFY.md` | Edge cases: discovery model key matching, business rule logic, normalization revert rules, dedup edge cases, content service, domain sep, IBM special case, SCCM deprecation, VMware keys, license metrics | ~900 | Complete |

### 1.4 QA self-check

| File | Purpose | Lines | Status |
|---|---|---|---|
| `04_QA/QA.md` | Per-phase self-checks; overall end-to-end validation; go/no-go decision; 55+ checklist items | ~700 | Complete |

### 1.5 Final configuration reference

| File | Purpose | Lines | Status |
|---|---|---|---|
| `05_FINAL/SAM_CONFIG_REFERENCE.md` | Exhaustive config reference: module changes; tables; order of ops; insert-vs-update; CI config; discovery models; normalization; duplicates; reconciliation; config options; key tables; 12 known gaps | ~1300 | Complete |
| `05_FINAL/FINAL_SUMMARY.md` | Final synthesis of entire SAM module docs; coverage map; parameter inventory (must-consider + full); folder structure verification; 12 known gaps + 10 UNVERIFIED questions; complete source ledger (53 sources) | ~1500 | Complete |

### 1.6 Research raw files

| Directory | Purpose | Source count |
|---|---|---|
| `research/` | Raw search→digest transcripts from khub API (Australia maps); 299-topic index JSON | 299 titles in `topics_brazil_itam_sam.json` |
| `research/raw/` | Individual source articles fetched via khub content API; each artifact tagged S1–S37 | 37+ individual articles |

---

## 2. Scope boundaries

### 2.1 In-scope (documented explicitly)

- ServiceNow SAM module activation and configuration
- All 5 SAM-created tables and their purposes
- Discovery → SAM data flow (insert vs. update rules)
- CI-side configuration to display SAM data (related lists)
- Software Discovery Models: storage, population, manual normalization, ML normalization
- Normalization process, statuses, scheduling, content-service rules
- Duplicate and stale-data hygiene (REST API delete; dedup job)
- Compliance reconciliation (3-tier outputs; Oracle summary)
- Configuration options (roles; plugins; CI forms; SCCM; properties; domain sep; content service; jobs; knobs)
- Key tables inventory (8 tables with notes)
- 12 documented known gaps / caveats
- 10 UNVERIFIED open questions
- 5-phase implementation plan (Crawl → Walk → Run)
- Per-phase QA self-checks (55+ checklist items)
- Complete parameter inventory (must-consider + full per-screen list)
- Source ledger (53 sources with release labels and local file mappings)

### 2.2 Out-of-scope (not documented in this worktree)

- Pattern authoring for Discovery (deliberately out of scope; proposes `SNC_DISC__WT2`)
- CMDB IRE identification rules in full detail (referenced sibling: `ALT_PARALLELSWARM`)
- CMDB dynamic reconciliation rules (requires CMDB 360; noted as "must be enabled" but not detailed)
- Classic UI vs. new workspace full diff beyond "workspace hides classic menus"
- Exact business rule sys_id or advanced BR logic on `cmdb_sam_sw_install`
- Full `glide.cmdb.sam.*` / remaining `samp.*` system property catalog (not published by docs)
- Machine learning algorithmic detail (plugin effect only; not algorithmic)
- HAM vs SAM catalog publish interaction beyond `[S27][S29]` (not fully documented)
- Now Create / Success Checklist PDFs (login-gated; not fetched)
- RHEL threshold property internal name (not captured)
- Zurich/Yokohama deltas vs Brazil pin (not fetched)
- All KB articles (Now Support restricted access)
- Full metric enum for license metrics (see `[S31]`; too large to duplicate)
- Allocation management (8k article; treat as follow-on worktree)
- Success Checklist PDFs (login-gated)
- Path to Value / Quick Start / Office Hours / Starter Kit details (Community corroboration, not product docs)

### 2.3 File-level scope notes

- **`research/` directory**: Contains 299-topic index JSON and 37+ individual source articles (`research/raw/`). These are raw fetches from the khub API; not all were fully read, but all were retained for provenance.
- **`research/raw/S<n>` files**: Each tagged with source ID (S1–S37); content varies from short descriptions to full procedural documentation. Not all were equally exhaustive; discrepancies flagged rather than silently resolved.
- **System property table**: Documents 53+ named properties with defaults where documented; acknowledges gaps in full catalog depth.
- **Discovery reference cross-link**: Explicitly notes that the CMDB/IRE/reconciliation underlying flow is a sibling topic covered in `ALT_PARALLELSWARM`; this document focuses on SAM-module-specific additions.

---

## 3. Worktree completion status

| Category | Status |
|---|---|
| Phase documentation (03_PHASES) | ✅ All 4 phase files complete |
| Plan & prerequisites (00_PREREQ, 01_PLAN) | ✅ Both files complete |
| Clarifications (02_CLARIFICATIONS) | ✅ Complete |
| QA self-check (04_QA) | ✅ Complete |
| Final reference (05_FINAL) | ✅ Both files complete (SAM_CONFIG_REFERENCE.md + FINAL_SUMMARY.md) |
| File inventory & scope (06_FILESCOPE) | ✅ Complete |
| **Overall worktree** | ✅ **All 7 phases + filescope complete** |

---

## 4. Next steps (if continuing work)

- Verify against live instance: all UI paths, system property values, business rule logic
- Resolve 10 UNVERIFIED open questions via instance testing (`sam_admin` session required)
- Cross-reference with `ALT_PARALLELSWARM` Discovery/CMDB reference for sibling topics
- Create Agent Manager assignments for peer review or parallel agent work
- Deploy documentation to production via `workflow_dispatch` (hourly cron guarantees full refresh within the hour)