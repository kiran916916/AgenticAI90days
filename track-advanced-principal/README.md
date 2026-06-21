# 🏛️ Advanced / Principal Track — System Design × Agentic AI

A repeating **2-week (Mon–Fri) program** that fuses **senior/principal system-design
mastery** with **hard agentic builds**. Every day pairs an engineering discipline
(scalability, resilience, security, identity, cost, observability, governance) with
an agent you build to *practice* it — then a **Principal move** to turn the learning
into organizational leverage.

> Do this **after** (or alongside) the [90-day foundations](../README.md). The
> foundations teach you to *build* agents; this track teaches you to build them
> **reliable, secure, observable, and governable** — the way a Principal engineer
> ships them.

---

## 🧠 Advanced agentic-AI concepts to master (reference)
- **Agent loops:** ReAct · Plan-and-Execute · Reflexion / self-critique · Tree-of-Thoughts
- **Tool use:** function calling · JSON-schema tool contracts · MCP (Model Context Protocol) servers
- **Multi-agent:** orchestrator–worker · planner→worker→critic · hierarchical & debate patterns
- **Memory & context:** short/long-term memory · vector stores · RAG · context engineering
- **Reliability:** guardrails · deny-by-default tool scoping · human-in-the-loop gates · idempotent tool calls
- **Evaluation:** eval harnesses · golden sets · LLM-as-judge · regression gates on agent quality
- **Identity & safety:** per-agent identity · least-privilege short-lived creds · full action audit
- **Ops:** tracing/observability (spans per tool call) · cost/latency control (model routing, caching)

**Stack to practice with:** an LLM SDK with tool-calling · an MCP server · a vector DB · a tracing/eval tool.

## 🧰 Your agent-library toolkit (already built, in `shared/`)
Reusable assets you'll lean on every day — import them and harden as you go:

| Module | What it gives you | Used on |
| --- | --- | --- |
| [`shared/reliability.py`](../shared/reliability.py) | `retry`, `timeout`, `CircuitBreaker`, `resilient`, idempotency | Wk1 Tue / Wk2 Thu |
| [`shared/policy.py`](../shared/policy.py) ⭐ | deny-by-default `PolicyGate` + audit trail + HITL | Wk1 Fri |
| [`shared/tracing.py`](../shared/tracing.py) | `Tracer` — one span per tool call + attributes | Wk2 Wed/Thu |
| [`shared/evals.py`](../shared/evals.py) | `GoldenCase`, `run_eval`, `llm_judge`, `regression_gate` | Wk2 Fri |
| [`shared/routing.py`](../shared/routing.py) | `routed_chat` — model routing + caching | Wk2 Mon |

> Run examples from the repo root so `from shared... import ...` resolves
> (e.g. `python shared/policy.py`). In a notebook, use the **▶ Run this first** cell.

---

## 🗓️ The two-week cycle

### Week 1 — Foundations of trustworthy agents
| Day | Discipline × Build | Brief |
| --- | --- | --- |
| Mon | **Scalability** × a ReAct design-review agent | [open](week-1-mon-scalability.md) |
| Tue | **Fault tolerance** × a chaos agent | [open](week-1-tue-fault-tolerance.md) |
| Wed | **Event-driven design** × planner→worker→critic over a queue | [open](week-1-wed-event-driven.md) |
| Thu | **Security-by-design** × a STRIDE threat-model agent (+ verifier) | [open](week-1-thu-security-by-design.md) |
| Fri ⭐ | **Identity & access FOR AGENTS** × a scoped, deny-by-default agent | [open](week-1-fri-identity-and-access-for-agents.md) |

### Week 2 — Operating agents at principal scale
| Day | Discipline × Build | Brief |
| --- | --- | --- |
| Mon | **Cost & efficiency** × a FinOps agent (routing + caching) | [open](week-2-mon-cost-and-efficiency.md) |
| Tue | **API & integration** × an MCP tool server | [open](week-2-tue-api-and-integration-mcp.md) |
| Wed | **Observability** × a self-healing observability agent | [open](week-2-wed-observability.md) |
| Thu | **Performance & latency** × a closed-loop optimization agent | [open](week-2-thu-performance-and-latency.md) |
| Fri | **Governance, ADRs & evaluation** × an ADR agent + eval harness | [open](week-2-fri-governance-adrs-evaluation.md) |

> **Repeat each cycle with the NEXT layer of each topic so depth compounds.**
> (e.g. Wk1 Tue v1 = retries+breakers; v2 = bulkheads, hedged requests, backpressure.)

---

## 🔁 Turn learning into leverage
1. Each takeaway → a **reusable asset** (checklist, template, agent prompt, ADR, module).
2. Save every agent (with guardrails + evals) into your **agent library** (`shared/` + briefs).
3. **Friday:** roll the week into ONE insight shared in shiproom / a design review.
4. Track **Principal signals:** a standard adopted · a team unblocked · a space claimed · a doc that traveled.
5. When a topic clicks, **teach it** — a 10-minute brown-bag turns learning into org capability.

## How a brief is structured
Each day's file has: **Maps to** (course phase + concept + toolkit) · **Engineering
tips** · **Agentic build** · **🧪 Exercise** (with acceptance criteria) · **Principal
move** · **Reusable asset** · **Done when**.

**→ Start with [Week 1 · Monday](week-1-mon-scalability.md).**
