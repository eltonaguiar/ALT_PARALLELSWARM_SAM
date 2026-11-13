# Phase 3 — table/field contract + insert/update (done)

- Fixed the five record types and their keys: install (`cmdb_sam_sw_install`) → discovery model (`cmdb_sam_sw_discovery_model`, key Publisher + Display name + Version) → software model (`cmdb_software_product_model`) → entitlement (`alm_license`) → optional catalog item.
- Recorded all label-only columns as `U` with the `sys_dictionary` query to resolve them.
- Built the insert/update matrices for install, discovery model, software model, entitlement, allocation, catalog item.
- Established the software-boundary facts from the reference repo: FBD writes `cmdb_file_information` / `samp_file_name` / `samp_custom_file_name` / `cmdb_unidentified_file_set` / `cmdb_swid_tag`; third-party insert uses IRE REST + `com.snc.samp.ire.datasource.integration`.
