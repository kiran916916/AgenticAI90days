# Week 1 · Tuesday — Fault tolerance × a chaos agent

**Advanced / Principal Track · ~60–90 min**

> **Discipline × Build:** Resilience × a chaos agent that proposes & runs sandboxed
> fault injections.

## 🧭 Maps to
- **Course:** Phase 8 (production reliability)
- **Concepts:** Reliability — **idempotent tool calls**, guardrails
- **Toolkit:** [`shared/reliability.py`](../shared/reliability.py) — `retry`, `timeout`, `CircuitBreaker`, `resilient`

## 💡 Engineering tips
- Treat **timeouts + retries + circuit breakers as a set** — none is enough alone.
- **Idempotent retries** only: never retry a non-idempotent side effect blindly.
- Choose **fail-fast vs fail-open deliberately**, per dependency.

## 🤖 Agentic build
A **chaos agent** that reads a **dependency graph**, generates **failure hypotheses**
("what if the cache is slow?"), and proposes — then runs in a **sandbox** — fault
injections, reporting blast radius.

## 🧪 Exercise
1. Wrap **every agent tool call** with `resilient(...)` (timeout + retry + breaker)
   from the toolkit.
2. Add an **idempotency key** to any tool with side effects (use `IdempotencyStore`).
3. Make the agent loop **survive a flaky/slow tool** (simulate random failures + delays)
   **without corrupting state**.

**Acceptance:** with a tool that fails 50% of the time and occasionally hangs, the
agent still completes correctly, the breaker opens under sustained failure, and no
side effect runs twice.

## 🎖️ Principal move
Reframe **one resilience gap as business risk**: *downtime → affected customers → $$*.

## 📦 Reusable asset
A **resilient tool wrapper** pattern + a short **"failure modes" checklist** for any
new tool you add to an agent.

## ✅ Done when
- Every tool call is wrapped; the loop survives injected chaos.
- You can show the circuit breaker tripping and recovering (half-open → closed).
- You wrote the one-line business-risk reframing.
