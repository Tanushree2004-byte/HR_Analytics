# Data Quality Report

**Generated:** 2026-06-29 12:07:10

## Quality Score Summary

| Check | Status | Details |
|-------|--------|---------|
| Completeness | PASS | 0 missing values handled |
| Uniqueness | PASS | 0 duplicates removed |
| Validity | PASS | All categorical values validated |
| Consistency | PASS | Data types standardized |
| Timeliness | PASS | Dataset current for analysis |

## Column Statistics

|                          |   count |   unique | top                    |   freq |         mean |         std |   min |      25% |      50% |      75% |   max |
|:-------------------------|--------:|---------:|:-----------------------|-------:|-------------:|------------:|------:|---------:|---------:|---------:|------:|
| Age                      |    1470 |      nan | nan                    |    nan |    36.9238   |    9.13537  |    18 |   30     |    36    |    43    |    60 |
| Attrition                |    1470 |        2 | No                     |   1233 |   nan        |  nan        |   nan |  nan     |   nan    |   nan    |   nan |
| BusinessTravel           |    1470 |        3 | Travel_Rarely          |   1043 |   nan        |  nan        |   nan |  nan     |   nan    |   nan    |   nan |
| DailyRate                |    1470 |      nan | nan                    |    nan |   802.486    |  403.509    |   102 |  465     |   802    |  1157    |  1499 |
| Department               |    1470 |        3 | Research & Development |    961 |   nan        |  nan        |   nan |  nan     |   nan    |   nan    |   nan |
| DistanceFromHome         |    1470 |      nan | nan                    |    nan |     9.19252  |    8.10686  |     1 |    2     |     7    |    14    |    29 |
| Education                |    1470 |      nan | nan                    |    nan |     2.91293  |    1.02416  |     1 |    2     |     3    |     4    |     5 |
| EducationField           |    1470 |        6 | Life Sciences          |    606 |   nan        |  nan        |   nan |  nan     |   nan    |   nan    |   nan |
| EmployeeNumber           |    1470 |      nan | nan                    |    nan |  1024.87     |  602.024    |     1 |  491.25  |  1020.5  |  1555.75 |  2068 |
| EnvironmentSatisfaction  |    1470 |      nan | nan                    |    nan |     2.72177  |    1.09308  |     1 |    2     |     3    |     4    |     4 |
| Gender                   |    1470 |        2 | Male                   |    882 |   nan        |  nan        |   nan |  nan     |   nan    |   nan    |   nan |
| HourlyRate               |    1470 |      nan | nan                    |    nan |    65.8912   |   20.3294   |    30 |   48     |    66    |    83.75 |   100 |
| JobInvolvement           |    1470 |      nan | nan                    |    nan |     2.72993  |    0.711561 |     1 |    2     |     3    |     3    |     4 |
| JobLevel                 |    1470 |      nan | nan                    |    nan |     2.06395  |    1.10694  |     1 |    1     |     2    |     3    |     5 |
| JobRole                  |    1470 |        9 | Sales Executive        |    326 |   nan        |  nan        |   nan |  nan     |   nan    |   nan    |   nan |
| JobSatisfaction          |    1470 |      nan | nan                    |    nan |     2.72857  |    1.10285  |     1 |    2     |     3    |     4    |     4 |
| MaritalStatus            |    1470 |        3 | Married                |    673 |   nan        |  nan        |   nan |  nan     |   nan    |   nan    |   nan |
| MonthlyIncome            |    1470 |      nan | nan                    |    nan |  6502.93     | 4707.96     |  1009 | 2911     |  4919    |  8379    | 19999 |
| MonthlyRate              |    1470 |      nan | nan                    |    nan | 14313.1      | 7117.79     |  2094 | 8047     | 14235.5  | 20461.5  | 26999 |
| NumCompaniesWorked       |    1470 |      nan | nan                    |    nan |     2.6932   |    2.49801  |     0 |    1     |     2    |     4    |     9 |
| OverTime                 |    1470 |        2 | No                     |   1054 |   nan        |  nan        |   nan |  nan     |   nan    |   nan    |   nan |
| PercentSalaryHike        |    1470 |      nan | nan                    |    nan |    15.2095   |    3.65994  |    11 |   12     |    14    |    18    |    25 |
| PerformanceRating        |    1470 |      nan | nan                    |    nan |     3.15374  |    0.360824 |     3 |    3     |     3    |     3    |     4 |
| RelationshipSatisfaction |    1470 |      nan | nan                    |    nan |     2.71224  |    1.08121  |     1 |    2     |     3    |     4    |     4 |
| StockOptionLevel         |    1470 |      nan | nan                    |    nan |     0.793878 |    0.852077 |     0 |    0     |     1    |     1    |     3 |
| TotalWorkingYears        |    1470 |      nan | nan                    |    nan |    11.2796   |    7.78078  |     0 |    6     |    10    |    15    |    40 |
| TrainingTimesLastYear    |    1470 |      nan | nan                    |    nan |     2.79932  |    1.28927  |     0 |    2     |     3    |     3    |     6 |
| WorkLifeBalance          |    1470 |      nan | nan                    |    nan |     2.76122  |    0.706476 |     1 |    2     |     3    |     3    |     4 |
| YearsAtCompany           |    1470 |      nan | nan                    |    nan |     7.00816  |    6.12653  |     0 |    3     |     5    |     9    |    40 |
| YearsInCurrentRole       |    1470 |      nan | nan                    |    nan |     4.22925  |    3.62314  |     0 |    2     |     3    |     7    |    18 |
| YearsSinceLastPromotion  |    1470 |      nan | nan                    |    nan |     2.18776  |    3.22243  |     0 |    0     |     1    |     3    |    15 |
| YearsWithCurrManager     |    1470 |      nan | nan                    |    nan |     4.12313  |    3.56814  |     0 |    2     |     3    |     7    |    17 |
| AgeGroup                 |    1470 |        5 | 26-35                  |    606 |   nan        |  nan        |   nan |  nan     |   nan    |   nan    |   nan |
| IncomeCategory           |    1470 |        4 | Low                    |    369 |   nan        |  nan        |   nan |  nan     |   nan    |   nan    |   nan |
| TenureRatio              |    1470 |      nan | nan                    |    nan |     0.678067 |    0.328097 |     0 |    0.412 |     0.8  |     1    |     1 |
| AvgSatisfaction          |    1470 |      nan | nan                    |    nan |     2.73095  |    0.505815 |     1 |    2.5   |     2.75 |     3    |     4 |
| PromotionGap             |    1470 |      nan | nan                    |    nan |     4.82041  |    4.84776  |     0 |    1     |     4    |     7    |    36 |
| LongTenureNoPromotion    |    1470 |      nan | nan                    |    nan |     0.176871 |    0.381689 |     0 |    0     |     0    |     0    |     1 |
| HighTravel               |    1470 |      nan | nan                    |    nan |     0.188435 |    0.391193 |     0 |    0     |     0    |     0    |     1 |
| LowWorkLifeBalance       |    1470 |      nan | nan                    |    nan |     0.288435 |    0.453189 |     0 |    0     |     0    |     1    |     1 |
| HighOvertime             |    1470 |      nan | nan                    |    nan |     0.282993 |    0.450606 |     0 |    0     |     0    |     1    |     1 |
| YoungEmployee            |    1470 |      nan | nan                    |    nan |     0.262585 |    0.440189 |     0 |    0     |     0    |     1    |     1 |
| LowStockOptions          |    1470 |      nan | nan                    |    nan |     0.429252 |    0.495138 |     0 |    0     |     0    |     1    |     1 |

## Recommendations

1. Monitor overtime and low work-life balance as primary attrition drivers
2. Track employees with long tenure without promotion
3. Review compensation outliers in Sales department
4. Use engineered satisfaction composite for workforce health monitoring
