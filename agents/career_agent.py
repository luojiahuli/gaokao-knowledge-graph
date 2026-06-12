"""Agent 3: Career Path - maps careers to parent industries."""

from .base import BaseAgent, AgentContext


class CareerPathAgent(BaseAgent):
    name = "career_path"
    description = "Maps careers/occupations to parent industries."

    def execute(self, ctx: AgentContext) -> AgentContext:
        import json, os

        path = os.path.join(os.path.dirname(__file__), "..", "data", "knowledge_base.json")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        ctx.careers = data.get("careers", [])
        return ctx
