# 🧩 No-Code Track — Build Agents with Microsoft Copilot Studio

A **parallel, codeless track** that teaches the *same* agentic concepts as the
90-day code course — but by building real agents in a browser with **Microsoft
Copilot Studio**, no Python required.

Do this track **alongside** the notebooks: each code idea has a no-code twin, so
you understand agents from *both* sides (how they work *and* how to ship them fast
in a managed product).

> Copilot Studio is a graphical, low-code tool for building **agents** and **agent
> flows**. You describe what you want in plain language; it coordinates a language
> model with **instructions**, **knowledge**, **topics**, **tools/actions**, and
> **triggers**, then publishes across channels. *(Source: Microsoft Learn,
> "What is Copilot Studio".)*

---

## Why learn the no-code path too?
- **Speed**: ship a working agent in an afternoon — great for prototypes & business users.
- **Reinforcement**: seeing "knowledge = RAG" and "actions = tools" in a product
  cements the concepts from the code track.
- **Reach**: publish to Microsoft Teams, Microsoft 365 Copilot, websites, and more.
- **Real-world**: most enterprises adopt agents through Copilot Studio first.

## How concepts map across the two tracks

| Code track (notebooks) | Copilot Studio (no-code) |
| --- | --- |
| The LLM call (Phase 1) | The agent's **language model** |
| System prompt | **Instructions** |
| Tools / function calling (Phase 2–3) | **Actions** & **connectors** (prebuilt/custom) |
| Multi-step tool use | **Agent flows** |
| RAG / retrieval (Phase 7) | **Knowledge sources** (websites, files, SharePoint, Dataverse) |
| The agent loop / planner | **Generative orchestration** |
| ReAct / deterministic steps | **Topics** (trigger phrases + nodes) |
| Multi-agent (Phase 6) | **Connected agents** / agent-to-agent |
| Memory & variables | **Variables & entities** |
| Eval, guardrails, safety (Phase 8) | **Test pane, content moderation, analytics, DLP** |
| Deploy (Phase 8) | **Publish to channels** |

## Setup (5 minutes)
1. Go to **<https://copilotstudio.microsoft.com>** and sign in with a work/school
   account. If you don't have a license, start a **free trial** when prompted.
2. No install — it's all in the browser.
3. Want a zero-commitment peek first? Try the demo: **<https://copilotstudio.microsoft.com/tryit>**.

> **Licensing in brief:** a *standalone Copilot Studio subscription* (or trial)
> gives you generative agents; some Microsoft 365 plans include a *Teams plan*
> (classic orchestration, publish to Teams only). You can also build agents that
> *extend Microsoft 365 Copilot*. Check your tenant's licensing with your admin.

> ⚠️ Copilot Studio is a live product — exact button labels may shift. These guides
> describe the **flow** ("Create → describe your agent → add knowledge → test →
> publish"); follow the in-product wording. When in doubt, use the **Create** and
> **Test** panes.

---

## Lessons

| # | Lesson | Maps to code track |
| --- | --- | --- |
| 1 | [What is Copilot Studio?](lesson-01-what-is-copilot-studio.md) | Phase 1 intro |
| 2 | [Create your first agent (describe it)](lesson-02-create-your-first-agent.md) | Day 3 first LLM call |
| 3 | [Knowledge sources = no-code RAG](lesson-03-knowledge-sources.md) | Phase 7 RAG |
| 4 | [Instructions & generative orchestration](lesson-04-instructions-and-orchestration.md) | System prompt + agent loop |
| 5 | [Topics & triggers (guided flows)](lesson-05-topics-and-triggers.md) | ReAct / deterministic steps |
| 6 | [Actions & connectors = no-code tools](lesson-06-actions-and-connectors.md) | Phase 2–3 tools |
| 7 | [Agent flows (multi-step automation)](lesson-07-agent-flows.md) | Multi-step tool use |
| 8 | [Autonomous agents & event triggers](lesson-08-autonomous-agents.md) | Agent autonomy |
| 9 | [Test, safety, analytics & governance](lesson-09-test-safety-governance.md) | Phase 8 eval/guardrails |
| 10 | [Publish & deploy + capstone](lesson-10-publish-and-deploy.md) | Phase 8 deploy |

**→ Start with [Lesson 1](lesson-01-what-is-copilot-studio.md).**
