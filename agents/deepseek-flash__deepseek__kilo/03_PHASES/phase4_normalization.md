# Phase 4 — normalisation deep dive (done)

- Enumerated **all six** normalisation statuses found in the Brazil docs: `New`, `Match Not Found`, `Publisher Normalized`, `Partially Normalized`, `Normalized`, `Manually Normalized` (the "4" commonly quoted are the four automatic outcomes; `New` and `Manually Normalized` are the extra states).
- Built the transition/revert/suggestion matrix, including the `com.snc.samp.auto_accept_normalization_suggestion` default-true behaviour.
- Documented rule families (Product/Package Map, Pattern, Enhanced Pattern, Wide-net, ML) and the exact precedence/fallback.
- Separated **software model vs publisher vs vendor vs PPN vs discovery model** — the confusion axis the user flagged.
