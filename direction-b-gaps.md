# Direction B — Guide-Covered but Not in ALT_PARALLELSWARM_SAM Repo

**Date:** 2026-11-13T15:47:53Z  
**Identifier:** kilo-kilo-ollama-checks-v2  
**Repo:** `alt_parallelswarm_SAM` (eltonaguiar/ALT_PARALLELSWARM_SAM)  
**Cross-reference:** vs. TSOM SAM guide at `https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/sam/sam-guide/`

---

## Gaps on the SAM Guide Page Not Documented in This Repo's Final Docs

### 1. Lab Steps 1–7 (Runnable Sub-Prod Activation Instructions)
- Step 6 ("Prove normalization matters") and Step 7 ("Teach back") now partially reflected in this repo; still no runnable sub-prod activation instructions beyond navigate paths.
- Missing: exact search filter on `sys_index_search_all` for discovery-model status-counts.

### 2. Reusable Code Blocks [Knowledge Base Material]
- Business Rule: "Flag an installation with no normalized software model" (`before` BR).
- Scheduled Job: "Expire entitlements past their end date" (basic `gr` get-list + setValue).
- Script Include: per-publisher compliance summary.
- Client Script: require a metric when creating an entitlement.
- OOB report definitions (Top unlicensed products, unused installations, contested entitlements, recent removals).

### 3. Mnemonics / Exam-Weight Mapping
- Exam-weight table (~15/25/30/20/10) + traps.
- Memory aids: Three-Record Types table, IRE before reconciliation flip "Unknown ≠ compliant."

### 4. Quiz Items
- 14 CIS-SAM style questions split by domain; the SAM guide page has a dedicated section.

### 5. Migration/Cutover Specifics for `alm_software`/`cmdb_ci_spkg`
- Guide mentions deprecation timeline; this repo mentions migration in one line only.

### 6. Processor-Pack Matrix with Version Specifics
- Version of Oracle LMS scripts, ILMT versions, and other publisher-specific version details.

### 7. CIS-SAM Curriculum vs DOC Open Questions Cross-Reference
- Which questions overlap, which are unique to each source. Both sides confess instance-dependent items.

### 8. All UNVERIFIED Items Consolidated into One Place
- Both the repo final docs and the SAM guide page confess instance-dependent items; a consolidated list would be helpful for maintainers.

### 9. CIS-SAM Quiz Items Mapped to WT1 Section Numbers
- Exam/interview prep material; useful for training new admins but not included in this repo's final analysis.

### 10. Ask-a-Ranger Video List (Community Resource Links)
- Not in repo scope, but a useful adjunct to the SAM guide for video-based learning.

### 11. Success Portal Widgets / Maturity Model
- Completed goals, actual vs projected savings, health checks passed, value-builder tasks, Crawl/Walk/Run maturity items.

---

## Recommended Addition to ALT_PARALLELSWARM_SAM

Create `final/FINAL_SAM_LAB_RUNBOOK.md` containing:
- Runnable sub-prod activation steps with exact search filters
- All reusable code blocks (Business Rule, Scheduled Job, Script Include, Client Script, OOB reports)
- Mnemonics, exam-weight mapping, and CIS-SAM quiz
- Cross-reference of open questions between repo and guide
- Directory: `final/` (already exists in this repo)

---

**Bottom line:** The ALT_PARALLELSWARM_SAM repo provides excellent configuration/Discovery-reference documentation for an existing SAM instance (CMDB contract, normalization, reconciliation, anti-patterns). The SAM guide page adds the learner-facing layer: lab steps, mnemonics, quiz items, reusable code snippets, and migration guidance that are essential for onboarding and exam prep but were not the focus of this repo's analysis.

*Documented for parity with the bidirectional coverage gap analysis (see `FINAL_CROSS_REFERENCE_COVERAGE_ANALYSIS.md` Direction B section).*