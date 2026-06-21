# Phase 3 — Tools, Memory & Planning (Days 23–34)

> **Status:** ✅ Built — 12 daily notebooks (concept → 🔬 exercise → 🔒 solution) are in the
> day folders below. Open any `day-*/*.ipynb` and run the "▶ Run this first" cell.

Deepen the from-scratch agent: make tools **safe and typed**, give the agent **durable
memory**, and teach it to **plan** before acting.

**Builds on:** Phase 2's `Agent` class + the [`shared/`](../shared) toolkit
(`policy.py`, `reliability.py`, `tracing.py`).

## Days
| Day | Topic | You'll be able to… |
| --- | --- | --- |
| 23 | Typed tool schemas (Pydantic) | Validate tool args before running |
| 24 | The tool registry & dispatch | Manage many tools cleanly |
| 25 | Tool authorization (PolicyGate) | Deny-by-default, scoped tool access |
| 26 | Working memory vs. long-term memory | Separate scratchpad from knowledge |
| 27 | Persistent memory (file/SQLite) | Remember across sessions |
| 28 | Summarized memory & context budgets | Stay under the token limit |
| 29 | Planning I: decompose a goal | Turn a goal into sub-tasks |
| 30 | Planning II: plan-and-execute | Run a plan step-by-step |
| 31 | Re-planning on failure | Recover when a step fails |
| 32 | Tracing the agent | See every thought, tool & result |
| 33 | Evaluating an agent (golden cases) | Catch regressions automatically |
| 34 | **Project: a planner agent** | Plan + remember + self-correct |

**Install for this phase:** already covered by `pip install -r ../requirements.txt`
(`pydantic`). No new heavy deps.

↩ [Handbook](../README.md) · ⬅ [Phase 2](../phase-2-agentic-foundations/README.md) · ➡ [Phase 4 — Frameworks](../phase-4-frameworks/README.md)
