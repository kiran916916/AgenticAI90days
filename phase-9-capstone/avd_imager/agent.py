"""Atlas Imager — the orchestrator agent (Phase 9 capstone).

Plans and (dry-run) drives the full AVD image pipeline, wiring the course toolkit:
  • shared.policy   — deny-by-default scoped Azure actions + audit trail + HITL
  • shared.reliability — resilient polling of the long-running build
  • shared.tracing  — one span per Azure operation

Run the demo (no Azure, no API key needed):
    python phase-9-capstone/avd_imager/agent.py
"""
from __future__ import annotations

import json
import pathlib
import sys

# ── bootstrap: make `shared` and the `avd_imager` package importable ──
_HERE = pathlib.Path(__file__).resolve()
for _p in _HERE.parents:
    if (_p / "shared" / "llm.py").exists():
        sys.path.insert(0, str(_p))            # repo root → import shared.*
        break
sys.path.insert(0, str(_HERE.parent.parent))   # phase-9-capstone → import avd_imager.*

from avd_imager import templates, tools, reviewer            # noqa: E402
from avd_imager.spec import ImageSpec, validate_spec         # noqa: E402
from shared.policy import PolicyGate, PolicyDenied           # noqa: E402
from shared.reliability import resilient                     # noqa: E402
from shared.tracing import Tracer                            # noqa: E402

DEFAULT_SPEC = _HERE.parent.parent / "specs" / "win11-avd-multisession.json"

PLAN = [
    "create_resource_group", "create_managed_identity", "create_gallery",
    "create_image_definition", "create_image_template", "run_image_build",
    "monitor_build", "scan_image_apps", "publish_version", "update_host_pool",
]

# The agent identity's granted scopes (least privilege — note: no '*').
GRANTED = {"infra:write", "identity:write", "gallery:write", "imagebuilder:write",
           "imagebuilder:run", "imagebuilder:read", "security:scan", "hostpool:write"}


# A monitor that survives a transient ARM throttle — shows the reliability toolkit.
_mon_attempts = {"n": 0}


@resilient(attempts=4, time_budget=30.0)
def _monitor(spec):
    _mon_attempts["n"] += 1
    if _mon_attempts["n"] < 2:
        raise ConnectionError("ARM 429 throttling (transient) — retrying")
    return tools.monitor_build(spec)


def _adr(spec) -> str:
    return (
        f"# ADR — AVD golden image '{spec.name}'\n"
        f"**Context:** standardize session hosts for host pool '{spec.host_pool['name']}'.\n"
        f"**Decision:** build a Gen2 TrustedLaunchSupported image via Azure VM Image "
        f"Builder; customizers: {', '.join(spec.customizers)}; distribute to Compute "
        f"Gallery '{spec.gallery['name']}' (regions {spec.gallery.get('replicationRegions', [])}).\n"
        f"**Consequences:** reproducible, versioned images; AIB managed identity holds "
        f"least-privilege distribute rights; host-pool rollout is staged behind human approval."
    )


def _print_scan(report) -> bool:
    """Print the app-validation + CVE report; return True if it PASSES the gate."""
    print("   application baseline:")
    for a in report["apps"]:
        mark = "✓" if a["ok"] else "✗"
        print(f"     {mark} {a['name']:36} {a['status']}")
    print("   CVE findings:")
    if not report["cves"]:
        print("     (none)")
    for c in report["cves"]:
        print(f"     [{c['severity']:8}] {c['id']:24} {c['product']} {c['version']} "
              f"→ fix ≥ {c['fixedVersion']}")
    verdict = report["verdict"]
    detail = "; ".join(report["reasons"]) or "compliant"
    print(f"   verdict: {verdict}  (block ≥ {report['threshold']}) — {detail}")
    return verdict == "PASS"


def _print_review(v) -> bool:
    """Print the second-agent security review; return True if it APPROVES."""
    print(f"   🧑‍⚖️  {v['reviewer']}: {v['decision']}")
    for b in v.get("blockers", []):
        print(f"     ✗ blocker:  {b}")
    for a in v.get("advisories", []):
        print(f"     • advisory: {a}")
    return v.get("decision") == "APPROVE"


def run(spec_path=DEFAULT_SPEC, approver=lambda tool, args: False):
    spec = ImageSpec.from_file(spec_path)

    print(f"=== Atlas Imager · DRY-RUN · '{spec.name}' ===\n")
    problems = validate_spec(spec)
    if problems:
        print("❌ spec invalid:")
        for p in problems:
            print("   -", p)
        return
    print("✅ spec valid\n")

    print("--- generated image template (truncated) ---")
    template = templates.build_image_template(spec)
    print(json.dumps(template, indent=2)[:900] + "\n   ...\n")

    print("--- az command plan ---")
    for cmd in templates.az_command_plan(spec):
        print("   $", cmd)
    print()

    gate = PolicyGate(tool_scopes=tools.TOOL_SCOPES, granted=GRANTED,
                      high_blast=tools.HIGH_BLAST, approver=approver)
    tracer = Tracer()

    print("--- executing plan (dry-run, policy-gated) ---")
    for step in PLAN:
        try:
            gate.authorize(step, spec.name)
        except PolicyDenied as exc:
            print(f"⛔ {step}: {exc}")
            if step in tools.HIGH_BLAST:
                print("   → high-blast change needs human approval; STOPPING here.\n")
                break
            continue
        fn = _monitor if step == "monitor_build" else getattr(tools, step)
        with tracer.span(step):
            cmd, result = fn(spec)
        if step == "scan_image_apps":
            print(f"✓ {step}:")
            if not _print_scan(result):
                print("🛑 SECURITY GATE FAILED — refusing to publish a vulnerable / "
                      "non-compliant image. Remediate, rebuild, and re-scan.\n")
                break
            # Two-key rule: a second, independent agent must also sign off.
            decision = reviewer.run_review(spec, template, result)
            approved = _print_review(decision)
            gate.audit.record("security_review",
                              "approved" if approved else "rejected",
                              f"two-key {decision['reviewer']}", spec.name)
            if not approved:
                print("🛑 SECURITY REVIEW REJECTED — second agent withheld sign-off. "
                      "Publish blocked.\n")
                break
        else:
            print(f"✓ {step:22} → {result}")

    print("\n--- audit trail ---")
    gate.audit.dump()
    print("\n--- trace (span per operation) ---")
    tracer.print_trace()
    print("\n--- governance: ADR ---")
    print(_adr(spec))


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SPEC
    run(target)
