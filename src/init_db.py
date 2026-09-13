from src.database import Base, SessionLocal, engine
from src.models import ProjectModel, RiskModel


def init_db():
    print("Creating database tables...")
    # Read models.py and generate tables in the database
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Check if sample data already exists
        existing_project = (
            db.query(ProjectModel).filter(ProjectModel.project_id == "PRJ-001").first()
        )

        if not existing_project:
            print("Seeding initial database records...")
            sample_project = ProjectModel(
                project_id="PRJ-001",
                name="HLS Systems Integration",
                budget=1500000.00,
                planned_value=500000.00,
                earned_value=480000.00,
                actual_cost=510000.00,
            )
            db.add(sample_project)
            db.flush()  # Flush to populate sample_project.id for the foreign key

            sample_risk = RiskModel(
                risk_id="R-101",
                title="Avionics supply chain delay",
                impact_score=4,
                likelihood_score=4,
                status="OPEN",
                project_db_id=sample_project.id,
            )
            db.add(sample_risk)
            db.commit()
            print("Database successfully initialized and seeded!")
        else:
            print("Database tables already exist and are seeded.")
    except Exception as e:
        db.rollback()
        print(f"Error initializing database: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    init_db()