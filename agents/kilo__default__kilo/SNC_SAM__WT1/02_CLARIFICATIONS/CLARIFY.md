# 02_CLARIFICATIONS — ServiceNow SAM Clarifications & Edge Cases

- **Compiled by:** `kilo` / provider **kilo** / harness **default** (`kilo__default__kilo`)
- **Date:** 2026-11-13
- **Purpose:** Clarify ambiguous, edge-case, or release-specific behaviors in the SAM module that are not covered in the core reference documentation. Mirrors the CLARIFY.md pattern from `ALT_PARALLELSWARM`.

---

## 0. Provenance & method

Sources were fetched from the ServiceNow khub API (Australia maps) on 2026-11-13 and retained as raw text in this agent's `research/` folder. Where two sources disagreed, the discrepancy is flagged rather than silently resolved.

---

## 1. Discovery model primary key matching edge cases

### 1.1 Publisher + Display Name + Version composite key

- The discovery model primary key is **Publisher + Display Name + Version** `[S14]`.
- **Version matching behavior**: exact version first, then rounds down to the major version when an exact match is absent (e.g. `8.0.4` matches `8.0`) `[S14]`.
- **Edge case**: What if Publisher is empty? The platform matches using:
  - Display Name + Version (if Publisher empty), or
  - Display Name only (if both Publisher and Version empty).
- **Edge case**: "Security Update" in install name — discovery models are **never** created when the install name contains `Security Update` `[S14]`.

### 1.2 Partial key matching

- If Publisher is present but Version empty → match on Display Name + Publisher.
- If both Publisher and Version empty → match on Display Name only.
- These partial-key matches are **not** explicitly documented as fallback behavior in all releases; treat as instance-verified.

---

## 2. Business rule insert-vs-update logic

### 2.1 Unnamed business rule on `cmdb_sam_sw_install`

- The business rule that matches/creates discovery models on insert to `cmdb_sam_sw_install` is **not named** in the official docs `[S16][S1]`.
- **Known**: It uses the composite key (Publisher, Display Name, Version) to search `cmdb_sam_sw_discovery_model`.
- **Known**: If a match exists → update the install record; if no match → create a new discovery model row.
- **UNVERIFIED**: Exact sys_id or advanced logic (e.g., edition handling, partial key precedence).

### 2.2 Duplicate detection across discovery sources

- Duplicate Software Installations occur when the same publisher/product/version/edition are discovered through **multiple discovery sources** (e.g. Discovery + SCCM) `[S11]`.
- The business rule does **not** prevent duplicates at insert time; duplicates are resolved later by the dedup job `[S11]`.
- Custom dedup rules can be created in table `sam_sw_dedup_rule` `[S13]`.

---

## 3. Normalization status revert rules

### 3.1 Revert behavior by status

| Current Status | Revert Target | Revert Action |
|---|---|---|
| `Normalized` | `Match Not Found` | `Revert Normalization` sets values back; rules associated with the discovery model are reset to original |
| `Partially Normalized` | `Match Not Found` | Same as above |
| `Publisher Normalized` | `Match Not Found` | Same as above |
| `Manually Normalized` | **Cannot revert** | Status is permanent; pattern-rule-normalized models **cannot** be reverted `[S8]` |
| Pattern-rule-normalized | **Cannot revert** | Same as Manually Normalized |

### 3.2 Manual normalization editing

- Legacy UI: editing only the `Software model` field and the `Approved` check box is permitted `[S5][S5]`.
- New UI: full normalize action only (status changes) `[S5][S5]`.

---

## 4. Reconciliation auto-create properties

### 4.1 `com.snc.samp.automaticsmrcreation`

- Default: **opt-in** (not enabled by default) `[S5]`.
- Effect: Auto software model for **licensable** unlicensed product results during reconciliation `[S5]`.
- **Crawl advisory**: Leave **off** in Crawl so the software-model table stays curated (Office Hours) `[S23]`.
- If enabled, extra software models may appear unexpectedly.

### 4.2 `com.snc.samp.automaticsmcreation`

- Default: **No** `[S5]`.
- Effect: Auto software model for **not licensable** (APM - Asset Performance Management) models.

### 4.3 `com.snc.samp.unlicensed_smr_creation`

- Default: **False** `[S5]`.
- Effect: Software *model results* for unlicensed models.

---

## 5. Content Service opt-in

### 5.1 Default state

- Content Service is **default off** `[S17]`.
- Sharing discovery models with statuses Match not found / Publisher normalized / Partially / Manually / (Normalized with empty version) improves automatic normalization `[S17]`.

### 5.2 Reversibility

- Content-service opt-in is **reversible** `[S17]`.
- Property typo in docs: `com.snc.samp.ml.overrride_ml_model_version` (three r's) `[S17]` — quote both if an instance shows a different spelling.

### 5.3 Data types shared

- Content Service shares: Discovery models, lifecycles, part numbers/discovery maps, processor names, product license exception rules `[S17]`.

---

## 6. Domain separation

### 6.1 Oracle reconciliation domain properties

- Activating `com.glide.domain.msp_extensions.installer` exposes domain-specific SAM application properties `[S4]`.
- Domain-separated properties exist for:
  - `com.snc.samp.oracle.reconlevel` (aggregation level for Oracle/WebLogic on VMware)
  - `com.snc.samp.oracle.hostaffinityenabled` (VM-host affinity rules for Oracle reconciliation on VMware)
- Configuration path per domain: Application Properties → Application Property Values related list.

### 6.2 Domain separation scope

- Not all SAM properties are domain-separated; only those explicitly listed above `[S4]`.
- Per-domain properties use the Application Properties related list after activating the Domain Support - Domain Extensions Installer plugin.

---

## 7. IBM dedup special case

- IBM: ServiceNow Discovery rows stay **Active**; authorized-provider duplicates are inactivated by `SAM - Deduplicate Install Table` `[S11]`.
- This is the only publisher-specific dedup behavior documented; other publishers use the standard dedup job.

---

## 8. SCCM integration deprecation

- Legacy SCCM 2012 v2 / 2016 usage plugins are **deprecated toward Tokyo** `[S1][S16]`.
- Preferred integration: Service Graph connector for Microsoft SCCM `[S1][S16]`.
- If using legacy plugins, ensure the software-usage plugin is also activated if usage data is desired.

---

## 9. VMware license key population

- `samp_vmware_license_key` and `samp_vmware_license_key_usage` are populated by Discovery (Kingston+) `[S1][S78]`.
- These tables are **not** created or managed by SAM plugin activation; they are Discovery artifacts that SAM references.

---

## 10. License metric types

- Full metric enum is **not** duplicated here; see `[S31]` for license metric types (IBM PVU/RVU, Oracle, SAP named user, Citrix, unlimited licenses, etc.) `[S31]`.
- Do not invent metric names; reference the S31 topic for the complete list.

---

## 11. Anti-patterns (quick reference)

- Treating a discovery model as a catalog item, or a catalog item as a license `[S14][S27]`
- Discovering before entitlements if PPN-driven models wanted `[S16][S9]`
- Customizing OOB recon jobs instead of properties / custom metrics
- Enabling `automaticsmrcreation` then wondering why extra software models appeared `[S5]`
- Rolling out all publishers on day one instead of phase-wise `[S22][S21]`
- Skipping Content Service opt-in then drowning in Match Not Found `[S17]`
- New SCCM work on deprecated 2012/2016 usage plugins `[S1]`
- Overlaying the unnamed install→discovery-model business rule `[S16]`
- Publishing to software catalog with `model_manager` vs `catalog_admin` mixed up `[S27][S29]`
- Assuming Workspace activation still leaves classic SAM navigation `[S18]`
- Leaving `automaticsmrcreation` off in Crawl so the software-model table stays curated `[S23]`
- Do not attach both SSO and a direct SaaS integration to the same app

---

## 12. Open questions / UNVERIFIED

1. Exact *name* of the install→discovery-model business rule and any UI policies on `cmdb_sam_sw_install`.
2. Full `glide.cmdb.sam.*` / remaining `samp.*` properties not on the Properties page table `[S4]`.
3. Install update-vs-insert matching *within the same discovery source* (row key beyond display/publisher/version).
4. Discovery-source reliability ranking used by dedup primary selection `[S12]`.
5. Customer Success Center "integrate a discovery source manually" page `[S16]`.
6. Whether `com.snc.samp.ml.overrride_ml_model_version` is a docs typo `[S17]`.
7. Now Create / Success Checklist PDFs (login-gated).
8. HAM vs SAM catalog publish interaction beyond `[S27][S29]`.
9. RHEL threshold property *internal name* `[S4]`.
10. Zurich/Yokohama deltas vs this Brazil pin.

---

## 13. Source ledger

| id | source | release label |
|---|---|---|
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