# QA — self-check against the success criteria

## 1. Structural parity with ALT_PARALLELSWARM

| Reference folder | Present here | Pass |
|---|---|---|
| `00_PREREQ/PREREQ.md` | yes | ✅ |
| `01_PLAN/PLAN.md` | yes | ✅ |
| `02_CLARIFICATIONS/CLARIFY.md` | yes | ✅ |
| `03_PHASES/phaseN_*` | 6 heartbeat files | ✅ |
| `04_QA/QA.md` | this file | ✅ |
| `05_FINAL/<REFERENCE>.md` + `FINAL_SUMMARY.md` | `SAM_MODULE_REFERENCE.md`, `ROUND2_GAP_ANALYSIS.md`, `FINAL_SUMMARY.md` | ✅ |
| `06_FILESCOPE/FILESCOPE.md` | yes | ✅ |
| `research/` | index + notes | ✅ |
| `plans/<agent>__WT1/` mirror | yes | ✅ |
| `final/` merged doc | `FINAL_deepseek-flash__deepseek__kilo.md` | ✅ |

## 2. Requested content order

| Requested item | Where | Pass |
|---|---|---|
| Out-of-box scripts, purpose, table/field target, customise vs leave, risk | reference §3 | ✅ |
| Add a new software model — every table/field | reference §10 | ✅ |
| Normalise a software model — rules, matching, reconciliation, reclassification | reference §6, §11 | ✅ |
| High-probability items (position, compliance, reclamation, true-up) | reference §7–§9 | ✅ |
| Named workspaces / dashboards / reports | reference §12 | ✅ |
| Parameter inventory: must-consider first, full list second | reference §14 | ✅ |

## 3. User's pointed questions (round 2)

| Question | Answer location | Short answer |
|---|---|---|
| Reporting covered? | reference §12 + round2 §2 | Yes: 9 named surfaces mapped to source tables, incl. Success portal and Health Check |
| Every combination for each critical item? | reference §5–§8 matrices + round2 §3 | Yes: 10 matrices (status, rule family, dedup, insert/update, rights, licence type, product type, PPN, scope, grouping) |
| Software Model Normalization? | reference §6, §11 | Yes: auto/manual/suggestion/revert/pattern, with tables and jobs |
| Software Model vs Vendor? | reference §2.4, §6.6 | Yes: publisher (`samp_sw_publisher`) → `core_company`; PPN; Vendor Catalog Item; catalog item — four different things |
| 4 normalisation statuses, fields documented? | reference §5.1 | Docs expose **six** values on the **Normalization status** column of `cmdb_sam_sw_discovery_model`; internal column is label-only in docs (`U`) |
| Typical SAM integrations? | reference §13 + round2 §5 | Yes: 14 integration families with plugin ids |
| Anything missed in other agents' notes? | round2 §6 | Yes: 12 items, incl. CMDB success advisor for SAM, CPE suggestions, overlapping usage, domain-separated published products |

## 4. Evidence discipline

- **V** claims: all traceable to `agents/grok-4.6__xai__kilo/SNC_SAM__WT1/research/raw/*.txt` (Brazil) or the reference repo's Australia corpus.
- **U** claims: enumerated in reference Appendix A. No column invented.
- Known conflicts recorded:
  1. reconciliation cadence — Brazil "weekly default + on demand" vs curriculum "nightly";
  2. suggestion table — `samp_normalization_suggestion` (singular, topic) vs `samp_normalization_suggestions` (dashboard topic);
  3. Foundation status roster — only `Manually Normalized` + `New` (Australia) vs Pro's six;
  4. `com.snc.samp.ml.overrride_ml_model_version` — triple-r spelling as printed in docs.

## 5. Known gaps (honest)

- No live instance → business-rule names/sys_ids, UI policies, ACLs, and label-only columns remain `U`.
- SaaS connector-by-connector detail and Spend Detection workflow are referenced, not exhaustively enumerated.
- Publisher licence-metric enum is summarised; full metric list is 100+ values and is delegated to the `software_license_metrics` topic (documented in §14 pointers) rather than risk transcription error.
- Zurich/Yokohama deltas not diffed.

## 6. Result

All success criteria in `01_PLAN/PLAN.md` §5 met at the documentary level. Remaining `U` items are instance-verification tasks, listed so the next run can close them.
