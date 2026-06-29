"""Data access layer for HR Analytics API."""
from __future__ import annotations

import json
from io import BytesIO

import pandas as pd

from src.config import (
    CLEANED_DATA_PATH,
    EDA_INSIGHTS_PATH,
    FEATURE_IMPORTANCE_PATH,
    MODEL_METRICS_PATH,
    SUMMARY_STATS_PATH,
)


class DataService:
    _df: pd.DataFrame | None = None

    @classmethod
    def get_dataframe(cls) -> pd.DataFrame:
        if cls._df is None:
            cls._df = pd.read_csv(CLEANED_DATA_PATH)
        return cls._df

    @classmethod
    def reload(cls):
        cls._df = pd.read_csv(CLEANED_DATA_PATH)

    @classmethod
    def get_kpis(cls) -> dict:
        df = cls.get_dataframe()
        total = len(df)
        left = int((df["Attrition"] == "Yes").sum())
        active = total - left
        return {
            "totalEmployees": total,
            "activeEmployees": active,
            "employeesLeft": left,
            "attritionRate": round(left / total * 100, 2) if total else 0,
            "averageSalary": round(float(df["MonthlyIncome"].mean()), 2),
            "averageExperience": round(float(df["TotalWorkingYears"].mean()), 1),
            "averageAge": round(float(df["Age"].mean()), 1),
            "averageSatisfaction": round(float(df["AvgSatisfaction"].mean()), 2),
        }

    @classmethod
    def get_employees(cls, page=1, per_page=20, search="", department="", sort_by="EmployeeNumber", sort_dir="asc") -> dict:
        df = cls.get_dataframe().copy()
        if search:
            mask = df.astype(str).apply(lambda row: row.str.contains(search, case=False, na=False).any(), axis=1)
            df = df[mask]
        if department:
            df = df[df["Department"] == department]
        if sort_by in df.columns:
            df = df.sort_values(sort_by, ascending=(sort_dir == "asc"))
        total = len(df)
        start = (page - 1) * per_page
        end = start + per_page
        page_df = df.iloc[start:end]
        records = page_df.to_dict(orient="records")
        for r in records:
            for k, v in r.items():
                if pd.isna(v):
                    r[k] = None
                elif hasattr(v, "item"):
                    r[k] = v.item()
        return {
            "employees": records,
            "total": total,
            "page": page,
            "perPage": per_page,
            "totalPages": max(1, (total + per_page - 1) // per_page),
        }

    @classmethod
    def get_departments(cls) -> dict:
        df = cls.get_dataframe()
        result = []
        for dept in df["Department"].unique():
            subset = df[df["Department"] == dept]
            result.append({
                "name": dept,
                "count": len(subset),
                "attritionRate": round((subset["Attrition"] == "Yes").mean() * 100, 2),
                "avgSalary": round(float(subset["MonthlyIncome"].mean()), 2),
                "avgAge": round(float(subset["Age"].mean()), 1),
            })
        return {"departments": result}

    @classmethod
    def get_jobs(cls) -> dict:
        df = cls.get_dataframe()
        result = []
        for role in df["JobRole"].value_counts().head(15).index:
            subset = df[df["JobRole"] == role]
            result.append({
                "name": role,
                "count": len(subset),
                "attritionRate": round((subset["Attrition"] == "Yes").mean() * 100, 2),
                "avgSalary": round(float(subset["MonthlyIncome"].mean()), 2),
            })
        return {"jobs": result}

    @classmethod
    def get_chart_data(cls) -> dict:
        if EDA_INSIGHTS_PATH.exists():
            data = json.loads(EDA_INSIGHTS_PATH.read_text(encoding="utf-8"))
            return data.get("chart_data", {})
        return {}

    @classmethod
    def get_insights(cls) -> dict:
        if EDA_INSIGHTS_PATH.exists():
            return json.loads(EDA_INSIGHTS_PATH.read_text(encoding="utf-8"))
        return {"insights": [], "chart_data": {}}

    @classmethod
    def get_model_metrics(cls) -> dict:
        if MODEL_METRICS_PATH.exists():
            return json.loads(MODEL_METRICS_PATH.read_text(encoding="utf-8"))
        return {}

    @classmethod
    def get_feature_importance(cls) -> dict:
        if FEATURE_IMPORTANCE_PATH.exists():
            return json.loads(FEATURE_IMPORTANCE_PATH.read_text(encoding="utf-8"))
        return {}

    @classmethod
    def get_summary_stats(cls) -> dict:
        if SUMMARY_STATS_PATH.exists():
            return json.loads(SUMMARY_STATS_PATH.read_text(encoding="utf-8"))
        return {}

    @classmethod
    def export_csv(cls) -> BytesIO:
        buf = BytesIO()
        cls.get_dataframe().to_csv(buf, index=False)
        buf.seek(0)
        return buf

    @classmethod
    def export_excel(cls) -> BytesIO:
        buf = BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as writer:
            cls.get_dataframe().to_excel(writer, sheet_name="Employees", index=False)
            kpis = cls.get_kpis()
            pd.DataFrame([kpis]).to_excel(writer, sheet_name="KPIs", index=False)
        buf.seek(0)
        return buf
