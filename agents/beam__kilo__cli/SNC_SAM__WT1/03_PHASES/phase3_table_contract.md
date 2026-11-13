# Phase 3 — order + table contract

Order documented; table contract from “Discovery with SAM”:
- Software Discovery Model [cmdb_sam_sw_discovery_model]
- Software Model [cmdb_software_product_model]
- Software Installation [cmdb_sam_sw_install]
When SAM plugin inactive, original schema (Software [cmdb_ci_spkg], Software Model
[cmdb_software_product_model]) behaviour remains; when active, Discovery populates
cmdb_sam_sw_install. A business rule on that table matches/creates a discovery model; CI related
lists / reference fields must point at the new table.
Status: complete.
