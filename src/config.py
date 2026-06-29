"""Central configuration for HR Intelligence Platform."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
MODELS_DIR = BASE_DIR / "models"
CHARTS_DIR = REPORTS_DIR / "charts"
FRONTEND_DIR = BASE_DIR / "frontend"
ASSETS_DIR = BASE_DIR / "assets"

RAW_DATA_PATH = DATA_DIR / "HR-Employee-Attrition.csv"
CLEANED_DATA_PATH = DATA_DIR / "cleaned_hr_data.csv"
ENCODED_DATA_PATH = DATA_DIR / "encoded_hr_data.csv"

CLEANING_REPORT_PATH = REPORTS_DIR / "cleaning_report.md"
DATA_QUALITY_REPORT_PATH = REPORTS_DIR / "data_quality_report.md"
SUMMARY_STATS_PATH = REPORTS_DIR / "summary_statistics.json"
EDA_INSIGHTS_PATH = REPORTS_DIR / "eda_insights.json"
MODEL_METRICS_PATH = MODELS_DIR / "metrics.json"
FEATURE_IMPORTANCE_PATH = MODELS_DIR / "feature_importance.json"
BEST_MODEL_PATH = MODELS_DIR / "best_model.joblib"
PREPROCESSOR_PATH = MODELS_DIR / "preprocessor.joblib"
LABEL_ENCODERS_PATH = MODELS_DIR / "label_encoders.joblib"
FEATURE_COLUMNS_PATH = MODELS_DIR / "feature_columns.json"

RANDOM_STATE = 42
TEST_SIZE = 0.2

for directory in (DATA_DIR, REPORTS_DIR, MODELS_DIR, CHARTS_DIR, ASSETS_DIR):
    directory.mkdir(parents=True, exist_ok=True)

API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("PORT", os.getenv("API_PORT", "5000")))
DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
