# Pre-requisite check — kilo-sam-pro__kilo__sam-module

Model: `kilo-sam-pro`
Base URL: `https://api.openrouter.ai/v1`

| capability | pass | evidence |
|---|---|---|
| Outbound HTTP | YES | HTTP 200 in 0.0s |
| Playwright + Chromium | YES | chromium available |
| JavaScript rendering | YES | js output='after' |
| Web search reachable | YES | servicenow.com results reachable |
| Context window | YES | kilo-sam-pro (api, assumed): 128000 tokens |

## Verdict

**CAN proceed with independent web research.** Browsing tools reachable and context is adequate.

## Backup plan if blocked

- Ask the orchestrator for a pre-fetched evidence digest (another agent's research output).
- Restrict output to structure/planning work that needs no live sources.
- Never fabricate URLs; mark unsourced claims as UNVERIFIED.