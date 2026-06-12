"""Agent 1: Policy Analysis - extracts policy documents from knowledge base."""

from .base import BaseAgent, AgentContext


class PolicyAnalysisAgent(BaseAgent):
    name = "policy_analysis"
    description = "Extracts national policy documents for the 15th Five-Year Plan."

    def execute(self, ctx: AgentContext) -> AgentContext:
        import json, os

        path = os.path.join(os.path.dirname(__file__), "..", "data", "knowledge_base.json")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        ctx.policies = data.get("policies", [])
        return ctx
