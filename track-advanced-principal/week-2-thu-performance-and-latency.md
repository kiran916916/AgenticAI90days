# Week 2 · Thursday — Performance & latency × a closed-loop optimization agent

**Advanced / Principal Track · ~60–90 min**

> **Discipline × Build:** Performance & latency × an agent that profiles →
> hypothesizes → patches → re-benchmarks.

## 🧭 Maps to
- **Course:** Phase 8 (performance/caching)
- **Concepts:** Ops — latency control, caching, parallel I/O
- **Toolkit:** [`shared/tracing.py`](../shared/tracing.py) · [`shared/reliability.py`](../shared/reliability.py)

## 💡 Engineering tips
- **Measure p99, not averages** — tail latency is the user experience.
- **Optimize the critical path first**; batch/parallelize I/O.
- **Cache computed results**; **profile before guessing.**

## 🤖 Agentic build
A **closed-loop optimization agent**: **profile → hypothesize → patch → re-benchmark**,
accepting a change only on a measured win.

## 🧪 Exercise
1. Give the agent a **profiler output + the code**.
2. Have it propose and **apply ONE patch** (e.g., cache a hot call, parallelize I/O).
3. **Re-run the benchmark** and **report the delta**; **gate acceptance on a real
   speedup** (revert if not faster).

**Acceptance:** the agent reports before/after p99 (or wall-clock), and only keeps the
patch if it measurably improves — otherwise it reverts and says why.

## 🎖️ Principal move
Compress the investigation into **one crisp, confidence-rated recommendation**
("85% confident: cache layer X → −40% p99").

## 📦 Reusable asset
A **profile→patch→benchmark loop** + a **benchmark-report template** (p50/p95/p99,
delta, confidence).

## ✅ Done when
- The agent applies a patch and re-benchmarks automatically.
- Acceptance is gated on a real, measured speedup.
- You wrote a confidence-rated one-line recommendation.
