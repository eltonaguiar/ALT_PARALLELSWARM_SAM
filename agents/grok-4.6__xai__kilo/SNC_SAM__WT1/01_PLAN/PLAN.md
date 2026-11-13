# PLAN — SNC_SAM__WT1 (ServiceNow Software Asset Management research)

**Agent:** `grok-4.6__xai__kilo`
**Model:** `grok-4.6` · **Provider:** xAI · **Harness:** Kilo
**Goal owner:** this worktree. **Deliverable lives in** `05_FINAL/SAM_CONFIG_REFERENCE.md`.
**Question list:** `01_PLAN/PLANNING_QUESTIONS.md` (SAM analog of the Discovery private topic map).
**Mirror:** `plans/grok-4.6__xai__kilo__WT1/PLAN.md`

Contract copied from `eltonaguiar/ALT_PARALLELSWARM` after inspecting that swarm’s PLAN/QA/FINAL
files (especially `deepseek-flash` SC1–SC7, Buffy four-rule-family QA, and the private topic map
areas: match-vs-create, conflicting values, permitted sources, staleness, UI breadcrumbs,
properties).

## Goal

Thorough technical reference on **ServiceNow Software Asset Management (SAM)** covering:

1. configuration options / properties, grouped by *where you set them*;
2. order of operations — **setup** and **runtime** pipelines;
3. Software Asset Workspace (and classic) breadcrumbs;
4. duplicate prevention and **insert vs update** at four layers (install, discovery model,
   software model, entitlement);
5. **OOB components** — business rules, flows/subflows, UI policies, scheduled jobs, roles
   from “Components installed with Software Asset Management Professional”;
6. **catalog vs discovery** — (a) add software to the service/software catalog, (b) create
   SAM product/model *before* discovery, (c) how a discovered install is linked to a model /
   catalog item, (d) how software is blocked / excluded / not published;
7. implementation-success meta-research — foundational data, baseline metrics, phase-wise
   plan, and module-implementation-in-general.

## Output format

`05_FINAL/SAM_CONFIG_REFERENCE.md`, numbered sections:

```
0   Evidence policy + release scope
1   Mental model: SAM vs HAM vs CMDB vs Discovery vs Service Catalog; Foundation vs Professional
2   Data model / tables
3   Configuration surface (catalog of controls, by where you set them)
4   Order of operations — setup (A) and runtime (B)
5   Software Asset Workspace + classic breadcrumbs
6   Discovery sources that feed SAM
7   Installations + discovery models — insert vs update
8   Normalization / Content Service / pattern rules / custom products
9   Software models, products, editions, versions, lifecycle, parent/child
10  FOUR PATHS: catalog publish vs pre-discovery create vs discover-and-link vs block/exclude
11  Entitlements, allocations, license metrics, upgrade/downgrade
12  License reconciliation engine + properties
13  Reclamation rules + removal candidates + request/reclaim flows
14  OOB components: business rules, flows, UI policies, jobs, roles
15  Duplicate-prevention playbook + insert-vs-update decision table
16  Types inventory (metrics, statuses, entitlement types, packs, suites, …)
17  System properties (full named catalog with defaults)
18  Verification: dashboards, license position, health check, success portal
19  Anti-patterns
20  META — successful SAM implementation (foundational data, baselines, phase-wise plan)
21  META — successful ServiceNow module implementation in general
22  Open questions (UNVERIFIED)
23  Source ledger
```

Every non-obvious claim carries `[S<n>]` → section 23. No invented property names or UI paths.

## Phases (heartbeat written in `03_PHASES/` **when the phase starts**)

| phase | what | exit condition |
|---|---|---|
| 1 | capability gate | `00_PREREQ/PREREQ.md` PASS/FAIL |
| 2 | corpus: Brazil ITAM khub map + topic index | ≥200 SAM topic IDs in `research/topics_*.json` |
| 3 | retrieve: fetch priority articles to `research/raw/` | ≥25 topics fetched covering Q1–Q28 |
| 4 | extract + synthesize reference | all 24 sections present and cited |
| 5 | QA against success criteria below | `04_QA/QA.md` scored |
| 6 | final summary + filescope | blockers stated honestly |

## Success criteria (Discovery SC analog)

| # | Criterion | Measurement |
|---|---|---|
| SC1 | Coverage of SAM options | Sections 3, 6–13, 17 present with named properties/tables |
| SC2 | Correct order of operations | §4 ordered lists with prerequisites and exit checks |
| SC3 | Workspace breadcrumbs | Exact nav paths + which screens are classic-only |
| SC4 | Duplicate prevention + insert/update | Decision table for all four matching layers |
| SC5 | Traceability | Every non-obvious claim has a docs source |
| SC6 | No fabricated names/URLs | Spot-check property names against fetched text |
| SC7 | Honest limitations | UNVERIFIED list + no-instance caveat |
| SC8 | OOB objects | §14 inventories BR / flow / UI policy / job types from “Components installed with…” |
| SC9 | Four catalog/discovery paths | §10 answers Q19–Q22 as separate procedures |
| SC10 | Implementation success | §20 names foundational data, baseline metrics, phase-wise plan |
| SC11 | Types inventory | §16 lists metric / status / entitlement / pack / suite types |

## Risks

| risk | mitigation |
|---|---|
| Release drift (Brazil vs Yokohama vs Zurich ITAM maps) | Pin Brazil as primary (Discovery pass default); note Zurich/Yokohama variants |
| Foundation vs Professional vs SaaS LM split | Name the product on every control |
| Collapsing catalog-item vs software-model vs discovery-model | §10 keeps four paths separate |
| OOB BR names without an instance | Quote docs component lists; sys_ids marked UNVERIFIED |
| Login-gated Now Create | Success portal / maturity / health-check public docs only |
| Implementation-success as marketing | Prefer named data prerequisites and metrics over slogans |

## Scope exclusions (named, not silent)

- HAM-only configuration except where it shares catalog-publish or CSDM foundations
- Full pattern *authoring* (horizontal pattern editor) — listed as a surface, not a tutorial
- Customer true-up arithmetic for a specific publisher pack beyond documented metrics
