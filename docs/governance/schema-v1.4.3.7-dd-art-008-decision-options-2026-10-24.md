# DD-ART-008 — Directory Manifest Contract Decision Options

**Status:** review proposal only; no option is approved by this document.  
**Candidate:** Schema v1.4.3.7; current pre-sync implementation HEAD `9bebbdf279fefba098fa237915ff71361103201a`.  
**Owner decision required:** yes. No Schema semantics or historical hash was changed while preparing this comparison.

## 1. Current facts to preserve

The current helper:

- NFC-normalizes `relative_path`, rejects absolute/traversal/empty segments, and rejects paths that collide after NFC;
- sorts the normalized entry array using Python string ordering;
- serializes the normalized **FileEntry array** with `json.dumps(ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)`;
- computes SHA-256 over those UTF-8 bytes;
- rejects all symlink entries and rejects `allow_symlinks=True`.

The Artifact Schema still permits `entry_type: "symlink"`. The `size_bytes` property has no upper bound. The helper hashes the normalized entries array, not a wrapper object containing a schema version or other manifest metadata. These are contract questions, not failures of the reported tests.

The owner reports that the dedicated provisional golden-vector test passed as part of 8/8 directory-manifest tests on pre-sync HEAD `9bebbdf`. The vector is labelled `provisional_not_normative`; it captures the current implementation, not a final interoperable contract.

## 2. Canonical serialization and numeric domain

| Option | Contract | Advantages | Costs / compatibility impact |
|---|---|---|---|
| **A — RFC 8785 JCS + bounded JSON integers** | Use a tested JCS implementation; constrain numeric `size_bytes` to an agreed safe-integer domain, commonly (0 \le n \le 2^{53}-1) for interoperable IEEE-754 integer values. | Standardized canonical JSON; broad cross-language interoperability. | Adding a maximum changes Schema validation semantics and must be owner-approved. Existing larger values would need explicit handling; do not silently rewrite historical hashes. |
| **B — Python implementation profile** | Keep the current `json.dumps` output and define it as Python-specific. | Lowest immediate code change; matches the current golden vector. | Does not establish RFC 8785 compatibility or guarantee identical output across independent implementations. Not suitable as a cross-language hash contract. |
| **C — Versioned custom arbitrary-precision profile** | Define exact UTF-8 escaping, integer lexical representation, object-key order, array order and null handling independently of JCS. | Can preserve arbitrary-precision integers without a numeric upper bound. | Becomes a project-specific standard; every language needs conformance vectors and the contract must be versioned. It must not be called RFC 8785. |
| **D — Decimal-string size in the hash preimage** | Encode `size_bytes` as a decimal string in the canonical hash payload while retaining a numeric source field, or change the schema field itself to a string. | Preserves exact large integer values. | Hash preimage no longer directly matches the Schema object; a schema-level type change is more disruptive. Requires explicit versioning and owner approval. |

**Review recommendation, not an approval:** Option A is the simplest standard route if a safe-integer maximum is acceptable. Option C is the alternative if arbitrary-precision byte counts must be preserved. Option B should be treated as a local regression profile only, not as cross-language interoperability.

## 3. Normalized path-array ordering

JCS defines object-property ordering; it does **not** choose the order of elements in the manifest array. The array ordering must be separately specified.

| Option | Ordering rule | Example with NFC-normalized paths U+E000 and U+1F600 | Assessment |
|---|---|---|---|
| **A — Unicode scalar-value order / UTF-8 bytewise order** | Compare normalized POSIX path strings by Unicode scalar values, equivalently lexicographically by valid UTF-8 bytes; no locale. | U+E000 sorts before U+1F600. | Recommended for review: locale-independent, portable, and matches Python's current Unicode-code-point ordering for valid strings. |
| **B — UTF-16 code-unit order** | Compare UTF-16 code units, as some language-native string sort functions do. | U+1F600 begins with a surrogate code unit and sorts before U+E000. | Viable only if stated explicitly; differs from the current Python order and the provisional vector. |
| **C — Locale-aware collation** | Use system or user locale. | May vary by runtime and locale. | Reject for a content-hash contract because ordering can vary across machines. |

**Review recommendation, not an approval:** Option A. The normative wording should say that paths are first NFC-normalized and converted to POSIX separators, then sorted by UTF-8 bytewise lexicographic order, with no locale-dependent comparison. Keep the U+E000/U+1F600 vector as a distinguishing test, and add at least one multi-segment path case.

## 4. Symlink policy

| Option | Schema/helper contract | Security and migration implications |
|---|---|---|
| **A — Prohibit symlink entries** | Remove `symlink` from the normative `entry_type` enum and keep the helper fail-closed. Filesystem traversal must not follow symlinks. | Simplest and most conservative. Removing the enum value is a Schema semantic change and requires owner approval plus compatibility review. |
| **B — Represent symlinks as link metadata** | Keep `entry_type: "symlink"`; define `symlink_target` encoding and required fields; hash link metadata without following the link. | Preserves the type but requires precise rules for relative/absolute targets, dangling links, chains, root containment, and platform-specific link semantics. |
| **C — Dereference symlinks** | Follow the link and hash the target file/directory contents. | Not recommended as a default: can escape the source root, create cycles, and introduce time-of-check/time-of-use races unless a filesystem-aware verifier enforces a strict policy. |

**Conservative interim behavior:** continue to reject symlink entries in the helper and do not follow links. Do not remove the Schema enum or implement metadata support until the owner explicitly chooses Option A or B. The present Schema/helper mismatch must remain an open gate, not be hidden.

## 5. Digest preimage scope

The current helper hashes the normalized **entry array**. The design proposal speaks more generally about hashing the normalized manifest JSON. These are not necessarily the same.

Owner decision required:

- **Entries-only digest:** hash only the normalized FileEntry array; schema/bundle version and other envelope fields do not affect the digest.
- **Full-manifest digest:** hash a canonical object that includes the selected envelope fields, such as the manifest profile/version and the entry array.

The contract must list the exact included fields and their order/normalization rules. Do not change the current preimage or recompute historical digests until this choice is approved. If the payload shape changes, assign a new named/versioned profile.

## 6. Minimum conformance tests after the decision

1. Golden canonical UTF-8 bytes and SHA-256 for an ordinary manifest and an NFC-equivalent input.
2. Numeric boundary tests at the chosen maximum and immediately above it; if arbitrary precision is selected, include values above (2^{53}-1).
3. Path-order tests for U+E000 versus U+1F600, composed/decomposed characters, nested POSIX paths, and locale independence.
4. Symlink tests matching the approved policy, including an attempted root escape and a dangling link where applicable.
5. A digest-preimage test proving whether envelope metadata is included or excluded.
6. At least two independent implementations (or a language-independent conformance harness) producing the same approved bytes and digest.

## 7. Current disposition

- This document records alternatives and a review recommendation only.
- DD-ART-008 remains pending explicit owner approval.
- The current golden vector remains `provisional_not_normative`.
- No Schema field, enum, numeric constraint, or historical hash was changed.
- Migration remains staging-only; `commit_allowed=false` remains mandatory.
