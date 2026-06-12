#!/usr/bin/env python3
"""高考志愿知识图谱系统 - 多智能体管道入口

Usage:
    python main.py                    # Run pipeline and output graph JSON
    python main.py --serve            # Start a local HTTP server for frontend
"""

import json
import os
import sys

from agents import (
    OrchestratorAgent,
    PolicyAnalysisAgent,
    IndustryMappingAgent,
    CareerPathAgent,
    MajorMappingAgent,
    SchoolMappingAgent,
    SupplyDemandAgent,
    GraphAssemblyAgent,
)


def build_graph() -> dict:
    agents = [
        PolicyAnalysisAgent(),
        IndustryMappingAgent(),
        CareerPathAgent(),
        MajorMappingAgent(),
        SchoolMappingAgent(),
        SupplyDemandAgent(),
        GraphAssemblyAgent(),
    ]
    orchestrator = OrchestratorAgent(agents)
    ctx = orchestrator.run()
    return ctx.graph_data


def main():
    print("=" * 50)
    print("  高考志愿知识图谱系统")
    print("  基于十五五计划的多智能体分析管道")
    print("=" * 50)

    graph = build_graph()

    # Save to frontend directory
    output_dir = os.path.join(os.path.dirname(__file__), "frontend")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "graph_data.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Graph data saved to {output_path}")
    print(f"   Nodes: {len(graph['nodes'])}")
    print(f"   Links: {len(graph['links'])}")


if __name__ == "__main__":
    if "--serve" in sys.argv:
        port = int(sys.argv[sys.argv.index("--serve") + 1]) if "--serve" in sys.argv and len(sys.argv) > sys.argv.index("--serve") + 1 else 8765
        print(f"Starting HTTP server on http://localhost:{port}")
        os.chdir(os.path.join(os.path.dirname(__file__), "frontend"))
        import http.server
        http.server.HTTPServer(("", port), http.server.SimpleHTTPRequestHandler).serve_forever()
    else:
        main()
