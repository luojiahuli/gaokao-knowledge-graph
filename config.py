"""Configuration for the gaokao knowledge graph system."""
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
KNOWLEDGE_BASE_PATH = os.path.join(DATA_DIR, "knowledge_base.json")

# Tier score ranges
TIER_RANGES = {
    "清北": (680, 710),
    "华五": (660, 690),
    "985": (620, 675),
    "211": (560, 655),
    "一本": (520, 610),
    "二本": (410, 530),
}

TIER_ORDER = ["清北", "华五", "985", "211", "一本", "二本"]

# Supply-demand thresholds
DEMAND_UNDERSUPPLIED = 7   # >= 7 means undersupplied (hot)
DEMAND_OVERSUPPLIED = 4    # <= 4 means oversupplied

# Agent pipeline config
AGENT_CONFIG = {
    "graph_output": os.path.join(os.path.dirname(__file__), "frontend", "graph_data.json"),
}


def load_knowledge_base() -> dict:
    with open(KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
