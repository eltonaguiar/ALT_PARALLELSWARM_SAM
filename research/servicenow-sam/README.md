# ServiceNow Software Asset Management (SAM) — module deep dive

**Agent:** `kilo-sam-deepdive__kilo__cli` · **Model:** Kilo (inherited) · **Harness:** Kilo CLI
**Date:** 2026-11-13 · **Release pin:** Brazil ITAM map, corroborated by Australia pages where labelled
**Method:** the corpus was fetched through the ServiceNow docs khub content API by the earlier swarm and retained as stripped text; this pass re-read every cited file and transcribed table/field/property names verbatim. No instance was available — behaviour is documented, not executed.

This folder is the SAM analog of `ALT_PARALLELSWARM/research/servicenow-discovery/`: one consolidated guide plus its raw source corpus. The agent's phase artifacts live in `agents/kilo-sam-deepdive__kilo__cli/SNC_SAM__WT3/`.

## Contents

| file | what it is |
|---|---|
| `SAM_MODULE_DEEP_DIVE.md` | the guide: mental model → out-of-box scripts → maintenance (add / normalize a software model) → high-probability items (license position, compliance, reclamation, true-up) → workspaces & dashboards → parameter inventory → insert/update rules → order of operations → verification → anti-patterns → source index → gaps |
| `CURRICULUM_COMPARE.md` | round-2 diff against the CIS-SAM learning curriculum and the community pack (AGREE / CONFLICT / CURRICULUM-ONLY / DOCS-ONLY / CURRICULUM-WRONG) |
| `FINAL_FEEDBACK.md` | round-3 cross-check against the latest findings from other agents plus ranked recommendations |
| `sources/` | raw `.txt` of every cited article (Brazil set + `_australia/` abstracts + implementation-success digest + Australia config inventory) |

## How to verify / reproduce

Every non-obvious claim carries `[S<n>]` → the "Source index" at §12 of the guide, which lists the local file for each source. Property defaults and UI paths are quoted from those files, never from memory; spelling variants are preserved rather than normalized.

## Known bounds

- OOB business-rule sys_ids, UI policies and ACLs are not published by the component article; §2.8 gives an audit recipe instead of guessing.
- Reconciliation script includes were reorganized into `com.sn_itam_samp` for Yokohama — pre-Yokohama customizations must be moved, not copied.
- Community learning packs contain wrong table/role names; official docs win (see the curriculum-compare file in the agent folder).
- Release drift between Brazil/Australia/Yokohama/Xanadu is only partially diffed; version-gated values are flagged inline.
