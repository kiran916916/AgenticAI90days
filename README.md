# 🤖 The 90-Day Generative & Agentic AI Handbook

A self-paced, hands-on program that takes you from *"what even is generative AI?"*
to *shipping a production-grade multi-agent system* — **one ~30–45 minute notebook
a day.**

You **start with Generative AI** (how models work, prompting, embeddings) and
**transition into Agentic AI** (tools, loops, memory, multi-agent teams, including
a dedicated **AutoGen** phase). You learn by **building**: every day you write real
code and watch it run.

By Day 90 you'll have built **Atlas** — your own agent that grows a new capability
each phase.

---

## How this works

### The daily rhythm (the method)
Each day is one Jupyter notebook that follows the same five beats:

| Beat | Icon | What you do |
| --- | --- | --- |
| **Concept** | 🧠 | A short, focused explanation (5–10 min) |
| **Visualize** | 🗺️ | A diagram so the idea *sticks* |
| **Code** | 🔬 | Fill in the `TODO`s in the exercise cell |
| **Reflect** | 📝 | Answer 1–2 journal prompts in your own words |
| **Solution** | 🔒 | Compare with the worked answer (peek only after trying) |

> **Spaced repetition is built in:** the last day of each phase is a **capstone**
> that recombines everything you learned.

### The through-line: build **Atlas**
You don't build 90 throwaway scripts — you grow **one** assistant:

```
Phase 1  Atlas's brain: reliable, structured generation (GenAI)
Phase 2  Atlas gains a loop + tools — it starts to *act*
Phase 3  Atlas plans, remembers, and reflects
Phase 4  Atlas is rebuilt on real frameworks (+ MCP tools)
Phase 5  Atlas becomes a team of agents with AutoGen
Phase 6  Atlas orchestrates specialists (multi-agent)
Phase 7  Atlas reads your private documents (RAG)
Phase 8  Atlas is evaluated, guarded, traced, and deployed
Phase 9  Atlas ships for real: an agent that builds AVD images on Azure
```

### Before you start
1. Read **[SETUP.md](SETUP.md)** (10 min). Days 1–2 need *no* API key.
2. Each day is a single **Jupyter notebook** (`day-NN.ipynb`) — concept, exercise,
   and solution together. Open it in VS Code and run cells top to bottom.
3. The reusable model helpers live in **`shared/`** (a real Python package the
   notebooks import). Keep that as-is.
4. Optional: keep a `journal.md` for your daily reflections.
5. Start **[Day 1](phase-1-generative-ai/day-01-what-is-generative-ai/day-01-what-is-generative-ai.ipynb)**.

---

## The 9 phases at a glance

Every phase has its own folder + index README (click the phase name). ✅ = notebooks
built and runnable · 🧭 = guide ready, day notebooks built on request.

| Phase | Days | Theme | Status |
| --- | --- | --- | --- |
| [**1 — Generative AI Foundations**](phase-1-generative-ai/README.md) | 1–10 | How LLMs work, prompting, embeddings | ✅ built |
| [**2 — From Generative to Agentic**](phase-2-agentic-foundations/README.md) | 11–22 | The loop, tools, ReAct, memory | ✅ built |
| [**3 — Tools, Memory & Planning**](phase-3-tools-memory-planning/README.md) | 23–34 | Robust tools, memory, planning | ✅ built |
| [**4 — Frameworks**](phase-4-frameworks/README.md) | 35–46 | OpenAI SDK, LangGraph, SK, MCP | ✅ built |
| [**5 — AutoGen (dedicated)**](phase-5-autogen/README.md) | 47–57 | AutoGen AgentChat & teams | ✅ built |
| [**6 — Multi-Agent Orchestration**](phase-6-multi-agent/README.md) | 58–67 | Supervisors, handoffs, debate | ✅ built |
| [**7 — Knowledge & RAG**](phase-7-rag/README.md) | 68–77 | Embeddings, vector search, agentic RAG | ✅ built |
| [**8 — Production**](phase-8-production/README.md) | 78–87 | Eval, tracing, guardrails, deploy | ✅ built |
| [**9 — Capstone**](phase-9-capstone/README.md) | 88–90 | Design → build → ship | ✅ built |

---

## 🧩 Three ways to learn: code · no-code · advanced

This handbook has **three complementary tracks** — do one or mix them:

- **Code track (the 90 days below)** — build agents from scratch in Python
  notebooks. Deep understanding, full control.
- **[No-Code Track — Microsoft Copilot Studio](track-no-code-copilot-studio/README.md)**
  — build and ship real agents in the browser, *no code*. Fast and enterprise-ready,
  and it mirrors every concept here: **knowledge = RAG**, **actions = tools**,
  **generative orchestration = the agent loop**, **publish = deploy**.
- **[Advanced / Principal Track](track-advanced-principal/README.md)** — a repeating
  2-week, senior-engineer program fusing system-design mastery (scalability,
  resilience, security, **identity for agents**, cost, observability, governance) with
  hard agentic builds (ReAct, multi-agent, MCP, guardrails, tracing, eval harnesses).
  Ships a reusable **agent-library toolkit** in `shared/` (reliability · policy ·
  tracing · evals · routing).

Mix and match: learn a concept in code, ship it no-code, then harden it in the
advanced track.

---

## Full 90-day plan & progress tracker

Tick each box as you go. Days marked ✅ are fully built notebooks; the rest are
specified here and built out as you reach each phase.

### Phase 1 — Generative AI Foundations (Days 1–10)
- [ ] **Day 1** ✅ What *is* generative AI? — build a Markov text generator (no setup)
- [ ] **Day 2** ✅ Tokens & next-token prediction — tokenizer + next-word predictor
- [ ] **Day 3** ✅ Your first LLM call — messages, roles, the `chat()` helper
- [ ] **Day 4** ✅ Sampling & decoding — temperature, top-p, max tokens
- [ ] **Day 5** ✅ Prompt engineering I — system messages & personas
- [ ] **Day 6** ✅ Prompt engineering II — few-shot & patterns
- [ ] **Day 7** ✅ Structured output — reliable JSON with a repair loop
- [ ] **Day 8** ✅ Embeddings & semantic similarity — cosine similarity
- [ ] **Day 9** ✅ Limits & safety — hallucination, context, prompt injection
- [ ] **Day 10** ✅ **Project:** a GenAI content assistant (summary + sentiment + keywords)

### Phase 2 — From Generative to Agentic (Days 11–22)
- [ ] **Day 11** ✅ What *is* an AI agent? — a reflex agent
- [ ] **Day 12** ✅ The agent loop — sense → think → act → observe
- [ ] **Day 13** ✅ Tools as functions — a tool registry & dispatcher
- [ ] **Day 14** ✅ From prompt to agent — the Echo agent (manual tool-calling)
- [ ] **Day 15** Native function/tool calling — let the model call tools
- [ ] **Day 16** The ReAct pattern — interleave Reasoning + Acting
- [ ] **Day 17** Robust tool-call handling — multiple & parallel calls
- [ ] **Day 18** Short-term memory — the conversation buffer
- [ ] **Day 19** The `Agent` class — refactor into a clean abstraction
- [ ] **Day 20** Errors, retries & timeouts — resilient agents
- [ ] **Day 21** Reflection & self-critique
- [ ] **Day 22** **Capstone:** Atlas v1 — a from-scratch ReAct agent with 3 tools

### Phase 3 — Tools, Memory & Planning (Days 23–34)
- [ ] **Day 23** Designing great tools (names, descriptions, arguments)
- [ ] **Day 24** Tool schemas & validation with Pydantic
- [ ] **Day 25** Real tools: calling HTTP APIs
- [ ] **Day 26** File & code tools (run code safely)
- [ ] **Day 27** A web-search tool
- [ ] **Day 28** Memory types: working, episodic, semantic, long-term
- [ ] **Day 29** Summarization memory (compress long history)
- [ ] **Day 30** Vector memory (semantic recall)
- [ ] **Day 31** Planning: plan-then-execute
- [ ] **Day 32** Task decomposition
- [ ] **Day 33** Reasoning strategies tour: CoT, ReAct, ReWOO, Reflexion
- [ ] **Day 34** **Capstone:** Atlas v2 — planning + memory + reflection

### Phase 4 — Frameworks (Days 35–46)
- [ ] **Day 35** Why frameworks? The landscape & trade-offs
- [ ] **Day 36** OpenAI Agents SDK — basics
- [ ] **Day 37** OpenAI Agents SDK — tools & handoffs
- [ ] **Day 38** LangChain essentials (models, tools, LCEL)
- [ ] **Day 39** LangGraph — state graphs
- [ ] **Day 40** LangGraph — cycles & conditional edges (a ReAct graph)
- [ ] **Day 41** Rebuild Atlas in LangGraph
- [ ] **Day 42** Semantic Kernel — kernel & plugins
- [ ] **Day 43** Semantic Kernel — functions & planners
- [ ] **Day 44** Model Context Protocol (MCP) — concepts
- [ ] **Day 45** Build & connect an MCP server (expose tools)
- [ ] **Day 46** **Capstone:** a framework agent using MCP tools

### Phase 5 — AutoGen (dedicated) (Days 47–57)
- [ ] **Day 47** AutoGen intro & architecture (AgentChat · Core · Extensions)
- [ ] **Day 48** Model clients (OpenAI / Azure / Ollama via `OpenAIChatCompletionClient`)
- [ ] **Day 49** `AssistantAgent` basics — `run` and `run_stream`
- [ ] **Day 50** Tools & function calling in AutoGen
- [ ] **Day 51** Code-execution agents (local / Docker executor)
- [ ] **Day 52** Two-agent conversations
- [ ] **Day 53** `RoundRobinGroupChat` & termination conditions
- [ ] **Day 54** `SelectorGroupChat` — LLM-routed teams
- [ ] **Day 55** Handoffs & the Swarm pattern
- [ ] **Day 56** Human-in-the-loop (`UserProxyAgent`)
- [ ] **Day 57** **Capstone:** an AutoGen multi-agent team (planner + coder + reviewer)

### Phase 6 — Multi-Agent Orchestration (Days 58–67)
- [ ] **Day 58** Why multi-agent? Patterns overview
- [ ] **Day 59** Supervisor / worker
- [ ] **Day 60** Group chat / round-robin (framework-agnostic)
- [ ] **Day 61** Handoffs & routing
- [ ] **Day 62** Debate & critique
- [ ] **Day 63** Shared state / blackboard
- [ ] **Day 64** Designing specialist roles & prompts
- [ ] **Day 65** Sequential vs parallel orchestration
- [ ] **Day 66** Cost & latency in multi-agent systems
- [ ] **Day 67** **Capstone:** a multi-agent workflow

### Phase 7 — Knowledge & RAG (Days 68–77)
- [ ] **Day 68** Embeddings deep dive (chunk-level)
- [ ] **Day 69** Vector stores (Chroma / FAISS)
- [ ] **Day 70** Chunking strategies
- [ ] **Day 71** Build a basic RAG pipeline
- [ ] **Day 72** RAG as a *tool* for an agent
- [ ] **Day 73** Query rewriting & multi-query
- [ ] **Day 74** Agentic RAG (retrieve → decide → loop)
- [ ] **Day 75** Hybrid search & reranking
- [ ] **Day 76** Evaluating RAG (faithfulness, relevance)
- [ ] **Day 77** **Capstone:** agentic RAG over *your* documents

### Phase 8 — Production (Days 78–87)
- [ ] **Day 78** Evaluation fundamentals (offline eval sets)
- [ ] **Day 79** LLM-as-judge
- [ ] **Day 80** Tracing & observability (OpenTelemetry / Langfuse)
- [ ] **Day 81** Guardrails: input/output validation
- [ ] **Day 82** Safety: prompt-injection defenses (deep dive)
- [ ] **Day 83** Cost tracking & token budgets
- [ ] **Day 84** Caching & performance
- [ ] **Day 85** Deploy as an API (FastAPI)
- [ ] **Day 86** Containerize (Docker)
- [ ] **Day 87** **Capstone:** productionize Atlas (API + eval + tracing)

### Phase 9 — Capstone: an agentic AVD image-build orchestrator (Days 88–90)
> Build **Atlas Imager** — an agent that drives **Azure Virtual Desktop** image creation
> end-to-end (spec → VM Image Builder template → build → publish to Compute Gallery →
> staged host-pool rollout), **safe-by-default** (dry-run + human-approval gates).
> Full brief & runnable scaffold: **[phase-9-capstone/](phase-9-capstone/README.md)**.
- [ ] **Day 88** Design & spec — the build spec + the identity/safety model
- [ ] **Day 89** Build the core — plan → generate image template + `az` plan → guarded
      execute; wire the policy gate + reliability + tracing toolkit
- [ ] **Day 90** **Ship & demo** — add eval + ADR, run the dry-run end-to-end, retrospective

---

## Glossary (your quick reference)

| Term | Plain-English meaning |
| --- | --- |
| **Generative AI** | Models that *produce* new content (text, code, images, audio) |
| **LLM** | Large Language Model — predicts the next **token**, over and over |
| **Token** | A chunk of text (≈¾ word) the model actually reads; cost & limits are in tokens |
| **Context window** | Max tokens a model can attend to at once |
| **Temperature** | Randomness of generation — low = focused, high = creative |
| **Embedding** | Text turned into a vector of *meaning*; similar text → nearby vectors |
| **Hallucination** | A confident but false output |
| **Agent** | An LLM that runs in a **loop**, choosing **tools** to reach a **goal** |
| **Tool** | A function the agent can call (math, search, an API, your code) |
| **ReAct** | Prompting style interleaving **Rea**soning and **Act**ing |
| **RAG** | Retrieval-Augmented Generation — fetch facts, then answer |
| **AutoGen** | Microsoft framework for building multi-agent applications |
| **MCP** | Model Context Protocol — a standard way to expose tools to any agent |

---

### A note on honesty with yourself
The point is **understanding**, not speed. Struggle a little before opening the
🔒 Solution cell. If a day clicks fast, push on the challenge in the notebook. Show
up daily — momentum is the real curriculum.

**→ Begin with [Day 1](phase-1-generative-ai/day-01-what-is-generative-ai/day-01-what-is-generative-ai.ipynb).**
