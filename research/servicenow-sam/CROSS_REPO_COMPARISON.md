# Cross-repo comparison — SAM research vs protocol vs training page

**Agent:** `kilo-sam-deepdive__kilo__cli` · **Date:** 2026-11-13
**Stamp:** 2026-11-13T15:44:29Z · **run-id:** `4178ec70-e3f5-4bc9-a0ab-9c7cdb2acf25`

---

## ELI5

Three libraries describe the same subject (SAM):

- **GitHub research repo** (`alt_parallelswarm_SAM`) = the engineer's notebook: exact table names, properties, procedures.
- **Learning protocol repo** (`ServiceNow_Learning`) = the study method: how to learn fast and deliver safely.
- **Training page** (`sam-guide`) = the exam-focused storybook.

This note compares what each library contains, and what none of them contain.

---

## Coverage matrix

| Dimension | SAM research repo | Protocol repo | Training page |
|---|---|---|---|
| Exact tables/fields/properties | **Strong** (finals + deep dive) | None (out of scope) | Weak/errors present |
| Step-by-step procedures | **Strong** (DD §3–§5) | Labs only (generic) | Good conceptual steps |
| OOB component inventory | **Strong** (DD §2) | Partial (OOB doc generic) | Feature list only |
| Normalization / reconciliation mechanics | **Strong** | None | Conceptual |
| Implementation gates / acceptance criteria | Missing (see COVERAGE_GAP_ANALYSIS) | **Proposed now** (lessons doc) | None |
| Test cases / expected results | **Missing everywhere** | Proposed pattern | Quiz only |
| Ownership / RACI / source contracts | Missing | Proposed template | None |
| Change control / rollback | Missing | Proposed | None |
| Cutover / hypercare / monitoring | Missing | Proposed | None |
| Learning science / personas / mnemonics | None | **Added now** (experimental doc) | Memory aids only |
| Exam alignment (CIS-SAM weights) | Referenced | N/A | **Strong** |
| Diagrams / infographics | None | **Added now** (SVG assets) | Mermaid diagrams |

---

## What each side contributes that the others lack

**Research repo unique:** exact property names/defaults, job inventory, insert/update matrices, troubleshooting, anti-patterns, source citations.
**Protocol repo unique:** learning loop, gate checklists, RACI/source-contract/change-control templates, infographics, bridging rules.
**Training page unique:** CIS-SAM domain weights, publisher-trap detail, optimization priority order, day-one report definitions, indicative KPIs, lab/quiz/memory aids.

## General gaps vs ServiceNow implementation best practice

1. No success criteria or pilot go/no-go gates anywhere.
2. No test-case catalogue with expected results.
3. No ownership/RACI model.
4. No source-system contract template.
5. No change-control procedure for models/metrics/rules.
6. No rollback/exception procedures.
7. No UAT/sign-off, cutover/hypercare, monitoring model, training/runbooks.
8. No performance/capacity sizing guidance.

## Gaps vs Success Pack best practice

The protocol has basic prerequisites (`docs/success-packs/success-pack-prerequisites.md`), but nothing in either repo covers:

1. Version-compatibility matrix per release.
2. Dependency activation ordering and failure modes.
3. Storage/capacity estimate before install.
4. Backup snapshot requirement; limited uninstallability warning.
5. Post-install smoke-test checklist.
6. Entitlement verification for the pack.
7. Update/upgrade path (pack updates vs family upgrades).
8. Owner assignment for pack content after install.

> Note: neither repo currently mentions Success Packs at all in a research context — this is a catalog-level blind spot.

---

## Bridging actions

| Action | Owner suggestion |
|---|---|
| Apply page corrections E1–E10 from CURRICULUM_FINDINGS | Curriculum maintainers |
| Add A1–A12 operational sections to the page | Curriculum maintainers |
| Adopt protocol gate checklist for module delivery | Implementation teams |
| Commission HAM research counterpart (page exists, repo does not) | Fleet lead |
| Add Success Pack section to the protocol with the 8 items above | Protocol maintainers |

---

*Comparison only; no external repos modified by this document.*
