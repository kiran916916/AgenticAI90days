# Week 2 · Wednesday — Observability × a self-healing observability agent

**Advanced / Principal Track · ~60–90 min**

> **Discipline × Build:** Observability & operability × an agent that clusters
> anomalies, summarizes incidents, and proposes gated remediations.

## 🧭 Maps to
- **Course:** Phase 8 (tracing & observability)
- **Concepts:** Ops — **tracing/observability** (a span per tool call), HITL gates
- **Toolkit:** [`shared/tracing.py`](../shared/tracing.py) · [`shared/policy.py`](../shared/policy.py)

## 💡 Engineering tips
- **Consistent correlation IDs** across logs / metrics / traces.
- **Alert on symptoms** (user-visible), not every cause.
- **SLOs before dashboards**; **every alert must be actionable.**

## 🤖 Agentic build
A **self-healing observability agent**: it ingests noisy telemetry, **clusters
anomalies**, **summarizes incidents**, and **proposes remediations** behind a
human-approval gate.

## 🧪 Exercise
1. **Instrument your agent with tracing**: a **span per tool call** plus **token &
   latency** attributes (use `Tracer` / `tr.traced(...)`).
2. Feed it a **noisy log sample**; have it cluster + summarize the top incident.
3. Have it **propose a fix behind a human-approval gate** (reuse `PolicyGate` HITL).

**Acceptance:** the trace shows per-tool latency/token attributes; the agent's
proposed remediation never auto-applies — it waits for approval.

## 🎖️ Principal move
Define **one SLO the whole org (not just your service) should adopt.**

## 📦 Reusable asset
A **tracing wrapper** for tool calls + an **incident-summary prompt** + an **SLO
definition template**.

## ✅ Done when
- Every tool call emits a span with latency + token attributes.
- The agent summarizes a noisy sample into one actionable incident.
- Remediation is gated behind human approval.
