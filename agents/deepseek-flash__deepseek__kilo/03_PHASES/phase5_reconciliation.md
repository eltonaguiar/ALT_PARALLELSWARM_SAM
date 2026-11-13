# Phase 5 — reconciliation / position / true-up / reclamation (done)

- Rights algebra fixed to the three reconciliation tiers: Product Results → Software Model Results → License Metric Results (`samp_product_result`, `samp_license_metric_result`).
- Mapped every rights bucket (allocated-in-use, not-allocated-in-use, allocated-not-in-use, not-allocated, allocations-needed, non-transferable) to its remediation option and field.
- Documented licence-type impact (Perpetual, +SA, +Maintenance, Subscription, Upgrade, Step-up, Subscription Step-up, Add-on, From SA, Enterprise agreements) and the "maintenance ≠ licence" reconciliation rule.
- True-up cost sources: software-model licence/plus-maintenance cost, else average entitlement cost; override licence cost zeroed on metric creation; Oracle Employee 1-year.
- Reclamation: `samp_sw_usage`, rule types, `samp_sw_reclamation_candidate`, removal candidates, timeout property, CSD uninstall-only licence, SaaS/SSO auto-rule.
