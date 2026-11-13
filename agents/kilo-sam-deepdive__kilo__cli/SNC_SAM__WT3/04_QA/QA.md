# QA — SNC_SAM__WT3

**Date:** 2026-11-13 · **Result:** PASS (SC1–SC10)

| # | Criterion | Evidence | Result |
|---|---|---|---|
| SC1 | OOB scripts enumerated extensively | §2.2 has J1–J15 with type/trigger/table/fields/customize/risk; §2.3 BR; §2.4 script includes; §2.5 flows; §2.6 plugins; §2.7 matrix; §2.8 audit recipe | PASS |
| SC2 | Add-software-model procedure | §3 prerequisites table, 9-step procedure with table+field per step, related lists, PPN scenarios table, insert/update semantics | PASS |
| SC3 | Normalize procedure | §4 statuses, five rule families, workspace+classic paths, revert rules, suggestions, matching job algorithm, pattern rule fields, reclassification loop table | PASS |
| SC4 | High-probability items | §5 license-position field list + two-report scenarios; three-tier compliance tables; reclamation types/tables; true-up inputs/traps; duplicate hygiene table | PASS |
| SC5 | Workspaces & dashboards | §6 eight named dashboards/reports with source tables and nav paths; classic-only menu list; activity-center alert table; role-per-screen | PASS |
| SC6 | Parameter inventory | §7.2 Tier 0/1/2 must-consider (defaults + effect); §7.3 screens A–O full field/property list; §7.4 prioritization | PASS |
| SC7 | Traceability | every non-obvious claim carries `[S<n>]`; §12 maps all IDs to local files | PASS |
| SC8 | Exact-name fidelity | grep spot-checks against `research/servicenow-sam/sources/`: `com.snc.samp.automaticsmrcreation` (3 files), `cmdb_sam_sw_discovery_model` (7), `cmdb_software_product_model` (3), `samp_license_metric_result` (3), `sam_sw_dedup_rule`, `com.sn_itam_samp`, `samp_vmware_license_key`, `SAM - Deduplicate Install Table`, `SAM – Discovery Model to Software Model matching`, `Edition Override`, `Instance key`, `ISO serial number`, `Omit from suites`, `Automatically matched`, `Created source`, `Stale Record Threshold`, `Discovered publisher is empty` — all present verbatim | PASS |
| SC9 | Honest limitations | §13 lists 15 UNVERIFIED/gap items incl. BR sys_ids, UI policies, ACLs, spelling variants, community-pack errors | PASS |
| SC10 | Structural parity | same folder contract as reference; 14 sections covering moving parts → order of ops → catalog → troubleshooting → runbook → sources → gaps | PASS |

## Findings fixed during QA

- Removed a plugin-id typo (`com.sn_sap_sap` → `com.sn_samp_sap`) before commit.
- Preserved both spellings where docs disagree instead of silently choosing one.
- Marked the RHEL threshold programmatic name UNVERIFIED rather than guessing.

## Residual risk

No live instance; behaviour claims are documentation-derived. Round 2 (curriculum compare) may surface additional curriculum-only topics to absorb without overwriting documented facts.
