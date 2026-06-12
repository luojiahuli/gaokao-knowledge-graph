"""Agent 6: Supply-Demand Analysis - computes supply-demand indicators."""

from .base import BaseAgent, AgentContext


class SupplyDemandAgent(BaseAgent):
    name = "supply_demand"
    description = "Computes supply-demand balance for industries and careers."

    def execute(self, ctx: AgentContext) -> AgentContext:
        careers = ctx.careers
        industries = ctx.industries

        # Compute industry-level supply-demand from child careers
        ind_demand: dict[str, dict] = {}
        for ind in industries:
            ind_id = ind["id"]
            related = [c for c in careers if c.get("parent_industry") == ind_id]
            scores = [c.get("demand_score", 5) for c in related]
            avg_score = round(sum(scores) / len(scores), 1) if scores else 5
            status = "供不应求" if avg_score >= 7 else ("供大于求" if avg_score <= 4 else "供需平衡")
            ind_demand[ind_id] = {
                "industry_name": ind["name"],
                "avg_demand_score": avg_score,
                "status": status,
                "career_count": len(related),
            }

        # Career-level supply-demand from demand_score
        car_demand = {}
        for c in careers:
            score = c.get("demand_score", 5)
            status = "供不应求" if score >= 7 else ("供大于求" if score <= 4 else "供需平衡")
            car_demand[c["id"]] = {
                "career_name": c["name"],
                "demand_score": score,
                "status": status,
                "demand_level": c.get("demand_level", "中等"),
            }

        ctx.supply_demand = {
            "industries": ind_demand,
            "careers": car_demand,
        }
        return ctx
