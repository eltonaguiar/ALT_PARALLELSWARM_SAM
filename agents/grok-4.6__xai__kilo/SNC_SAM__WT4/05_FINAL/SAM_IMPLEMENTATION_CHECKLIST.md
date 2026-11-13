# SAM implementation checklist (gates)

**Agent:** `grok-4.6__xai__kilo` · Use as go/no-go. Config how-to lives in `final/FINAL_grok-4.6__xai__kilo.md`.

## A. Prerequisites
- [ ] Family pin recorded (Brazil vs Yokohama vs Zurich)
- [ ] Foundation `com.snc.sams` vs Pro `com.sn_samp_master_ws` / `com.snc.samp` decided (upgrade to Pro **irreversible**)
- [ ] SaaS LM `sn_sam_saas_int`, Spend, publisher packs listed in/out of scope
- [ ] Roles: `sam_admin`, `sam_user`, `sam_integrator`, `model_manager`, `contract_manager` (procurement as needed)
- [ ] Content Service opt-in decision (default **off**)
- [ ] `automaticsmrcreation` **off** for Crawl

## B. Data model & sources (before configuration binge)
- [ ] Inventory source(s): Discovery and/or SGC SCCM / Intune / Jamf — confirm they write `cmdb_sam_sw_install`
- [ ] Non-Discovery feeds use IRE (`com.snc.samp.ire.datasource.integration`) not raw inserts
- [ ] Entitlement source: PPN/MLS/CSV/ERP — **column map documented** (still a repo gap)
- [ ] Contract/PO system → `ast_contract` / entitlement link
- [ ] User + device identity good enough for per-user / per-device metrics
- [ ] SaaS portals in/out; assigned-seat vs sign-in
- [ ] Exclude-CI strategy (`com.snc.samp.exclude_device_flag`)

## C. Software-model / metric strategy
- [ ] Priority publishers (80% spend list)
- [ ] Content Library / PPN first; custom product only if not in library
- [ ] Metric group per product (not default Common if a pack exists)
- [ ] Suite / downgrade / SA-linked-to-perpetual rules
- [ ] Published-products freeze (`com.snc.samp.manage.published.products`) for pilot

## D. Process & ownership
- [ ] Owner: Match Not Found queue
- [ ] Owner: entitlement import errors / PPN collisions
- [ ] Owner: reclamation (IT vs manager vs procurement)
- [ ] Owner: metric/model **change control** (changes compliance $)
- [ ] Cadence: daily normalize, weekly recon, monthly Success Goals, quarterly true-up

## E. Validation (write expected numbers)
- [ ] 1 per-device entitlement + 2 active installs → shortfall **1**
- [ ] Named-user metric without allocations → allocations needed > 0
- [ ] Maintenance-only entitlement → **does not** cover installs until linked to perpetual
- [ ] Two sources same IBM install → one Active after dedup
- [ ] Retired CI → installs gone; excluded CI → installs omitted after adjust job
- [ ] Catalog publish creates requestable item **without** changing recon

## F. SaaS
- [ ] Connector list, API owner, refresh cadence, **dead-connector alert**
- [ ] Do not run SSO + direct integration on the same app
- [ ] Reclaim window (practice 60–90 days) vs property `sam_reclamation_flow_error_timeout` (30)

## G. Pilot → prod
- [ ] Baseline: DMAP count by norm status, unlicensed product results, CI owner %
- [ ] Pilot publishers only; recon treated as data-quality loop not invoice
- [ ] Go/no-go: Workbench numbers match a sampled contract **and** sampled devices
- [ ] Hypercare: job filter `Name starts with SAM`; known-issue list
- [ ] Rollback: how to deactivate a bad software model / wrong metric without editing history
