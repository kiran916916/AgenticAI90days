"""A tiny eval harness — golden set + LLM-as-judge + regression gate.

Advanced Track · Week 2 Fri. Score the agents you build and treat the score as a
**regression gate** before shipping (run it in CI).

    from shared.evals import GoldenCase, run_eval, regression_gate
"""
from __future__ import annotations

import json
from dataclasses import dataclass


@dataclass
class GoldenCase:
    name: str
    input: str
    criteria: str   # what a good answer must satisfy


def _strip_json(s):
    s = s.strip().strip("`").strip()
    if s[:4].lower() == "json":
        s = s[4:].strip()
    return s


def llm_judge(question, answer, criteria):
    """Score an answer 0..1 against criteria with an LLM grader. Returns (score, reason)."""
    from shared.llm import chat
    raw = chat(
        [
            {"role": "system", "content":
             'You are a strict grader. Given QUESTION, ANSWER, and CRITERIA, reply '
             'with ONLY JSON: {"score": <0..1>, "reason": "<short>"}.'},
            {"role": "user", "content":
             f"QUESTION:\n{question}\n\nANSWER:\n{answer}\n\nCRITERIA:\n{criteria}"},
        ],
        temperature=0,
    )
    try:
        data = json.loads(_strip_json(raw))
        return float(data["score"]), str(data.get("reason", ""))
    except Exception as exc:  # noqa: BLE001
        return 0.0, f"judge parse error: {exc}"


def run_eval(agent_fn, cases, judge=llm_judge):
    """Run `agent_fn` on each case, judge the output, print + return results."""
    results = []
    for c in cases:
        answer = agent_fn(c.input)
        score, reason = judge(c.input, answer, c.criteria)
        results.append({"name": c.name, "score": score, "reason": reason})
        print(f"{score:4.2f}  {c.name}  — {reason}")
    return results


def regression_gate(results, threshold=0.8):
    """Return True if the mean score clears the bar — fail your CI build otherwise."""
    if not results:
        return False
    avg = sum(r["score"] for r in results) / len(results)
    passed = avg >= threshold
    print(f"\nmean {avg:.2f} vs threshold {threshold:.2f} -> {'PASS' if passed else 'FAIL'}")
    return passed
