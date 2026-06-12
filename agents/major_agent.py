"""Agent 4: Major Mapping - maps majors to parent careers."""

from .base import BaseAgent, AgentContext


class MajorMappingAgent(BaseAgent):
    name = "major_mapping"
    description = "Maps university majors to parent careers."

    def execute(self, ctx: AgentContext) -> AgentContext:
        import json, os

        path = os.path.join(os.path.dirname(__file__), "..", "data", "knowledge_base.json")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        ctx.majors = data.get("majors", [])
        return ctx
