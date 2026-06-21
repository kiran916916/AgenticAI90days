# Week 1 · Monday — Scalability × a ReAct design-review agent

**Advanced / Principal Track · ~60–90 min**

> **Discipline × Build:** Scalability patterns × a design-review agent that returns
> ranked bottlenecks.

## 🧭 Maps to
- **Course:** Phase 2 (ReAct, Day 16) · Phase 8 (production)
- **Concepts:** Agent loops — **ReAct**, **Reflexion / self-critique**
- **Toolkit:** [`shared/tracing.py`](../shared/tracing.py) (time each analysis step)

## 💡 Engineering tips
- **Scale stateless first**; push state to the edges (DB, cache, queue).
- **Partition by access pattern**, not by table convenience.
- **Cache read-heavy / change-rarely** paths; measure hit rate.
- **Find the knee before optimizing** — profile, don't guess.

## 🤖 Agentic build
A **design-review agent** using a **ReAct loop** whose *tools* are your architecture
checklist + repo reading. It reasons step-by-step, inspects the system, and returns a
**ranked list of bottlenecks** with rationale.

## 🧪 Exercise
1. Implement the **ReAct loop from scratch**: `thought → action → observation`, looping
   until a final answer (build on your Phase 2 agent).
2. Give it two tools: `read_repo(path)` and `arch_checklist()` (returns your scaling
   heuristics).
3. Add a **reflection pass**: a second LLM call that **critiques its own findings** and
   reorders/removes weak ones (Reflexion).

**Acceptance:** the agent cites *evidence* (file/line or checklist item) for each
bottleneck, and the reflection pass changes at least one ranking with a stated reason.

## 🎖️ Principal move
Write a **3-sentence tradeoff verdict**: *"Shard now because… accepting… revisit when…"*

## 📦 Reusable asset
Save the **architecture checklist** (as an `arch_checklist()` tool) and the **ReAct +
reflection** loop into your agent library.

## ✅ Done when
- The ReAct loop runs thought/action/observation transparently (print each step).
- Reflection demonstrably improves the ranking.
- You produced a one-paragraph tradeoff verdict.
