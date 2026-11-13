# FINAL_SUMMARY.md — ServiceNow SAM Module Final Summary

- **Compiled by:** `kilo` / provider **kilo** / harness **default** (`kilo__default__kilo`)
- **Date:** 2026-11-13
- **Purpose:** Final synthesis of the entire SAM module documentation effort, mirroring the `FINAL_SUMMARY.md` pattern from `ALT_PARALLELSWARM` (`final/FINAL_SUMMARY.md`).

---

## 0. Provenance & method

This final summary compiles and synthesizes all documentation produced across the 7 phases of the SAM module research:
- `00_PREREQ/PREREQ.md` — Platform and role pre-conditions
- `01_PLAN/PLAN.md` — 5-phase implementation plan (Crawl → Walk → Run)
- `02_CLARIFICATIONS/CLARIFY.md` — Edge cases, anti-patterns, open questions
- `03_PHASES/` — Phase-by-phase heartbeat markers (5 phase files)
- `04_QA/QA.md` — Self-check validations per phase
- `05_FINAL/SAM_CONFIG_REFERENCE.md` — Exhaustive configuration reference
- `06_FILESCOPE/FILESCOPE.md` — File inventory and scope boundaries

All sources fetched from the ServiceNow khub API (Australia maps) on 2026-11-13. Where two sources disagreed, the discrepancy is flagged rather than silently resolved.

---

## 1. Documentation coverage map

### 1.1 Phase coverage

| Phase | File | Key focus |
|---|---|---|
| **Phase 1** | `00_PREREQ/PREREQ.md` | CMDB health, entitlement source of truth, publisher scope, exclude-SAM devices, baseline metrics |
| | `01_PLAN/PLAN.md` | Phase-gate transitions (Crawl→Walk→Run), activation sequence, scope freeze |
| | `02_CLARIFICATIONS/CLARIFY.md` | Discovery model key matching, business rule logic, normalization revert rules, dedup edge cases |
| | `03_PHASES/phase1_started.md` | CMDB identity validation, metric capture, gate exit criteria |
| | `03_PHASES/phase2_corpus.md` | SAM activation, CI related-list, discovery sources, entitlement loading |
| | `03_PHASES/phase3_research_done.md` | Daily normalization, weekly reconciliation, dedup job, reclamation rules |
| | `03_PHASES/phase4_synthesis.md` | Discovery Status QA, CMDB Health KPIs, anti-pattern checklist, stabilization |
| | `04_QA/QA.md` | Per-phase self-checks; overall end-to-end validation; go/no-go decision |

### 1.2 Configuration coverage

| Topic | Reference section | Depth |
|---|---|---|
| Plugin activation | `§1` | Full OOB plugin list + optional plugins |
| Tables created | `§2` | 5 SAM tables + 2 legacy exclusions + Discovery artifacts |
| Order of operations | `§3` | 9-step sequence from activation through hygiene |
| Insert-vs-update | `§4` | Business rule logic; duplicate scenarios; no IRE-style IDs |
| CI display config | `§5` | Related-list setup; `cmdb_ci_spkg` → `cmdb_sam_sw_install` migration |
| Discovery models | `§6` | Storage; manual normalize; suggestions; ML normalization |
| Normalization | `§7` | Process; benefits; scheduling; 5 statuses; content-service rules |
| Duplicates/stale | `§8` | Double-write; REST API delete; approval rules |
| Reconciliation | `§9` | Weekly/on-demand; 3-tier results; Oracle summary |
| Config options | `§10` | Roles; plugins; CI forms; SCCM; properties; domain sep; content svc; jobs; knobs |
| Key tables | `§11` | 8 tables with notes |
| Known gaps | `§12` | 14 documented gaps + 10 UNVERIFIED open questions |

### 1.3 High-probability items coverage

| Concern | Tables/Fields | Documentation depth |
|---|---|---|
| License position | `samp_oracle_options`, reconciliation 3-tier outputs | Full §9 coverage |
| Compliance | Reconciliation results; License Workbench; License Position report | §9.2 + §9.3 |
| Reclamation | `cmdb_sam_sw_install` REST delete; `sam_reclamation_flow_error_timeout` = 30d | §8.2 + §10.8 |
| True-up | Unlicensed product-result count; License Metric Results | §9.2 tier 2+3 |
| Software model normalization | `cmdb_sam_sw_discovery_model`; 5 statuses; content-service rules | §6 + §7 |
| Discovery→SAM insert-vs-update | Business rule on `cmdb_sam_sw_install`; Publisher+Display+Version key | §4.1+4.2 |
| CI display | `Software Installations` related-list; `cmdb_ci_spkg` → `cmdb_sam_sw_install` | §5 + §8.2 |

---

## 2. Parameter inventory

### 2.1 Must-consider items (priority high)

| Parameter | Table/Field | Why it matters |
|---|---|---|
| `com.snc.samp.manage.published.products` | Application Property | Phase-wise scope freeze; enables Published products UX |
| `com.snc.samp.recon.group` | Application Property | Weekly recon grouping (country, department, company, region, cost center) |
| `com.snc.samp.recon.subgroup` | Application Property | Secondary grouping for reconciliation |
| `com.snc.samp.recon.enablecustommetrics` | Application Property | Apply custom metrics (default Yes) |
| `com.snc.samp.debug` | Application Property | Recon + on-prem import debug (default No) |
| `com.snc.samp.automaticsmrcreation` | Application Property | Auto SM for licensable unlicensed (opt-in; default off) |
| `com.snc.samp.unlicensed_smr_creation` | Application Property | SMR rows for unlicensed (default False) |
| `com.snc.samp.automaticsmcreation` | Application Property | Auto SM for not-licensable (default No) |
| `com.snc.samp.exclude_device_flag` | Application Property | Hardware boolean column name (empty by default) |
| `sam_reclamation_flow_error_timeout` | System Property | Reclamation flow cancel timeout (default 30 days) |
| `com.snc.samp.wide_net_normalization.enabled` | System Property | Wide-net fallback (default enabled) |
| `com.snc.samp.enable.ml_normalization` | System Property | ML fallback (default enabled) |
| `com.snc.samp.oracle.reconlevel` | System Property | Oracle pack aggregation level (default ESX cluster) |
| `com.snc.samp.oracle.hostaffinityenabled` | System Property | Oracle pack VM-host affinity (opt-in) |
| `sn_samp_ibm_lic.default_region` | System Property | IBM pack default region (North America and South America) |
| `sn_samp_ibm_lic.ilmt_api_version` | System Property | ILMT/BigFix API version (picker) |
| `com.snc.samp.sqlserver.standard_sa.to.enterprise_sa.cost.ratio` | System Property | SQL pack cost ratio (default 0.25) |
| `com.snc.samp.ms.sa.to.nonsa.cost.ratio` | System Property | SQL SA pack cost ratio (default 1.25) |
| `com.snc.samp.use_lifecycle_approximation` | System Property | Lifecycle report (default enabled) |
| `com.snc.samp.generate.calculated.lifecycles` | System Property | Calculated EOS/EOES/EOL (opt-in) |
| `sn_samp_ibm_lic.default_region` | System Property | IBM default region |
| `sn_samp_workspace.sam_license_operations_list_count` | System Property | List count cap (default 5000000) |
| `com.snc.samp.citrix.app.license.period` | System Property | Citrix pack (default 90) |
| `com.snc.samp.eng.app.peak.usage.period` | System Property | Engineering pack (default 30) |
| `com.snc.samp.sam_ci_billing_threshold` | System Property | Cloud Insights billing age (default 30) |
| `com.snc.samp.windowserver.license.threshold` | System Property | Windows Server pack (default 4.59) |

### 2.2 Full per-screen parameter list (priority lower, for completeness)

| Screen | Parameter | Category |
|---|---|---|
| Discovery Schedules form | Discover (CI / IP addresses / Networks / Service / Serverless / Cloud application / Cloud resources / Certificates) | Schedule type |
| | MID Server selection method (Auto-Select / Specific MID Cluster / Specific MID Server / Use Behavior) | MID selection |
| | Behavior (preconfigured) | Multi-credential/protocol handling |
| | Location | CI location assignment |
| | Max run time | Hard stop duration |
| | Max Idle time | Stalled run cancellation (hidden column) |
| | Log state changes | Bool per-state logging |
| | Shazzam batch size | IP batch size (min 256, default 1000) |
| | Shazzam cluster support | Distribute across cluster MIDs |
| | Use SNMP Version | ALL / v1 / v2c / v3 |
| | Active | Schedule active/inactive |
| CI Class Manager → Identifiers | Identifier entries (Regular / Lookup / Hybrid) | Insert-vs-match decision |
| | Entry priorities | Source precedence |
| | Related entries | Create/update on other tables (not used for ID) |
| CI Class Manager → Reconciliation Rules | Static reconciliation rules | Source precedence per attribute |
| | Data Refresh Rules | Per-source staleness/Effective Duration |
| | Dynamic reconciliation rules | CMDB 360 attribute-value win |
| IRE Data Source Rule | Applies to class | Block insert, allow update |
| | Data source | Specific source to block/allow |
| | Insert Not Allowed | Per-source/class pair |
| Software Asset Administration > Properties | All `com.snc.samp.*` / `samp.*` properties | Per-publisher/per-feature tuning |
| Software Asset Workspace | License operations > Custom software products | Custom product creation |
| | License operations > Dedup rules | Custom dedup rules |
| | SAM Implementation > Published products | Phase-wise published product list |
| | Success portal | Goals, health checks, savings, value-builder tasks |
| Application Properties | `glide.cmdb.sam.*` / remaining `samp.*` | Not published in full numeric catalog |
| Content Service Setup | Data-type toggles (Discovery models, lifecycles, PPNs, product license exception rules) | Opt-in toggles |
| | Exclude-from-content-service flags | Per-product exclusion |

---

## 3. Folder structure verification

```
SNC_SAM__WT1/
├── 00_PREREQ/
│   └── PREREQ.md
├── 01_PLAN/
│   └── PLAN.md
├── 02_CLARIFICATIONS/
│   └── CLARIFY.md
├── 03_PHASES/
│   ├── phase1_started.md
│   ├── phase2_corpus.md
│   ├── phase3_research_done.md
│   └── phase4_synthesis.md
├── 04_QA/
│   └── QA.md
├── 05_FINAL/
│   ├── SAM_CONFIG_REFERENCE.md
│   └── FINAL_SUMMARY.md
└── 06_FILESCOPE/
    └── FILESCOPE.md
```

---

## 4. Known gaps & UNVERIFIED questions (summary)

### 12 documented gaps:
1. Property catalog depth — no full numeric catalog of every SAM Application Property
2. Pattern inventory — OOTB Discovery patterns not exhaustively listed
3. ML algorithmic detail — not covered (plugin effect only)
4. Migration/version differences beyond Yokohama/Kingston — not diffed
5. Classic UI limited support — classic steps included but workspace is primary
6. KB articles not opened — Now Support restricted access
7. Discovery reference sibling — see ALT_PARALLELSWARM for CMDB/IRE/reconciliation
8. Discovery model primary key matching algorithm edge cases — exact vs. major-version rounding
9. Content Service sharing opt-in implications — not exhaustively detailed
10. System property naming inconsistency — `glide.identification_engine.skip_duplicates` vs `glide.identificationengine.skipduplicates`
11. Edition override field BR logic — not fully documented
12. Content Service data fields — full field inventory on `cmdb_sam_sw_discovery_model` not published

### 10 UNVERIFIED open questions:
1. Exact name of install→discovery-model business rule + UI policies on `cmdb_sam_sw_install`
2. Full `glide.cmdb.sam.*` / remaining `samp.*` properties not on Properties page
3. Install update-vs-insert matching within same discovery source (row key beyond display/publisher/version)
4. Discovery-source reliability ranking used by dedup primary selection
5. Customer Success Center "integrate a discovery source manually" page
6. Whether `com.snc.samp.ml.overrride_ml_model_version` is a docs typo (three r's)
7. Now Create / Success Checklist PDFs (login-gated)
8. HAM vs SAM catalog publish interaction beyond `[S27][S29]`
9. RHEL threshold property internal name
10. Zurich/Yokohama deltas vs this Brazil pin

---

## 5. Source ledger (complete)

| id | source | release label | local file |
|---|---|---|---|
| S1 | `s5fH~A1sUUyDzngPzlKmoA` Components installed with SAM Professional | `research/raw/components_installed_sam_pro.txt` |
| S4 | `wlowLFRyzTKG~aYlKoWGrQ` SAM properties | `research/raw/sam_properties.txt` |
| S5 | `YdVZA9~1YsBKai3GydfjJA` Automatic creation of software models | `research/raw/automatic_creation_of_software_models.txt` |
| S7 | `R~CU_~6K11G9N63vdhdQWg` Exclude software assets on CIs | `research/raw/exclude_software_assets_on_cis.txt` |
| S8 | `GAqHdgqn0gug8rl5B76dyg` Software normalization | `research/raw/software_normalization.txt` |
| S9 | `zi3EfIdp~5LlvSHt7BRxKw` Software models and entitlements | `research/raw/software_models_and_entitlements.txt` |
| S10 | `yUYtBYnrAlpWRL9jsnCm~g` Add custom software products in workspace | `research/raw/add_custom_software_products_workspace.txt` |
| S11 | `zFgm8oWPo81mqLn7665rlA` Duplicate software installations | `research/raw/duplicate_software_installations.txt` |
| S12 | `g2vJ_yZvxLks~NfUSm6NCw` Software install deduplication | `research/raw/software_install_deduplication.txt` |
| S13 | `dZMVh50f2PI16cqrLVlo9A` Create a custom deduplication rule | `research/raw/create_custom_dedup_rule.txt` |
| S14 | `dQyVDoW8zEmzF_zQvv_7dg` Discovery models and software installations | `research/raw/discovery_models_and_installs.txt` |
| S15 | `G_ROnN2e7dWK~A768krQWQ` Software reclamation rules | `research/raw/software_reclamation_rules.txt` |
| S16 | `14CNM8vUS0aV7EE9TGFLeQ` Software discovery | `research/raw/software_discovery.txt` |
| S17 | `WwxD09ptVyD8cbEzLYjEmg` SAM Content Service | `research/raw/sam_content_service.txt` |
| S18 | `z5dNeUywZUMF8aknX1Rl3g` Exploring SAM | `research/raw/exploring_sam.txt` |
| S19 | `DRViqEpnohcgiWnVqbYzYQ` Configuring SAM | `research/raw/configuring_sam.txt` |
| S20 | `U70gtq8ZRqZT3ELF2Ty8xA` SAM installation methods | `research/raw/sam_installation_methods.txt` |
| S21 | `5i6qYMLaESV6cbIeDDKSVQ` Maturity stages | `research/raw/maturity_stages_sam.txt` |
| S23 | `5Zth~lyu8PmPCG7eB5RPbg` Success portal | `research/raw/success_portal.txt` |
| S30 | `ABprxDQ~V1MOP2hP0odeMQ` Software installation fields | `research/raw/software_installation_fields.txt` |
| S31 | `hA25DFvIh8F2QUGYaqk0Gw` Software license metrics | `research/raw/software_license_metrics.txt` |
| S32 | `mHTmD2kNfjmeq6ksQCUSOQ` Allocation management | `research/raw/allocation_management.txt` |
| S33 | `OYewkvjy6lR2jJcPmLZN0g` Catalog request to reclaim | `research/raw/catalog_request_to_reclaim.txt` |
| S34 | `qVOtwtGQrYVLxP4inhYWXA` Software request workflow | `research/raw/software_request_workflow.txt` |
| S35 | `NkFF6uEfaBVCY2EASAorGA` License compliance position | `research/raw/license_compliance_position.txt` |
| S36 | `vvheubQ7n2nV1Nh15QIilA` True-up cost | `research/raw/true_up_cost.txt` |
| S37 | Path to Value / Quick Start / Office Hours / Starter Kit / Measuring Outcomes (ServiceNow employee Community) | `research/IMPLEMENTATION_SUCCESS.md` |

Topic index: `research/topics_brazil_itam_sam.json` (299 titles).