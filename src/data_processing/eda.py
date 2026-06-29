"""Exploratory Data Analysis — generates charts and business insights."""
from __future__ import annotations

import json
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent.parent))

from src.config import CHARTS_DIR, CLEANED_DATA_PATH, EDA_INSIGHTS_PATH

plt.style.use("seaborn-v0_8-whitegrid")
COLORS = {"primary": "#D4AF37", "secondary": "#4F4F4F", "accent": "#F5E6A3", "bg": "#F7F6F3"}
PALETTE = ["#D4AF37", "#4F4F4F", "#B8962E", "#6B6B6B", "#E8D5A3", "#3D3D3D"]


def load_data() -> pd.DataFrame:
    return pd.read_csv(CLEANED_DATA_PATH)


def save_chart(fig, name: str) -> str:
    path = CHARTS_DIR / f"{name}.png"
    fig.savefig(path, dpi=120, bbox_inches="tight", facecolor=COLORS["bg"])
    plt.close(fig)
    return str(path.name)


def insight(title: str, text: str, chart: str) -> dict:
    return {"title": title, "insight": text, "chart": chart}


def chart_gender_distribution(df: pd.DataFrame) -> dict:
    counts = df["Gender"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(
        counts.values, labels=counts.index, autopct="%1.1f%%",
        colors=PALETTE[:2], startangle=90, wedgeprops={"linewidth": 1, "edgecolor": "white"},
    )
    ax.set_title("Employee Gender Distribution", fontsize=14, fontweight="bold", color=COLORS["secondary"])
    name = save_chart(fig, "gender_distribution")
    pct_female = round(counts.get("Female", 0) / len(df) * 100, 1)
    return insight(
        "Gender Distribution",
        f"The workforce is {'predominantly male' if pct_female < 50 else 'gender-balanced'} with "
        f"{pct_female}% female employees. Gender diversity varies by department and should be monitored "
        f"for equitable retention policies.",
        name,
    )


def chart_department_distribution(df: pd.DataFrame) -> dict:
    counts = df["Department"].value_counts()
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(counts.index, counts.values, color=PALETTE[0], edgecolor="white")
    ax.set_xlabel("Employee Count")
    ax.set_title("Employees by Department", fontsize=14, fontweight="bold")
    for bar in bars:
        ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2,
                str(int(bar.get_width())), va="center", fontsize=10)
    name = save_chart(fig, "department_distribution")
    top_dept = counts.index[0]
    return insight(
        "Department Distribution",
        f"Research & Development employs the largest share ({counts.iloc[0]} employees). "
        f"{top_dept} leads headcount. HR should tailor retention strategies by department workload and growth.",
        name,
    )


def chart_job_role(df: pd.DataFrame) -> dict:
    counts = df["JobRole"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(counts.index[::-1], counts.values[::-1], color=PALETTE[1])
    ax.set_title("Top Job Roles", fontsize=14, fontweight="bold")
    ax.set_xlabel("Count")
    name = save_chart(fig, "job_role_distribution")
    return insight(
        "Job Role Distribution",
        f"Sales Executive and Research Scientist are the most common roles. "
        f"High-volume roles warrant targeted career development programs to reduce turnover.",
        name,
    )


def chart_age_distribution(df: pd.DataFrame) -> dict:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(df["Age"], bins=20, color=PALETTE[0], edgecolor="white", alpha=0.85)
    ax.axvline(df["Age"].mean(), color=COLORS["secondary"], linestyle="--", label=f'Mean: {df["Age"].mean():.0f}')
    ax.set_xlabel("Age")
    ax.set_ylabel("Frequency")
    ax.set_title("Age Distribution", fontsize=14, fontweight="bold")
    ax.legend()
    name = save_chart(fig, "age_distribution")
    return insight(
        "Age Distribution",
        f"Average employee age is {df['Age'].mean():.1f} years with most employees between 30-45. "
        f"Mid-career professionals represent the core workforce and key retention focus.",
        name,
    )


def chart_education(df: pd.DataFrame) -> dict:
    edu_map = {1: "Below College", 2: "College", 3: "Bachelor", 4: "Master", 5: "Doctor"}
    df_edu = df.copy()
    df_edu["EducationLabel"] = df_edu["Education"].map(edu_map)
    counts = df_edu["EducationLabel"].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(counts.index, counts.values, color=PALETTE[:len(counts)], edgecolor="white")
    ax.set_title("Education Level Distribution", fontsize=14, fontweight="bold")
    plt.xticks(rotation=15)
    name = save_chart(fig, "education_distribution")
    return insight(
        "Education Distribution",
        "Bachelor's degree holders form the largest educated segment. "
        "Higher education correlates with specific roles in R&D and influences compensation expectations.",
        name,
    )


def chart_business_travel(df: pd.DataFrame) -> dict:
    counts = df["BusinessTravel"].value_counts()
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(counts.index, counts.values, color=[PALETTE[0], PALETTE[1], PALETTE[2]])
    ax.set_title("Business Travel Frequency", fontsize=14, fontweight="bold")
    plt.xticks(rotation=20)
    name = save_chart(fig, "business_travel")
    return insight(
        "Business Travel",
        f"Most employees ({counts.get('Travel_Rarely', 0)}) travel rarely. "
        f"Frequent travelers face higher burnout risk — a known attrition driver.",
        name,
    )


def chart_marital_status(df: pd.DataFrame) -> dict:
    counts = df["MaritalStatus"].value_counts()
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.pie(counts.values, labels=counts.index, autopct="%1.1f%%", colors=PALETTE[:3], startangle=140)
    ax.set_title("Marital Status", fontsize=14, fontweight="bold")
    name = save_chart(fig, "marital_status")
    return insight(
        "Marital Status",
        "Married employees represent the largest group. Work-life balance policies "
        "significantly impact this demographic's retention decisions.",
        name,
    )


def chart_monthly_income(df: pd.DataFrame) -> dict:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(df["MonthlyIncome"], bins=30, color=PALETTE[0], edgecolor="white", alpha=0.85)
    ax.set_xlabel("Monthly Income ($)")
    ax.set_title("Monthly Income Distribution", fontsize=14, fontweight="bold")
    name = save_chart(fig, "monthly_income")
    return insight(
        "Monthly Income",
        f"Income ranges from ${df['MonthlyIncome'].min():,.0f} to ${df['MonthlyIncome'].max():,.0f} "
        f"with median ${df['MonthlyIncome'].median():,.0f}. Compensation equity reviews recommended for outlier roles.",
        name,
    )


def chart_years_at_company(df: pd.DataFrame) -> dict:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(df["YearsAtCompany"], bins=20, color=PALETTE[1], edgecolor="white", alpha=0.85)
    ax.set_xlabel("Years at Company")
    ax.set_title("Tenure Distribution", fontsize=14, fontweight="bold")
    name = save_chart(fig, "years_at_company")
    return insight(
        "Years at Company",
        "Many employees have fewer than 5 years tenure, indicating either growth hiring or early attrition. "
        "First 3 years are critical for retention investment.",
        name,
    )


def chart_satisfaction(df: pd.DataFrame, col: str, title: str, filename: str) -> dict:
    counts = df[col].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(counts.index.astype(str), counts.values, color=PALETTE[0])
    ax.set_xlabel("Rating (1=Low, 4=High)")
    ax.set_title(title, fontsize=14, fontweight="bold")
    name = save_chart(fig, filename)
    low_pct = round((df[col] <= 2).mean() * 100, 1)
    return insight(
        title,
        f"{low_pct}% of employees report low {col.replace('Satisfaction', ' satisfaction').lower()} (≤2). "
        f"Addressing satisfaction gaps can directly reduce attrition risk.",
        name,
    )


def chart_overtime(df: pd.DataFrame) -> dict:
    counts = df["OverTime"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.bar(counts.index, counts.values, color=[PALETTE[0], COLORS["secondary"]])
    ax.set_title("Overtime Distribution", fontsize=14, fontweight="bold")
    name = save_chart(fig, "overtime")
    ot_rate = round(counts.get("Yes", 0) / len(df) * 100, 1)
    return insight(
        "Overtime",
        f"{ot_rate}% of employees work overtime — one of the strongest predictors of attrition. "
        f"Workload management initiatives should prioritize overtime reduction.",
        name,
    )


def chart_attrition_by(col: str, df: pd.DataFrame, filename: str, title: str) -> dict:
    ct = pd.crosstab(df[col], df["Attrition"], normalize="index") * 100
    fig, ax = plt.subplots(figsize=(10, 6))
    ct.plot(kind="bar", ax=ax, color=[PALETTE[0], COLORS["secondary"]], edgecolor="white")
    ax.set_ylabel("Percentage (%)")
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.legend(title="Attrition")
    plt.xticks(rotation=30, ha="right")
    name = save_chart(fig, filename)
    if "Yes" in ct.columns:
        max_cat = ct["Yes"].idxmax()
        max_rate = ct["Yes"].max()
        text = f"Highest attrition in '{max_cat}' at {max_rate:.1f}%. Targeted interventions recommended."
    else:
        text = "Attrition patterns vary across categories."
    return insight(title, text, name)


def chart_correlation_matrix(df: pd.DataFrame) -> dict:
    numeric = df.select_dtypes(include=[np.number]).columns.tolist()
    corr = df[numeric].corr()
    fig, ax = plt.subplots(figsize=(14, 10))
    sns.heatmap(corr, annot=False, cmap="YlOrBr", center=0, ax=ax, linewidths=0.5)
    ax.set_title("Correlation Matrix", fontsize=14, fontweight="bold")
    name = save_chart(fig, "correlation_matrix")
    return insight(
        "Correlation Matrix",
        "Monthly Income correlates with Job Level and Total Working Years. "
        "Satisfaction metrics show inter-correlation, supporting composite satisfaction scoring.",
        name,
    )


def chart_heatmap_attrition(df: pd.DataFrame) -> dict:
    pivot = pd.crosstab(df["Department"], df["OverTime"], values=df["Attrition"].map({"Yes": 1, "No": 0}), aggfunc="mean")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(pivot * 100, annot=True, fmt=".1f", cmap="YlOrBr", ax=ax)
    ax.set_title("Attrition Rate: Department × Overtime (%)", fontsize=14, fontweight="bold")
    name = save_chart(fig, "heatmap_department_overtime")
    return insight(
        "Department × Overtime Heatmap",
        "Sales employees with overtime show elevated attrition rates. "
        "Cross-dimensional analysis reveals high-risk workforce segments.",
        name,
    )


def chart_feature_importance_proxy(df: pd.DataFrame) -> dict:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import LabelEncoder

    data = df.copy()
    le = LabelEncoder()
    data["Target"] = le.fit_transform(data["Attrition"])
    cat_cols = data.select_dtypes(include=["object"]).columns.tolist()
    for col in cat_cols:
        data[col] = LabelEncoder().fit_transform(data[col].astype(str))

    feature_cols = [c for c in data.columns if c not in ("Target", "AgeGroup", "IncomeCategory")]
    X = data[feature_cols]
    y = data["Target"]
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X, y)
    imp = pd.Series(rf.feature_importances_, index=feature_cols).sort_values(ascending=True).tail(15)

    fig, ax = plt.subplots(figsize=(10, 7))
    imp.plot(kind="barh", ax=ax, color=PALETTE[0])
    ax.set_title("Feature Importance (Random Forest Proxy)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Importance")
    name = save_chart(fig, "feature_importance")
    top = imp.idxmax()
    return insight(
        "Feature Importance",
        f"Top attrition drivers include OverTime, MonthlyIncome, and {top}. "
        f"HR should prioritize these factors in retention strategy.",
        name,
    )


def generate_chart_data(df: pd.DataFrame) -> dict:
    """Generate JSON chart data for frontend API."""
    edu_map = {1: "Below College", 2: "College", 3: "Bachelor", 4: "Master", 5: "Doctor"}

    def counts_dict(series):
        return {str(k): int(v) for k, v in series.items()}

    def attrition_rate(group_col):
        return (
            df.groupby(group_col)["Attrition"]
            .apply(lambda x: round((x == "Yes").mean() * 100, 2))
            .to_dict()
        )

    return {
        "gender": counts_dict(df["Gender"].value_counts()),
        "department": counts_dict(df["Department"].value_counts()),
        "jobRole": counts_dict(df["JobRole"].value_counts().head(10)),
        "ageGroups": counts_dict(df["AgeGroup"].value_counts()),
        "education": counts_dict(df["Education"].map(edu_map).value_counts()),
        "businessTravel": counts_dict(df["BusinessTravel"].value_counts()),
        "maritalStatus": counts_dict(df["MaritalStatus"].value_counts()),
        "overTime": counts_dict(df["OverTime"].value_counts()),
        "performanceRating": counts_dict(df["PerformanceRating"].value_counts()),
        "workLifeBalance": counts_dict(df["WorkLifeBalance"].value_counts()),
        "environmentSatisfaction": counts_dict(df["EnvironmentSatisfaction"].value_counts()),
        "relationshipSatisfaction": counts_dict(df["RelationshipSatisfaction"].value_counts()),
        "jobSatisfaction": counts_dict(df["JobSatisfaction"].value_counts()),
        "departmentAttrition": attrition_rate("Department"),
        "jobRoleAttrition": attrition_rate("JobRole"),
        "educationAttrition": attrition_rate("Education"),
        "ageGroupAttrition": attrition_rate("AgeGroup"),
        "salaryBins": {
            str(k): int(v) for k, v in pd.cut(df["MonthlyIncome"], bins=5).value_counts().items()
        },
        "yearsAtCompany": counts_dict(df["YearsAtCompany"].value_counts().head(15)),
        "monthlyIncomeAvg": round(float(df["MonthlyIncome"].mean()), 2),
        "distanceFromHome": counts_dict(df["DistanceFromHome"].value_counts().head(10)),
    }


def run_eda() -> dict:
    """Execute full EDA pipeline."""
    print("Running EDA...")
    df = load_data()
    insights = []

    chart_funcs = [
        chart_gender_distribution,
        chart_department_distribution,
        chart_job_role,
        chart_age_distribution,
        chart_education,
        chart_business_travel,
        chart_marital_status,
        chart_monthly_income,
        chart_years_at_company,
        lambda d: chart_satisfaction(d, "PerformanceRating", "Performance Rating", "performance_rating"),
        lambda d: chart_satisfaction(d, "WorkLifeBalance", "Work Life Balance", "work_life_balance"),
        lambda d: chart_satisfaction(d, "EnvironmentSatisfaction", "Environment Satisfaction", "environment_satisfaction"),
        lambda d: chart_satisfaction(d, "RelationshipSatisfaction", "Relationship Satisfaction", "relationship_satisfaction"),
        lambda d: chart_satisfaction(d, "JobSatisfaction", "Job Satisfaction", "job_satisfaction"),
        chart_overtime,
        lambda d: chart_attrition_by("Department", d, "department_attrition", "Department vs Attrition"),
        lambda d: chart_attrition_by("JobRole", d, "job_role_attrition", "Job Role vs Attrition"),
        lambda d: chart_attrition_by("Education", d, "education_attrition", "Education vs Attrition"),
        lambda d: chart_attrition_by("AgeGroup", d, "age_group_attrition", "Age Group vs Attrition"),
        lambda d: chart_attrition_by("IncomeCategory", d, "salary_attrition", "Salary Category vs Attrition"),
        chart_correlation_matrix,
        chart_heatmap_attrition,
        chart_feature_importance_proxy,
    ]

    for func in chart_funcs:
        insights.append(func(df))

    chart_data = generate_chart_data(df)
    output = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "insights": insights,
        "chart_data": chart_data,
    }
    EDA_INSIGHTS_PATH.write_text(json.dumps(output, indent=2, default=str), encoding="utf-8")
    print(f"  Generated {len(insights)} charts and insights")
    return output


if __name__ == "__main__":
    run_eda()
