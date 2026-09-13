from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base


class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    budget = Column(Float, nullable=False)
    planned_value = Column(Float, default=0.0)
    earned_value = Column(Float, default=0.0)
    actual_cost = Column(Float, default=0.0)

    # Relationship link to risk items
    risks = relationship("RiskModel", back_populates="project", cascade="all, delete-orphan")


class RiskModel(Base):
    __tablename__ = "risks"

    id = Column(Integer, primary_key=True, index=True)
    risk_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    impact_score = Column(Integer, nullable=False)
    likelihood_score = Column(Integer, nullable=False)
    status = Column(String, default="OPEN")

    # Foreign Key linking back to project
    project_db_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    project = relationship("ProjectModel", back_populates="risks")