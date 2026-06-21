"""Dry-run-safe agent tools for the AVD image build.

Each tool returns (command_string, simulated_result). In DRY-RUN nothing touches
Azure. To go live you'd replace the bodies with real `az`/SDK calls — but only
behind the policy gate + approval (see agent.py). Scopes below feed the deny-by-default
PolicyGate so the agent identity runs with least privilege.
"""
from __future__ import annotations

from . import appscan

# tool name -> Azure permission scope it requires (least-privilege model)
TOOL_SCOPES = {
    "create_resource_group": "infra:write",
    "create_managed_identity": "identity:write",
    "create_gallery": "gallery:write",
    "create_image_definition": "gallery:write",
    "create_image_template": "imagebuilder:write",
    "run_image_build": "imagebuilder:run",
    "monitor_build": "imagebuilder:read",
    "scan_image_apps": "security:scan",
    "publish_version": "gallery:write",
    "update_host_pool": "hostpool:write",
}

# Tools that ALWAYS require human approval (production blast radius).
HIGH_BLAST = {"update_host_pool"}


def create_resource_group(spec):
    return (f"az group create -n {spec.resource_group} -l {spec.location}",
            {"ok": True})


def create_managed_identity(spec):
    return (f"az identity create -g {spec.resource_group} -n {spec.managed_identity}",
            {"identity": spec.managed_identity, "least_privilege": True})


def create_gallery(spec):
    return (f"az sig create -g {spec.resource_group} --gallery-name {spec.gallery['name']}",
            {"gallery": spec.gallery["name"]})


def create_image_definition(spec):
    g = spec.gallery
    return (f"az sig image-definition create -g {spec.resource_group} "
            f"--gallery-name {g['name']} --gallery-image-definition {g['imageDefinition']}",
            {"imageDefinition": g["imageDefinition"], "gen": "V2"})


def create_image_template(spec):
    return (f"az image builder create -g {spec.resource_group} -n {spec.name} "
            f"--image-template-file imagetemplate.json",
            {"template": spec.name, "immutable": True})


def run_image_build(spec):
    return (f"az image builder run -g {spec.resource_group} -n {spec.name}",
            {"status": "Running"})


def monitor_build(spec):
    return (f"az image builder show -g {spec.resource_group} -n {spec.name} "
            f"--query lastRunStatus",
            {"runState": "Succeeded", "runtimeMinutes": 58})


def scan_image_apps(spec):
    """Validate apps + scan for CVEs (pre-publish security gate). See appscan.py.

    Real-mode command would query Defender Vulnerability Management software inventory
    + weaknesses, or run an inventory on the image via `az vm run-command`.
    """
    report = appscan.scan_report(spec)
    cmd = ("# Defender Vulnerability Management: software inventory + weaknesses (CVEs) "
           "| or: az vm run-command invoke ... --scripts 'Get-Package; winget list'")
    return (cmd, report)


def publish_version(spec):
    return (f"az sig image-version list -g {spec.resource_group} "
            f"--gallery-name {spec.gallery['name']} "
            f"--gallery-image-definition {spec.gallery['imageDefinition']} -o table",
            {"newVersion": "1.0.0", "replicated": spec.gallery.get("replicationRegions", [])})


def update_host_pool(spec):
    hp = spec.host_pool
    return (f"# staged session-host rollout for host pool '{hp['name']}' to new image version",
            {"hostPool": hp["name"], "rollout": hp.get("rollout", "staged")})
