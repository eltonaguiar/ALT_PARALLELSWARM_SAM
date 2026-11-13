# LEARNING PROTOCOL ADDITIONS — generic module protocol

**Agent:** `deepseek-flash__deepseek__kilo` · **Date:** 2026-11-13
**Target repo:** `ServiceNow_Learning` — `docs/00-methodology.md`, `docs/08-SAM-SETUP.md`, and the module-guide family.
**Purpose:** the module guides teach *what a module is*; the research repo supplies *how to operate it*. This file extracts the reusable artefacts from `ALT_PARALLELSWARM_SAM` so any module guide (HAM, CSM, FSM, ITSM, Discovery, CMDB, TSOM, Sales CRM, HRSD, AI) can reach the same depth without copying SAM specifics.

Marks: **P** = protocol practice; **V** = product-documented; **U** = verify on instance.

---

## 0. Where this fits the existing loop

`00-methodology.md` defines **ORIENT → MODEL → PRACTISE → PROVE → TEACH**. The additions slot in as follows:

| Loop stage | New artefact |
|---|---|
| ORIENT | record-chain map; scope and release pin |
| MODEL | identity/normalisation state machine; insert/update matrix; quantity algebra |
| PRACTISE | OOB object inventory; property inventory; reporting map; integration contract |
| PROVE | numeric test cases; acceptance gates; rollback; audit chain |
| TEACH | confidence legend; "what breaks it" triage; quiz/lab hooks |

The existing `08-SAM-SETUP.md` already has a build order, prerequisites, ten mistakes, a lab, and a verification checklist. The additions below are the missing **artefact layer** between that narrative and an implementable reference.

---

## 1. Ten protocol artefacts (add to every module)

### 1.1 Record-chain map (ORIENT)

**What:** the 4–6 records that form the module's value chain, each marked **owned / observed / computed**.

**Template:**

| Stage | Record | Table | Owned by | Created by | Mutability |
|---|---|---|---|---|---|
| Owned | … | … | … | … | … |
| Observed | … | … | … | … | … |
| Computed | … | … | … | … | … |

**SAM example:** `alm_license` (owned) → `cmdb_sam_sw_discovery_model` (observed) → `cmdb_sam_sw_install` (observed) → `samp_license_metric_result` (computed).

**Why:** every module failure is a broken arrow in this chain. The map makes the success criterion explicit: the chain closes, not "a record was inserted".

---

### 1.2 Identity / normalisation state machine (MODEL)

**What:** every state a discovered/imported record can hold, which states allow manual intervention, which allow revert, and what each state means for downstream computation.

**Template:**

| State | Meaning | Manual fix allowed | Revert allowed | Downstream effect |
|---|---|---|---|---|

**SAM example:** six normalisation states; only `Partially`, `Publisher`, `Match Not Found` allow manual; `Manually`/pattern cannot revert.

**Why:** "normalised / not normalised" is not a state machine; admins need the exact states to triage.

---

### 1.3 Insert/update matrix (MODEL)

**What:** for each record, the match key, insert condition, update condition, and the control that can stop the insert.

**Template:**

| Incoming | Match key | Insert when | Update when | Stop control |
|---|---|---|---|---|

**SAM example:** discovery model key Publisher + Display name + Version; install→model business rule; IRE data-source gate for third-party.

**Why:** prevents the "why did this duplicate?" and "why did it overwrite?" questions.

---

### 1.4 Quantity / entitlement algebra (MODEL)

**What:** only for modules with rights, allocations, quotas, or consumption. The arithmetic and every bucket.

**Template:**

| Bucket | Formula | Meaning | Remediation if > 0 |
|---|---|---|---|

**SAM example:** owned − used = available; used = allocated-in-use + not-allocated-in-use; allocated-not-in-use; allocations needed; unlicensed.

**Why:** a module that reports "compliant" without showing the buckets is unfalsifiable.

---

### 1.5 OOB object inventory (PRACTISE)

**What:** scheduled jobs, business rules, flows, script includes, UI actions — purpose, target table/field, and **customise vs leave**.

**Template:**

| Object | Type | Target | Purpose | Customise? | Risk if customised |
|---|---|---|---|---|---|

**Why:** the most expensive mistakes are overlays on OOB logic. The inventory is the "do not touch" list plus the sanctioned extension points.

---

### 1.6 Property inventory (PRACTISE)

**What:** two lists — **must-consider** (with default, blast radius, owner) and **full** (all documented properties).

**Template:**

| Property | Default | Effect | Blast radius | Decide before go-live? |
|---|---|---|---|---|

**Why:** a flat list hides the ten decisions that change the module's output.

---

### 1.7 Reporting map (PRACTISE)

**What:** every named dashboard/widget/report → source table → grouping → owner.

**Template:**

| Surface | Metric | Source table | Grouping | Owner |
|---|---|---|---|---|

**Why:** "the dashboard says X" is not evidence unless the table is known; this is also how you detect a stale or miswired widget.

---

### 1.8 Integration contract (PRACTISE)

**What:** for each feed: plugin/app id, direction, target record, required fields, frequency, latency, dedup key, error/retry, count reconciliation, **absence/uninstall semantics**, owner.

**Template:**

| Source | Plugin | Direction | Target | Required fields | Frequency | Error path | Absence signal | Owner |
|---|---|---|---|---|---|---|---|---|

**Why:** integrations are interfaces, not bullet lists. The absence signal is the one everybody forgets (deletes never propagate by default).

---

### 1.9 Programme controls (PROVE)

**What:** RACI, numeric test cases, acceptance gates, rollback, change control, audit chain.

**Minimum:**

- RACI for each record/decision (accountable/responsible/consulted/informed).
- 5–10 numeric tests with expected values (not "it ran").
- Data-quality thresholds before production.
- Rollback for every compliance/financial-affecting change.
- Change-control list: which objects move the number.
- Evidence chain: source document → record → allocation → computed result.

**Why:** the technical config can be right and the programme still untrustworthy.

---

### 1.10 Confidence and release discipline (every artefact)

**What:** a release pin; `V/C/U` marks; verification queries; a "known conflicts" section.

**Template:**

- Release: `<family>` + doc date.
- `V` = printed in official docs; `C` = corroborated; `U` = label-only, verify.
- Queries: `sys_dictionary.list?sysparm_query=name=<table>^elementLIKE<term>`, `sys_db_object.list?sysparm_query=nameLIKE<prefix>`.
- Conflicts: curriculum vs docs, release drift, singular/plural names.

**Why:** exact table/field names are the difference between a runbook and a guess.

---

### 1.11 Closed-loop modules (SAM, HAM, SPM, …)

Some modules reconcile two independent truths (owned vs observed). Add these seven rules to the protocol for them:

1. **Success is not a row insert.** Success = the two truths reconcile and the result is explainable.
2. **Four object types when a catalog exists:** requestable item (catalog / `sc_cat_item`), master data (model/entitlement), observed data (install/usage), computed result. Never collapse them.
3. **Pin plugin IDs** for Foundation vs Professional/Pro; mark irreversible upgrades (e.g. Basic SAM → Pro).
4. **Name the scheduled jobs** and their target fields in the PRACTISE gate; "the module runs jobs" is not enough.
5. **One numeric test minimum:** 1 right + 2 observations → shortfall 1; same 2 observations on 1 device with dedup → 1.
6. **Stamp teaching code** `not OOB` / `verify`; never present a custom `u_*` script as product behaviour.
7. **Sibling-module contrast** in ORIENT (HAM vs SAM vs ITAM), because the shared `alm_*` tables cause most confusion.

**Do not** replace the existing ORIENT → MODEL → PRACTISE → PROVE → TEACH loop (or the 95-minute format) with a configuration encyclopedia. The artefacts above are inputs to the loop, not a new curriculum.

---

## 2. Proposed files in `ServiceNow_Learning`

| File | Contents |
|---|---|
| `docs/module-protocol.md` | §1.1–§1.10 templates with one worked example each (SAM), plus a blank template table |
| `docs/module-protocol-checklist.md` | per-module gate list: records mapped, states enumerated, insert/update matrix, OOB inventory, properties split, reporting map, integration contracts, tests, gates, rollback, change control, audit chain |
| `docs/00-methodology.md` (edit) | add a short "Artefacts per loop stage" table pointing to the two new files |
| `docs/08-SAM-SETUP.md` (edit) | link each step to the corresponding artefact; correct nightly → weekly; add six-status and three-tier pointers |

**Do not** turn the protocol into a SAM dump. The worked examples stay short; depth links to `ALT_PARALLELSWARM_SAM`.

---

## 3. Per-module application (examples)

| Module | Record chain | State machine | Quantity algebra | Key integration absence signal |
|---|---|---|---|---|
| HAM | asset → CI → stockroom → contract | asset state / install status | on-hand vs allocated | hardware disposal |
| CSM | account → contact → case → SLA | case state / escalation | entitlements vs cases | customer merge |
| FSM | work order → task → assignment → asset | dispatch state | skills/capacity | technician leave |
| ITSM | incident → problem → change → CI | incident/change state | SLA clocks | CI retirement |
| Discovery | schedule → device → CI | scan → classify → identify → explore | n/a | device offline |
| CMDB | class → CI → relation | identified / duplicate / retired | n/a | CI decommission |
| SAM | entitlement → model → discovery model → install → result | six normalisation states | rights algebra | uninstall |

The protocol is the same; the content changes.

---

## 4. Quality bar

Before publishing any module artefact:

1. Release pinned; every non-obvious claim marked `V/C/U`.
2. No invented table/column; label-only fields carry a verification query.
3. Every dashboard has a source table.
4. Every feed has an absence/uninstall rule and an owner.
5. At least five numeric tests with expected outputs.
6. Rollback and change-control lists exist.
7. Conflicts are recorded, not smoothed over.
8. One "what breaks it" triage table and one "fields people forget" list.

---

## 5. Anti-patterns this protocol prevents

- Teaching a module as a feature list with no record chain.
- Treating "record inserted" as success.
- Listing integrations without error/absence semantics.
- A flat property list with no must-consider shortlist.
- Dashboards with no source table.
- "Reconciliation ran" as acceptance.
- Assuming the vendor's default cadence from memory (e.g. nightly vs weekly).
- Copying community table names (`cmdb_sam_sw_usage`, `sam_sw_reconciliation_result`, `alm_software`) into a guide.
- Customising OOB jobs instead of using extension points.
- No owner after go-live.

---

## 6. Immediate edits recommended to the existing SAM path

1. `08-SAM-SETUP.md`: change "reconciliation" cadence language to weekly/on-demand; add the six statuses and the three-tier result tables.
2. `sam-guide.md`: apply the 18 corrections in `GUIDE_VS_REPO_DELTA.md` §3 before adding new sections.
3. Add `module-protocol.md` + checklist; link from `00-methodology.md`.
4. Add a "confidence legend" block to every module guide (the SAM guide already says "verify"; make it systematic).

---

## 7. Relationship to this repo

- `SAM_MODULE_REFERENCE.md` is the worked example of §1.1–§1.8.
- `ROUND2_GAP_ANALYSIS.md` is the worked example of §1.9 and the numeric tests.
- `MODULE_IMPLEMENTATION_PLAN.md` is the programme wrapper.
- `SAM_IMPLEMENTATION_CHECKLIST.md` is the gate list.
- `GUIDE_VS_REPO_DELTA.md` is the migration plan for the existing SAM guide.
