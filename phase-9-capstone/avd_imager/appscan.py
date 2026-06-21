"""Application validation + CVE scan for the built AVD image (pre-publish gate).

WHAT IT CHECKS
  1) **Application baseline** — required apps present at safe versions (e.g. Microsoft
     Teams, Microsoft 365 Apps / Office, FSLogix), org line-of-business tools
     (e.g. HancePro — an *example*), and a forbidden/blocklist.
  2) **CVEs** — installed software mapped to known vulnerabilities; Critical/High
     findings (configurable) block publishing.

DRY-RUN vs PRODUCTION
  Here we SIMULATE the image's software inventory and use a small OFFLINE,
  ILLUSTRATIVE CVE knowledge base (SAMPLE ids — *not authoritative*). In production,
  source the real data from:
    • Microsoft Defender Vulnerability Management — software inventory + weaknesses
      (CVEs) + security recommendations (via Defender for Endpoint/Servers / Defender
      for Cloud), onboarding AVD session hosts.
    • or run `Get-Package` / `winget list` on the image with `az vm run-command`,
      then map versions to CVEs via NVD (nvd.nist.gov) or OSV (osv.dev).
"""
from __future__ import annotations

SEVERITY_ORDER = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}

# Default baseline (override per spec via spec.app_baseline).
DEFAULT_BASELINE = {
    "required": [
        {"name": "Microsoft 365 Apps", "exe": "winword.exe", "min_version": "16.0.17000.0"},
        {"name": "Microsoft Teams", "exe": "ms-teams.exe", "min_version": "24000.0.0"},
        {"name": "FSLogix", "exe": "frx.exe", "min_version": "2.9.8000.0"},
    ],
    "org_tools": [],
    "forbidden": ["uTorrent", "Microsoft Teams (classic)"],
}

# ILLUSTRATIVE offline CVE KB — product -> [{below: fixedVersion, id, severity, title}].
# Replace with Defender Vulnerability Management / NVD / OSV. SAMPLE ids only.
CVE_DB = {
    "OpenSSL": [{"below": "3.0.14", "id": "CVE-2024-OSSL-SAMPLE", "severity": "High",
                 "title": "Illustrative OpenSSL flaw"}],
    "7-Zip": [{"below": "24.07", "id": "CVE-2024-7ZIP-SAMPLE", "severity": "Medium",
               "title": "Illustrative 7-Zip flaw"}],
    "HancePro": [{"below": "3.2.0", "id": "CVE-2024-ORGTOOL-SAMPLE", "severity": "High",
                  "title": "Illustrative org line-of-business tool flaw"}],
}


def _ver(v):
    out = []
    for p in str(v).replace("-", ".").split("."):
        out.append(int(p) if p.isdigit() else 0)
    return tuple(out)


def _lt(a, b):
    return _ver(a) < _ver(b)


def simulate_inventory(spec):
    """Stand-in for the real image software inventory (Defender TVM / Get-Package)."""
    baseline = spec.app_baseline or DEFAULT_BASELINE
    inv = [
        {"name": "Microsoft 365 Apps", "exe": "winword.exe", "version": "16.0.17328.20162"},
        {"name": "Microsoft Teams", "exe": "ms-teams.exe", "version": "24166.1414.2986.3000"},
        {"name": "Microsoft Edge", "exe": "msedge.exe", "version": "126.0.2592.81"},
        {"name": "Microsoft Visual C++ 2015-2022 Redistributable",
         "exe": "vcruntime140.dll", "version": "14.40.33810"},
        {"name": "OpenSSL", "exe": "openssl.exe", "version": "3.0.14"},   # patched
        {"name": "7-Zip", "exe": "7z.exe", "version": "23.01"},          # -> sample Medium
    ]
    if "InstallFSLogix" in spec.customizers:
        inv.append({"name": "FSLogix", "exe": "frx.exe", "version": "2.9.8884.27471"})
    # Org line-of-business tools (the version the image *has*, per the spec for this demo).
    for app in baseline.get("org_tools", []):
        inv.append({"name": app["name"], "exe": app.get("exe", ""),
                    "version": app.get("installed_version", "0")})
    return inv


def validate_apps(inventory, baseline):
    by_name = {i["name"]: i for i in inventory}
    results = []
    for want in baseline.get("required", []) + baseline.get("org_tools", []):
        name, minv = want["name"], want.get("min_version", "0")
        found = by_name.get(name)
        if not found:
            results.append({"name": name, "ok": False, "status": "MISSING (required)"})
        elif _lt(found["version"], minv):
            results.append({"name": name, "ok": False,
                            "status": f"OUTDATED {found['version']} < min {minv}"})
        else:
            results.append({"name": name, "ok": True, "status": f"present {found['version']}"})
    for i in inventory:
        if i["name"] in baseline.get("forbidden", []):
            results.append({"name": i["name"], "ok": False, "status": "FORBIDDEN app present"})
    return results


def scan_cves(inventory):
    findings = []
    for item in inventory:
        for entry in CVE_DB.get(item["name"], []):
            if _lt(item["version"], entry["below"]):
                findings.append({"product": item["name"], "version": item["version"],
                                 "id": entry["id"], "severity": entry["severity"],
                                 "fixedVersion": entry["below"], "title": entry["title"]})
    return findings


def gate_verdict(apps, cves, block_on_severity="High"):
    reasons = []
    for a in apps:
        if not a["ok"]:
            reasons.append(f"{a['name']}: {a['status']}")
    thr = SEVERITY_ORDER.get(block_on_severity, 3)
    for c in cves:
        if SEVERITY_ORDER.get(c["severity"], 0) >= thr:
            reasons.append(f"{c['severity']} {c['id']} in {c['product']}")
    return ("PASS" if not reasons else "FAIL"), reasons


def scan_report(spec):
    baseline = spec.app_baseline or DEFAULT_BASELINE
    inventory = simulate_inventory(spec)
    apps = validate_apps(inventory, baseline)
    cves = scan_cves(inventory)
    if "ApplyWindowsUpdates" not in spec.customizers:
        cves.append({"product": "Windows 11 (OS)", "version": "unpatched",
                     "id": "CVE-OS-MISSING-UPDATES", "severity": "High",
                     "fixedVersion": "latest cumulative update",
                     "title": "Image not patched (ApplyWindowsUpdates customizer missing)"})
    threshold = (spec.security or {}).get("block_on_severity", "High")
    verdict, reasons = gate_verdict(apps, cves, threshold)
    return {"inventory": inventory, "apps": apps, "cves": cves,
            "verdict": verdict, "reasons": reasons, "threshold": threshold}
