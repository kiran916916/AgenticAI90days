"""Reusable example tools used across many exercises.

A "tool" is just a Python function an agent can choose to call. Keep them
small, well-named, and safe. The calculator below uses an AST evaluator
(NOT `eval`) so a model can never run arbitrary code through it.
"""
from __future__ import annotations

import ast
import datetime as _dt
import operator

# Only these math operations are allowed — anything else is rejected.
_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _safe_eval(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_safe_eval(node.operand))
    raise ValueError("unsupported expression")


def calculator(expression: str) -> str:
    """Evaluate basic arithmetic, e.g. '2 + 3 * 4'. Safe (no code execution)."""
    try:
        return str(_safe_eval(ast.parse(expression, mode="eval").body))
    except Exception as exc:  # noqa: BLE001 - return error as a string for the agent
        return f"Error: {exc}"


def clock(_: str = "") -> str:
    """Return the current local date and time."""
    return _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def word_count(text: str) -> str:
    """Count the words in a piece of text."""
    return str(len(text.split()))


if __name__ == "__main__":
    print(calculator("2 + 3 * 4"))   # 14
    print(clock())
    print(word_count("agents act in a loop"))  # 5
