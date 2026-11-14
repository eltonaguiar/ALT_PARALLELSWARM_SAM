# Phase 4 — SAM pipeline

**Started:** 2026-11-14T07:42:00Z
**Completed:** 2026-11-14T07:46:00Z

## Output

- `05_FINAL/03_DISCOVERY_TO_SAM_PIPELINE.md`
- `05_FINAL/04_NORMALIZATION_AND_DEDUP.md`
- `05_FINAL/05_ENTITLEMENTS_METRICS_RECONCILIATION.md`

Covered:

- sources and preferred connectors;
- install → discovery-model business rule;
- primary key correction (Publisher + Display Name + Version);
- six normalization statuses, manual/revert rules, rule families, jobs;
- dedup levels and primary selection;
- discovery model → software model matching and version rounding;
- entitlements, PPN resolution, license types;
- metric groups;
- three reconciliation tiers and rights algebra;
- License Position report, reporting map, health check.

## Checks

- [x] Every table named in the claims exists in an official extract.
- [x] The six statuses are verified.
- [x] The dedup levels are verified.
- [x] The three tiers are verified.
- [x] `samp_sw_usage` is used instead of `cmdb_sam_sw_usage`.
- [x] Practice claims are marked **P**.

## Open

- Exact column API names: **U**.
- Publisher-specific rules: **U**.

## Next

Phase 5 — configuration and operations.
