# Coverage vs SAM / module-plan gaps

**Agent:** `grok-4.6__xai__kilo` · **WT4** · **Date:** 2026-11-13  
**Corpus:** all `*.md` under this repo except other agents’ `research/raw/`.  
**Scoring:** **C** = documented enough to act · **T** = named, not operational · **M** = missing · **W** = present but wrong/unsafe.

Files: **G** = `final/FINAL_grok-4.6__xai__kilo.md` · **B** = `final/FINAL_SAM_MODULE_REFERENCE.md` (beam) · **R** = `final/FINAL_SAM_CONFIG_REFERENCE.md` (sam-research) · **K** = `final/FINAL_CURRICULUM_COMPARISON_AND_SAM_GUIDE_RECOMMENDATIONS.md`

---

## 1. Entitlement-to-consumption chain

| Item | G | B | R | K | Combined | Note |
|---|---|---|---|---|---|---|
| Plugin/roles (`sam_admin`, `sam_user`, …) | C | T | C | T | **C** | G+R list Pro roles; B thinner |
| `cmdb_sam_sw_install` + DMAP BR | C | C | C | T | **C** | Strongest shared coverage |
| Insert vs update / dedup / stale | C | C | C | T | **C** | G: Brazil Exact/Major/Any; retired CI deletes installs |
| Normalization + Content Service | C | C | C | C | **C** | |
| Software models / discovery maps | C | T | C | C | **C** | |
| Entitlement table `alm_license` | C | T | C | C | **C** | B Discovery-centric |
| PPN import / Content Library auto-model | C | M | T | T | **T** | G has PPN match scenarios; **no CSV/MLS column map, no ERP contract** |
| Allocations user vs device | T | T | T | T | **T** | Tables named; 8k allocation article not extracted |
| License metrics (per device/user/core/…) | T | M | C | T | **T** | R stronger; G deferred full catalog to S31 |
| Vendor metric groups / packs | T | T | C | C | **T** | Packs named; no publisher×metric matrix |
| Suite / upgrade / downgrade rights | T | M | C | C | **T** | Tables + weekly job; little suite-roll-up how-to |
| Maintenance ≠ license | C | M | T | C | **C** | G S42 |
| SaaS seats / usage / renewals | T | M | T | C | **T** | Plugin `sn_sam_saas_int`; no connector runbook or health alerts |
| Consumption summaries | M | M | T | T | **M** | |
| Reclamation / removal candidates | C | T | T | C | **C** | |
| License Workbench / three-tier recon | C | C | C | C | **C** | Weekly not nightly |
| IRE for 3rd-party inventory | C | T | T | T | **C** | G: `com.snc.samp.ire.datasource.integration` |
| Intune/Jamf as SAM install sources | T | M | C | T | **T** | G: SGC, not native SAM; R lists Store connectors |
| Catalog publish vs SAM model | C | M | M | M | **T** | **G only** (four paths) |

---

## 2. Setup sequence the user listed

| Gate | Combined | Where | Overlooked? |
|---|---|---|---|
| Confirm SAM Pro/Foundation + roles | C | G §1, R plugins | `procurement_user` / full contract_manager operating model **T** |
| Define data model **before** config | T | G §20 Crawl | No source×field contract spreadsheet |
| Inventory sources populate `cmdb_sam_sw_install` | C | G §6, B, R | |
| Import entitlements before trusting recon | C | G §4A step 6 | Import **format** **M** |
| Model high-value publishers first | C | G published-products + Path to Value | |
| On-demand recon + inspect Workbench | T | G §12, B | No expected-number examples |
| Pilot then scale | C | G Crawl/published products | No go/no-go numeric gates |

---

## 3. CMDB assumptions to challenge

| Control | Combined | Gap |
|---|---|---|
| Success = CI insert/update | **Challenged in G** | G §21: closed loop entitlement↔model↔install↔recon. B still Discovery-finish-line. |
| CI-to-install linkage | C | `installed_on`; exclude-CI flag |
| Duplicate/stale installs | C | Dedup job; uninstalls **not** auto-deleted; 3rd-party DELETE |
| IRE for non-Discovery | C | Property + payload keys |
| Discovery-model governance / approval | T | Manual normalize; **no RACI for Match Not Found queue** |
| Suite/bundle/cross-grade | T | Inference property; not a modeling playbook |

---

## 4. Operational / general module-plan items

| Item | Combined | Verdict |
|---|---|---|
| In-scope vs out-of-scope publishers/geos | T | Published products = product freeze, not geo/legal |
| Baseline KPIs before go-live | T | G lists metrics; 85%/95% is community not SLA |
| Source-system contracts (freq, errors, owners) | **M** | Named sources only |
| Entitlement import format / transform maps | **M** | |
| Process cadence (daily/weekly/monthly/quarterly) | T | Jobs named; no operating calendar with owners |
| Data/process owners | T | Path to Value RACI in G IMPLEMENTATION_SUCCESS |
| Change control for model/metric/rule changes | **M** | |
| Audit evidence PO→contract→entitlement→recon | **M** | `ast_contract` named in R; no evidence pack |
| Concrete test cases (1 entitlement + 2 installs → shortfall 1) | **M** | CIS-SAM lab is qualitative |
| Data-quality acceptance thresholds | T | |
| UAT / performance at volume | **M** | List-count property 5M only |
| Reporting consumption / training / runbooks | T | Success portal, Workspace |
| Cutover from `cmdb_ci_spkg` / hypercare / rollback | T/M | Foundation migrate mentioned; **no hypercare** |
| Dead SaaS connector monitoring | **M** | Curriculum asked; not in product refs |
| Optimization owners (reclaim vs true-up vs buy) | T | Remediation options exist; no business owner map |

---

## 5. Honest combined picture

The repo is **not** still “CMDB-only.” **G + R** already carry entitlements, models, Content Service, recon tiers, packs, reclamation, Crawl/Walk/Run. **B** remains the Discovery-contract specialist. **K** is a curriculum roadmap and **over-credits G** for publisher-trap depth that actually lives in the *learning* sam-guide, not in G’s Brazil fetch.

**Still the structural hole:** purchased-rights operations (import contract, metric matrix, PO audit trail, SaaS runbook, test cases with numbers, change control). Discovery→DMAP→normalize is the mature half.

---

## 6. What a general ServiceNow *module* plan needs that this SAM corpus under-weights

Same pattern as any module (ITSM, HAM, CSM, HRSD):

1. Scope + **numeric** success + baseline **before** plugins.  
2. Dependency map (irreversible Foundation→Pro). **Covered.**  
3. Source-system **field contracts**. **Missing.**  
4. Process + exception queues with names. **Thin.**  
5. Governance / SoD / change control on anything that moves money. **Missing.**  
6. Expected-result tests. **Missing.**  
7. Who consumes which workspace on Monday morning. **Thin.**  
8. Cutover + hypercare + rollback. **Missing.**

SAM-specific extra: the closed loop is the success criterion, not “rows exist.”
