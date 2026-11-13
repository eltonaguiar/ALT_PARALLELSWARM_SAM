# CLARIFY — SNC_SAM__WT3

Questions raised and answered inline; none block the work.

| # | question | answer |
|---|---|---|
| 1 | Deliver one consolidated guide or only per-screen parameter tables? | Both, layered: six operational themes first (scripts, maintenance, high-probability items, workspaces, parameters), with the full per-screen parameter list inside §7 — mirroring how the CMDB guide leads with mechanisms and then catalogs properties. |
| 2 | Overwrite the existing grok WT1 / beam SAM references? | No. They stay as corpus. This worktree adds an independent deep dive under its own folder; `research/servicenow-sam/` is new. |
| 3 | Which release pin? | Brazil ITAM map (pages updated Sep/Oct/Nov 2026) primary, matching the largest fetched corpus; Australia abstract set used as corroboration and labeled when it differs (e.g., Foundation plugin, VMware license-key tables). |
| 4 | Push to main or a branch? | Dedicated branch `docs/sam-module-deep-dive`; no shared fleet files touched; other agents' uncommitted work is not included. |
| 5 | What does "OOB scripts" include when ServiceNow does not publish BR sys_ids? | Everything the docs name as shipped executable logic: scheduled jobs (`Name starts with SAM`), the documented install→discovery-model business rule, reconciliation script includes, flows/workflows, health-check KPI jobs, content-download jobs, and the migration script — plus an audit recipe for the unpublished objects (BRs, UI policies, ACLs). |
