"""Reliability primitives for agent tool calls (Advanced Track · Week 1 Tue).

Timeouts + retries + circuit breakers work as a *set* — no single one is enough.
Import these to make any agent loop survive a flaky or slow tool without corrupting
state.

    from shared.reliability import retry, timeout, CircuitBreaker, resilient
"""
from __future__ import annotations

import functools
import random
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as _FutureTimeout


class CircuitOpen(RuntimeError):
    """Raised when a circuit breaker is open and rejecting calls fast."""


class ToolTimeout(TimeoutError):
    """Raised when a call exceeds its time budget."""


def retry(attempts=3, base_delay=0.2, max_delay=2.0, jitter=True,
          exceptions=(Exception,), on_retry=None):
    """Retry with exponential backoff + jitter. Use ONLY for idempotent calls."""
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            delay, last = base_delay, None
            for i in range(1, attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as exc:
                    last = exc
                    if i == attempts:
                        break
                    if on_retry:
                        on_retry(i, exc)
                    sleep = min(delay, max_delay) * ((0.5 + random.random()) if jitter else 1)
                    time.sleep(sleep)
                    delay *= 2
            raise last
        return wrapper
    return deco


def timeout(seconds):
    """Bound a call's wall-clock time. The worker thread can't be force-killed, so
    use this for *latency* protection, not to stop runaway CPU."""
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            with ThreadPoolExecutor(max_workers=1) as ex:
                future = ex.submit(fn, *args, **kwargs)
                try:
                    return future.result(timeout=seconds)
                except _FutureTimeout:
                    raise ToolTimeout(f"{fn.__name__} exceeded {seconds}s")
        return wrapper
    return deco


class CircuitBreaker:
    """Trip after `threshold` consecutive failures; reject fast while open; allow a
    trial call after `reset_after` seconds (half-open)."""

    def __init__(self, threshold=5, reset_after=30.0):
        self.threshold = threshold
        self.reset_after = reset_after
        self._failures = 0
        self._opened_at = None

    @property
    def state(self):
        if self._opened_at is None:
            return "closed"
        if time.time() - self._opened_at >= self.reset_after:
            return "half-open"
        return "open"

    def call(self, fn, *args, **kwargs):
        if self.state == "open":
            raise CircuitOpen(f"circuit open after {self._failures} failures")
        try:
            result = fn(*args, **kwargs)
        except Exception:
            self._failures += 1
            if self._failures >= self.threshold:
                self._opened_at = time.time()
            raise
        self._failures, self._opened_at = 0, None
        return result


class IdempotencyStore:
    """Remember results by key so a retried call doesn't repeat a side effect."""

    def __init__(self):
        self._seen = {}

    def run(self, key, fn, *args, **kwargs):
        if key not in self._seen:
            self._seen[key] = fn(*args, **kwargs)
        return self._seen[key]


def resilient(attempts=3, time_budget=10.0, breaker=None, exceptions=(Exception,)):
    """Compose timeout + retry (+ an optional shared CircuitBreaker) on one tool."""
    def deco(fn):
        timed = timeout(time_budget)(fn)

        @retry(attempts=attempts, exceptions=exceptions)
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            if breaker is not None:
                return breaker.call(timed, *args, **kwargs)
            return timed(*args, **kwargs)
        return wrapper
    return deco


if __name__ == "__main__":
    calls = {"n": 0}

    @resilient(attempts=4, time_budget=2.0)
    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise ConnectionError("boom")
        return "ok"

    print("result:", flaky(), "after", calls["n"], "attempts")
