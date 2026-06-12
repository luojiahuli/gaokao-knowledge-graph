"""Multi-agent system core: base agent, context, and orchestrator."""

from __future__ import annotations
import time
import json
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class AgentContext:
    """Shared blackboard for all agents in the pipeline."""
    # Pipeline state
    province: str = "全国"
    score: int = 0
    subject: str = "理科"  # 文科/理科/不限
    search_query: str = ""

    # Agent outputs (populated sequentially)
    policies: list[dict] = field(default_factory=list)
    industries: list[dict] = field(default_factory=list)
    careers: list[dict] = field(default_factory=list)
    majors: list[dict] = field(default_factory=list)
    schools: list[dict] = field(default_factory=list)
    supply_demand: dict = field(default_factory=dict)

    # Final graph data
    graph_data: dict = field(default_factory=dict)

    # Execution telemetry
    agent_times: dict = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)


class BaseAgent:
    """Abstract base agent with execute(context) pattern."""
    name: str = ""
    description: str = ""

    def execute(self, ctx: AgentContext) -> AgentContext:
        raise NotImplementedError


class OrchestratorAgent:
    """Runs agents sequentially, passing context between them."""

    def __init__(self, agents: list[BaseAgent]):
        self.agents = agents

    def run(self, ctx: Optional[AgentContext] = None) -> AgentContext:
        ctx = ctx or AgentContext()
        for agent in self.agents:
            t0 = time.time()
            try:
                print(f"  [{agent.name}] running...")
                ctx = agent.execute(ctx)
                elapsed = time.time() - t0
                ctx.agent_times[agent.name] = round(elapsed, 2)
                print(f"  [{agent.name}] done ({elapsed:.1f}s)")
            except Exception as e:
                elapsed = time.time() - t0
                ctx.agent_times[agent.name] = round(elapsed, 2)
                err = f"[{agent.name}] failed: {e}"
                ctx.errors.append(err)
                print(f"  {err}")
        return ctx
