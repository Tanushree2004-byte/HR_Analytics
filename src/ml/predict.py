"""Prediction service for employee attrition."""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.config import BEST_MODEL_PATH, MODELS_DIR
from src.ml.train import CATEGORICAL, FEATURE_COLS, NUMERIC

RECOMMENDATIONS = {
    "low": [
        "Employee shows strong retention indicators.",
        "Continue current engagement and development programs.",
        "Schedule regular check-ins to maintain satisfaction.",
    ],
    "medium": [
        "Moderate attrition risk detected — monitor closely.",
        "Review workload balance and overtime hours.",
        "Discuss career development and promotion timeline.",
        "Consider compensation benchmarking for their role.",
    ],
    "high": [
        "High attrition risk — immediate HR intervention recommended.",
        "Conduct stay interview to understand concerns.",
        "Review overtime, work-life balance, and manager relationship.",
        "Evaluate compensation against market and internal equity.",
        "Offer targeted retention incentives if critical talent.",
    ],
}


class AttritionPredictor:
    def __init__(self):
        self.pipeline = None
        self.meta = None
        self._load()

    def _load(self):
        if BEST_MODEL_PATH.exists():
            self.pipeline = joblib.load(BEST_MODEL_PATH)
        meta_path = MODELS_DIR / "model_meta.json"
        if meta_path.exists():
            self.meta = json.loads(meta_path.read_text())

    def is_ready(self) -> bool:
        return self.pipeline is not None

    def _build_features(self, data: dict) -> pd.DataFrame:
        row = {}
        for col in FEATURE_COLS:
            row[col] = data.get(col, self._default_value(col))
        df = pd.DataFrame([row])

        if "TenureRatio" not in data:
            tw = float(row.get("TotalWorkingYears", 1))
            df["TenureRatio"] = row["YearsAtCompany"] / tw if tw > 0 else 0
        if "AvgSatisfaction" not in data:
            df["AvgSatisfaction"] = np.mean([
                float(row.get("EnvironmentSatisfaction", 3)),
                float(row.get("JobSatisfaction", 3)),
                float(row.get("RelationshipSatisfaction", 3)),
                float(row.get("WorkLifeBalance", 3)),
            ])
        if "PromotionGap" not in data:
            df["PromotionGap"] = float(row.get("YearsAtCompany", 0)) - float(row.get("YearsSinceLastPromotion", 0))
        for flag, cond in [
            ("LongTenureNoPromotion", lambda r: int(r["YearsAtCompany"] >= 5 and r["YearsSinceLastPromotion"] >= 5)),
            ("HighTravel", lambda r: int(r.get("BusinessTravel") == "Travel_Frequently")),
            ("LowWorkLifeBalance", lambda r: int(r["WorkLifeBalance"] <= 2)),
            ("HighOvertime", lambda r: int(r.get("OverTime") == "Yes")),
            ("YoungEmployee", lambda r: int(r["Age"] <= 30)),
            ("LowStockOptions", lambda r: int(r["StockOptionLevel"] == 0)),
        ]:
            if flag not in data:
                df[flag] = cond(row)

        return df[FEATURE_COLS]

    @staticmethod
    def _default_value(col: str):
        defaults = {
            "Age": 35, "BusinessTravel": "Travel_Rarely", "DailyRate": 800,
            "Department": "Research & Development", "DistanceFromHome": 5,
            "Education": 3, "EducationField": "Life Sciences",
            "EnvironmentSatisfaction": 3, "Gender": "Male", "HourlyRate": 65,
            "JobInvolvement": 3, "JobLevel": 2, "JobRole": "Research Scientist",
            "JobSatisfaction": 3, "MaritalStatus": "Married", "MonthlyIncome": 5000,
            "MonthlyRate": 20000, "NumCompaniesWorked": 2, "OverTime": "No",
            "PercentSalaryHike": 15, "PerformanceRating": 3,
            "RelationshipSatisfaction": 3, "StockOptionLevel": 1,
            "TotalWorkingYears": 10, "TrainingTimesLastYear": 2,
            "WorkLifeBalance": 3, "YearsAtCompany": 5, "YearsInCurrentRole": 3,
            "YearsSinceLastPromotion": 1, "YearsWithCurrManager": 3,
        }
        return defaults.get(col, 0)

    def predict(self, employee_data: dict) -> dict:
        if not self.is_ready():
            return {"error": "Model not trained. Run the training pipeline first."}

        X = self._build_features(employee_data)
        prob = float(self.pipeline.predict_proba(X)[0][1])
        pred = int(prob >= 0.5)

        if prob < 0.35:
            risk_level, risk_color = "Low", "green"
        elif prob < 0.65:
            risk_level, risk_color = "Medium", "yellow"
        else:
            risk_level, risk_color = "High", "red"

        confidence = round(max(prob, 1 - prob) * 100, 1)

        return {
            "prediction": "Yes" if pred else "No",
            "will_leave": bool(pred),
            "probability": round(prob * 100, 2),
            "retention_probability": round((1 - prob) * 100, 2),
            "confidence": confidence,
            "risk_level": risk_level,
            "risk_color": risk_color,
            "recommendations": RECOMMENDATIONS[risk_level.lower()],
        }


predictor = AttritionPredictor()
