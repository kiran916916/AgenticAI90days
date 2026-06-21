"""The image build spec + validation (grounded in Azure VM Image Builder rules)."""
from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass, field, fields


@dataclass
class ImageSpec:
    name: str
    resource_group: str
    location: str
    managed_identity: str       # user-assigned identity AIB uses to distribute (least privilege)
    source: dict                # PlatformImage: publisher/offer/sku/version/hyperVGeneration/securityType
    gallery: dict               # Azure Compute Gallery target: name/imageDefinition/.../replicationRegions
    customizers: list           # ordered built-in/custom customizers
    build: dict                 # vmSize / timeoutMinutes
    host_pool: dict             # rollout target (high-blast)
    app_baseline: dict = field(default_factory=dict)   # required/forbidden apps + org tools
    security: dict = field(default_factory=dict)        # e.g. {"block_on_severity": "High"}

    @staticmethod
    def from_file(path) -> "ImageSpec":
        data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
        known = {f.name for f in fields(ImageSpec)}
        return ImageSpec(**{k: v for k, v in data.items() if k in known})


REQUIRED_SOURCE = {"publisher", "offer", "sku", "hyperVGeneration", "securityType"}


def validate_spec(spec: ImageSpec) -> list[str]:
    """Return a list of problems ([] = valid). Encodes real AIB/AVD constraints."""
    problems = []
    if not spec.customizers:
        problems.append("no customizers selected")
    missing = REQUIRED_SOURCE - set(spec.source)
    if missing:
        problems.append(f"source missing keys: {sorted(missing)}")
    if spec.source.get("hyperVGeneration") != "V2":
        problems.append("AVD multi-session requires Gen2 (hyperVGeneration=V2)")
    # AIB: source and distribute must both be TrustedLaunchSupported (not TrustedLaunch).
    if spec.source.get("securityType") == "TrustedLaunch":
        problems.append("source securityType must be 'TrustedLaunchSupported', not 'TrustedLaunch'")
    if not spec.managed_identity:
        problems.append("a user-assigned managed identity is required to distribute the image")
    if not spec.gallery.get("imageDefinition"):
        problems.append("gallery.imageDefinition is required")
    return problems
