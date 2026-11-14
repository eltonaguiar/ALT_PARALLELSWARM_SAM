# Phase 3 — CMDB/IRE layer

**Started:** 2026-11-14T07:38:00Z
**Completed:** 2026-11-14T07:42:00Z

## Output

`05_FINAL/02_CMDB_IRE_GOVERNANCE.md`:

- four rule families and their insert/update applicability;
- identify-first processing order;
- identification details (keys, criterion attributes, inclusion, duplicates, partial payloads);
- static vs dynamic reconciliation, precedence, child override, nulls, filters;
- data refresh staleness;
- IRE data source insert gate;
- the SAM boundary;
- configuration paths, properties, verification queries, failure modes.

## Checks

- [x] Truth table matches the official pages.
- [x] Reconciliation is marked update-only.
- [x] IRE data source rule is marked insert-only.
- [x] Data refresh is marked update-only.
- [x] Dynamic IRE caveat included.
- [x] The diagram's ordering is reconciled with engine behavior.

## Open

- Exact data-refresh definition table name: **U**.

## Next

Phase 4 — SAM pipeline.
