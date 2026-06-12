"""Agent 5: School Mapping - maps school-majors with score tiers."""

from .base import BaseAgent, AgentContext


class SchoolMappingAgent(BaseAgent):
    name = "school_mapping"
    description = "Maps schools and their major-specific score tiers."

    def execute(self, ctx: AgentContext) -> AgentContext:
        import json, os

        path = os.path.join(os.path.dirname(__file__), "..", "data", "knowledge_base.json")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        ctx.schools = data.get("schools", [])
        return ctx
