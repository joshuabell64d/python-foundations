from enum import Enum
from pydantic import BaseModel, Field


class RiskStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    MITIGATED = "MITIGATED"
    CLOSED = "CLOSED"


class RiskItemCreate(BaseModel):
    risk_id: str = Field(..., example="R-101")
    title: str = Field(..., example="Avionics supply chain delay")
    impact_score: int = Field(..., ge=1, le=5, description="Impact score between 1 and 5")
    likelihood_score: int = Field(..., ge=1, le=5, description="Likelihood score between 1 and 5")


class RiskItemResponse(BaseModel):
    risk_id: str
    title: str
    impact_score: int
    likelihood_score: int
    risk_score: int
    status: RiskStatus


class ProjectCreate(BaseModel):
    project_id: str = Field(..., example="PRJ-001")
    name: str = Field(..., example="HLS Systems Integration")
    budget: float = Field(..., gt=0, example=1500000.0)
    planned_value: float = Field(0.0, ge=0)
    earned_value: float = Field(0.0, ge=0)
    actual_cost: float = Field(0.0, ge=0)


class EVMMetricsResponse(BaseModel):
    planned_value: float
    earned_value: float
    actual_cost: float
    cost_variance: float
    schedule_variance: float


class ProjectPerformanceResponse(BaseModel):
    project_id: str
    name: str
    budget: float
    evm_metrics: EVMMetricsResponse
    high_priority_risks: list[RiskItemResponse]