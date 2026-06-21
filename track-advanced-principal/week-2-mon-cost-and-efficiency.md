# Week 2 · Monday — Cost & efficiency × a FinOps agent

**Advanced / Principal Track · ~60–90 min**

> **Discipline × Build:** Cost & efficiency × a FinOps agent that finds top drivers
> and drafts remediations.

## 🧭 Maps to
- **Course:** Phase 8 (cost/token control)
- **Concepts:** Ops — **model routing**, **caching**, cost/latency control
- **Toolkit:** [`shared/routing.py`](../shared/routing.py) — `routed_chat`, `pick_model`

## 💡 Engineering tips
- **Right-size before you reserve**; kill zombie resources.
- **Tier storage**; make **cost observable per service**.
- Watch **egress AND token spend** — both are silent killers for agents.

## 🤖 Agentic build
A **FinOps agent** over a **billing export** (CSV/JSON) that ranks **top cost drivers**
and **drafts remediations** (rightsizing, caching, tiering, model routing).

## 🧪 Exercise
1. Add **model routing** to one of your agents: cheap model for easy steps, strong
   model for hard ones (`routed_chat(messages, difficulty="easy"|"hard")`).
2. Add **response caching** for identical calls (built into `routed_chat`).
3. **Measure the token/$ reduction** vs. an all-strong-model baseline (count calls,
   estimate tokens, report % saved).

**Acceptance:** the routed+cached run produces equivalent answers at a clearly lower
modeled cost; you can show the before/after numbers and the cache-hit count.

## 🎖️ Principal move
Frame **one optimization as a customer-value story**, not a savings number ("this
funds X for customers").

## 📦 Reusable asset
A **routing policy** (which step → which model) + a **cost dashboard prompt** for the
FinOps agent.

## ✅ Done when
- Routing + caching are wired into a real agent.
- You reported a measured token/$ reduction.
- You wrote the customer-value framing.
