# Normative decision register

All four decisions below remain **recommended / pending approval**. Their presence in a candidate bundle is not approval.

| Decision | Recommendation under review | Status |
|---|---|---|
| DD-ART-007 | Require an explicit artifact_storage_kind enum distinguishing file and directory artifacts | Pending approval |
| DD-ART-008 | Canonicalize restricted POSIX-style manifest paths with NFC normalization and stable ordering; define and test the FileEntry manifest digest | Pending approval |
| DD-ART-009 | A file without a raw-byte hash remains needs_review; verified alternative identity must not imply byte-level integrity | Pending approval |
| DD-ART-010 | Include alternative_identity_methods in the versioned Task Execution Contract hash payload; changes require a new version/digest | Pending approval |

Before approval, record the decision owner, rationale, alternatives, compatibility impact, migration requirements, normative text changes, and the exact tests that would fail under rejected alternatives.

Full review: schema-v1.4.3.7-four-decisions-review.md. Detailed candidate package evidence: schema/v1.4.3.7/audit/v1.6.6-four-decisions-review.csv.
