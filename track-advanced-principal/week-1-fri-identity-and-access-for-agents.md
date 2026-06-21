# Week 1 · Friday ⭐ — Identity & access FOR AGENTS

**Advanced / Principal Track · ~75–90 min · your space**

> **Discipline × Build:** Identity & access for agents × an agent with explicitly
> scoped tool permissions + a deny-by-default policy engine.

## 🧭 Maps to
- **Course:** Phase 8 (safety/guardrails)
- **Concepts:** Identity & safety — **per-agent identity**, **least-privilege
  short-lived creds**, **human-in-the-loop**, **full action audit**
- **Toolkit:** [`shared/policy.py`](../shared/policy.py) ⭐ — `PolicyGate`, `AuditLog`

## 💡 Engineering tips
- **Agents get their own identity** — never borrow a human's token.
- Issue **short-lived, least-privilege, scoped** credentials per agent/task.
- **Human-in-the-loop for high-blast actions** (delete, pay, publish, grant).
- Keep a **full audit trail** — every tool call, decision, and reason.

## 🤖 Agentic build
An agent whose tools are gated by a **deny-by-default policy engine**: each tool
declares a required **scope**; the agent identity holds a minimal **granted** set;
high-blast tools require **human approval**; everything is **logged**.

## 🧪 Exercise
1. Use `PolicyGate` to **authorize every tool call against scopes** before it runs
   (`gate.guard("tool_name")` or `gate.authorize(...)`).
2. Grant the agent the **minimum** scopes; mark destructive tools as `high_blast`
   (require an `approver` callback).
3. **Log every action** via the built-in `AuditLog`.
4. **Red-team your own agent:** prompt it to overstep (call an ungranted or
   destructive tool) and **watch the gate hold** — then confirm the audit trail shows
   the denial.

**Acceptance:** no ungranted tool ever executes; every high-blast call pauses for
approval; the audit log reconstructs exactly what was attempted, allowed, and denied.

## 🎖️ Principal move
Write a **one-pager: "How should our org handle agent identity?"** (identity model,
scope issuance, approval gates, audit/retention, revocation).

## 📦 Reusable asset
The **scoped-tool policy pattern** + the **agent-identity one-pager** — both
high-leverage in your IAM wheelhouse.

## ✅ Done when
- Red-team attempts to overstep are all denied and logged.
- High-blast tools route through the human gate.
- Your agent-identity one-pager is written and shareable.
