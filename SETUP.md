# Setup — get ready in ~10 minutes

> **Good news:** Days 1–2 need **no API key** — just Python and the VS Code
> Jupyter extension. Set up a model provider before **Day 3**.

---

## 1. Python

Use Python 3.10+ (check with `python --version`).

```powershell
# from the AILearning folder
python -m venv .venv
.\.venv\Scripts\Activate.ps1      # Windows PowerShell
pip install -r requirements.txt
```

> Days 1–2 only use the standard library, so you can even skip the install
> until Day 3 if you want to start immediately.

## 2. Pick a model provider (needed Day 3+)

Copy the example config and edit it:

```powershell
Copy-Item .env.example .env
```

Then choose **one** option inside `.env`:

### Option A — Ollama (free, local, recommended to start)
1. Install from <https://ollama.com>
2. Pull a model: `ollama pull llama3.1`
3. Start it: `ollama serve`
4. In `.env`: `LLM_PROVIDER=ollama`

### Option B — OpenAI
1. Get a key from <https://platform.openai.com>
2. In `.env`: `LLM_PROVIDER=openai` and `OPENAI_API_KEY=sk-...`

### Option C — Azure OpenAI
1. Create a deployment in the Azure portal
2. In `.env`: set `LLM_PROVIDER=azure` and the four `AZURE_OPENAI_*` values

### Verify your provider works
```powershell
python shared/llm.py
```
You should see a one-line greeting from the model.

## 3. How to run a daily lesson

Each day is a single **Jupyter notebook**. To start a day:

1. In VS Code, open the day's notebook, e.g.
   `phase-1-generative-ai/day-01-what-is-generative-ai/day-01-what-is-generative-ai.ipynb`
2. When prompted, **Select Kernel** → your `.venv` (or Python 3).
3. Run cells top to bottom with **Shift+Enter**.

Every notebook is laid out the same way:
| Section | What it's for |
| --- | --- |
| Concept + diagram | The idea, explained, with a visual |
| **▶ Run this first** (Day 3+) | Makes the `shared/` helpers importable |
| 🔬 **Your turn** | **You** fill in the `TODO`s and run the cell |
| 🔒 **Solution** | Worked answer — run it only after you try |

## Troubleshooting
- **`ModuleNotFoundError: openai`** → run `pip install -r requirements.txt`.
- **`Connection refused` (Ollama)** → run `ollama serve` in another terminal.
- **`KeyError: 'OPENAI_API_KEY'`** → fill it in `.env`, or switch `LLM_PROVIDER`.
- **Import `shared` fails** → run the notebook's first **▶ Run this first** cell,
  which puts the repo root on the path. (Opening the `AILearning` folder as your
  VS Code workspace also helps it be found.)
- **No kernel / "Select Kernel"** → pick your `.venv` (or Python 3) interpreter;
  VS Code installs `ipykernel` automatically if prompted.
- **Diagrams show as `mermaid` code** in a notebook cell → that's fine; they render
  on GitHub and in VS Code's Markdown preview. The text always explains the diagram.
