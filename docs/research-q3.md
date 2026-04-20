# Research Q3: Weekend vs Weekday Pollution

## Research Question

Are air pollution levels significantly lower on weekends compared to weekdays?

## Hypothesis

Air pollution levels are significantly lower on weekends due to reduced industrial activity and commuter traffic.

## Literature Review

- **Weekday-Weekend Air Quality Differences** (EPA Study): Significant NO2 and PM2.5 reductions on weekends
- **Urban Air Pollution Patterns** (Atmospheric Environment Journal): Traffic-driven pollution peaks on weekdays
- **Air Quality Variability and Human Activity** (Science of Total Environment): Weekend effect documented in major cities

## Proposed Data Sources

| Dataset | Source | Variables |
|---------|--------|-----------|
| EPA Air Quality System | epa.gov | Hourly/daily pollution data |
| EU Air Quality Portal | eea.europa.eu | European city pollution levels |
| Kaggle Air Quality Dataset | kaggle.com/datasets | Historical air quality data |

## Variables Required

- Date (with day of week)
- PM2.5 concentration (μg/m³)
- PM10 concentration (μg/m³)
- NO2 concentration (μg/m³)
- O3 concentration (μg/m³)
- CO concentration (ppm)

## Methodology

1. Collect daily/hourly pollution data
2. Categorize data by day of week (weekend vs weekday)
3. Calculate mean pollution levels for each category
4. Perform t-test or Mann-Whitney U test for significance
5. Create bar charts comparing weekend vs weekday
6. Analyze time-of-day patterns