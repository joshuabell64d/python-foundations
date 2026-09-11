import pytest
from src.risk_manager import ProgramProject, RiskItem

def test_evm_calculations():
    project = ProgramProject("PRJ-TEST", "Test Baseline", 1_000_000.00)
    project.planned_value = 100_000.00
    project.earned_value = 80_000.00
    project.actual_cost = 110_000.00

    assert project.calculate_cost_variance() == -30_000.00
    assert project.calculate_schedule_variance() == -20_000.00


def test_high_priority_risk_filtering():
    project = ProgramProject("PRJ-TEST", "Test Baseline", 1_000_000.00)

    low_risk = RiskItem("R-01", "Minor issue", impact_score=2, likelihood_score=2)
    high_risk = RiskItem("R-02", "Critical delay", impact_score=4, likelihood_score=4)

    project.add_risk(low_risk)
    project.add_risk(high_risk)

    filtered_risks = project.get_high_priority_risks()

    assert len(filtered_risks) == 1
    assert filtered_risks[0].risk_id == "R-02"
    assert filtered_risks[0].risk_score == 16