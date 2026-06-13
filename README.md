# Customer Segmentation & Churn Pattern Analytics in European Banking

## Background and Context

Customer churn represents one of the largest hidden costs in retail banking. Losing existing customers leads to:

- Reduced lifetime value
- Increased acquisition costs
- Revenue instability

While banks often track churn rates, they frequently lack the granular segmentation insights needed to answer:

- Which customer groups are most likely to churn?
- How churn differs across countries, age groups, and financial profiles?
- Whether churn is concentrated among high-value or low-value customers?

This project addresses those gaps through systematic segmentation-driven analytics.

## Problem Statement

Despite having rich customer-level data, banks face challenges in:

- Identifying high-risk customer segments
- Understanding churn differences by geography and demographics
- Quantifying the financial profile of churned customers

Without structured analytics, churn management strategies remain generic, reactive, and inefficient.

## Project Objectives

### Primary Objectives

- Measure overall churn rate
- Identify churn distribution across customer segments
- Compare churn behavior across European regions

### Secondary Objectives

- Understand churn among high-value customers
- Evaluate engagement and tenure patterns
- Support strategic planning and marketing decisions

## Dataset Description

The dataset includes the following columns:

- `CustomerId` — Unique customer identifier
- `Surname` — Customer surname
- `CreditScore` — Customer creditworthiness
- `Geography` — France, Spain, Germany
- `Gender` — Male / Female
- `Age` — Customer age
- `Tenure` — Years with the bank
- `Balance` — Account balance
- `NumOfProducts` — Number of bank products
- `HasCrCard` — Credit card ownership
- `IsActiveMember` — Activity indicator
- `EstimatedSalary` — Estimated annual salary
- `Exited` — Churn indicator (target)

## Analytical Methodology

### 1. Data Ingestion & Validation

- Load the dataset from `Data/European_Bank_Cleaned.csv`
- Validate engagement and product fields
- Ensure binary variables are consistent
- Confirm churn labeling accuracy

### 2. Data Cleaning & Preparation

- Remove non-analytical fields such as `Surname`
- Convert categorical variables for grouping
- Create derived segmentation fields like age buckets, credit bands, tenure groups, balance segments, and high-value flags

### 3. Customer Segmentation Design

Segmentation dimensions include:

- Geographic Segmentation: France, Spain, Germany
- Age Segmentation: `<30`, `30-45`, `46-60`, `60+`
- Tenure Segmentation: `New`, `Mid-Term`, `Long-Term`
- Credit Score Bands: `Low`, `Medium`, `High`
- Balance Segments: `Zero Balance`, `Low Balance`, `High Balance`
- High-Value Customer Flag: large-balance accounts

## Key Performance Indicators (KPIs)

- **Overall Churn Rate** — Percentage of customers who exited
- **Segment Churn Rate** — Churn percentage by segment
- **High-Value Churn Ratio** — Churn rate for premium customers
- **Geographic Risk Index** — Regional churn exposure
- **Engagement Drop Indicator** — Inactive vs active churn difference

## Streamlit Web Application Requirements

### Core Modules

- Overall churn summary
- Geography-wise churn visualization
- Age & tenure churn comparison
- High-value customer churn explorer

### User Capabilities

- Segment filters for geography, gender, age, credit band, tenure, and balance
- Dynamic KPI updates based on selected filters
- Drill-down views for high-risk and premium customers

## Deliverables and Submission

- Research paper covering EDA, insights, and recommendations
- Streamlit dashboard for live analytics
- Executive summary for government stakeholders and banking decision-makers

## Conclusion

This project provides a segmentation-driven understanding of customer churn in European banking. By uncovering churn patterns across geography, demographics, and financial profiles, it equips decision-makers with actionable insights to design targeted, data-driven retention strategies.

## Workspace Files

- `app.py` — Streamlit dashboard application
- `Data/European_Bank_Cleaned.csv` — Processed analytics dataset
- `requirements.txt` — Python package dependencies

## Run the Streamlit Dashboard Locally

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the app from the project folder:

```bash
streamlit run app.py
```

3. Open the provided local URL in your browser (usually `http://localhost:8501`).

4. Adjust sidebar filters to explore churn patterns across geography, age, credit score, tenure, and balance.
