"""Generate the Azure VM Image Builder template + the `az` command plan.

Deterministic and offline — this is the agent's 'structured output' tool. The AVD
built-in customizer scripts live in github.com/Azure/RDS-Templates; we reference them
by name (URIs are placeholders you confirm against the current repo path).
"""
from __future__ import annotations

# Maps an AVD built-in customizer name -> AIB customizer type.
BUILTIN = {
    "InstallLanguagePacks": "PowerShell",
    "SetDefaultOsLanguage": "PowerShell",
    "TimeZoneRedirection": "PowerShell",
    "DisableStorageSense": "PowerShell",
    "InstallFSLogix": "PowerShell",
    "ConfigureTeamsOptimizations": "PowerShell",
    "EnableRdpShortpath": "PowerShell",
    "EnableScreenCaptureProtection": "PowerShell",
    "SetSessionTimeouts": "PowerShell",
    "RemoveAppxPackages": "PowerShell",
    "ApplyWindowsUpdates": "WindowsUpdate",
}

RDS = ("https://raw.githubusercontent.com/Azure/RDS-Templates/master/"
       "CustomImageTemplateScripts/CustomImageTemplateScripts_2024-03-27")

_SUB = "<SUBSCRIPTION_ID>"


def _customize_block(customizers):
    block = []
    for c in customizers:
        kind = BUILTIN.get(c, "PowerShell")
        if kind == "WindowsUpdate":
            block.append({
                "type": "WindowsUpdate",
                "searchCriteria": "IsInstalled=0",
                "filters": ["exclude:$_.Title -like '*Preview*'", "include:$true"],
                "updateLimit": 40,
            })
            block.append({"type": "WindowsRestart", "restartTimeout": "10m"})
        else:
            block.append({
                "type": "PowerShell", "name": c, "runElevated": True,
                "scriptUri": f"{RDS}/{c}.ps1",
            })
    block.append({"type": "WindowsRestart", "restartTimeout": "10m"})
    return block


def build_image_template(spec) -> dict:
    """Return a Microsoft.VirtualMachineImages/imageTemplates resource (dict)."""
    g = spec.gallery
    rg, mi = spec.resource_group, spec.managed_identity
    mi_id = (f"/subscriptions/{_SUB}/resourceGroups/{rg}/providers/"
             f"Microsoft.ManagedIdentity/userAssignedIdentities/{mi}")
    gallery_image_id = (f"/subscriptions/{_SUB}/resourceGroups/{rg}/providers/"
                        f"Microsoft.Compute/galleries/{g['name']}/images/{g['imageDefinition']}")
    return {
        "type": "Microsoft.VirtualMachineImages/imageTemplates",
        "apiVersion": "2024-02-01",
        "name": spec.name,
        "location": spec.location,
        "identity": {"type": "UserAssigned", "userAssignedIdentities": {mi_id: {}}},
        "properties": {
            "source": {
                "type": "PlatformImage",
                "publisher": spec.source["publisher"],
                "offer": spec.source["offer"],
                "sku": spec.source["sku"],
                "version": spec.source.get("version", "latest"),
            },
            "customize": _customize_block(spec.customizers),
            "distribute": [{
                "type": "SharedImage",
                "galleryImageId": gallery_image_id,
                "runOutputName": f"{spec.name}-runout",
                "replicationRegions": g.get("replicationRegions", [spec.location]),
                "storageAccountType": "Standard_LRS",
                "artifactTags": {"built-by": "atlas-imager", "source": "agentic"},
            }],
            "buildTimeoutInMinutes": spec.build.get("timeoutMinutes", 120),
            "vmProfile": {"vmSize": spec.build.get("vmSize", "Standard_D2ds_v4"),
                          "osDiskSizeGB": 127},
        },
    }


def az_command_plan(spec) -> list[str]:
    """The `az` CLI sequence an operator (or the agent, when --execute) would run."""
    g, rg = spec.gallery, spec.resource_group
    return [
        f"az group create -n {rg} -l {spec.location}",
        f"az identity create -g {rg} -n {spec.managed_identity}",
        "# Grant the identity a LEAST-PRIVILEGE custom role scoped to the gallery RG "
        "(image read/write + distribute). Never Owner/Contributor at subscription scope.",
        f"az sig create -g {rg} --gallery-name {g['name']}",
        (f"az sig image-definition create -g {rg} --gallery-name {g['name']} "
         f"--gallery-image-definition {g['imageDefinition']} --publisher {g['publisher']} "
         f"--offer {g['offer']} --sku {g['sku']} --os-type Windows --os-state Generalized "
         f"--hyper-v-generation V2 --features SecurityType=TrustedLaunchSupported"),
        f"az image builder create -g {rg} -n {spec.name} --image-template-file imagetemplate.json",
        f"az image builder run -g {rg} -n {spec.name}    # long-running build",
        f"az image builder show -g {rg} -n {spec.name} --query lastRunStatus    # monitor",
        (f"az sig image-version list -g {rg} --gallery-name {g['name']} "
         f"--gallery-image-definition {g['imageDefinition']} -o table"),
        f"# HIGH-BLAST (human approval): roll '{spec.host_pool['name']}' session hosts "
        "to the new image version via your staged host-pool update process.",
    ]
