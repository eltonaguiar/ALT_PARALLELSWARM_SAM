# PLAN — SNC_SAM_RESEARCH (SAM module)

## Goal
Produce an exhaustive reference for the ServiceNow **Software Asset Management (SAM)** module's
configuration surface, with emphasis on how SAM changes the CMDB/Discovery contract: which
tables are created by the plugin, how Discovery writes them, insert-vs-update and
duplicate behaviour, normalization (auto + manual), compliance reconciliation, and the
config options that prevent dupes or incorrect license positions.

## Output format
Final deliverable: `SAM_MODULE_REFERENCE.md` (markdown, headings + matrices + property tables),
mirroring the CMDB/Discovery reference shape from ALT_PARALLELSWARM.

## Phases
1. Source collection — fetch official SAM docs (Australia release) via khub API; retain raw excerpts.
2. Scope mapping — roles, plugins, entry points, tables.
3. Order of operations — plugin activation → discovery sources → Software Discovery Models
   → software installations → normalization → reconciliation → compliance.
4. Insert vs update / duplicates — primary key on discovery models, duplicate install behaviour.
5. Configuration options — properties, pattern customization, related-list config, domain-separation.
6. QA — success-criteria check + gap log.
7. Final — merged reference + summary.

## Risks
- SAM-specific property catalogs are thin in the official docs (many are surfaced only in-instance
  under `Application Properties`); documented facts will be preferred over invented ones,
  and gaps listed in §"Known gaps".

## Success criteria
- [ ] References primary source(s) for every factual claim about tables, plugin, insert/update.
- [ ] Includes the SAM-specific table contract (`cmdb_sam_sw_install`, `cmdb_sam_sw_discovery_model`,
      `cmdb_software_product_model`, `samp_vmware_license_key*`).
- [ ] Explains the Discovery→SAM business rule and the create-vs-update behaviour.
- [ ] Covers normalization modes, statuses, and scheduled jobs.
- [ ] Covers reconciliation/compliance cadence and outputs.
- [ ] Covers duplicate-prevention and de-duplication (uninstalled software removal).
- [ ] Lists known gaps honestly.
