# Phase 4 — Agent Frameworks (Days 35–46)

> **Status:** ✅ Built — 12 daily notebooks below. Framework days need the per-day `pip install` + a provider.

You've built agents by hand — now build them the **production way**. Same concepts
(loop, tools, memory) expressed in the major frameworks, so you can read any codebase.

## Days
| Day | Topic | You'll be able to… |
| --- | --- | --- |
| 35 | Why frameworks? (map to your code) | See your hand-built loop in each SDK |
| 36 | OpenAI Agents SDK I | Build an agent with tools |
| 37 | OpenAI Agents SDK II: handoffs | Route between agents |
| 38 | LangChain core (LCEL) | Compose chains & tools |
| 39 | LangGraph I: state graphs | Model an agent as a graph |
| 40 | LangGraph II: cycles & memory | Loops, checkpoints, human-in-the-loop |
| 41 | Semantic Kernel I: plugins | Tools as SK plugins |
| 42 | Semantic Kernel II: planners | Auto-plan over plugins |
| 43 | MCP I: what & why | Tools as a server (Model Context Protocol) |
| 44 | MCP II: build a server | Expose your tools over MCP |
| 45 | Framework trade-offs | Pick the right tool for the job |
| 46 | **Project: same agent, 3 frameworks** | Compare ergonomics head-to-head |

**Install for this phase:**
```bash
pip install openai-agents langgraph langchain semantic-kernel mcp
```
(All are already listed in [../requirements.txt](../requirements.txt).)

↩ [Handbook](../README.md) · ⬅ [Phase 3](../phase-3-tools-memory-planning/README.md) · ➡ [Phase 5 — AutoGen](../phase-5-autogen/README.md)
