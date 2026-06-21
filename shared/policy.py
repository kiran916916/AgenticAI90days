"""Identity & access FOR AGENTS — deny-by-default tool authorization + audit trail.

The flagship asset of the Advanced Track (Week 1 Fri ⭐). Every tool call is checked
against the scopes THIS agent identity holds; high-blast tools require human
approval; every decision is logged for a full audit trail.

    from shared.policy import PolicyGate, PolicyDenied
"""
from __future__ import annotations

import datetime as _dt
import functools
from dataclasses import dataclass, field


class PolicyDenied(PermissionError):
    """Raised when a tool call is not authorized by the policy gate."""


@dataclass
class AuditEvent:
    time: str
    tool: str
    decision: str          # allow | deny | approved | rejected
    reason: str
    args_summary: str


class AuditLog:
    def __init__(self):
        self.events: list[AuditEvent] = []

    def record(self, tool, decision, reason, args):
        self.events.append(AuditEvent(
            time=_dt.datetime.now().isoformat(timespec="seconds"),
            tool=tool, decision=decision, reason=reason,
            args_summary=str(args)[:200],
        ))

    def dump(self):
        for e in self.events:
            print(f"{e.time} | {e.decision:9} | {e.tool:18} | {e.reason}")


@dataclass
class PolicyGate:
    """Deny-by-default authorization for agent tools.

    - tool_scopes : tool name -> the scope it requires (e.g. 'repo:read').
    - granted     : the scopes THIS agent identity holds (least privilege).
    - high_blast  : tools that ALWAYS require human approval.
    - approver    : callable(tool, args) -> bool for the human-in-the-loop gate.
    """
    tool_scopes: dict
    granted: set
    high_blast: set = field(default_factory=set)
    approver: object = None
    audit: AuditLog = field(default_factory=AuditLog)

    def authorize(self, tool, args=None):
        required = self.tool_scopes.get(tool)
        if required is None:                                   # deny-by-default
            self.audit.record(tool, "deny", "unknown tool (deny-by-default)", args)
            raise PolicyDenied(f"'{tool}' is not a registered tool")
        if required not in self.granted:                       # least privilege
            self.audit.record(tool, "deny", f"missing scope '{required}'", args)
            raise PolicyDenied(f"'{tool}' requires scope '{required}'")
        if tool in self.high_blast:                            # human-in-the-loop
            ok = bool(self.approver and self.approver(tool, args))
            self.audit.record(tool, "approved" if ok else "rejected",
                              "human-in-the-loop gate", args)
            if not ok:
                raise PolicyDenied(f"'{tool}' requires human approval")
            return True
        self.audit.record(tool, "allow", f"scope '{required}' granted", args)
        return True

    def guard(self, tool_name):
        """Decorator: authorize before the tool runs (wrap every tool with this)."""
        def deco(fn):
            @functools.wraps(fn)
            def wrapper(*args, **kwargs):
                self.authorize(tool_name, kwargs or args)
                return fn(*args, **kwargs)
            return wrapper
        return deco


if __name__ == "__main__":
    gate = PolicyGate(
        tool_scopes={"read_repo": "repo:read", "delete_branch": "repo:admin"},
        granted={"repo:read"},                 # this agent can read, not admin
        high_blast={"delete_branch"},
        approver=lambda tool, args: False,      # always refuse in this demo
    )
    print("read_repo  ->", gate.authorize("read_repo"))
    for bad in ("delete_branch", "exfiltrate"):
        try:
            gate.authorize(bad)
        except PolicyDenied as exc:
            print(f"{bad:14}-> DENIED: {exc}")
    print("\n--- audit trail ---")
    gate.audit.dump()
