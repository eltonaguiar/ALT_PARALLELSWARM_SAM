# FINAL SUMMARY — SNC_SAM__WT3 SAM module deep dive

**Deliverable:** `research/servicenow-sam/SAM_MODULE_DEEP_DIVE.md` (identical copy in this folder)

## What was produced

A 1,048-line, exact-name ServiceNow SAM reference organized around the six components every org hits, in the requested order:

1. **Out-of-box scripts** — 15 scheduled jobs, the documented install→discovery-model business rule, reconciliation script includes (Yokohama `com.sn_itam_samp` move), flows/workflows, plugin payloads; each with purpose, table/field target, customize-vs-leave guidance and risk; plus an audit recipe for unpublished objects.
2. **Add a new software model** — 9-step procedure touching `cmdb_software_product_model`, `samp_sw_publisher`/`samp_sw_product`, lifecycle/downgrade/client-access related lists, `alm_license` PPN resolution scenarios.
3. **Normalize a software model** — statuses, five rule families (Product/Package Map, Pattern, Enhanced Pattern, Wide-net, ML), manual/revert rules, `samp_normalization_suggestion`, matching job algorithm and manual lock, custom-product consolidation, reconciliation + reclassification steps.
4. **High-probability items** — License Position report fields; three-tier compliance results and remediation options; reclamation rules/candidates/flows; true-up cost inputs and publisher traps; duplicate/stale hygiene tables.
5. **Key workspaces & dashboards** — eight workspace views, classic-only menus, eight named dashboards/reports with source tables, activity-center alerts, roles per screen.
6. **Parameter inventory** — Tier 0/1/2 must-consider properties prioritized above the full per-screen parameter list (screens A–O).

Supporting sections cover Discovery feed and CI/license insert-update rules, setup/runtime order of operations, verification/health, anti-patterns, troubleshooting, go-live runbook, source index and gaps.

## Verification performed

- Every cited source file mirrored to `research/servicenow-sam/sources/` (61 files).
- Exact-name grep spot-checks passed (see `04_QA/QA.md`).
- Plan phases 1–6 executed in order; QA signed off SC1–SC10.

## Blockers / caveats

- No entitled SAM instance — nothing executed; verify procedures in sub-production first.
- Business-rule sys_ids, UI policies and ACLs are not published; §2.8 provides an audit recipe.
- Community learning packs contain incorrect tables/roles; do not merge them as fact (see round-2 curriculum compare).

## Round 2

`CURRICULUM_COMPARE.md` (also at `research/servicenow-sam/CURRICULUM_COMPARE.md`) diffs this guide against the CIS-SAM curriculum guide and the sam-buffy community pack, marking AGREE / CONFLICT / CURRICULUM-ONLY / DOCS-ONLY / CURRICULUM-WRONG. Headline: reconciliation default is **weekly** (curriculum says nightly), result table is **`samp_reconciliation_result`** (curriculum says `sam_sw_reconciliation_result`), and the community pack is rejected outright. No documented fact was overwritten by curriculum material.
