"""Agent 7: Graph Assembly - assembles final graph data for D3.js."""

from collections import defaultdict

from .base import BaseAgent, AgentContext


class GraphAssemblyAgent(BaseAgent):
    name = "graph_assembly"
    description = "Assembles the final hierarchical graph for D3.js visualization."

    def execute(self, ctx: AgentContext) -> AgentContext:
        nodes = []
        links = []
        link_counter = 0

        def link_id():
            nonlocal link_counter
            link_counter += 1
            return f"l{link_counter}"

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

        # Layer 2: Hot/Star industries (type="hot") + regular industries (type="industry")
        for ind in ctx.industries:
            size = ind.get("employment_scale", 5) * 2
            demand_info = ctx.supply_demand.get("industries", {}).get(ind["id"], {})
            status = demand_info.get("status", "供需平衡")
            is_star = ind.get("is_star", False)
            nodes.append({
                "id": ind["id"],
                "name": ind["name"],
                "layer": 2,
                "type": "hot" if is_star else "industry",
                "size": size,
                "desc": ind.get("desc", ""),
                "is_star": is_star,
                "growth_rate": ind.get("growth_rate", ""),
                "tags": ind.get("tags", []),
                "supply_demand_status": status,
            })
            links.append({
                "id": link_id(),
                "source": ind["parent_policy"],
                "target": ind["id"],
                "relation": "包含行业",
            })

        # Layer 3: Careers
        for car in ctx.careers:
            score = car.get("demand_score", 5)
            size = score * 2
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
                "id": link_id(),
                "source": car["parent_industry"],
                "target": car["id"],
                "relation": "对应岗位",
            })

        # Layer 4: Majors
        for m in ctx.majors:
            size = m.get("热度", 5) * 2
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
                "id": link_id(),
                "source": m["parent_career"],
                "target": m["id"],
                "relation": "对应专业",
            })

        # Layer 5: Schools — one node per unique school name
        # Group all school entries by school_name
        school_groups = defaultdict(list)
        for sch in ctx.schools:
            school_groups[sch["school_name"]].append(sch)

        for school_name, entries in school_groups.items():
            # Use first entry's id as base + suffix
            base_id = entries[0]["id"].rsplit("_", 1)[0] if "_" in entries[0]["id"] else entries[0]["id"]

            # Aggregate info across all major-specific entries
            all_major_ids = []
            all_tiers = set()
            all_provinces = set()
            min_score = 750
            max_score = 0
            all_directions = []
            all_subjects = set()
            all_rates = []

            for e in entries:
                all_major_ids.append(e.get("major_id", ""))
                all_tiers.add(e.get("tier", "一本"))
                all_provinces.add(e.get("province", "全国"))
                score_low = e.get("score_low", 0)
                score_high = e.get("score_high", 750)
                if score_low > 0 and score_low < min_score:
                    min_score = score_low
                if score_high > 0 and score_high > max_score:
                    max_score = score_high
                if e.get("employment_direction"):
                    all_directions.append(e["employment_direction"])
                all_subjects.add(e.get("subject_required", "不限"))
                if e.get("employment_rate"):
                    all_rates.append(e["employment_rate"])

            # Best tier (highest precedence)
            tier_order = ["清北", "华五", "985", "211", "一本", "二本"]
            best_tier = "二本"
            for t in tier_order:
                if t in all_tiers:
                    best_tier = t
                    break

            # Average employment rate
            avg_rate = ""
            if all_rates:
                clean = [float(r.replace("%", "").replace("+", "")) for r in all_rates if r.replace("%", "").replace("+", "").isdigit()]
                if clean:
                    avg_rate = f"{sum(clean) / len(clean):.0f}%"

            nodes.append({
                "id": school_name,
                "name": school_name,
                "layer": 5,
                "type": "school",
                "major_ids": all_major_ids,
                "size": _tier_size(best_tier),
                "tier": best_tier,
                "province": ", ".join(sorted(all_provinces)),
                "score_low": min_score if min_score < 750 else 0,
                "score_high": max_score if max_score > 0 else 750,
                "employment_direction": " | ".join(d for d in all_directions),
                "employment_rate": avg_rate,
                "subject_required": ", ".join(sorted(all_subjects)),
                "num_majors": len(all_major_ids),
            })

            # Connect to all parent majors
            for mid in all_major_ids:
                if mid:
                    links.append({
                        "id": link_id(),
                        "source": mid,
                        "target": school_name,
                        "relation": "开设院校",
                    })

        ctx.graph_data = {"nodes": nodes, "links": links}
        return ctx


def _tier_size(tier: str) -> int:
    mapping = {"清北": 18, "华五": 15, "985": 12, "211": 10, "一本": 8, "二本": 6}
    return mapping.get(tier, 8)
