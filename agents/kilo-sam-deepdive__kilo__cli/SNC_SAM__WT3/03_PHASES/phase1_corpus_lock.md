# Phase 1 — capability gate + corpus lock

**Started:** 2026-11-13 · **Status:** COMPLETE

## What was done

- Read the reference guide `ALT_PARALLELSWARM/research/servicenow-discovery/DISCOVERY_END_TO_END_GUIDE.md` in full and extracted its section skeleton, evidence policy and property-catalog conventions.
- Locked the SAM corpus: 58 Brazil ITAM raw articles (`agents/grok-4.6__xai__kilo/SNC_SAM__WT1/research/raw/`), beam Australia abstracts (`agents/beam__kilo__cli/SNC_SAM__WT1/research/`), the committed `final/FINAL_SAM_MODULE_REFERENCE.md` (beam) and `final/FINAL_grok-4.6__xai__kilo.md`, and grok WT2 `CURRICULUM_COMPARE.md` (used only as a cross-check target).
- Created isolated branch `docs/sam-module-deep-dive` from `origin/main`.
- Wrote `01_PLAN/PLAN.md`, `00_PREREQ/PREREQ.md`, `02_CLARIFICATIONS/CLARIFY.md`.

## Exit check

- [x] PREREQ PASS
- [x] every source cited later in the guide is present locally and greppable
- [x] no shared fleet file modified

## Notes carried into phase 2

- The corpus names OOB jobs explicitly but does **not** publish business-rule sys_ids, UI policies or ACLs — §2 must mark those UNVERIFIED and provide audit queries instead of inventing names.
- Brazil pages are dated Mar/Sep/Oct/Nov 2026; the guide must pin per-claim dates where they matter.
- Known duplicate spellings to preserve rather than normalize: `samp_normalization_suggestion` vs `samp_normalization_suggestions`; `com.snc.samp.manage.published.product(s)`; `com.snc.samp.ml.overrride_ml_model_version`.
