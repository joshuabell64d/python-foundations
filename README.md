# Enterprise Risk & EVM Program Foundations

A structured Python package demonstrating object-oriented domain modeling, Earned Value Management (EVM) metric evaluation, and automated unit testing.

## Overview
This repository serves as the core domain foundation for an Enterprise Program Risk & Performance Platform. It provides domain logic to track program baselines, calculate cost and schedule variances, and score high-priority project risks.

## Features
- **Object-Oriented Domain Models**: Implements `ProgramProject` and `RiskItem` dataclasses.
- **EVM Metrics**: Automated calculation of Cost Variance ($CV = EV - AC$) and Schedule Variance ($SV = EV - PV$).
- **Risk Scoring**: Severity scoring ($Impact \times Likelihood$) with automated high-priority risk filtering.
- **Automated Testing**: Unit test coverage powered by `pytest`.

## Project Structure
```text
python-foundations/
├── src/
│   ├── __init__.py
│   └── risk_manager.py
├── tests/
│   └── test_risk_manager.py
├── app.py
├── .gitignore
└── README.md