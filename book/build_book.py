"""
Builds a book-style PDF tutorial for the Generative and Agentic AI course.

    python book/build_book.py

Output: book/Generative-and-Agentic-AI-A-Hands-On-Handbook.pdf
Pure Python (ReportLab). No emojis or icons are used anywhere in the book.
"""
import html
import pathlib

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    Preformatted, Table, TableStyle, ListFlowable, ListItem,
)
from reportlab.platypus.tableofcontents import TableOfContents

OUT = pathlib.Path(__file__).resolve().parent / "Generative-and-Agentic-AI-A-Hands-On-Handbook.pdf"

LEFT = RIGHT = 0.9 * inch
TOP = BOTTOM = 0.9 * inch
CONTENT_WIDTH = letter[0] - LEFT - RIGHT

# ---------------------------------------------------------------- styles
styles = getSampleStyleSheet()
body = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica",
                      fontSize=10.5, leading=15, alignment=TA_JUSTIFY, spaceAfter=8)
part_style = ParagraphStyle("Part", parent=styles["Title"], fontName="Helvetica-Bold",
                            fontSize=26, leading=30, spaceBefore=40, spaceAfter=14,
                            textColor=colors.HexColor("#1a1a1a"))
chap_style = ParagraphStyle("Chapter", parent=styles["Heading1"], fontName="Helvetica-Bold",
                            fontSize=17, leading=21, spaceBefore=18, spaceAfter=10,
                            textColor=colors.HexColor("#222222"))
sec_style = ParagraphStyle("Section", parent=styles["Heading2"], fontName="Helvetica-Bold",
                           fontSize=12.5, leading=16, spaceBefore=10, spaceAfter=5,
                           textColor=colors.HexColor("#333333"))
code_style = ParagraphStyle("Code", fontName="Courier", fontSize=8.3, leading=11,
                            textColor=colors.HexColor("#1b1b1b"))
note_style = ParagraphStyle("Note", parent=body, fontName="Helvetica-Oblique",
                            fontSize=10, leading=14, leftIndent=10, textColor=colors.HexColor("#444444"))
practice_style = ParagraphStyle("Practice", parent=body, fontSize=10, leading=14,
                                leftIndent=8, spaceAfter=4)
title_big = ParagraphStyle("TitleBig", parent=styles["Title"], fontName="Helvetica-Bold",
                           fontSize=30, leading=36, alignment=TA_CENTER)
title_sub = ParagraphStyle("TitleSub", parent=styles["Title"], fontName="Helvetica",
                           fontSize=14, leading=20, alignment=TA_CENTER, textColor=colors.HexColor("#555555"))


def esc(text):
    return html.escape(text)


# ---------------------------------------------------------------- doc template
class BookDoc(BaseDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, pagesize=letter, leftMargin=LEFT, rightMargin=RIGHT,
                         topMargin=TOP, bottomMargin=BOTTOM,
                         title="Generative and Agentic AI: A Hands-On Handbook", **kw)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="n")
        self.addPageTemplates([PageTemplate(id="body", frames=[frame], onPage=self._footer)])
        self._page_count_start = 1

    def _footer(self, canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(colors.grey)
        if doc.page > 1:
            canvas.drawCentredString(letter[0] / 2.0, 0.5 * inch, str(doc.page))
            canvas.setFont("Helvetica", 8)
            canvas.drawRightString(letter[0] - RIGHT, 0.5 * inch,
                                   "Generative and Agentic AI")
        canvas.restoreState()

    def afterFlowable(self, flowable):
        key = getattr(flowable, "_toc_level", None)
        if key is not None:
            self.notify("TOCEntry", (key, flowable.getPlainText(), self.page))


def heading(text, level, style):
    p = Paragraph(esc(text), style)
    p._toc_level = level
    return p


def code_block(src):
    pre = Preformatted(esc(src.strip("\n")), code_style)
    tbl = Table([[pre]], colWidths=[CONTENT_WIDTH])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f5f5f5")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return tbl


def bullets(items):
    # Plain dash markers, no bullet glyph or icon.
    item_style = ParagraphStyle("Bullet", parent=body, leftIndent=20,
                                firstLineIndent=-12, spaceAfter=4)
    return [Paragraph("-&nbsp;&nbsp;" + esc(i), item_style) for i in items]


def practice(text):
    return Paragraph("<b>Practice.</b> " + esc(text), practice_style)


def note(text):
    return Paragraph("<i>Note.</i> " + esc(text), note_style)


# ---------------------------------------------------------------- content
# Each chapter: (title, [blocks]). A block is a tuple (kind, payload).
#   ("p", str)  ("sec", str)  ("bul", [..])  ("code", str)  ("note", str)  ("prac", str)

BOOK = []  # list of (part_title, part_intro, [chapters])


def add_part(title, intro, chapters):
    BOOK.append((title, intro, chapters))


# ===== PART I ==========================================================
add_part(
    "Part I. Generative AI Foundations",
    "Before an agent can act, it needs a brain. This part explains how generative language "
    "models work, how to steer them, and how to get reliable, structured output you can build on.",
    [
("Chapter 1. What Generative AI Is", [
("p", "A generative model produces new content one piece at a time. A language model, the kind we use "
      "throughout this book, has learned the statistical shape of human text by reading a very large amount "
      "of it. Given some text, it predicts what is likely to come next. Repeat that prediction in a loop and "
      "you get sentences, code, and answers."),
("p", "It is important to be precise about what this is and is not. The model does not look anything up, "
      "does not reason in the human sense, and has no memory of you between calls. It is a function from text "
      "to a probability distribution over the next token. Everything an agent does is built on top of that one "
      "humble capability, combined with tools, memory, and control logic that you supply."),
("sec", "Why this matters"),
("p", "Understanding the model as a next-token predictor demystifies both its strengths and its failures. It "
      "explains why prompting works, why the model sometimes invents facts, and why giving it tools and "
      "structure is the path to dependable systems."),
("prac", "Write down three tasks you want an agent to do. For each, note whether it needs fresh information, "
         "an action in the world, or only language. That distinction drives the whole design."),
]),
("Chapter 2. Tokens and Next-Token Prediction", [
("p", "Models do not read characters or whole words. They read tokens, which are common chunks of text. A "
      "word like prediction might be one token, while an unusual word may split into several. Costs and context "
      "limits are measured in tokens, so it pays to have a feel for them."),
("p", "At each step the model outputs a score for every possible next token. Those scores become probabilities, "
      "one token is chosen, it is appended to the text, and the process repeats. The loop is the entire mechanism "
      "of generation."),
("code",
 "# A toy of the idea: pick the next word by frequency.\n"
 "import collections, random\n"
 "text = \"the cat sat on the mat the cat ran\".split()\n"
 "nxt = collections.defaultdict(list)\n"
 "for a, b in zip(text, text[1:]):\n"
 "    nxt[a].append(b)\n"
 "word = \"the\"\n"
 "for _ in range(5):\n"
 "    print(word, end=\" \")\n"
 "    word = random.choice(nxt[word])"),
("prac", "Estimate the token count of a paragraph by dividing its character count by about four. Compare with a "
         "real tokenizer later to calibrate your intuition."),
]),
("Chapter 3. Calling a Model", [
("p", "Every later chapter calls a model the same way: send a list of messages, get back a reply. A message has a "
      "role, which is system, user, or assistant, and content. The system message sets behavior, the user message "
      "asks, and the assistant message is the reply."),
("p", "Throughout this book a small helper named chat hides provider differences so the same code runs against a "
      "hosted model or a free local one. The shape never changes."),
("code",
 "from shared.llm import chat\n\n"
 "reply = chat([\n"
 "    {\"role\": \"system\", \"content\": \"You are concise.\"},\n"
 "    {\"role\": \"user\", \"content\": \"Define an agent in one sentence.\"},\n"
 "])\n"
 "print(reply)"),
("note", "Keep provider keys in environment variables, never in code. The appendix shows the setup for hosted and "
         "local models."),
]),
("Chapter 4. Sampling and Decoding", [
("p", "How the next token is chosen shapes the output. Temperature controls randomness. At zero the model takes the "
      "most likely token every time, which is repeatable and good for extraction and code. Higher values add variety, "
      "which helps brainstorming but raises the chance of drift."),
("p", "Top-p, also called nucleus sampling, restricts the choice to the smallest set of tokens whose probabilities "
      "add up to p. Together temperature and top-p trade determinism for creativity. For agents that must be reliable, "
      "low temperature is usually the right default."),
("bul", ["Temperature 0 to 0.3: extraction, classification, tool use, code.",
         "Temperature 0.7 to 1.0: drafting, ideation, varied phrasing.",
         "Set the value deliberately; do not leave it to chance."]),
("prac", "Ask the same question three times at temperature 0, then three times at 1.0. Observe how stability changes."),
]),
("Chapter 5. Prompting: System Messages and Few-Shot", [
("p", "The system message is your strongest lever. It sets role, tone, format, and rules that persist across the "
      "conversation. Specific instructions beat vague ones. Telling the model what to do is better than telling it "
      "what not to do."),
("p", "When a rule is hard to state, show examples instead. A few input and output pairs, called few-shot prompting, "
      "teach format and style by demonstration. Two or three good examples often outperform a paragraph of instructions."),
("code",
 "system = (\n"
 "    \"You classify a message as QUESTION, REQUEST, or COMPLAINT. \"\n"
 "    \"Reply with one word only.\"\n"
 ")\n"
 "examples = [\n"
 "    {\"role\": \"user\", \"content\": \"Where is my order?\"},\n"
 "    {\"role\": \"assistant\", \"content\": \"QUESTION\"},\n"
 "]"),
("prac", "Take a prompt that misbehaves and add two worked examples. Measure whether the format becomes reliable."),
]),
("Chapter 6. Structured Output", [
("p", "Agents need answers a program can read, not prose. Ask the model for JSON that matches a schema, then parse it. "
      "Validating the result turns an unpredictable text generator into a dependable component."),
("p", "Two habits make this robust: state the exact shape you want in the system message, and never trust the output "
      "blindly. Strip stray formatting, parse, and validate. If parsing fails, you can ask again or fall back."),
("code",
 "import json\n"
 "raw = chat([\n"
 "    {\"role\": \"system\", \"content\":\n"
 "        'Reply ONLY JSON: {\"sentiment\": \"pos|neg\", \"score\": 0..1}'},\n"
 "    {\"role\": \"user\", \"content\": \"I love this product.\"},\n"
 "])\n"
 "data = json.loads(raw)\n"
 "print(data[\"sentiment\"], data[\"score\"])"),
("note", "Libraries such as Pydantic let you declare the schema once and validate automatically. Part III returns to this."),
]),
("Chapter 7. Embeddings and Similarity", [
("p", "An embedding turns text into a vector of numbers so that similar meanings sit close together. This is the basis of "
      "search, recommendation, and retrieval. Closeness is measured with cosine similarity, the cosine of the angle "
      "between two vectors."),
("code",
 "def cosine(a, b):\n"
 "    dot = sum(x * y for x, y in zip(a, b))\n"
 "    na = sum(x * x for x in a) ** 0.5\n"
 "    nb = sum(y * y for y in b) ** 0.5\n"
 "    return dot / (na * nb)"),
("p", "Part VII builds a full retrieval system on this idea. For now, the key insight is that meaning becomes geometry, "
      "and geometry is something a computer can compare quickly."),
]),
("Chapter 8. Limitations and Safety", [
("p", "A language model can state false things confidently, a behavior called hallucination. It can be wrong about recent "
      "events, arithmetic, and anything not well represented in its training. It can also be steered by malicious text. "
      "Treating output as a draft to be verified, not as truth, is the professional stance."),
("bul", ["Ground answers in retrieved sources and show citations.",
         "Give the model tools for facts and math rather than trusting it.",
         "Validate output at the boundary before acting on it.",
         "Treat any text from tools or the web as untrusted input."]),
("p", "These are not afterthoughts. The strongest agents in this book are the ones with the most disciplined boundaries, "
      "and the capstone makes safety a hard gate rather than a hope."),
]),
    ])

# ===== PART II =========================================================
add_part(
    "Part II. From Generative to Agentic",
    "An agent is a program that uses a model in a loop to pursue a goal, taking actions through tools and adjusting "
    "based on results. This part builds one from first principles so every later framework feels familiar.",
    [
("Chapter 9. What an Agent Is", [
("p", "A plain model call is a single question and a single answer. An agent wraps that call in a loop: it observes the "
      "situation, decides what to do, acts through a tool, observes the result, and repeats until the goal is met. The "
      "model supplies the decision; you supply the loop, the tools, and the stopping rule."),
("p", "This definition is liberating. You do not need a special library to have an agent. You need a model, a few "
      "functions it can call, and the discipline to manage the loop. Everything else is convenience."),
]),
("Chapter 10. The Agent Loop", [
("p", "The loop has four moves: observe, decide, act, repeat. A step budget prevents it from running forever, and a clear "
      "finish action lets it stop when done. The skeleton below captures the entire idea in a dozen lines."),
("code",
 "def agent_loop(goal, tools, max_steps=6):\n"
 "    context = goal\n"
 "    for _ in range(max_steps):\n"
 "        decision = decide(context)          # model picks a tool or finishes\n"
 "        if decision.action == \"finish\":\n"
 "            return decision.answer\n"
 "        result = tools[decision.action](decision.arg)\n"
 "        context += f\"\\nObservation: {result}\"\n"
 "    return \"stopped: out of steps\""),
("prac", "Draw the loop for a task you care about. Name the tools and the condition under which the agent should stop."),
]),
("Chapter 11. Tools as Functions", [
("p", "A tool is just a function the agent may call. Keep tools small, well named, and safe. A calculator that evaluates "
      "arithmetic should never run arbitrary code; build it on a parser, not on a blanket evaluation of strings."),
("code",
 "import ast, operator\n"
 "OPS = {ast.Add: operator.add, ast.Sub: operator.sub,\n"
 "       ast.Mult: operator.mul, ast.Div: operator.truediv}\n\n"
 "def calc(node):\n"
 "    if isinstance(node, ast.Constant):\n"
 "        return node.value\n"
 "    if isinstance(node, ast.BinOp):\n"
 "        return OPS[type(node.op)](calc(node.left), calc(node.right))\n"
 "    raise ValueError(\"unsupported\")"),
("note", "A safe tool is a security boundary. The calculator above cannot be tricked into executing code, no matter what "
         "the model asks."),
]),
("Chapter 12. Native Tool Calling", [
("p", "Production models have a built-in way to call tools. You pass a list of tool schemas, and instead of plain text the "
      "model replies with structured tool calls. You run the tool, return the result, and let it continue. Every framework "
      "in Part IV does exactly this under the hood."),
("code",
 "from shared.llm import chat_with_tools\n"
 "TOOLS = [{\"type\": \"function\", \"function\": {\n"
 "    \"name\": \"calculator\",\n"
 "    \"parameters\": {\"type\": \"object\",\n"
 "        \"properties\": {\"expression\": {\"type\": \"string\"}},\n"
 "        \"required\": [\"expression\"]}}}]\n"
 "msg = chat_with_tools([{\"role\": \"user\", \"content\": \"7*6?\"}], TOOLS)\n"
 "print(msg.tool_calls)"),
]),
("Chapter 13. The ReAct Pattern", [
("p", "ReAct stands for reasoning and acting. The agent writes a short thought, chooses an action, observes the result, and "
      "repeats. Making the model emit JSON each turn keeps parsing reliable and makes the reasoning visible, which is a gift "
      "when debugging."),
("code",
 "system = (\n"
 "  'Reply each turn with ONLY JSON: '\n"
 "  '{\"thought\":\"...\",\"action\":\"calculator|finish\",\"action_input\":\"...\"}'\n"
 ")"),
("p", "ReAct is the most influential agent pattern, and you can implement it with nothing more than the plain chat helper. "
      "Once you have built it by hand, every framework that offers it will feel like a convenience rather than a mystery."),
]),
("Chapter 14. Memory", [
("p", "A model has no memory between calls, so the agent must supply it. Short-term memory is a rolling buffer of recent "
      "turns. When the buffer grows past a budget, summarize the oldest turns into a running note and keep the most recent "
      "ones verbatim. This keeps the agent within the context limit without forgetting the thread."),
("bul", ["Working memory: a scratchpad for the current task, cleared when done.",
         "Long-term memory: facts that persist across tasks.",
         "Budgeted memory: summarize the old, keep the recent."]),
]),
("Chapter 15. Reflection", [
("p", "One of the cheapest ways to improve quality is to let the agent check its own work. It drafts an answer, critiques it "
      "against the goal, and revises once if needed. This single extra step catches many errors and is the seed of the "
      "critic pattern you will scale up with multiple agents later."),
("code",
 "draft = chat([{\"role\": \"user\", \"content\": goal}])\n"
 "critique = chat([\n"
 "    {\"role\": \"system\", \"content\": \"Reply OK if good, else one fix.\"},\n"
 "    {\"role\": \"user\", \"content\": f\"Goal: {goal}\\nAnswer: {draft}\"}])\n"
 "final = draft if critique.startswith(\"OK\") else revise(draft, critique)"),
]),
    ])

# ===== PART III ========================================================
add_part(
    "Part III. Tools, Memory, and Planning",
    "A capable agent needs safe typed tools, durable memory, and the ability to plan before it acts. This part hardens the "
    "hand-built agent into something you could trust with real work.",
    [
("Chapter 16. Typed Tools and a Registry", [
("p", "Validate tool inputs before running them. A schema library such as Pydantic lets you declare the expected fields once "
      "and reject bad input automatically, while also producing the JSON schema the model needs for native calling. As tools "
      "multiply, a registry that maps names to functions becomes the one place to add validation, authorization, and tracing."),
("code",
 "from pydantic import BaseModel, ValidationError\n\n"
 "class WeatherArgs(BaseModel):\n"
 "    city: str\n"
 "    units: str = \"celsius\"\n\n"
 "def get_weather(args: dict):\n"
 "    try:\n"
 "        a = WeatherArgs(**args)\n"
 "    except ValidationError as e:\n"
 "        return f\"Error: {e.errors()[0]['msg']}\"\n"
 "    return f\"Weather in {a.city}: 21 {a.units}\""),
]),
("Chapter 17. Tool Authorization and Least Privilege", [
("p", "The most important security idea for agents is deny by default. An agent identity holds a small set of scopes, and a "
      "tool runs only if its required scope is granted. High-impact actions require human approval, and every decision is "
      "written to an audit trail. This single control prevents a confused or manipulated agent from doing damage."),
("code",
 "from shared.policy import PolicyGate, PolicyDenied\n\n"
 "gate = PolicyGate(\n"
 "    tool_scopes={\"read_logs\": \"logs:read\", \"deploy\": \"prod:deploy\"},\n"
 "    granted={\"logs:read\"},          # may read logs, not deploy\n"
 "    high_blast={\"deploy\"},\n"
 "    approver=lambda tool, args: False)\n\n"
 "try:\n"
 "    gate.authorize(\"deploy\")\n"
 "except PolicyDenied as e:\n"
 "    print(\"blocked:\", e)"),
("p", "Grant the narrowest set of scopes that still lets the agent do its job. When in doubt, deny and require approval. The "
      "capstone in Part IX makes this gate the centerpiece of a real workflow."),
]),
("Chapter 18. Persistent and Summarized Memory", [
("p", "Long-term memory should survive a restart. A small SQLite table is enough, and it teaches an important habit: always "
      "use parameterized queries so user content cannot become SQL. When history grows too large for the context window, "
      "summarize the oldest turns and keep the recent ones."),
("code",
 "import sqlite3\n"
 "db = sqlite3.connect(\":memory:\")\n"
 "db.execute(\"CREATE TABLE mem (id INTEGER PRIMARY KEY, role TEXT, content TEXT)\")\n"
 "db.execute(\"INSERT INTO mem (role, content) VALUES (?, ?)\",\n"
 "           (\"user\", \"remember my name is Sam\"))   # parameterized, safe\n"
 "db.commit()"),
]),
("Chapter 19. Planning and Re-Planning", [
("p", "Hard goals become tractable when the agent breaks them into steps first, then executes the steps with results flowing "
      "from one to the next. Plans meet reality and break, so a robust agent notices a failed step and asks the planner for a "
      "revised plan for the remaining work instead of charging ahead."),
("code",
 "def plan(goal):\n"
 "    raw = chat([\n"
 "        {\"role\": \"system\", \"content\":\n"
 "            \"Return ONLY a JSON array of 2-5 step strings.\"},\n"
 "        {\"role\": \"user\", \"content\": goal}])\n"
 "    return json.loads(raw)"),
("prac", "Give the planner a goal with a step that will fail, and confirm it produces a sensible replacement plan."),
]),
("Chapter 20. Tracing and Evaluation", [
("p", "You cannot improve what you cannot see or measure. Tracing records one span per tool call with timing, so you can find "
      "the slow or expensive step. Evaluation pins behavior with a set of golden cases and a regression gate that fails the "
      "build when quality drops. These two practices turn agent development from guesswork into engineering."),
("code",
 "from shared.tracing import Tracer\n"
 "tr = Tracer()\n"
 "with tr.span(\"calculator\"):\n"
 "    calculator(\"2+2\")\n"
 "tr.print_trace()"),
]),
    ])

# ===== PART IV =========================================================
add_part(
    "Part IV. Agent Frameworks",
    "Having built agents by hand, you can now read any framework, because they all express the same ideas: a loop, tools, "
    "memory, and control flow. This part maps your code onto the major options.",
    [
("Chapter 21. Why Frameworks", [
("p", "Frameworks do not add new concepts; they add names, plumbing, and an ecosystem. Your agent loop becomes a runner or a "
      "graph, your tool function becomes a decorated function or a node, and your agent class becomes their agent type. Knowing "
      "the mapping means you can move between frameworks without relearning the fundamentals."),
("bul", ["The loop becomes a runner, a graph, or a group chat.",
         "A tool becomes a decorated function or a plugin.",
         "Memory becomes a checkpointer or a managed store.",
         "Handoffs become edges or routing."]),
]),
("Chapter 22. The OpenAI Agents SDK", [
("p", "This SDK packages the loop into an Agent and a Runner, and turns any typed function into a tool with a decorator. "
      "Handoffs let one agent route to a more specialized one, which is the first taste of multi-agent design."),
("code",
 "from agents import Agent, Runner, function_tool\n\n"
 "@function_tool\n"
 "def add(a: int, b: int) -> int:\n"
 "    return a + b\n\n"
 "agent = Agent(name=\"Math\", instructions=\"Use tools.\", tools=[add])\n"
 "print(Runner.run_sync(agent, \"What is 21 + 21?\").final_output)"),
]),
("Chapter 23. LangChain and LangGraph", [
("p", "LangChain composes components with a pipe operator: a prompt feeds a model feeds a parser. LangGraph models an agent as "
      "a graph whose nodes transform a shared state and whose edges set the order. Graphs make loops and branching explicit, "
      "and a checkpointer gives the graph memory across calls."),
("code",
 "from typing import TypedDict\n"
 "from langgraph.graph import StateGraph, START, END\n\n"
 "class State(TypedDict):\n"
 "    topic: str\n"
 "    joke: str\n\n"
 "def make(state):\n"
 "    return {\"joke\": f\"Why did the {state['topic']} cross the road?\"}\n\n"
 "g = StateGraph(State)\n"
 "g.add_node(\"make\", make)\n"
 "g.add_edge(START, \"make\"); g.add_edge(\"make\", END)\n"
 "print(g.compile().invoke({\"topic\": \"chicken\"})[\"joke\"])"),
]),
("Chapter 24. Semantic Kernel", [
("p", "Semantic Kernel, common in enterprise and .NET settings, treats tools as plugins whose methods carry a decorator. With "
      "automatic function calling enabled, the kernel lets the model pick and invoke plugin functions, which is its version of "
      "the ReAct loop you built by hand."),
("code",
 "from semantic_kernel import Kernel\n"
 "from semantic_kernel.functions import kernel_function\n\n"
 "class MathPlugin:\n"
 "    @kernel_function(name=\"add\", description=\"Add two integers\")\n"
 "    def add(self, a: int, b: int) -> str:\n"
 "        return str(a + b)\n\n"
 "kernel = Kernel()\n"
 "kernel.add_plugin(MathPlugin(), plugin_name=\"math\")"),
]),
("Chapter 25. The Model Context Protocol", [
("p", "The Model Context Protocol, or MCP, standardizes how agents discover and call tools that live in a separate server. You "
      "write a tool once and any MCP-aware client can use it. A minimal server is a few lines, and treating tools as a reusable "
      "service is a powerful organizing idea."),
("code",
 "from mcp.server.fastmcp import FastMCP\n"
 "mcp = FastMCP(\"demo\")\n\n"
 "@mcp.tool()\n"
 "def add(a: int, b: int) -> int:\n"
 "    return a + b\n\n"
 "# Serve over stdio with:  mcp.run()"),
]),
    ])

# ===== PART V ==========================================================
add_part(
    "Part V. AutoGen",
    "AutoGen frames problem solving as a conversation between agents. This part covers its model, its teams, and a security "
    "review team that mirrors the capstone.",
    [
("Chapter 26. The AutoGen Model", [
("p", "In AutoGen you compose specialized agents that talk to each other to solve a task. The pieces map directly onto what you "
      "already know: an assistant agent is your agent class, a tool is a function you pass in, a critic is a second agent, and a "
      "human approval step is a user proxy agent. The framework manages the turn taking."),
]),
("Chapter 27. Agents, Tools, and Teams", [
("p", "The smallest program is one assistant agent backed by a model client. Pass typed functions as tools and the framework "
      "exposes them to the model. Put two or more agents in a team and they take turns; an author and a critic, for example, can "
      "alternate until the work is approved."),
("code",
 "from autogen_agentchat.agents import AssistantAgent\n"
 "from autogen_ext.models.openai import OpenAIChatCompletionClient\n\n"
 "client = OpenAIChatCompletionClient(model=\"gpt-4o-mini\")\n"
 "agent = AssistantAgent(\"assistant\", model_client=client,\n"
 "                       system_message=\"Be concise.\")\n"
 "result = await agent.run(task=\"Say hello in five words.\")\n"
 "print(result.messages[-1].content)"),
("note", "AutoGen calls are asynchronous. In a notebook use top-level await; in a script wrap the call in asyncio.run."),
]),
("Chapter 28. Termination and Selection", [
("p", "A team that never stops is a bug. Termination conditions end the chat when a keyword appears or after a maximum number of "
      "messages, and conditions combine with simple operators. A round-robin team takes turns in a fixed order, while a selector "
      "team lets a manager model choose who speaks next based on context."),
("code",
 "from autogen_agentchat.conditions import (\n"
 "    TextMentionTermination, MaxMessageTermination)\n"
 "term = TextMentionTermination(\"APPROVE\") | MaxMessageTermination(6)"),
]),
("Chapter 29. A Two-Key Review Team", [
("p", "A powerful pattern pairs a builder that proposes work with a reviewer that must approve it. The reviewer replies APPROVE "
      "only when its checks pass, otherwise it names the exact risk to fix. This is the two-key control that the capstone uses to "
      "guard image publication, expressed as a conversation."),
("code",
 "builder = AssistantAgent(\"builder\", model_client=client,\n"
 "    system_message=\"Propose a config.\")\n"
 "reviewer = AssistantAgent(\"reviewer\", model_client=client,\n"
 "    system_message=\"Reply APPROVE if safe, else name the risk.\")"),
]),
    ])

# ===== PART VI =========================================================
add_part(
    "Part VI. Multi-Agent Orchestration",
    "When one agent is not enough, a team can help, but only when the work has distinct skills or parallel parts. This part covers "
    "the patterns that make teams work without runaway cost.",
    [
("Chapter 30. When to Use Multiple Agents", [
("p", "More agents mean more cost, more latency, and more ways to fail. Reach for a team only when a task has genuinely distinct "
      "skills or independent subtasks. Very often a single well-equipped agent with good tools is the better choice. Decide "
      "deliberately rather than by fashion."),
]),
("Chapter 31. Supervisors and Specialists", [
("p", "A supervisor does not do the work; it routes each task to the right specialist. A rule-based router is fast, free, and easy "
      "to debug, and you can replace it with a model-based router later. Specialists are focused agents that are simpler to test and "
      "reason about than one agent that tries to do everything."),
("code",
 "def route(task):\n"
 "    t = task.lower()\n"
 "    if any(w in t for w in [\"add\", \"sum\", \"+\"]):\n"
 "        return \"math\"\n"
 "    if any(w in t for w in [\"write\", \"draft\"]):\n"
 "        return \"writing\"\n"
 "    return \"general\""),
]),
("Chapter 32. Shared State and Debate", [
("p", "A blackboard is shared memory that every agent can read and write, a simple way to coordinate without direct messaging. A "
      "debate pattern pits a proposer against a critic, with a judge to decide, which can beat a single agent that only agrees with "
      "itself. Both are extensions of the reflection idea from Part II."),
]),
("Chapter 33. Parallelism and Budgets", [
("p", "Independent specialists can run at the same time, and a fan-in step merges their outputs. Whatever the topology, a budget that "
      "caps steps and tokens is non-negotiable, because a chattering team can run up a bill quickly. Stop cleanly when the budget is "
      "spent."),
("code",
 "from concurrent.futures import ThreadPoolExecutor\n"
 "def gather(task, specialists):\n"
 "    with ThreadPoolExecutor() as ex:\n"
 "        futures = {n: ex.submit(f, task) for n, f in specialists.items()}\n"
 "        return {n: f.result() for n, f in futures.items()}"),
]),
    ])

# ===== PART VII ========================================================
add_part(
    "Part VII. Knowledge and Retrieval-Augmented Generation",
    "To answer from your own knowledge, retrieve relevant text and put it in the prompt. This part builds retrieval from raw vectors "
    "to an agent that decides when to search.",
    [
("Chapter 34. The Retrieval Loop", [
("p", "Retrieval-augmented generation, or RAG, replaces the hope that a model memorized a fact with a reliable process: embed the "
      "question, find the most similar chunks of your documents, and put them in the prompt so the answer is grounded. The model "
      "generates, but the facts come from your sources."),
]),
("Chapter 35. Chunking and Embeddings", [
("p", "You cannot embed a whole book as a single vector, so you split it into chunks, with a little overlap so a fact that straddles "
      "a boundary still lands in at least one chunk. Each chunk becomes an embedding. Chunk size and overlap are tuning knobs that "
      "trade precision against recall."),
("code",
 "def chunk(text, size=400, overlap=40):\n"
 "    step = size - overlap\n"
 "    return [text[i:i + size] for i in range(0, len(text), step)]"),
]),
("Chapter 36. Vector Stores and Retrieval Quality", [
("p", "A vector store keeps text and its embedding together and finds the nearest by cosine similarity. A few lines of code capture "
      "the idea that libraries such as Chroma and FAISS scale up. Measure quality with precision and recall: of what you returned, how "
      "much was relevant, and of all relevant items, how much did you find."),
("code",
 "class VectorStore:\n"
 "    def __init__(self):\n"
 "        self.items = []\n"
 "    def add(self, id, text, emb):\n"
 "        self.items.append((id, text, emb))\n"
 "    def search(self, qe, k=2):\n"
 "        scored = sorted(\n"
 "            ((cosine(qe, e), i, t) for i, t, e in self.items),\n"
 "            reverse=True)\n"
 "        return scored[:k]"),
]),
("Chapter 37. Citations and Agentic RAG", [
("p", "A grounded answer says where each claim came from, so return source identifiers with the answer and let a reader verify. A "
      "naive system always searches; an agentic one lets the model decide whether a question needs retrieval at all, searching for "
      "company facts but answering simple questions directly. The decision itself is a small agent."),
]),
    ])

# ===== PART VIII =======================================================
add_part(
    "Part VIII. Production",
    "The difference between a demo and a product is evaluation, observability, guardrails, security, cost control, and a way to serve "
    "the agent. This part covers each.",
    [
("Chapter 38. Evaluation and Continuous Integration Gates", [
("p", "Ship behind a golden set. A harness runs the agent on fixed cases, scores each, and a regression gate fails the build when the "
      "mean drops below a threshold. For open-ended answers, a model can act as a grader against stated criteria, used sparingly. A "
      "red build is far cheaper than a bad release."),
("code",
 "from shared.evals import GoldenCase, run_eval, regression_gate\n"
 "cases = [GoldenCase(\"math\", \"2+2\", \"4\")]\n"
 "results = run_eval(my_agent, cases, judge=keyword_judge)\n"
 "regression_gate(results, threshold=0.8)"),
]),
("Chapter 39. Tracing and Observability", [
("p", "In production you must see every step. Record spans for each tool call and model call, capture timing and token usage, and "
      "export them to a system you can query. The local tracer in this book records the same data that tools such as Langfuse and "
      "OpenTelemetry collect at scale."),
]),
("Chapter 40. Guardrails and Prompt-Injection Defense", [
("p", "Validate at the boundaries. Block disallowed input before it reaches the model and check output before it reaches the user. "
      "The most important agent vulnerability is prompt injection, where text returned by a tool or web page instructs the model to "
      "misbehave. Treat all such text as untrusted data, scan it, and quarantine anything suspicious."),
("code",
 "INJECTION = [\"ignore previous\", \"disregard above\", \"system:\"]\n"
 "def is_injection(text):\n"
 "    low = text.lower()\n"
 "    return any(p in low for p in INJECTION)\n\n"
 "def sanitize(text):\n"
 "    return \"[quarantined]\" if is_injection(text) else text"),
]),
("Chapter 41. Identity, Budgets, and Serving", [
("p", "Give each agent identity the smallest set of scopes it needs and require approval for high-impact actions, exactly as in Part "
      "III. Cap tokens and time with a hard budget. Finally, wrap the agent in an HTTP service so other applications can call it, with "
      "typed requests and automatic documentation."),
("code",
 "from fastapi import FastAPI\n"
 "from pydantic import BaseModel\n"
 "app = FastAPI()\n\n"
 "class Query(BaseModel):\n"
 "    question: str\n\n"
 "@app.post(\"/chat\")\n"
 "def chat_endpoint(q: Query):\n"
 "    return {\"answer\": run_agent(q.question)}"),
]),
    ])

# ===== PART IX =========================================================
add_part(
    "Part IX. Capstone: An Agentic Image-Build Orchestrator",
    "The capstone brings every idea together in a realistic workflow: an agent that builds a virtual desktop image on a cloud, gated "
    "by security checks and a second reviewer that must sign off before anything is published.",
    [
("Chapter 42. The Orchestrator", [
("p", "The capstone reads a specification, plans the steps to build an image, and runs them through a sequence of tools: create the "
      "resource group and identity, define the image, run the build, monitor it, scan it, and only then publish. The orchestrator is "
      "the agent loop from Part II, wearing a domain. It uses tracing to show its work and reliability wrappers to survive a flaky "
      "step."),
("p", "Crucially, the tools run in a dry-run mode by default, printing the command they would issue and a simulated result. This makes "
      "the whole system safe to run and study, and it mirrors how you should develop any agent that touches real infrastructure: prove "
      "the logic before you grant it real power."),
]),
("Chapter 43. Security Gates and Two-Key Review", [
("p", "Before publishing, the orchestrator scans the image for vulnerable or outdated applications and missing updates. If the scan "
      "finds a high-severity issue, publication is blocked. This is a hard gate, not a warning. The example specifications include one "
      "compliant image that passes and one vulnerable image that is correctly stopped."),
("p", "Passing the scan is necessary but not sufficient. A second, independent reviewer must also approve, re-checking the critical "
      "posture and adding advisories. Only when both the automated scan and the reviewer agree does the agent proceed, and the highest "
      "impact action, updating the host pool, still requires a human. Least privilege, defense in depth, and human oversight, all in one "
      "workflow."),
("p", "If you take one lesson from the capstone, let it be this: the value of an agent is bounded by how well you constrain it. The most "
      "trustworthy systems are the ones with the most disciplined gates."),
]),
    ])

# ===== Appendices ======================================================
add_part(
    "Appendix A. Setup and Providers",
    "The course code runs against a hosted model or a free local one, selected by an environment variable so the same code works "
    "everywhere.",
    [
("A.1 Choosing a Provider", [
("p", "A single helper named chat reads a provider setting and routes to the right backend. Set the provider and its credentials in "
      "environment variables. The earliest lessons run with no provider at all, because they teach agent structure with pure Python."),
("bul", ["Hosted model: set the provider to the hosted option and supply an API key.",
         "Local model: run a local server and point the helper at it; no key or cost.",
         "Never commit keys; keep them in environment variables or a local file that is ignored by version control."]),
]),
("A.2 Running the Lessons", [
("p", "Each lesson is a notebook with a short concept, a runnable bootstrap cell, an exercise with blanks to fill, and a solution. Run "
      "the bootstrap cell first; it puts the shared toolkit on the path. Many lessons in the later parts run entirely offline."),
]),
    ])

add_part(
    "Appendix B. The Shared Toolkit",
    "A small set of reusable modules underpins the whole course, so every lesson speaks the same language.",
    [
("B.1 Modules", [
("bul", ["A model helper that hides provider differences behind one chat function.",
         "A set of safe example tools, including an arithmetic calculator built on a parser.",
         "Reliability helpers for retries, timeouts, and circuit breakers.",
         "A policy gate for deny-by-default tool authorization with an audit trail.",
         "A tracer that records one span per tool call.",
         "An evaluation harness with golden cases and a regression gate."]),
("p", "These modules are not magic. Each is small enough to read in a few minutes, and reading them is the fastest way to understand "
      "how the lessons fit together. The agent you build by hand and the frameworks you adopt later both rest on the same handful of "
      "ideas captured here."),
]),
    ])


# ---------------------------------------------------------------- assemble
def build():
    story = []

    # Title page
    story += [Spacer(1, 2.0 * inch),
              Paragraph("Generative and Agentic AI", title_big),
              Spacer(1, 0.2 * inch),
              Paragraph("A Hands-On Handbook", title_sub),
              Spacer(1, 0.5 * inch),
              Paragraph("From next-token prediction to safe, multi-agent systems", title_sub),
              Spacer(1, 2.6 * inch),
              Paragraph("A self-paced tutorial companion to the 90-day course", title_sub),
              PageBreak()]

    # Table of contents
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("toc0", fontName="Helvetica-Bold", fontSize=12, leading=18,
                       spaceBefore=6),
        ParagraphStyle("toc1", fontName="Helvetica", fontSize=10, leading=15, leftIndent=16),
    ]
    story += [Paragraph("Contents", chap_style), Spacer(1, 0.1 * inch), toc, PageBreak()]

    # Parts and chapters
    for part_title, intro, chapters in BOOK:
        story.append(heading(part_title, 0, part_style))
        story.append(Paragraph(esc(intro), body))
        story.append(Spacer(1, 0.1 * inch))
        for chap_title, blocks in chapters:
            story.append(heading(chap_title, 1, chap_style))
            for kind, payload in blocks:
                if kind == "p":
                    story.append(Paragraph(esc(payload), body))
                elif kind == "sec":
                    story.append(Paragraph(esc(payload), sec_style))
                elif kind == "bul":
                    story.extend(bullets(payload))
                    story.append(Spacer(1, 4))
                elif kind == "code":
                    story.append(code_block(payload))
                    story.append(Spacer(1, 6))
                elif kind == "note":
                    story.append(note(payload))
                elif kind == "prac":
                    story.append(practice(payload))
            story.append(Spacer(1, 0.08 * inch))
        story.append(PageBreak())

    doc = BookDoc(str(OUT))
    doc.multiBuild(story)
    print("wrote", OUT.name, "-", OUT.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    build()
