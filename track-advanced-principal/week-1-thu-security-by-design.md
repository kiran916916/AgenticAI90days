# Week 1 · Thursday — Security-by-design × a STRIDE threat-model agent

**Advanced / Principal Track · ~60–90 min**

> **Discipline × Build:** Security-by-design × an autonomous STRIDE threat-modeling
> agent (with a verifier).

## 🧭 Maps to
- **Course:** Phase 6 (multi-agent debate) · Phase 8 (safety)
- **Concepts:** Multi-agent **debate/critique**, guardrails
- **Toolkit:** [`shared/evals.py`](../shared/evals.py) (judge weak findings)

## 💡 Engineering tips
- **Default-deny**; open only what's needed.
- **Least privilege per identity**; validate at every **trust boundary**.
- **Assume compromise** — design to **limit lateral movement**.

## 🤖 Agentic build
An autonomous **STRIDE** threat-modeling agent that walks a **data-flow diagram** and
emits threats (Spoofing, Tampering, Repudiation, Info-disclosure, DoS, Elevation) with
mitigations.

## 🧪 Exercise
1. Feed the agent a **DFD as JSON** (nodes, data stores, trust boundaries, flows).
2. Have it emit **threats + mitigations** per element, mapped to STRIDE categories.
3. Add a second **"verifier" agent** that **refutes weak findings** (multi-agent check)
   — keep only threats the verifier can't dismiss.

**Acceptance:** every trust-boundary-crossing flow has ≥1 categorized threat; the
verifier removes or strengthens at least one weak finding with a reason.

## 🎖️ Principal move
Turn the curated output into a **reusable team standard/checklist** ("our STRIDE bar").

## 📦 Reusable asset
The **DFD-JSON schema**, the **STRIDE prompt**, and the **verifier** debate pattern.

## ✅ Done when
- Threats are categorized and tied to specific DFD elements.
- The verifier visibly improves precision (fewer weak/duplicate threats).
- You captured a reusable threat-modeling checklist.
