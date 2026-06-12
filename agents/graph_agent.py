"""Agent 7: Graph Assembly - assembles final graph data for D3.js."""

from .base import BaseAgent, AgentContext


class GraphAssemblyAgent(BaseAgent):
    name = "graph_assembly"
    description = "Assembles the final hierarchical graph for D3.js visualization."

    def execute(self, ctx: AgentContext) -> AgentContext:
        nodes = []
        links = []

        # Layer 1: Policies
        for p in ctx.policies:
            nodes.append({
                "id": p["id"],
                "name": p["name"],
                "layer": 1,
                "type": "policy",
                "size": p.get("priority_score", 5) * 2,
                "desc": p.get("desc", ""),
                "key_points": p.get("key_points", []),
                "source": p.get("source", ""),
            })

        # Layer 2: Industries
        for ind in ctx.industries:
            size = ind.get("employment_scale", 5) * 2
            demand_info = ctx.supply_demand.get("industries", {}).get(ind["id"], {})
            status = demand_info.get("status", "供需平衡")
            nodes.append({
                "id": ind["id"],
                "name": ind["name"],
                "layer": 2,
                "type": "industry",
                "size": size,
                "desc": ind.get("desc", ""),
                "is_star": ind.get("is_star", False),
                "growth_rate": ind.get("growth_rate", ""),
                "tags": ind.get("tags", []),
                "supply_demand_status": status,
            })
            links.append({
                "source": ind["parent_policy"],
                "target": ind["id"],
                "relation": "包含行业",
            })

        # Layer 3: Careers
        for car in ctx.careers:
            score = car.get("demand_score", 5)
            size = score * 1.5
            demand_info = ctx.supply_demand.get("careers", {}).get(car["id"], {})
            status = demand_info.get("status", "供需平衡")
            nodes.append({
                "id": car["id"],
                "name": car["name"],
                "layer": 3,
                "type": "career",
                "size": size,
                "desc": car.get("desc", ""),
                "demand_level": car.get("demand_level", "中等"),
                "salary_range": car.get("salary_range", ""),
                "demand_score": score,
                "supply_demand_status": status,
                "tags": car.get("tags", []),
            })
            links.append({
                "source": car["parent_industry"],
                "target": car["id"],
                "relation": "对应岗位",
            })

        # Layer 4: Majors
        for m in ctx.majors:
            size = m.get("热度", 5) * 1.5
            nodes.append({
                "id": m["id"],
                "name": m["name"],
                "layer": 4,
                "type": "major",
                "size": size,
                "desc": m.get("desc", ""),
                "category": m.get("category", "理科"),
                "study_years": m.get("study_years", "4年"),
                "热度": m.get("热度", 5),
            })
            links.append({
                "source": m["parent_career"],
                "target": m["id"],
                "relation": "对应专业",
            })

        # Layer 5: Schools
        for sch in ctx.schools:
            size = _tier_size(sch.get("tier", "一本"))
            nodes.append({
                "id": sch["id"],
                "name": sch["school_name"],
                "layer": 5,
                "type": "school",
                "major_id": sch.get("major_id", ""),
                "size": size,
                "tier": sch.get("tier", "一本"),
                "province": sch.get("province", "全国"),
                "score_low": sch.get("score_low", 0),
                "score_high": sch.get("score_high", 750),
                "employment_direction": sch.get("employment_direction", ""),
                "employment_rate": sch.get("employment_rate", ""),
                "subject_required": sch.get("subject_required", "理科"),
            })
            links.append({
                "source": sch["major_id"],
                "target": sch["id"],
                "relation": "开设院校",
            })

        ctx.graph_data = {"nodes": nodes, "links": links}
        return ctx


def _tier_size(tier: str) -> int:
    mapping = {"清北": 6, "华五": 5, "985": 4, "211": 3, "一本": 2, "二本": 1}
    return mapping.get(tier, 3)
