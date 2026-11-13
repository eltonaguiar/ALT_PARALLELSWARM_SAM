# Phase 9 — round 4: compile findings vs live curriculum

**Started:** 2026-11-13 · **Status:** COMPLETE

## What was done

- Fetched the live published CIS-SAM page and diffed it against the repository file: **identical (1,074 lines)**, so verdicts apply to the live site.
- Compiled `CURRICULUM_FINDINGS.md`: section-by-section verdicts for all 27 live sections, a consolidated 10-item error register, keep-list, CIS-SAM domain map, actionable edits for the curriculum maintainers, and fleet corroboration.
- Cross-linked from `CURRICULUM_COMPARE.md`.

## Key findings

- Curriculum errors confirmed at double strength (DD + grok WT3 independently): wrong usage table (`samp_sw_usage`), wrong recon-result table (`samp_reconciliation_result`), nightly-vs-weekly cadence, SUMN branding, plugin tip, breadcrumbs.
- Live page unchanged since 2026-11-12; no newer revision to compare against.

## Exit check

- [x] Live target fetched and verified identical
- [x] Findings doc committed with citations
- [x] No changes made to external repos
