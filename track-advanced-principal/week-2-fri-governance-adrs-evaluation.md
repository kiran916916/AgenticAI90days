# Week 2 · Friday — Governance, ADRs & agent evaluation

**Advanced / Principal Track · ~75–90 min**

> **Discipline × Build:** Governance × an ADR/doc agent **+** an eval harness for the
> agents you built this fortnight.

## 🧭 Maps to
- **Course:** Phase 8 (evaluation, LLM-as-judge)
- **Concepts:** Evaluation — **eval harness**, **golden set**, **LLM-as-judge**,
  **regression gate**
- **Toolkit:** [`shared/evals.py`](../shared/evals.py) — `GoldenCase`, `run_eval`, `regression_gate`

## 💡 Engineering tips
- **One-page ADRs:** context → decision → consequences. Preserve the **why**.
- Track tech debt with an **"interest rate"** (how fast it compounds).
- **Review on a cadence**; let docs travel beyond the team.

## 🤖 Agentic build
An **ADR/doc agent** that drafts decision records from a discussion **+** an **eval
harness** that scores your agents.

## 🧪 Exercise
1. Build an **eval harness** with a **golden set** (`GoldenCase`s) + **LLM-as-judge**
   (`run_eval`) that **scores the agents you built this fortnight**.
2. Set a **quality threshold** and treat it as a **regression gate** (`regression_gate`)
   — wire it so a drop **fails the build** (e.g., a `pytest` that asserts the gate).
3. Have the ADR agent draft a record for one decision you made this cycle.

**Acceptance:** rerunning the harness after a prompt change shows the score move; the
gate fails when quality drops below threshold.

## 🎖️ Principal move
**Publish one ADR or technical narrative to a wider-than-team audience.**

## 📦 Reusable asset
The **golden set + eval harness** (your regression gate) and a **one-page ADR
template** — the capstone assets of this track.

## ✅ Done when
- The harness scores ≥2 agents from the fortnight against a golden set.
- The regression gate fails on a deliberate quality regression.
- You published one ADR/narrative beyond your team.

---

## 🔁 Close the cycle
Roll the fortnight into **one shiproom insight**, file your new assets into the
**agent library**, then **repeat the two weeks with the next layer** of each topic so
depth compounds. ([Back to track index](README.md) · [Main handbook](../README.md))
