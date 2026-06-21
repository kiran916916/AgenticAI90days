"""Atlas Imager — an agentic AVD image-build orchestrator (Phase 9 capstone).

Safe-by-default: everything runs in DRY-RUN — it *generates* the Azure VM Image
Builder template + the `az` command plan and simulates results, but makes NO real
Azure changes. High-blast steps (rolling a host pool) always require human approval.
"""
