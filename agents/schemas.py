"""Pydantic-style dataclass schemas for agent communication contracts."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PolicyDoc:
    id: str
    name: str
    desc: str
    key_points: list[str] = field(default_factory=list)
    priority_score: int = 5  # 1-10
    source: str = ""


@dataclass
class Industry:
    id: str
    name: str
    parent_policy: str
    desc: str
    employment_scale: int = 5   # 1-10 node size
    growth_rate: str = ""
    is_star: bool = False       # highlighted priority
    tags: list[str] = field(default_factory=list)  # 理科/文科/不限


@dataclass
class Career:
    id: str
    name: str
    parent_industry: str
    desc: str
    demand_level: str = "中等"   # 旺盛/中等/饱和
    salary_range: str = ""
    demand_score: int = 5        # 1-10 supply-demand: 1=严重过剩, 10=严重不足
    tags: list[str] = field(default_factory=list)


@dataclass
class Major:
    id: str
    name: str
    parent_career: str
    desc: str
    category: str = "理科"       # 理科/文科/文理兼收
    study_years: str = "4年"
   热度: int = 5                 # 1-10 popularity


@dataclass
class SchoolMajor:
    """A specific major at a specific school (layer 5)."""
    id: str
    school_name: str
    major_id: str
    province: str = "全国"
    tier: str = "一本"           # 清北/华五/985/211/一本/二本
    score_low: int = 0
    score_high: int = 750
    employment_direction: str = ""
    employment_rate: str = ""
    subject_required: str = "理科"  # 理科/文科/不限


@dataclass
class SupplyDemand:
    industry_id: str = ""
    major_id: str = ""
    supply_score: int = 5     # 1-10 how saturated
    demand_score: int = 5     # 1-10 how demanded
    trend: str = "平稳"        # 上升/平稳/下降
    note: str = ""
