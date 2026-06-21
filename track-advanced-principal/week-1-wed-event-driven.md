# Week 1 · Wednesday — Event-driven design × planner→worker→critic

**Advanced / Principal Track · ~60–90 min**

> **Discipline × Build:** Event-driven design × a 3-agent pipeline over a queue.

## 🧭 Maps to
- **Course:** Phase 6 (multi-agent orchestration)
- **Concepts:** Multi-agent — **planner→worker→critic**, orchestrator–worker
- **Toolkit:** stdlib `queue.Queue` (or Redis/Service Bus to level up)

## 💡 Engineering tips
- **Events are past-tense facts** ("OrderPlaced"), not commands.
- **Version schemas on day one**; add fields, don't repurpose them.
- **At-least-once delivery ⇒ idempotent consumers.**
- **Hunt hidden ordering assumptions** — the network reorders.

## 🤖 Agentic build
A **planner → worker → critic** pipeline where agents communicate **over a message
bus**: the planner emits tasks, workers consume and produce results, the critic
reviews and can requeue.

## 🧪 Exercise
1. Build the **3-agent pipeline** with a `queue.Queue` (or two queues: tasks + results).
2. Enforce **idempotency keys** on the consumer and a defined **ordering** rule.
3. **Inject a duplicate and an out-of-order message** and **prove correctness**
   (the duplicate is ignored; ordering is restored or provably irrelevant).

**Acceptance:** with duplicates and reordering injected, final output is identical to
the clean run; you can point to the idempotency check that dropped the dupe.

## 🎖️ Principal move
**Draw the boundary diagram** (who owns which event/topic) and **teach one teammate**.

## 📦 Reusable asset
A **message-contract template** (event name, version, schema, idempotency key) and the
**planner/worker/critic** prompts.

## ✅ Done when
- The pipeline runs end-to-end over the bus.
- Duplicate + out-of-order injections do not change the result.
- You produced a boundary diagram.
