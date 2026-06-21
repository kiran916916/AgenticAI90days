# No-Code Lesson 2 — Create your first agent (just describe it)

**Track: Build Agents with Copilot Studio · ~25 min · browser only**

## 🎯 Objective
Build a working agent in minutes using **generative authoring** — describe it in
plain language and let Copilot Studio scaffold it.

## 🔗 Maps to the code track
This is your **Day 3 "first LLM call"** moment — but instead of `chat()`, you get a
full conversational agent with a brain already wired up.

## 🧠 Concept
Copilot Studio can build an agent from a **description**. You tell it the agent's
purpose, audience, and tone; it drafts a **name, instructions, and starter
knowledge/topics**. You then refine in the **authoring canvas** and chat with it in
the **Test** pane on the right — the tightest build-test loop in the product.

## 🛠️ Do it
1. In the maker portal, choose **Create → New agent**.
2. In the describe box, type something like:
   > *"You are 'Trailhead Helper', a friendly assistant for a hiking-gear store.
   > Answer questions about products, store hours, and returns. Be concise and
   > upbeat."*
3. Continue through the prompts (name, icon). Let it create the agent.
4. Open the **Test** pane and chat: *"What are your store hours?"*,
   *"Do you sell waterproof boots?"*
5. Find the **Instructions** field and tweak the tone; re-test and notice the change.

## ✅ Done when
- Your agent responds in the Test pane.
- Editing **Instructions** visibly changes its behavior (your system-prompt lever).

## 📝 Reflect
1. How is the **Instructions** box like the `system` message from Phase 1, Day 5?
2. The agent answered some things with no topic defined — where did those answers
   come from? (Foreshadows Lesson 3: knowledge + generative answers.)

## 🔭 Next
Lesson 3: ground the agent in real content — no-code RAG.
