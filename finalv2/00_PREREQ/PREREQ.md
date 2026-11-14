# 00 — PREREQ

**Run:** `finalv2` SAM documentation pass
**Timestamp:** 2026-11-14T07:30:00Z
**Agent:** Kilo CLI (`deepseek/deepseek-flash`)
**Question:** Can I browse, run Playwright, and hold the context? If not, ask another agent before writing.

## Capability probe

| Capability | Available? | Evidence |
|---|---|---|
| Web browse / fetch | **Yes** | `webfetch` retrieved the public SAM guide; `tavily` search returned a 432 error, but direct fetch worked |
| Local file read | **Yes** | Read official SAM extracts and the sibling Discovery IRE corpus |
| Playwright | **Yes, but not needed** | No UI under test; the target is a documentation repo |
| Hold context | **Yes** | Source corpus, v1 final docs, guide, and repo contract fit in the working context |
| Live ServiceNow instance | **No** | No instance credentials; all instance-specific claims are marked **U** |
| GitHub write access | **Yes** | `gh auth status` shows `eltonaguiar` with `repo` scope |

## Source access

- Official SAM pages (Brazil): retained khub API extracts under
  `agents/grok-4.6__xai__kilo/SNC_SAM__WT1/research/raw/` and `_meta.json`.
- Official IRE pages (Australia): sibling corpus at
  `/home/eaguiar2015/ALT_PARALLELSWARM/research/servicenow-discovery/sources/`.
- v1 merged docs: `final/` and the per-agent folders in this repo.
- Public guide: `webfetch` + local source under
  `/home/eaguiar2015/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/sam/sam-guide.md`.

## What is blocked

1. **No live instance** → cannot confirm business-rule names, ACLs, `sys_id`s, or exact column API names. Mitigation: mark **U**, provide verification queries.
2. **No full docs re-crawl** → the pass relies on retained official extracts. Mitigation: every non-obvious claim carries a **V/C/U/P** mark; disputed claims are checked against the extract text.
3. **Release mismatch** → SAM is Brazil; IRE is Australia. Mitigation: state the release in each claim and in the conflict log.
4. **No private rubric** → QA scores against the public plan, not the hidden grading rubric.

## Decision

Proceed. The minimum conditions for writing are met: browse, source access, and context. The missing live instance is a documented limitation, not a blocker for a documentary reference.
