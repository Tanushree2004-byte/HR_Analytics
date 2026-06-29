"""Flask REST API for HR Intelligence Platform."""
from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime

from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

from src.backend.services.data_service import DataService
from src.backend.services.report_service import ReportService
from src.config import BASE_DIR, CORS_ORIGINS, DEBUG, FRONTEND_DIR, API_HOST, API_PORT
from src.ml.predict import predictor
from src.data_processing.clean_data import run_cleaning_pipeline
from src.data_processing.eda import run_eda
from src.ml.train import run_training

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")
CORS(app, resources={r"/api/*": {"origins": CORS_ORIGINS.split(",") if CORS_ORIGINS != "*" else "*"}})

UPLOAD_DIR = BASE_DIR / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.route("/api/health")
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat(), "model_loaded": predictor.is_ready()})


@app.route("/api/dashboard")
def dashboard():
    return jsonify({
        "kpis": DataService.get_kpis(),
        "charts": DataService.get_chart_data(),
        "departments": DataService.get_departments(),
        "jobs": DataService.get_jobs(),
        "featureImportance": DataService.get_feature_importance(),
    })


@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    result = predictor.predict(data)
    if "error" in result:
        return jsonify(result), 503
    return jsonify(result)


@app.route("/api/employees")
def employees():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    search = request.args.get("search", "")
    department = request.args.get("department", "")
    sort_by = request.args.get("sort_by", "EmployeeNumber")
    sort_dir = request.args.get("sort_dir", "asc")
    return jsonify(DataService.get_employees(page, per_page, search, department, sort_by, sort_dir))


@app.route("/api/model-metrics")
def model_metrics():
    return jsonify(DataService.get_model_metrics())


@app.route("/api/insights")
def insights():
    return jsonify(DataService.get_insights())


@app.route("/api/departments")
def departments():
    return jsonify(DataService.get_departments())


@app.route("/api/jobs")
def jobs():
    return jsonify(DataService.get_jobs())


@app.route("/api/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files["file"]
    if not file.filename:
        return jsonify({"error": "Empty filename"}), 400

    filename = secure_filename(file.filename)
    if not filename.endswith(".csv"):
        return jsonify({"error": "Only CSV files are supported"}), 400

    save_path = UPLOAD_DIR / filename
    file.save(save_path)

    import shutil
    from src.config import CLEANED_DATA_PATH, RAW_DATA_PATH
    shutil.copy(save_path, RAW_DATA_PATH)

    try:
        run_cleaning_pipeline()
        run_eda()
        run_training()
        DataService.reload()
        predictor._load()
        return jsonify({"message": "Dataset uploaded and pipeline re-run successfully", "filename": filename})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/api/retrain", methods=["POST"])
def retrain():
    try:
        run_training()
        predictor._load()
        return jsonify({"message": "Model retrained successfully", "metrics": DataService.get_model_metrics()})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/api/download-report")
def download_report():
    fmt = request.args.get("format", "pdf")
    if fmt == "csv":
        buf = DataService.export_csv()
        return send_file(buf, mimetype="text/csv", as_attachment=True, download_name="hr_analytics_report.csv")
    elif fmt == "excel":
        buf = DataService.export_excel()
        return send_file(buf, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                         as_attachment=True, download_name="hr_analytics_report.xlsx")
    else:
        buf = ReportService.generate_pdf()
        return send_file(buf, mimetype="application/pdf", as_attachment=True, download_name="hr_analytics_report.pdf")


@app.route("/api/summary")
def summary():
    return jsonify(DataService.get_summary_stats())


@app.route("/assets/<path:filename>")
def serve_assets(filename):
    return send_from_directory(BASE_DIR / "assets", filename)


@app.route("/reports/charts/<path:filename>")
def serve_charts(filename):
    return send_from_directory(BASE_DIR / "reports" / "charts", filename)


@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:page>")
def serve_page(page):
    if page.endswith((".css", ".js", ".png", ".jpg", ".svg", ".ico")):
        return send_from_directory(FRONTEND_DIR, page)
    html_path = FRONTEND_DIR / f"{page.split('.')[0]}.html"
    if html_path.exists():
        return send_from_directory(FRONTEND_DIR, f"{page.split('.')[0]}.html")
    return send_from_directory(FRONTEND_DIR, "404.html"), 404


def create_app():
    return app


if __name__ == "__main__":
    print(f"Starting HR Intelligence Platform API on {API_HOST}:{API_PORT}")
    app.run(host=API_HOST, port=API_PORT, debug=DEBUG)
