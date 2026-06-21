# Phase 8 — Production (Days 78–87)

> **Status:** ✅ Built — 10 daily notebooks below. Most run **offline** on the `shared/` toolkit.

The part that separates a demo from a product: **evaluation, tracing, guardrails,
security, cost, and deployment**. This is the principal-engineer lens (see also
[../track-advanced-principal](../track-advanced-principal/README.md)).

## Days
| Day | Topic | You'll be able to… |
| --- | --- | --- |
| 78 | Evaluation that matters | Build a golden-set harness |
| 79 | LLM-as-judge | Score open-ended outputs |
| 80 | Tracing & observability | Instrument every step (Langfuse) |
| 81 | Guardrails & input/output filters | Block unsafe in & out |
| 82 | Prompt-injection defense | Resist hostile tool output |
| 83 | Identity & least privilege for agents | Scope what an agent may do |
| 84 | Cost & latency budgets | Keep runs cheap and fast |
| 85 | Serving an agent (FastAPI) | Expose an agent as an API |
| 86 | CI gates & regression tests | Block bad releases automatically |
| 87 | **Project: production-ready agent** | Eval + trace + guardrails + serve |

**Install for this phase:**
```bash
pip install langfuse deepeval fastapi uvicorn
```
(All are already listed in [../requirements.txt](../requirements.txt).)

↩ [Handbook](../README.md) · ⬅ [Phase 7](../phase-7-rag/README.md) · ➡ [Phase 9 — Capstone](../phase-9-capstone/README.md)
