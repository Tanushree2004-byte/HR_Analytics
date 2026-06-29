# Data Cleaning Report

**Generated:** 2026-06-29 12:07:10  
**Dataset:** IBM HR Employee Attrition  
**Source:** `HR-Employee-Attrition.csv`

---

## 1. Dataset Overview

| Metric | Value |
|--------|-------|
| Original Rows | 1,470 |
| Cleaned Rows | 1,470 |
| Original Columns | 35 |
| Cleaned Columns | 43 |
| Duplicates Removed | 0 |

---

## 2. Data Types

```
Age                          int64
Attrition                   object
BusinessTravel              object
DailyRate                    int64
Department                  object
DistanceFromHome             int64
Education                    int64
EducationField              object
EmployeeCount                int64
EmployeeNumber               int64
EnvironmentSatisfaction      int64
Gender                      object
HourlyRate                   int64
JobInvolvement               int64
JobLevel                     int64
JobRole                     object
JobSatisfaction              int64
MaritalStatus               object
MonthlyIncome                int64
MonthlyRate                  int64
NumCompaniesWorked           int64
Over18                      object
OverTime                    object
PercentSalaryHike            int64
PerformanceRating            int64
RelationshipSatisfaction     int64
StandardHours                int64
StockOptionLevel             int64
TotalWorkingYears            int64
TrainingTimesLastYear        int64
WorkLifeBalance              int64
YearsAtCompany               int64
YearsInCurrentRole           int64
YearsSinceLastPromotion      int64
YearsWithCurrManager         int64
```

---

## 3. Missing Values

No missing values detected in the dataset.

---

## 4. Duplicate Records

Removed **0** duplicate row(s).

---

## 5. Categorical Validation

- **Attrition** [PASS]: 2 unique values
- **BusinessTravel** [PASS]: 3 unique values
- **Department** [PASS]: 3 unique values
- **Gender** [PASS]: 2 unique values
- **OverTime** [PASS]: 2 unique values
- **Over18** [PASS]: 1 unique values

---

## 6. Outlier Detection (IQR Method)

| Column | Outliers | % | Lower | Upper |
|--------|----------|---|-------|-------|
| Age | 0 | 0.0% | 10.5 | 62.5 |
| DailyRate | 0 | 0.0% | -573.0 | 2195.0 |
| DistanceFromHome | 0 | 0.0% | -16.0 | 32.0 |
| Education | 0 | 0.0% | -1.0 | 7.0 |
| EmployeeCount | 0 | 0.0% | 1.0 | 1.0 |
| EmployeeNumber | 0 | 0.0% | -1105.5 | 3152.5 |
| EnvironmentSatisfaction | 0 | 0.0% | -1.0 | 7.0 |
| HourlyRate | 0 | 0.0% | -5.62 | 137.38 |
| JobInvolvement | 0 | 0.0% | 0.5 | 4.5 |
| JobLevel | 0 | 0.0% | -2.0 | 6.0 |
| JobSatisfaction | 0 | 0.0% | -1.0 | 7.0 |
| MonthlyIncome | 114 | 7.76% | -5291.0 | 16581.0 |
| MonthlyRate | 0 | 0.0% | -10574.75 | 39083.25 |
| NumCompaniesWorked | 52 | 3.54% | -3.5 | 8.5 |
| PercentSalaryHike | 0 | 0.0% | 3.0 | 27.0 |
| PerformanceRating | 226 | 15.37% | 3.0 | 3.0 |
| RelationshipSatisfaction | 0 | 0.0% | -1.0 | 7.0 |
| StandardHours | 0 | 0.0% | 80.0 | 80.0 |
| StockOptionLevel | 85 | 5.78% | -1.5 | 2.5 |
| TotalWorkingYears | 63 | 4.29% | -7.5 | 28.5 |
| TrainingTimesLastYear | 238 | 16.19% | 0.5 | 4.5 |
| WorkLifeBalance | 0 | 0.0% | 0.5 | 4.5 |
| YearsAtCompany | 104 | 7.07% | -6.0 | 18.0 |
| YearsInCurrentRole | 21 | 1.43% | -5.5 | 14.5 |
| YearsSinceLastPromotion | 107 | 7.28% | -4.5 | 7.5 |
| YearsWithCurrManager | 14 | 0.95% | -5.5 | 14.5 |

---

## 7. Standardization & Encoding

- Removed constant/redundant columns: EmployeeCount, StandardHours, Over18
- Engineered features: AgeGroup, IncomeCategory, TenureRatio, AvgSatisfaction, PromotionGap, and risk flags
- Label encoding applied to all categorical variables
- StandardScaler applied to numeric features
- Cleaned dataset saved to `data/cleaned_hr_data.csv`
- Encoded dataset saved to `data/encoded_hr_data.csv`

---

## 8. Feature Engineering Summary

| Feature | Description |
|---------|-------------|
| AgeGroup | Age binned into workforce segments |
| IncomeCategory | Monthly income quartile classification |
| TenureRatio | Years at company / total working years |
| AvgSatisfaction | Mean of satisfaction scores |
| PromotionGap | Years since last promotion relative to tenure |
| LongTenureNoPromotion | Flag for stagnation risk |
| HighTravel / LowWorkLifeBalance / HighOvertime | Behavioral risk indicators |
