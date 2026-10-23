#!/usr/bin/env python3
"""Restricted FileEntry manifest canonicalization profile proposed for approval.
This is intentionally limited to the FileEntry schema (ASCII keys, strings, ints/null);
it is NOT a general-purpose RFC 8785 implementation.
"""
import hashlib, json, unicodedata, re
from pathlib import PurePosixPath

class ManifestError(ValueError): pass

def normalize_relative_path(path):
    if not isinstance(path,str) or not path:
        raise ManifestError("relative_path must be a non-empty string")
    if "\\" in path:
        raise ManifestError("backslash is forbidden; use POSIX '/' separators")
    normalized=unicodedata.normalize("NFC",path)
    if normalized.startswith("/") or re.match(r"^[A-Za-z]:",normalized):
        raise ManifestError("absolute paths are forbidden")
    parts=normalized.split("/")
    if any(part in ("",".","..") for part in parts):
        raise ManifestError("empty, '.' and '..' path segments are forbidden")
    return normalized

def normalize_manifest(entries, allow_symlinks=False):
    if not isinstance(entries,list):
        raise ManifestError("manifest must be an array")
    out=[]; seen=set()
    for e in entries:
        if not isinstance(e,dict):
            raise ManifestError("each FileEntry must be an object")
        required={"relative_path","entry_type","size_bytes","content_sha256","symlink_target"}
        if not required.issubset(e):
            raise ManifestError("FileEntry missing required keys")
        p=normalize_relative_path(e["relative_path"])
        if p in seen:
            raise ManifestError("duplicate path after NFC normalization: "+p)
        seen.add(p)
        typ=e["entry_type"]
        if typ not in ("file","directory","symlink"):
            raise ManifestError("invalid entry_type")
        if typ=="symlink":
            raise ManifestError("symlinks are not supported by this manifest-only helper; a filesystem-aware verifier must resolve and prove the target remains inside the root")
        size=e["size_bytes"]; digest=e["content_sha256"]; target=e["symlink_target"]
        if typ=="file":
            if not isinstance(size,int) or isinstance(size,bool) or size<0: raise ManifestError("file size_bytes must be non-negative integer")
            if not isinstance(digest,str) or not re.fullmatch(r"[a-f0-9]{64}",digest): raise ManifestError("file content_sha256 must be lowercase SHA-256")
            if target is not None: raise ManifestError("file symlink_target must be null")
        elif typ=="directory":
            if size is not None or digest is not None or target is not None: raise ManifestError("directory size/hash/symlink target must be null")
        else:
            raise ManifestError("symlinks are not supported by this manifest-only helper")
        out.append({"relative_path":p,"entry_type":typ,"size_bytes":size,"content_sha256":digest,"symlink_target":target})
    out.sort(key=lambda x:x["relative_path"])
    return out

def canonical_manifest_bytes(entries, allow_symlinks=False):
    normalized=normalize_manifest(entries,allow_symlinks)
    # RFC 8785-compatible for this restricted schema: fixed ASCII object keys, no floats,
    # integer sizes only, no NaN/Infinity, Unicode emitted as UTF-8. General JCS needs a full implementation.
    return json.dumps(normalized,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode("utf-8")

def directory_manifest_sha256(entries, allow_symlinks=False):
    return hashlib.sha256(canonical_manifest_bytes(entries,allow_symlinks)).hexdigest()
