#!/usr/bin/env python3
"""Validate the release update-manifest.json and write meta.env for the Pages workflow."""
import json
import sys

manifest = json.load(open(sys.argv[1], encoding="utf-8"))
version = manifest.get("version_name") or ""
code = int(manifest.get("version_code") or 0)
sha = manifest.get("sha256") or ""
assert version and code > 0, manifest
assert len(sha) == 64, manifest
lines = {
    "VERSION": version,
    "VERSION_CODE": code,
    "SHA256": sha,
    "SIGNER_SHA256": manifest.get("signer_sha256") or "",
    "SOURCE_COMMIT": manifest.get("source_commit") or "",
    "PUBLISHED_AT": manifest.get("published_at") or "",
    "APK_URL": manifest.get("apk_url") or "",
}
with open(sys.argv[2], "w", encoding="utf-8") as handle:
    for key, value in lines.items():
        handle.write("%s=%s\n" % (key, value))
print(version, code, sha)
