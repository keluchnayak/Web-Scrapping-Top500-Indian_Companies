# Data Dictionary: AmbitionBox Top 500 Companies

This document describes the structure of the final cleaned dataset: `ambitionbox_top_500_cleaned.csv`

| Column | Meaning | Data Type |
|---|---|---|
| **rank** | The company's rank based on total employee review count | Integer |
| **company_name** | The official name of the company | String |
| **company_url** | The AmbitionBox URL for the company overview | String |
| **rating** | The overall employee rating (out of 5.0) | Float |
| **review_count** | Total number of employee reviews | Integer |
| **industry** | The primary industry/category of the company | String |
| **company_type** | Type of company (e.g., Public, Private, Corporate) | String |
| **headquarters** | Full location string for company headquarters | String |
| **employees** | Range of global employee count | String |
| **work_life_balance** | Sub-rating score for Work-Life Balance | Float |
| **job_security** | Sub-rating score for Job Security | Float |
| **skill_development** | Sub-rating score for Skill Development | Float |
| **salary_benefits** | Sub-rating score for Salary & Benefits | Float |
| **promotions_appraisals** | Sub-rating score for Promotions & Appraisals | Float |
| **company_culture** | Sub-rating score for Company Culture | Float |
| **work_satisfaction** | Sub-rating score for Work Satisfaction | Float |
| **hq_city** | Extracted primary city from the headquarters string | String |
| **employees_clean** | Cleaned version of the employees range string | String |

*Note: All sub-ratings (work_life_balance, job_security, etc.) are scored out of 5.0. If a field was unavailable for a specific company on AmbitionBox, its value is left as missing (NaN).*
