# HR Analytics — Employee Attrition Prediction & Dashboard

A full-stack HR Analytics platform that transforms employee data into actionable insights. This project combines data cleaning, exploratory data analysis, machine learning, and an interactive dashboard to predict employee attrition and support data-driven HR decisions.

![HR Dashboard Preview](assets/dashboard-preview.png)

> **Note:** Dashboard preview image will be added as the UI is implemented.

---

## Project Overview

Organizations lose talent and institutional knowledge when employees leave unexpectedly. This project analyzes HR workforce data to identify attrition patterns, build predictive models, and deliver an interactive dashboard for HR teams.

The workflow covers the complete data science lifecycle:

1. **Data ingestion & cleaning** — Load and preprocess the IBM HR Employee Attrition dataset
2. **Exploratory data analysis (EDA)** — Uncover trends in demographics, compensation, and satisfaction
3. **Machine learning** — Train and evaluate classification models for attrition prediction
4. **API layer** — Expose predictions via a Flask REST API
5. **Dashboard UI** — Visualize KPIs, trends, and individual employee risk scores

---

## Features

| Module | Status | Description |
|--------|--------|-------------|
| Data Cleaning | Planned | Handle missing values, encode categoricals, feature engineering |
| EDA & Reports | Planned | Statistical summaries, visualizations, insight reports |
| ML Models | Planned | Logistic Regression, Random Forest, and model comparison |
| Prediction API | Planned | Flask endpoints for single and batch predictions |
| HR Dashboard | Planned | Interactive charts, KPIs, employee lookup |
| Deployment | Planned | Production-ready configuration |

---

## Technologies Used

| Layer | Stack |
|-------|-------|
| **Language** | Python 3.10+ |
| **Data & ML** | Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn |
| **Notebooks** | Jupyter Notebook |
| **Backend** | Flask, Flask-CORS |
| **Frontend** | HTML, CSS, JavaScript (Chart.js / Plotly) |
| **Version Control** | Git, GitHub |
| **Deployment** | TBD (Render / Railway / Docker) |

---

## Dataset Information

**Source:** [IBM HR Analytics Employee Attrition & Performance](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)

**File:** `data/HR-Employee-Attrition.csv`

| Property | Value |
|----------|-------|
| Records | ~1,470 employees |
| Features | 35 columns |
| Target | `Attrition` (Yes / No) |

**Key columns:**

- **Demographics:** Age, Gender, MaritalStatus, Education, EducationField
- **Job details:** Department, JobRole, JobLevel, JobInvolvement, OverTime
- **Compensation:** MonthlyIncome, HourlyRate, PercentSalaryHike, StockOptionLevel
- **Satisfaction:** JobSatisfaction, EnvironmentSatisfaction, RelationshipSatisfaction, WorkLifeBalance
- **Tenure:** YearsAtCompany, YearsInCurrentRole, YearsSinceLastPromotion, TotalWorkingYears

---

## Machine Learning Workflow

```
Raw CSV → Data Cleaning → Feature Engineering → Train/Test Split
    → Model Training (Logistic Regression, Random Forest, etc.)
    → Evaluation (Accuracy, Precision, Recall, F1, ROC-AUC)
    → Model Serialization → Flask API → Dashboard
```

**Planned models:**

- Logistic Regression (baseline, interpretable)
- Random Forest Classifier
- Gradient Boosting (optional)

**Evaluation metrics:** Accuracy, Precision, Recall, F1-Score, Confusion Matrix, ROC-AUC

---

## Folder Structure

```
HR_Analytics/
├── .gitignore
├── README.md
├── requirements.txt
├── data/
│   └── HR-Employee-Attrition.csv
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_eda.ipynb
│   └── 03_model_training.ipynb
├── src/
│   ├── data_processing/
│   │   └── clean_data.py
│   ├── ml/
│   │   ├── train.py
│   │   └── predict.py
│   └── backend/
│       └── app.py
├── frontend/
│   ├── index.html
│   ├── css/
│   └── js/
├── models/
│   └── (trained model artifacts — gitignored)
├── reports/
│   └── (generated EDA reports and figures)
├── assets/
│   └── (dashboard screenshots, images)
└── deployment/
    └── (Dockerfile, deployment configs)
```

---

## Installation Steps

### Prerequisites

- Python 3.10 or higher
- Git
- (Optional) Node.js for frontend tooling

### Clone the repository

```bash
git clone https://github.com/Tanushree2004-byte/HR_Analytics.git
cd HR_Analytics
```

### Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Project Locally

> Steps will be updated as modules are implemented.

### 1. Data pipeline & notebooks

```bash
jupyter notebook notebooks/
```

### 2. Start the Flask backend

```bash
python src/backend/app.py
```

### 3. Open the dashboard

Open `frontend/index.html` in a browser, or serve via Flask static files at `http://localhost:5000`.

---

## Deployment Instructions

> Deployment configuration will be added in the final phase.

Planned options:

- **Render / Railway** — Deploy Flask API + static frontend
- **Docker** — Containerized deployment via `deployment/Dockerfile`

---

## API Endpoints

> Endpoints will be documented here once the Flask backend is implemented.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check |
| `POST` | `/api/predict` | Predict attrition for a single employee |
| `POST` | `/api/predict/batch` | Batch predictions |
| `GET` | `/api/stats` | Aggregate HR statistics |

---

## Future Enhancements

- [ ] SHAP / LIME model explainability
- [ ] Real-time data pipeline integration
- [ ] User authentication and role-based access
- [ ] Email alerts for high-risk attrition employees
- [ ] Power BI / Tableau export integration
- [ ] A/B testing for retention strategies
- [ ] Multi-dataset support

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

## Author Information

**Tanushree**

- GitHub: [@Tanushree2004-byte](https://github.com/Tanushree2004-byte)
- Repository: [HR_Analytics](https://github.com/Tanushree2004-byte/HR_Analytics)

---

## Git Workflow

This repository follows milestone-based commits:

- `Initial Project Structure`
- `Added Data Cleaning Module`
- `Completed Exploratory Data Analysis`
- `Implemented Machine Learning Models`
- `Added Attrition Prediction API`
- `Designed HR Dashboard UI`
- `Final Deployment Ready Version`

Each major module is committed and pushed to keep a clean, professional Git history.
