"""An ADK plugin that records timings, tool calls, tokens, and a trace for each run."""
from __future__ import annotations

import json
import time
from pathlib import Path

from google.adk.plugins.base_plugin import BasePlugin

LOG_DIR = Path(__file__).resolve().parents[2] / "logs"


class ObservabilityPlugin(BasePlugin):
    def __init__(self, name: str = "observability"):
        super().__init__(name=name)
        self._reset()

    def _reset(self) -> None:
        self._start = time.perf_counter()
        self._agent_starts: list[float] = []   # stack: agents nest, so pair start/end
        self._tool_starts: dict[str, float] = {}
        self.records: list[dict] = []
        self.agent_ms: dict[str, float] = {}
        self.tool_calls: dict[str, int] = {}
        self.tokens = 0
        self.route: str | None = None
        self.total_ms = 0.0
        self.trace_path: Path | None = None

    def _elapsed_ms(self) -> float:
        return round((time.perf_counter() - self._start) * 1000, 1)

    def _log(self, record: dict) -> None:
        self.records.append({"at_ms": self._elapsed_ms(), **record})

    async def before_run_callback(self, *, invocation_context):
        self._reset()
        self._session_id = getattr(getattr(invocation_context, "session", None), "id", "run")
        self._log({"event": "run_start"})

    async def after_run_callback(self, *, invocation_context):
        self.total_ms = self._elapsed_ms()
        self._log({"event": "run_end", "total_ms": self.total_ms})
        LOG_DIR.mkdir(exist_ok=True)
        self.trace_path = LOG_DIR / f"trace-{self._session_id}.jsonl"
        self.trace_path.write_text(
            "\n".join(json.dumps(r, default=str) for r in self.records) + "\n",
            encoding="utf-8",
        )

    async def before_agent_callback(self, *, agent, callback_context):
        self._agent_starts.append(time.perf_counter())

    async def after_agent_callback(self, *, agent, callback_context):
        start = self._agent_starts.pop() if self._agent_starts else None
        ms = round((time.perf_counter() - start) * 1000, 1) if start else 0.0
        self.agent_ms[agent.name] = self.agent_ms.get(agent.name, 0.0) + ms
        self._log({"agent": agent.name, "ms": ms})
        state = getattr(callback_context, "state", None)
        if state is not None:
            try:
                route = state.get("query_type")
                if route:
                    self.route = str(route).strip()
            except Exception:
                pass

    async def before_tool_callback(self, *, tool, tool_args, tool_context):
        self._tool_starts[tool.name] = time.perf_counter()

    async def after_tool_callback(self, *, tool, tool_args, tool_context, result):
        start = self._tool_starts.pop(tool.name, None)
        ms = round((time.perf_counter() - start) * 1000, 1) if start else 0.0
        self.tool_calls[tool.name] = self.tool_calls.get(tool.name, 0) + 1
        self._log({"tool": tool.name, "ms": ms})

    async def after_model_callback(self, *, callback_context, llm_response):
        usage = getattr(llm_response, "usage_metadata", None)
        if usage and usage.total_token_count:
            self.tokens += usage.total_token_count

    @property
    def metrics(self) -> dict:
        return {
            "route": self.route,
            "total_ms": round(self.total_ms, 1),
            "agent_ms": self.agent_ms,
            "tool_calls": self.tool_calls,
            "tokens": self.tokens,
        }

    def summary(self) -> str:
        lines = [
            "----- OBSERVABILITY -----",
            f"  route:        {self.route}",
            f"  total time:   {self.total_ms:.0f} ms",
        ]
        if self.agent_ms:
            lines.append("  per agent:    " + ", ".join(f"{k} {v:.0f}ms" for k, v in self.agent_ms.items()))
        if self.tool_calls:
            lines.append("  tool calls:   " + ", ".join(f"{k} x{v}" for k, v in self.tool_calls.items()))
        lines.append(f"  tokens used:  {self.tokens}")
        if self.trace_path:
            lines.append(f"  full trace:   {self.trace_path}")
        return "\n".join(lines)
