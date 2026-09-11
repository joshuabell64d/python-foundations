from src.risk_manager import ProgramProject, RiskItem


def main():
    # Initialize a sample project (e.g., Space Systems Integration baseline)
    project = ProgramProject("PRJ-001", "HLS Systems Integration", 1_500_000.00)

    # Set Earned Value Management (EVM) metrics
    project.planned_value = 500_000.00
    project.earned_value = 480_000.00
    project.actual_cost = 510_000.00

    # Log risks
    project.add_risk(
        RiskItem("R-101", "Avionics supply chain delay", impact_score=4, likelihood_score=4)
    )
    project.add_risk(
        RiskItem("R-102", "Minor documentation backlog", impact_score=2, likelihood_score=2)
    )

    print("=" * 55)
    print(f" PROJECT REPORT: {project.name} ({project.project_id})")
    print("=" * 55)
    print(f" Cost Variance (CV)    : ${project.calculate_cost_variance():,.2f}")
    print(f" Schedule Variance (SV): ${project.calculate_schedule_variance():,.2f}")
    print("-" * 55)

    high_risks = project.get_high_priority_risks()
    print(f" High-Priority Risks Identified: {len(high_risks)}")
    for r in high_risks:
        print(f"  - [{r.risk_id}] {r.title} | Severity Score: {r.risk_score}")
    print("=" * 55)


if __name__ == "__main__":
    main()