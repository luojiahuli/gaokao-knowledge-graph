"""Agent 2: Industry Mapping - maps industries under each policy."""

from .base import BaseAgent, AgentContext


class IndustryMappingAgent(BaseAgent):
    name = "industry_mapping"
    description = "Maps industries to parent policies."

    def execute(self, ctx: AgentContext) -> AgentContext:
        import json, os

        path = os.path.join(os.path.dirname(__file__), "..", "data", "knowledge_base.json")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        ctx.industries = data.get("industries", [])
        return ctx
