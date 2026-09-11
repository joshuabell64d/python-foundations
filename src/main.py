from fastapi import FastAPI
from src.risk_manager import ProgramProject, RiskItem
from src.schemas import ProjectPerformanceResponse, RiskItemCreate, RiskItemResponse

app = FastAPI(
    title="Enterprise Program Risk & Performance API",
    description="REST API for EVM metrics, performance tracking, and program risk management.",
    version="1.0.0",
)


@app.get("/")
def read_root():
    return {
        "status": "online",
        "system": "Enterprise Risk Platform",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/projects/sample", response_model=ProjectPerformanceResponse)
def get_sample_project():
    """Generates a sample program project with typed schema validation."""
    project = ProgramProject("PRJ-001", "HLS Systems Integration", 1_500_000.00)
    project.planned_value = 500_000.00
    project.earned_value = 480_000.00
    project.actual_cost = 510_000.00

    project.add_risk(
        RiskItem("R-101", "Avionics supply chain delay", impact_score=4, likelihood_score=4)
    )

    high_risks = project.get_high_priority_risks()

    return {
        "project_id": project.project_id,
        "name": project.name,
        "budget": project.budget,
        "evm_metrics": {
            "planned_value": project.planned_value,
            "earned_value": project.earned_value,
            "actual_cost": project.actual_cost,
            "cost_variance": project.calculate_cost_variance(),
            "schedule_variance": project.calculate_schedule_variance(),
        },
        "high_priority_risks": [
            {
                "risk_id": r.risk_id,
                "title": r.title,
                "impact_score": r.impact_score,
                "likelihood_score": r.likelihood_score,
                "risk_score": r.risk_score,
                "status": r.status,
            }
            for r in high_risks
        ],
    }


@app.post("/risks/eval", response_model=RiskItemResponse)
def evaluate_risk(risk_in: RiskItemCreate):
    """
    Accepts raw risk input, evaluates severity score using domain logic,
    and returns a validated risk record.
    """
    risk = RiskItem(
        risk_id=risk_in.risk_id,
        title=risk_in.title,
        impact_score=risk_in.impact_score,
        likelihood_score=risk_in.likelihood_score,
    )
    return {
        "risk_id": risk.risk_id,
        "title": risk.title,
        "impact_score": risk.impact_score,
        "likelihood_score": risk.likelihood_score,
        "risk_score": risk.risk_score,
        "status": risk.status,
    }