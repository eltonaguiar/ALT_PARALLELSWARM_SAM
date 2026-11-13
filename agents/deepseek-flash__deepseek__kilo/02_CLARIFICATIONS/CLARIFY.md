# CLARIFY — open questions / assumptions

Assumptions taken (no user clarification available mid-run):

1. **Module = SAM Professional** (Brazil `com.sn_samp_master_ws`), not Basic/Foundation `com.snc.sams`. Foundation differences are called out where they change a status or a table.
2. **Release = Brazil.** Australia-only facts are marked `C` and never silently mixed.
3. **No live instance.** Internal field names that the product docs do not print are marked `U`. The reference therefore gives the *query* to settle each one:
   `sys_dictionary.list?sysparm_query=name=<table>^elementLIKE<norm>` and `sys_db_object.list?sysparm_query=nameLIKEsamp`.
4. **"Every combination"** is interpreted as every *documented* combination of a critical option, presented as a matrix; undocumented combinations are declared and given a verification query, not invented.
5. **Scope of Discovery** is limited to how it writes SAM tables (`cmdb_sam_sw_install`, FBD files, IRE third-party insert). MID/Shazzam/IRE internals stay in `ALT_PARALLELSWARM`.

Questions that would change the answer if a human replies:

- Is **SaaS License Management** (`sn_sam_saas_int`) in scope? The reference covers its tables and reclamation side-effects but does not enumerate every SaaS connector.
- Is **Software Spend Detection** in scope? Covered as an integration and property, not a full spend workflow.
- Does the target instance use **domain separation**? Domain-specific published-products and Oracle properties are documented in §14; if yes, every property must be re-read per domain.
- Is the **classic UI** still used? Brazil gives it limited support; paths are given for both, workspace first.
