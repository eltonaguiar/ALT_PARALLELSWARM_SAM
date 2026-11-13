# research/ — source index for this agent

This pass reused the Brazil corpus already fetched by `grok-4.6__xai__kilo` rather than re-fetching, to avoid duplicate work and rate-limit contention in the shared harness.

- **Primary corpus:** `agents/grok-4.6__xai__kilo/SNC_SAM__WT1/research/raw/` — 58 Brazil ITAM pages (~3.3k lines), map `PMOYmdGTPDs40EbYh10h4g`.
- **Australia corroboration:** `agents/grok-4.6__xai__kilo/SNC_SAM__WT1/research/CONFIG_INVENTORY_AUSTRALIA.md`.
- **Discovery boundary:** `alt_parallelswarm/research/servicenow-discovery/DISCOVERY_END_TO_END_GUIDE.md` + `final/FINALdeepseek-flash.MD` (FBD tables, software properties, IRE).
- **Curriculum:** `grok-4.6__xai__kilo` WT2 `CURRICULUM_COMPARE.md`; WT3 `CIS_SAM_CHEATSHEET.md`; learning guide at `ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/sam/sam-guide.md`.

No new HTTP fetches were made in this pass. Every `V` claim maps to a file in the corpus; every `U` is listed in `SAM_MODULE_REFERENCE.md` Appendix A with the `sys_dictionary`/`sys_db_object` query needed to settle it.
