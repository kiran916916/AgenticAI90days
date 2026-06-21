"""Minimal agent tracing — one span per tool call, with attributes.

Advanced Track · Week 2 Wed. Zero dependencies; swap for OpenTelemetry/Langfuse in
production. Record token & latency attributes so you can see cost/latency per step.

    from shared.tracing import Tracer
    tr = Tracer()
    with tr.span("calculator", tokens=0) as s:
        ...
    tr.print_trace()
"""
from __future__ import annotations

import functools
import time
from dataclasses import dataclass, field


@dataclass
class Span:
    name: str
    start: float
    end: float = 0.0
    attributes: dict = field(default_factory=dict)

    @property
    def duration_ms(self):
        return round((self.end - self.start) * 1000, 1)


class Tracer:
    def __init__(self):
        self.spans: list[Span] = []

    def span(self, name, **attributes):
        tracer = self

        class _Ctx:
            def __enter__(self):
                self.s = Span(name=name, start=time.perf_counter(),
                              attributes=dict(attributes))
                return self.s

            def __exit__(self, exc_type, exc, tb):
                self.s.end = time.perf_counter()
                if exc_type:
                    self.s.attributes["error"] = repr(exc)
                tracer.spans.append(self.s)
                return False
        return _Ctx()

    def traced(self, name=None):
        """Decorator that opens a span around a tool call."""
        def deco(fn):
            label = name or fn.__name__
            @functools.wraps(fn)
            def wrapper(*args, **kwargs):
                with self.span(label) as s:
                    result = fn(*args, **kwargs)
                    s.attributes["ok"] = True
                    return result
            return wrapper
        return deco

    def print_trace(self):
        total = sum(s.duration_ms for s in self.spans)
        for s in self.spans:
            attrs = " ".join(f"{k}={v}" for k, v in s.attributes.items())
            print(f"{s.duration_ms:8.1f}ms  {s.name:22} {attrs}")
        print(f"{'-' * 44}\n{total:8.1f}ms  TOTAL · {len(self.spans)} spans")


if __name__ == "__main__":
    tr = Tracer()

    @tr.traced("slow_tool")
    def slow_tool():
        time.sleep(0.05)
        return 42

    @tr.traced("fast_tool")
    def fast_tool():
        return "hi"

    slow_tool(); fast_tool(); slow_tool()
    tr.print_trace()
