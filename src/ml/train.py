"""Machine learning training pipeline — compare models and save best."""
from __future__ import annotations

import json
from datetime import datetime

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent.parent))

from src.config import (
    BEST_MODEL_PATH,
    CHARTS_DIR,
    CLEANED_DATA_PATH,
    FEATURE_IMPORTANCE_PATH,
    MODEL_METRICS_PATH,
    MODELS_DIR,
    RANDOM_STATE,
    TEST_SIZE,
)

try:
    from xgboost import XGBClassifier
    HAS_XGB = True
except ImportError:
    HAS_XGB = False


FEATURE_COLS = [
    "Age", "BusinessTravel", "DailyRate", "Department", "DistanceFromHome",
    "Education", "EducationField", "EnvironmentSatisfaction", "Gender",
    "HourlyRate", "JobInvolvement", "JobLevel", "JobRole", "JobSatisfaction",
    "MaritalStatus", "MonthlyIncome", "MonthlyRate", "NumCompaniesWorked",
    "OverTime", "PercentSalaryHike", "PerformanceRating",
    "RelationshipSatisfaction", "StockOptionLevel", "TotalWorkingYears",
    "TrainingTimesLastYear", "WorkLifeBalance", "YearsAtCompany",
    "YearsInCurrentRole", "YearsSinceLastPromotion", "YearsWithCurrManager",
    "TenureRatio", "AvgSatisfaction", "PromotionGap", "LongTenureNoPromotion",
    "HighTravel", "LowWorkLifeBalance", "HighOvertime", "YoungEmployee", "LowStockOptions",
]

CATEGORICAL = [
    "BusinessTravel", "Department", "EducationField", "Gender",
    "JobRole", "MaritalStatus", "OverTime",
]
NUMERIC = [c for c in FEATURE_COLS if c not in CATEGORICAL]


def prepare_data() -> tuple:
    df = pd.read_csv(CLEANED_DATA_PATH)
    X = df[FEATURE_COLS]
    y = (df["Attrition"] == "Yes").astype(int)
    return train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y)


def build_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL),
        ]
    )


def get_models() -> dict:
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=RANDOM_STATE, class_weight="balanced"),
        "Decision Tree": DecisionTreeClassifier(max_depth=8, random_state=RANDOM_STATE, class_weight="balanced"),
        "Random Forest": RandomForestClassifier(n_estimators=200, max_depth=12, random_state=RANDOM_STATE, class_weight="balanced"),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=150, max_depth=5, random_state=RANDOM_STATE),
    }
    if HAS_XGB:
        models["XGBoost"] = XGBClassifier(
            n_estimators=150, max_depth=5, learning_rate=0.1,
            random_state=RANDOM_STATE, eval_metric="logloss", use_label_encoder=False,
        )
    return models


def evaluate_model(name: str, pipeline: Pipeline, X_test, y_test) -> dict:
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    cm = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)

    metrics = {
        "model": name,
        "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
        "precision": round(float(precision_score(y_test, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, y_pred, zero_division=0)), 4),
        "f1_score": round(float(f1_score(y_test, y_pred, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, y_prob)), 4),
        "confusion_matrix": cm.tolist(),
        "classification_report": report,
    }
    return metrics, y_prob


def plot_roc_curves(results: list, y_test) -> None:
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ["#D4AF37", "#4F4F4F", "#B8962E", "#6B6B6B", "#E8D5A3"]
    for i, (name, pipeline) in enumerate(results):
        y_prob = pipeline.predict_proba(X_test_global)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        auc = roc_auc_score(y_test, y_prob)
        ax.plot(fpr, tpr, label=f"{name} (AUC={auc:.3f})", color=colors[i % len(colors)], linewidth=2)
    ax.plot([0, 1], [0, 1], "k--", alpha=0.5)
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curves — Model Comparison", fontsize=14, fontweight="bold")
    ax.legend(loc="lower right")
    fig.savefig(CHARTS_DIR / "roc_curves.png", dpi=120, bbox_inches="tight")
    plt.close(fig)


def extract_feature_importance(pipeline: Pipeline, model_name: str) -> dict:
    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["classifier"]

    cat_features = preprocessor.named_transformers_["cat"].get_feature_names_out(CATEGORICAL)
    all_features = list(NUMERIC) + list(cat_features)

    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    elif hasattr(model, "coef_"):
        importances = np.abs(model.coef_[0])
    else:
        return {}

    imp_series = pd.Series(importances, index=all_features).sort_values(ascending=False).head(20)
    return {str(k): round(float(v), 4) for k, v in imp_series.items()}


X_test_global = None


def run_training() -> dict:
    global X_test_global
    print("Training ML models...")
    X_train, X_test, y_train, y_test = prepare_data()
    X_test_global = X_test
    preprocessor = build_preprocessor()

    all_metrics = []
    trained_pipelines = []
    best_auc = 0
    best_pipeline = None
    best_name = ""

    for name, model in get_models().items():
        print(f"  Training {name}...")
        pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("classifier", model),
        ])
        pipeline.fit(X_train, y_train)
        metrics, _ = evaluate_model(name, pipeline, X_test, y_test)
        all_metrics.append(metrics)
        trained_pipelines.append((name, pipeline))

        if metrics["roc_auc"] > best_auc:
            best_auc = metrics["roc_auc"]
            best_pipeline = pipeline
            best_name = name

        print(f"    Accuracy: {metrics['accuracy']:.4f} | F1: {metrics['f1_score']:.4f} | AUC: {metrics['roc_auc']:.4f}")

    plot_roc_curves(trained_pipelines, y_test)

    joblib.dump(best_pipeline, BEST_MODEL_PATH)
    feature_importance = extract_feature_importance(best_pipeline, best_name)

    output = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "best_model": best_name,
        "best_roc_auc": best_auc,
        "feature_columns": FEATURE_COLS,
        "categorical_columns": CATEGORICAL,
        "numeric_columns": NUMERIC,
        "models": all_metrics,
    }
    MODEL_METRICS_PATH.write_text(json.dumps(output, indent=2), encoding="utf-8")
    FEATURE_IMPORTANCE_PATH.write_text(json.dumps(feature_importance, indent=2), encoding="utf-8")

    meta = {
        "feature_cols": FEATURE_COLS,
        "categorical": CATEGORICAL,
        "numeric": NUMERIC,
        "best_model": best_name,
    }
    (MODELS_DIR / "model_meta.json").write_text(json.dumps(meta, indent=2))

    print(f"  Best model: {best_name} (AUC: {best_auc:.4f})")
    print(f"  Saved to {BEST_MODEL_PATH}")
    return output


if __name__ == "__main__":
    run_training()
