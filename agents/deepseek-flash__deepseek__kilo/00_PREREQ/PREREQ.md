# PREREQ — capability gate

| Check | Result | Notes |
|---|---|---|
| Can read GitHub repos | **yes** | `eltonaguiar/alt_parallelswarm` and `..._SAM` shallow-cloned to `/tmp/kilo` |
| Can read the existing Brazil corpus | **yes** | `agents/grok-4.6__xai__kilo/SNC_SAM__WT1/research/raw/` (58 pages, ~3.3k lines) + `CONFIG_INVENTORY_AUSTRALIA.md` |
| Can browse ServiceNow docs | **yes** (fleet already did) | Brazil khub map `PMOYmdGTPDs40EbYh10h4g`; Australia corroboration in the reference repo |
| Playwright / JS-rendered SPA | not needed | the khub content API returns `target=DESIGNED_READER` text |
| Context window | sufficient | corpus is small enough to hold the whole SAM page set; Discovery internals deliberately out of scope |
| Live ServiceNow instance | **no** | consequence: internal column names that the docs do not print are marked `U`, never guessed |
| Write access to target repo | **yes** | `gh auth status` = `eltonaguiar` |

**Backup plan if a page is missing:** use the Australia `CONFIG_INVENTORY_AUSTRALIA.md` already in the WT1 folder, then the `ALT_PARALLELSWARM` discovery reference for the CMDB half of any software-write path. Anything still missing is listed in `04_QA/QA.md`.
