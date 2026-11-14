# 02 — CLARIFICATIONS

**Timestamp:** 2026-11-14T07:32:00Z

## What is blocked

| # | Block | Impact | Decision |
|---|---|---|---|
| B1 | No live ServiceNow instance | Cannot verify `sys_id`s, ACLs, BR names, exact column API names | Mark **U**; provide `sys_dictionary` / `sys_db_object` queries |
| B2 | SAM docs are Brazil; IRE docs are Australia | Cross-release claims could be wrong | State the release in the claim; put cross-release risks in the conflict log |
| B3 | No full docs API re-crawl | Reliance on retained official extracts | Every claim marked; disputed claims re-read from the extract text |
| B4 | Private rubric is outside the repo and was not read | QA cannot use the hidden rubric | Score against the public plan; say so |
| B5 | Public guide is a learning asset, not official | Guide claims may conflict | Treat as **C/P**; corrections in `GUIDE_CROSS_REFERENCE.md` |
| B6 | No `finalv2` branch yet | Publish target unknown | Push only `finalv2/**` + the requested root README section; use `main` if allowed, else a branch + PR |

## What has to be solved in another worktree before this one continues

Nothing. The source corpus is local, the guide is fetched, and the repo contract is clear. The only unresolved work is **verification**, which is delegated to subagents in parallel rather than blocking the draft.

## Decisions

1. **Self-contained v2, not a v1 patch.** The user asked for a new folder; v2 explains the chain without requiring v1.
2. **Cross-reference, don't duplicate.** Every deep doc links to the relevant v1 artifact and the guide.
3. **Official wins.** Where v1, the guide, or a secondary source conflicts with a Brazil/Australia official page, the official page wins; the losing claim is recorded.
4. **Practice is labeled.** "One entitlement per contract line", "60–90-day reclaim window", and "5–15% savings" are **P**, not product facts.
5. **Cheat sheet in two places.** The user asked for it at the bottom of `README.MD`; it is also included in `finalv2/README.md` so the folder is self-contained.
6. **Subagents are cross-checkers, not authors.** They read and report; the main pass writes and resolves.
