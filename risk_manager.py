from dataclasses import dataclass, field
from typing import List


@dataclass
class RiskItem:
    risk_id: str
    title: str
    impact_score: int  # 1 (Low) to 5 (Critical)
    likelihood_score: int  # 1 (Low) to 5 (Critical)
    status: str = "OPEN"

    @property
    def risk_score(self) -> int:
        """Calculates total risk severity score."""
        return self.impact_score * self.likelihood_score


class ProgramProject:

    def __init__(self, project_id: str, name: str, budget: float):
        self.project_id = project_id
        self.name = name
        self.budget = budget
        self.actual_cost: float = 0.0
        self.planned_value: float = 0.0
        self.earned_value: float = 0.0
        self.risks: List[RiskItem] = []

    def add_risk(self, risk: RiskItem) -> None:
        self.risks.append(risk)

    def calculate_cost_variance(self) -> float:
        """EVM Cost Variance (CV = EV - AC). Positive is favorable."""
        return self.earned_value - self.actual_cost

    def calculate_schedule_variance(self) -> float:
        """EVM Schedule Variance (SV = EV - PV). Positive is favorable."""
        return self.earned_value - self.planned_value

    def get_high_priority_risks(self) -> List[RiskItem]:
        """Returns risks with a score of 12 or higher."""
        return [r for r in self.risks if r.risk_score >= 12]