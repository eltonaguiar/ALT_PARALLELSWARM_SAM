# CIS-SAM cheat sheet → WT1 sections

**Agent:** `grok-4.6__xai__kilo` · **WT3** · Quiz text from learning `sam-guide.md`. Answers grounded in WT1 + Brazil docs.

## Domain map

| CIS-SAM domain (LG) | WT1 |
|---|---|
| 1 Overview | §1, §20–21 |
| 2 Models / normalization / Content Library | §7–9, §8 |
| 3 Entitlements + recon | §11–12, §15 |
| 4 Reclamation / audit | §13, §10D, publisher packs §6 |
| 5 Workspace / reporting | §5, §18 |

## Quiz → WT1

| # | Question (LG) | Answer (official names) | WT1 |
|---|---|---|---|
| 1 | Software model vs discovery model vs installation | Model = `cmdb_software_product_model` (purchased/canonical). Discovery model = `cmdb_sam_sw_discovery_model` (Publisher+Display Name+Version fingerprint; cannot create manually). Install = `cmdb_sam_sw_install` on a CI. | §1, §7 |
| 2 | Three inputs recon compares | Entitlements (`alm_license`) vs normalized installs vs (for reclaim) usage `samp_sw_usage`. Output is **three tiers**: Product Results → Software Model Results → License Metric Results (`samp_license_metric_result`). Not a single `sam_sw_reconciliation_result`. | §12 |
| 3 | Why metric must match | LMR is per metric; mismatch compares different counting bases. Named User/Device also need allocations. | §11–12, §41 |
| 4 | Unknown ≠ compliant | License Position status is only Compliant / Not Compliant. Unlicensed installs and rights needed are columns, not a green dot. Do not report missing models as compliant. | §12, §35 |
| 5 | Suite membership | `com.snc.sam.auto_suite_inference`; suite parent on reclamation pulls components. Without suite roll-up, components over-count. | §13, properties §17 |
| 6 | Fix under-licensing from wrong qty | Do **not** overwrite the entitlement. Create true-up / additional entitlement. SA/Maintenance must be **linked** to perpetual or they are ignored. | §11, §42 |
| 7 | Reclaim window | DOC: reclamation rules use Total Usage Time or Last Used Date; flow error timeout 30 days. LG 60–90 day inactivity is **practice**, not a property default. | §13, §40 |
| 8 | Publisher traps | IBM pack + ILMT v2 / PVU; Oracle recon aggregation ESX cluster default; SAP named user pack; MS SQL/Windows cost-ratio properties. | §6, §17 |

## Lab (LG) mapped to DOC nav

1. Software model — Workspace License operations / classic Software Models. Need License under management + type Licensable. §9
2. Entitlement qty=1 — `alm_license`, Publish build→in use. §11
3. Installs — `cmdb_sam_sw_install` filtered by discovery model / product. §7
4. Run recon — Workspace overview or License usage → Run Reconciliation (`sam_user` or `sam_admin`). Weekly default. §12
5. Raise qty, re-run — Historical Results keep history. §12, §39
6. Normalize unmatched DMAP — manual normalize when Match Not Found. §8, §10C

## Names the exam curriculum got wrong (do not memorize)

| Curriculum | Official |
|---|---|
| `cmdb_sam_sw_usage` | `samp_sw_usage` |
| `sam_sw_reconciliation_result` | Product / Software Model / License Metric Results (`samp_license_metric_result`) |
| recon default nightly | weekly or on-demand |
| SUMN | Content Library + named normalize jobs |
| `alm_software` (sam-buffy) | do not use |
