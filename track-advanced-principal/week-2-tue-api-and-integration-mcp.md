# Week 2 · Tuesday — API & integration design × an MCP tool server

**Advanced / Principal Track · ~75–90 min**

> **Discipline × Build:** API/integration design × an MCP-style tool server exposing
> your capabilities to an agent.

## 🧭 Maps to
- **Course:** Phase 4 (MCP, Days 44–45)
- **Concepts:** Tool use — **function calling**, **JSON-schema tool contracts**, **MCP**
- **Stack:** the `mcp` Python SDK (or hand-roll a JSON-schema tool server)

## 💡 Engineering tips
- **Contract-first**; design the interface before the implementation.
- **Version from v1**; never break a published contract silently.
- **Machine-readable errors** (code + message + hint), so agents can self-correct.
- **Paginate + rate-limit by default.**

## 🤖 Agentic build
An **MCP server** that exposes your tools to any MCP-capable agent — a clean,
portable contract instead of bespoke glue.

## 🧪 Exercise
1. Build an **MCP server with 3 tools**: `repo_search`, `run_tests`, `query_api`.
2. Write **strict JSON schemas** for inputs/outputs and **good error contracts**.
3. **Connect an agent** and **make a deliberately bad call** (wrong arg type/missing
   field) — watch the agent **self-correct** from your structured error.

**Acceptance:** the agent recovers from a malformed call using only the error contract
(no human fix), and each tool validates inputs against its schema.

## 🎖️ Principal move
Identify **one API you own that, cleaned up, unblocks multiple teams** — write the v1
contract.

## 📦 Reusable asset
The **MCP server scaffold** + a **tool-contract template** (name, schema, errors,
pagination, rate limits).

## ✅ Done when
- Three schema-validated tools are served over MCP.
- An agent self-corrects from a structured error.
- You drafted a v1 contract for a real API you own.
