# Phase 7 — Knowledge & RAG (Days 68–77)

> **Status:** ✅ Built — 10 daily notebooks below. Most run **offline** (tiny built-in embedder).

Give your agent **your** knowledge. From raw embeddings (you already met them in
Day 8) to a vector store, retrieval, and **agentic RAG** (the agent decides when to search).

## Days
| Day | Topic | You'll be able to… |
| --- | --- | --- |
| 68 | RAG, end to end | Explain the retrieve-then-generate loop |
| 69 | Chunking strategies | Split documents well |
| 70 | Embeddings at scale | Embed a corpus |
| 71 | Vector stores (Chroma/FAISS) | Store & query vectors |
| 72 | Retrieval quality | Measure recall & precision |
| 73 | Re-ranking & hybrid search | Combine keyword + vector |
| 74 | Citations & grounding | Make answers traceable |
| 75 | RAG as a tool | Let the agent call "search" |
| 76 | Agentic RAG | Agent decides when/what to retrieve |
| 77 | **Project: chat with your docs** | A grounded Q&A agent |

**Install for this phase:**
```bash
pip install chromadb faiss-cpu
```
(Both are already listed in [../requirements.txt](../requirements.txt).)

↩ [Handbook](../README.md) · ⬅ [Phase 6](../phase-6-multi-agent/README.md) · ➡ [Phase 8 — Production](../phase-8-production/README.md)
