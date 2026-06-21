# Phase 5 — AutoGen (dedicated) (Days 47–57)

> **Status:** ✅ Built — 11 daily notebooks below (AutoGen 0.7.5). A live preview also runs in
> the **capstone** — see [../phase-9-capstone/avd_imager/reviewer.py](../phase-9-capstone/avd_imager/reviewer.py).

A full track on **Microsoft AutoGen** (`autogen-agentchat`), the framework for
conversational multi-agent systems. You already have it installed (0.7.5).

## Days
| Day | Topic | You'll be able to… |
| --- | --- | --- |
| 47 | AutoGen mental model | Agents that talk to solve tasks |
| 48 | `AssistantAgent` + model client | Your first AutoGen agent |
| 49 | Tools in AutoGen | Give an agent Python tools |
| 50 | `UserProxyAgent` & human-in-the-loop | Insert a human approval step |
| 51 | Two-agent chat | Author + Critic pattern |
| 52 | `RoundRobinGroupChat` | A team that takes turns |
| 53 | Termination conditions | Stop teams cleanly |
| 54 | `SelectorGroupChat` | Let a manager pick the next speaker |
| 55 | Code execution agents | Agents that run code safely |
| 56 | Observability & cost | Trace and budget AutoGen runs |
| 57 | **Project: AutoGen image-review team** | Planner + Builder + Reviewer (ties into the capstone) |

**Install for this phase:**
```bash
pip install "autogen-agentchat" "autogen-ext[openai]"
```
**Try the live preview now:**
```bash
$env:REVIEWER="autogen"   # PowerShell
python phase-9-capstone/avd_imager/agent.py
```

↩ [Handbook](../README.md) · ⬅ [Phase 4](../phase-4-frameworks/README.md) · ➡ [Phase 6 — Multi-Agent](../phase-6-multi-agent/README.md)
