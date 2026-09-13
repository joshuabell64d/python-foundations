from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.models import ProjectModel, RiskModel
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


@app.get("/projects/{project_id}", response_model=ProjectPerformanceResponse)
def get_project_by_id(project_id: str, db: Session = Depends(get_db)):
    """Fetches project record from the database and computes live EVM metrics."""
    db_project = (
        db.query(ProjectModel).filter(ProjectModel.project_id == project_id).first()
    )

    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Instantiate domain class to calculate live EVM metrics
    project_domain = ProgramProject(
        db_project.project_id, db_project.name, db_project.budget
    )
    project_domain.planned_value = db_project.planned_value
    project_domain.earned_value = db_project.earned_value
    project_domain.actual_cost = db_project.actual_cost

    # Extract high priority risks linked via ORM relationship
    high_risks = [
        {
            "risk_id": r.risk_id,
            "title": r.title,
            "impact_score": r.impact_score,
            "likelihood_score": r.likelihood_score,
            "risk_score": r.impact_score * r.likelihood_score,
            "status": r.status,
        }
        for r in db_project.risks
        if (r.impact_score * r.likelihood_score) >= 12
    ]

    return {
        "project_id": project_domain.project_id,
        "name": project_domain.name,
        "budget": project_domain.budget,
        "evm_metrics": {
            "planned_value": project_domain.planned_value,
            "earned_value": project_domain.earned_value,
            "actual_cost": project_domain.actual_cost,
            "cost_variance": project_domain.calculate_cost_variance(),
            "schedule_variance": project_domain.calculate_schedule_variance(),
        },
        "high_priority_risks": high_risks,
    }


@app.post("/risks/eval", response_model=RiskItemResponse)
def evaluate_and_persist_risk(risk_in: RiskItemCreate, db: Session = Depends(get_db)):
    """
    Evaluates raw risk input via domain logic and persists the item into the database.
    """
    risk_domain = RiskItem(
        risk_id=risk_in.risk_id,
        title=risk_in.title,
        impact_score=risk_in.impact_score,
        likelihood_score=risk_in.likelihood_score,
    )

    # Persist record using SQLAlchemy session
    db_risk = RiskModel(
        risk_id=risk_domain.risk_id,
        title=risk_domain.title,
        impact_score=risk_domain.impact_score,
        likelihood_score=risk_domain.likelihood_score,
        status=risk_domain.status,
    )
    db.add(db_risk)
    db.commit()
    db.refresh(db_risk)

    return {
        "risk_id": db_risk.risk_id,
        "title": db_risk.title,
        "impact_score": db_risk.impact_score,
        "likelihood_score": db_risk.likelihood_score,
        "risk_score": risk_domain.risk_score,
        "status": db_risk.status,
    }