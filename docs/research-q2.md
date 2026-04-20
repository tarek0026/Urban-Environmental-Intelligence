# Research Q2: Temperature & Electricity Consumption

## Research Question

How does temperature variation correlate with electricity consumption across major cities?

## Hypothesis

Higher temperature variation (extreme heat/cold) leads to increased electricity consumption due to heating/cooling demand.

## Literature Review

- **Climate and Energy Consumption** (IEA, 2022): Temperature extremes drive peak electricity demand
- **Urban Energy Demand and Climate** (Energy Policy Journal): Strong correlation between degree-days and energy use
- **Electricity Consumption Patterns in Cities** (World Bank Energy Statistics): Seasonal variations linked to climate zones

## Proposed Data Sources

| Dataset | Source | Variables |
|---------|--------|-----------|
| NOAA Global Climate Database | noaa.gov | Temperature data by city |
| World Bank Energy Statistics | data.worldbank.org | Electricity consumption by city |
| IEA Energy Data | iea.org | City-level electricity demand |

## Variables Required

- City name
- Average temperature (°C)
- Temperature range/standard deviation
- Heating degree days (HDD)
- Cooling degree days (CDD)
- Total electricity consumption (kWh)

## Methodology

1. Collect temperature data for each city (annual averages + variance)
2. Collect electricity consumption data
3. Calculate HDD and CDD for each city
4. Perform correlation analysis between temperature metrics and electricity
5. Create time-series plots if monthly data available
6. Statistical significance testing (p < 0.05)