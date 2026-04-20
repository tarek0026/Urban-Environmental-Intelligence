# Research Q1: Green Space & Air Quality

## Research Question

Does air quality improve in cities with higher green space coverage per capita?

## Hypothesis

Cities with higher green space coverage per capita have lower air pollution levels (PM2.5, PM10, NO2).

## Literature Review

- **Urban Green Spaces and Air Quality** (WHO, 2021): Green spaces filter pollutants and reduce particulate matter
- **Green Infrastructure and Urban Air Quality** (EU Environmental Agency): Trees and parks absorb NO2 and ozone
- **Urban Vegetation and Air Pollution** (Journal of Environmental Management): Positive correlation between green space and air quality improvement

## Proposed Data Sources

| Dataset | Source | Variables |
|---------|--------|-----------|
| WHO Air Quality Database | who.int/airquality | PM2.5, PM10, NO2 levels by city |
| European Urban Green Space Database | copernicus.eu | Green space % by city |
| World Bank Cities Database | data.worldbank.org | Urban green space per capita |

## Variables Required

- City name
- Green space area (km²) per capita
- PM2.5 concentration (μg/m³)
- PM10 concentration (μg/m³)
- NO2 concentration (μg/m³)

## Methodology

1. Collect city-level data for green space and air quality
2. Calculate green space per capita ratio
3. Perform correlation analysis (Pearson/Spearman)
4. Create scatter plots with regression lines
5. Statistical significance testing (p < 0.05)