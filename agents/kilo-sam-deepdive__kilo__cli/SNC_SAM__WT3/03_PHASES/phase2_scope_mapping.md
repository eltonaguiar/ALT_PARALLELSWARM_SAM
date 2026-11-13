# Phase 2 — scope mapping: OOB component inventory

**Started:** 2026-11-13 · **Status:** COMPLETE

## What was done

- Enumerated every shipped executable object named anywhere in the corpus and classified by type: scheduled jobs (J1–J15), documented business rule, reconciliation script includes, flows/workflows, plugin payloads.
- Established the audit recipe for objects the docs never enumerate (BR sys_ids, UI policies, client scripts, ACLs) instead of inventing names.
- Confirmed the "Name starts with SAM" filter as the only vendor-sanctioned discovery mechanism for scheduled jobs `[S1]`.

## Exit check

- [x] Every job named in `[S8]`–`[S45]` appears in §2.2 or §2.5
- [x] Customize-vs-leave guidance present per component
- [x] No invented sys_ids

## Notes carried into phase 3

- The corpus splits cleanly into six themes; extraction can proceed top-down in the user's requested order.
- Reconciliation script include customization is the single highest-severity upgrade risk surfaced.
