#!/usr/bin/env python3
"""Quick API smoke tests for HR Intelligence Platform."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.backend.app import app


def run_tests():
    client = app.test_client()
    tests_passed = 0
    tests_failed = 0

    def check(name, response, expected_status=200):
        nonlocal tests_passed, tests_failed
        if response.status_code == expected_status:
            tests_passed += 1
            print(f"  PASS: {name}")
        else:
            tests_failed += 1
            print(f"  FAIL: {name} (status {response.status_code})")

    print("Running API tests...")
    check("health", client.get("/api/health"))
    check("dashboard", client.get("/api/dashboard"))
    check("employees", client.get("/api/employees"))
    check("model-metrics", client.get("/api/model-metrics"))
    check("insights", client.get("/api/insights"))
    check("departments", client.get("/api/departments"))
    check("jobs", client.get("/api/jobs"))
    check("summary", client.get("/api/summary"))

    pred = client.post("/api/predict", json={
        "Age": 35, "Gender": "Male", "Department": "Sales",
        "JobRole": "Sales Executive", "MonthlyIncome": 5000,
        "OverTime": "Yes", "BusinessTravel": "Travel_Frequently",
        "MaritalStatus": "Single", "Education": 3,
        "EducationField": "Life Sciences", "JobLevel": 2,
        "JobInvolvement": 3, "JobSatisfaction": 2,
        "EnvironmentSatisfaction": 2, "RelationshipSatisfaction": 2,
        "WorkLifeBalance": 2, "PerformanceRating": 3,
        "DistanceFromHome": 10, "TotalWorkingYears": 8,
        "YearsAtCompany": 3, "YearsInCurrentRole": 2,
        "YearsSinceLastPromotion": 2, "YearsWithCurrManager": 2,
        "NumCompaniesWorked": 3, "StockOptionLevel": 0,
        "PercentSalaryHike": 11, "TrainingTimesLastYear": 1,
        "DailyRate": 800, "HourlyRate": 65, "MonthlyRate": 20000,
    })
    check("predict", pred)
    if pred.status_code == 200:
        data = pred.get_json()
        assert "prediction" in data and "probability" in data

    check("download-pdf", client.get("/api/download-report?format=pdf"))
    check("download-csv", client.get("/api/download-report?format=csv"))
    check("index", client.get("/"))

    print(f"\nResults: {tests_passed} passed, {tests_failed} failed")
    return tests_failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
