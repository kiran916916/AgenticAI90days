"""A tiny deterministic 'LLM' so the earliest lessons run with zero setup.

It does NOT understand language. It follows a couple of keyword rules so you
can focus on agent *structure* (the loop, tools, memory) before plugging in a
real model on Day 4.
"""
from __future__ import annotations

import re


def fake_chat(prompt: str) -> str:
    """Pretend to 'reason' and emit either a TOOL call or an ANSWER."""
    p = prompt.lower()

    if any(word in p for word in ("add", "sum", "plus", "+")):
        numbers = re.findall(r"-?\d+", prompt)
        expr = "+".join(numbers) if numbers else "0"
        return f'TOOL calculator {{"expression": "{expr}"}}'

    if "time" in p or "date" in p:
        return 'TOOL clock {}'

    return "ANSWER I'm a stand-in model. Ask me to add numbers or for the time."
