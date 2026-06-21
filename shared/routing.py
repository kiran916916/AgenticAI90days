"""Model routing + response caching to cut tokens/$ (Advanced Track · Week 2 Mon).

Route easy steps to a cheap model and hard steps to a strong one; cache identical
calls so you never pay twice for the same request.

    from shared.routing import routed_chat
    text, cached = routed_chat(messages, difficulty="easy")
"""
from __future__ import annotations

import hashlib
import json
import os

_CACHE: dict[str, str] = {}


def pick_model(difficulty: str) -> str:
    """Map a difficulty label ('easy'/'hard') to a model name (override via env)."""
    easy = os.getenv("ROUTE_EASY_MODEL", os.getenv("OLLAMA_MODEL", "gpt-4o-mini"))
    hard = os.getenv("ROUTE_HARD_MODEL", "gpt-4o")
    return easy if difficulty == "easy" else hard


def _key(messages, model) -> str:
    blob = json.dumps({"m": messages, "model": model}, sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()


def routed_chat(messages, difficulty="easy", use_cache=True, **kwargs):
    """chat() with a routed model + optional cache. Returns (text, was_cached: bool)."""
    from shared.llm import chat
    model = pick_model(difficulty)
    key = _key(messages, model)
    if use_cache and key in _CACHE:
        return _CACHE[key], True
    text = chat(messages, model=model, **kwargs)
    if use_cache:
        _CACHE[key] = text
    return text, False


def cache_stats():
    return {"entries": len(_CACHE)}
