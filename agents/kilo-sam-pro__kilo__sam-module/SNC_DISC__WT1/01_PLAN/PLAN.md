# Plan — SAM_RESEARCH

**Agent:** `kilo-sam-pro__kilo__sam-module`
**Model / provider:** `kilo-sam-pro` / `kilo`
**Worktree:** `/home/eaguiar2015/wt-kilo-sam-pro__kilo__sam-module` → folder `agents/kilo-sam-pro__kilo__sam-module/SNC_DISC__WT1`

## Goal

Produce as thorough a technical reference as possible on **ServiceNow Software Asset Management (SAM) Module configuration**:
configuration options and properties, order of operations, the key bread crumbs under **CI Class Manager**,
and the configuration that prevents **duplicate CIs** and governs **insert vs update** of CMDB records
as they apply to SAM.

## Output format

`05_FINAL/SAM_CONFIG_REFERENCE.md` — markdown, headed sections, every factual claim carrying a source URL
or marked `UNVERIFIED`. Plus `04_QA/QA.md` self-scoring and `05_FINAL/FINAL_SUMMARY.md`.

## Phases

1. **Capability gate** — can I browse? playwright? is my context enough? → `00_PREREQ/PREREQ.md`
2. **Research** — 3 targeted passes (config/order, CI Class Manager, duplicates/insert-update) via the shared harness
3. **Synthesis** — write the reference from evidence only
4. **QA** — coverage + citation check
5. **Final summary** — goal met? blockers? clarifications?

## Risks

- Official `docs.servicenow.com` is bot-walled for headless browsers → prefer `support.servicenow.com` KB and community.
- Search engines throttle (DDG/Bing) → harness falls back to a real-browser Startpage/Brave query.
- Free/local models lose tool discipline → answer must be built from the evidence digest, not memory.
- Context window: digests are truncated to 4–5k chars per call to stay inside it.

## Success criteria

- Covers ≥5 of: configuration_options, order_of_operations, ci_class_manager, duplicates, insert_vs_update, identification, reconciliation, mid_server
- Every non-trivial claim has a URL, or is explicitly UNVERIFIED
- Names the CI Class Manager locations it claims
- States blockers honestly instead of inventing content

## Capability verdict

CAN browse and research independently.