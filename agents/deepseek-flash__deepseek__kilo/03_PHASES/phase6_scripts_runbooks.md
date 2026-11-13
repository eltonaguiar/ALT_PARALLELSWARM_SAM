# Phase 6 — OOB scripts + maintenance runbooks (done)

- Enumerated the OOB **scheduled jobs** with target table/field and customise-vs-leave verdict (normalise, model-matching, dedup, exclude-CI adjust, daily job, health scan, spend label, downgrade creation, CDS status, weekly reconciliation).
- Enumerated the documented **business rules / flows / UI actions / script includes**; unnamed objects are marked `U` rather than invented.
- Wrote the **add-a-software-model** runbook (two entry paths) listing every table and field, including `core_company` → `samp_sw_publisher` → `cmdb_software_product_model` → `alm_license` → `alm_entitlement_user|asset`.
- Wrote the **normalise-a-software-model** runbook: auto → manual → suggestion → revert → pattern rule → model matching → reconciliation eligibility → product-type reclassification.
