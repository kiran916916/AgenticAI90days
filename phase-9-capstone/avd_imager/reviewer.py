"""Security reviewer — a SECOND agent that must sign off before publish (two-key rule).

Realizes the multi-agent **critic/verifier** pattern: independent of the automated
scan, a reviewer agent judges the whole release (scan report + image template +
identity posture) against a security rubric and returns APPROVE / REJECT. Publishing
requires BOTH the scan gate AND this reviewer (defense in depth / two-person rule).

Backends (set env `REVIEWER`):
  rules    (default) deterministic rubric — runs offline, no provider needed
  llm      provider-flexible LLM reviewer via shared.llm (needs a provider)
  autogen  a real AutoGen `AssistantAgent` reviewer (needs autogen-agentchat + provider)

Any backend error falls back to the deterministic rubric, so the gate never silently opens.
"""
from __future__ import annotations

import os

CRITICAL = {"Critical", "High"}


def review(spec, template, scan_report):
    """Deterministic rubric. Returns {reviewer, decision, blockers, advisories}."""
    blockers, advisories = [], []
    if [c for c in scan_report["cves"] if c["severity"] in CRITICAL]:
        blockers.append("Critical/High CVE present")
    if [a for a in scan_report["apps"] if not a["ok"]]:
        blockers.append("application baseline failure")
    if spec.source.get("securityType") != "TrustedLaunchSupported":
        blockers.append("source is not TrustedLaunchSupported")
    ident = template.get("identity", {})
    if ident.get("type") != "UserAssigned" or not ident.get("userAssignedIdentities"):
        blockers.append("template must use a user-assigned managed identity")
    if "ApplyWindowsUpdates" not in spec.customizers:
        blockers.append("ApplyWindowsUpdates customizer missing")

    for c in template["properties"]["customize"]:
        uri = c.get("scriptUri", "")
        if uri and not uri.startswith("https://"):
            advisories.append(f"non-HTTPS script URI ({c.get('name', '?')})")
        if "/master/" in uri or "/main/" in uri:
            advisories.append(f"unpinned script ref ({c.get('name', '?')}) — pin to a commit")
    if len(template["properties"]["distribute"][0].get("replicationRegions", [])) < 2:
        advisories.append("single replication region (no cross-region DR)")

    return {"reviewer": "security-reviewer (rules)",
            "decision": "REJECT" if blockers else "APPROVE",
            "blockers": blockers, "advisories": advisories}


_SYSTEM = (
    "You are a strict Azure Virtual Desktop image SECURITY REVIEWER. Independently "
    "decide whether to PUBLISH. Reply with ONLY JSON: "
    '{"decision":"APPROVE|REJECT","blockers":[...],"advisories":[...]}. '
    "REJECT on any High/Critical CVE, any missing/forbidden app, a source that is not "
    "TrustedLaunchSupported, or a non-managed identity."
)


def _payload(spec, scan_report):
    import json
    return json.dumps({
        "securityType": spec.source.get("securityType"),
        "customizers": spec.customizers,
        "scan_verdict": scan_report["verdict"],
        "apps": scan_report["apps"],
        "cves": scan_report["cves"],
    })[:3500]


def _parse(raw):
    import json
    s = raw.strip()
    if s.startswith("```"):
        s = s.strip("`").split("\n", 1)[-1]
    try:
        d = json.loads(s)
        return {"decision": d.get("decision", "REJECT"),
                "blockers": d.get("blockers", []), "advisories": d.get("advisories", [])}
    except Exception:  # noqa: BLE001
        return None


def llm_review(spec, template, scan_report):
    from shared.llm import chat
    raw = chat([{"role": "system", "content": _SYSTEM},
                {"role": "user", "content": _payload(spec, scan_report)}], temperature=0)
    parsed = _parse(raw)
    if parsed:
        parsed["reviewer"] = "security-reviewer (llm)"
        return parsed
    return {"reviewer": "security-reviewer (llm)", "decision": "REJECT",
            "blockers": ["unparseable reviewer output"], "advisories": []}


def autogen_review(spec, template, scan_report):
    """A real AutoGen AssistantAgent reviewer (needs autogen-agentchat + a provider)."""
    import asyncio

    async def _run():
        from autogen_agentchat.agents import AssistantAgent
        from autogen_ext.models.openai import OpenAIChatCompletionClient
        if os.getenv("LLM_PROVIDER", "ollama").lower() == "ollama":
            client = OpenAIChatCompletionClient(
                model=os.getenv("OLLAMA_MODEL", "llama3.1"),
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
                api_key="ollama",
                model_info={"vision": False, "function_calling": True,
                            "json_output": True, "family": "unknown",
                            "structured_output": True},
            )
        else:
            client = OpenAIChatCompletionClient(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                api_key=os.environ.get("OPENAI_API_KEY", ""),
            )
        agent = AssistantAgent("security_reviewer", model_client=client, system_message=_SYSTEM)
        result = await agent.run(task=_payload(spec, scan_report))
        await client.close()
        return result.messages[-1].content

    try:
        parsed = _parse(asyncio.run(_run()))
        if parsed:
            parsed["reviewer"] = "security-reviewer (autogen)"
            return parsed
    except Exception as exc:  # noqa: BLE001
        print(f"   (autogen reviewer unavailable: {exc}; using rules)")
    return review(spec, template, scan_report)


def run_review(spec, template, scan_report):
    """Dispatch to the configured reviewer backend; always falls back to rules."""
    mode = os.getenv("REVIEWER", "rules").lower()
    try:
        if mode == "llm":
            return llm_review(spec, template, scan_report)
        if mode == "autogen":
            return autogen_review(spec, template, scan_report)
    except Exception as exc:  # noqa: BLE001
        print(f"   (reviewer '{mode}' failed: {exc}; using rules)")
    return review(spec, template, scan_report)
