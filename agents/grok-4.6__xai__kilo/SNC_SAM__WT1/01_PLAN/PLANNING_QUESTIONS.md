# Planning questions — derived from ALT_PARALLELSWARM Discovery pass

The Discovery swarm did **not** start with “list every property.” The private topic map
(`matching_incoming_to_existing`, `conflicting_values`, `which_sources_may_feed`,
`keeping_data_current`, `ci_class_manager_locations`, plus global property probes) forced
every agent to answer **decision questions**. QA then scored four *rule families* plus
breadcrumbs, order of operations, and insert-vs-update.

This file is the SAM analog. Answers go in `05_FINAL/SAM_CONFIG_REFERENCE.md`.
Anything not sourced is UNVERIFIED.

---

## A. Match vs create (Discovery analog: identification)

1. How does ServiceNow decide whether an incoming **software installation** refers to an
   existing `cmdb_sam_sw_install` row vs inserting a new one? Which attributes are the
   match key (display name, publisher, version, installed_on, serial, discovery source)?
2. How is a **discovery model** (`samp_discovered_model`) matched vs created when a new
   install string appears?
3. How is a **software model** (`cmdb_software_product_model` / product+edition+version)
   matched vs created? When does Content Service create it vs a human vs “automatic
   creation of software models”?
4. How is an **entitlement** matched vs created (product + metric + license metric +
   agreement number)? What uniqueness rules exist?
5. When several candidates match, what is the priority / “next entry” loop analog?

## B. Conflicting values (Discovery analog: reconciliation)

6. When SCCM, Discovery, ILMT, Intune, and a SaaS connector disagree on publisher /
   version / last-used / assigned user, which value wins?
7. Where is that authority configured (properties, reconciliation, source precedence,
   “software asset connections”)?
8. What happens when the higher-priority source **stops reporting** (stale install,
   remove-uninstalled, last discovered)?

## C. Which sources may feed SAM (Discovery analog: IRE data source rules)

9. Which upstream systems are permitted to write software installs? How is origin stored
   (`discovery_source`)?
10. Can a source be blocked from **inserting** new installs or models without blocking
    **updates**? (insert-only vs update-only split — this was the #1 Discovery terminology
    trap.)
11. How do you **exclude software assets on CIs** / ignore a publisher / ignore a
    discovery model / deny a product?

## D. Keeping data current (Discovery analog: data refresh / staleness)

12. What scheduled jobs re-normalize, re-reconcile, drop uninstalled software, refresh
    content library?
13. What configuration controls how old an install may be before it is stale / removed?
14. File-signature vs process vs add/remove-programs vs SCCM usage — which clocks apply?

## E. UI breadcrumbs (Discovery analog: CI Class Manager)

15. Exact nav paths in **Software Asset Workspace** vs classic SAM menus for:
    software models, discovery models, entitlements, normalization, reclamation,
    properties, content service, success portal, health check, catalog publish.
16. Which of those are *not* in the workspace (classic-only), like IRE data source rules
    were not in CI Class Manager?

## F. Out-of-box platform objects (Discovery agents flagged query BRs / sensor BRs)

17. What does **Components installed with Software Asset Management Professional** actually
    install? Inventory by type:
    - tables / columns
    - business rules (especially on `cmdb_sam_sw_install`, discovery model, software model)
    - script includes / scheduled jobs
    - flows / subflows / workflow (reclaim, software request, EOL)
    - UI policies / client scripts / ACLs / roles
    - notifications, properties, demo data
18. Which OOB rules must **not** be customized (overwrite-on-upgrade), and which are the
    intended extension points (pattern normalization rules, custom products, reclamation
    rules, suite inference, dedup rules)?

## G. Catalog vs discovered software (operator, 2026-11-13)

These are four *different* paths. Do not collapse them.

19. **Add software to the catalog (service catalog / software catalog)** — steps to
    publish a software model / product as a requestable item (`Link an item to the
    software catalog`, `Publish an item to the software catalog`, `Publish models to
    the hardware or software catalog`). Who can request it? What roles?
20. **Create software in SAM before any discovery** — custom software product + software
    model + entitlement with no install yet. When is this required (contracts signed,
    SaaS, not-yet-deployed)?
21. **Discovered software linked to catalog / SAM model** — install → discovery model →
    normalize (Content Service, pattern rule, or manual) → software model → entitlement
    → license position. What statuses exist (Normalized, Partially Normalized, Match Not
    Found, Manually Normalized, Publisher Normalized, …)?
22. **Blocked / excluded / not-in-catalog** — exclude on CI, ignore discovery model,
    unlicensed-but-not-requestable, restricted publisher, pattern that never creates a
    model, “do not create software model automatically.” How does each block differ?

## H. Types inventory (Discovery listed classifier types, identifier types, recon types)

23. List the **key types** with where they are configured:
    - license metrics (per device, per user, CAL, processor, PVU, SaaS seat, …)
    - normalization statuses
    - entitlement types (perpetual, subscription, maintenance, unlimited, SA)
    - allocation types (user vs device vs license key)
    - discovery sources
    - publisher packs
    - suite vs component vs inferred suite
    - reclamation rule types
    - software model relationship types (parent/child, downgrade, upgrade)
    - install condition / primary vs component installs

## I. Implementation success (operator, 2026-11-13)

24. Foundational data that must exist **before** SAM value appears (CMDB computers with
    owners/location/dept, users, discovery coverage, entitlement source docs, in-scope
    publishers).
25. Baseline metrics to capture before go-live vs after (normalization %, unlicensed,
    reclaimable, true-up, SaaS assigned-vs-used, time-to-reconcile).
26. Phase-wise plan (`Manage phase-wise Software Asset Management implementation`,
    maturity stages, success portal, health check, Guided Experiences).
27. What a successful **any-module** ServiceNow implementation needs (process, data,
    MVP scope, RACI, KPIs, hypercare) — SAM as the worked example.

## J. Properties probe (Discovery global probe)

28. Full **Software Asset Management properties** catalog: name, default, effect, where
    set (`Software Asset Management properties` topic + domain-specific publish property).

---

## Questions we will *not* pretend to answer without an instance

- Exact sys_ids of OOB business rules (docs name them; sys_ids are instance-local).
- Customer-specific reconciliation priority.
- Login-gated Now Create / Success Checklist PDFs.
