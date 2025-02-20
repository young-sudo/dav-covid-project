# DAV project

*by Younginn Park and Maria Nizik*

`DAV24_project_USA`

## Description

Project USA aims to describe the course of the SARS-CoV-2 in the USA, analyze its influence on the economy of the country and conduct a simple forecast inference on the data.

The project repository contains:
- `data` - processed datasets used for plots
- `scripts` - python scripts used to make the plots
- `plots` - the plots
- `DAV_poster` - static pdf version of the plots
- `DAV_presentation` - interactive html version of the plots

## Data sources

- [Cases, deaths, vaccinations for **whole countries**](https://github.com/owid/covid-19-data) - WHO data organized by Our World in Data
    - us-cases.csv, us-deaths.csv, us-vacc.csv (from new_cases_per_million.csv, new_deaths_per_million.csv, vaccinations.csv)
    - pol-cases.csv, pol-deaths.csv, pol-vacc.csv
    - us-states-vaccinations.csv (from us_state_vaccinations.csv)
- [Cases, deaths for **states and counties**](https://github.com/nytimes/covid-19-data) - CDC data organized by NY Times
    - us-states.csv
    - us-counties.csv (combined from us-counties[2020, 2021, 2022, 2023].csv)
- Economic data from [Bureau of Labor Statistics](https://www.bls.gov/data/)
    - Unemployment rate
    - [Product prices](https://beta.bls.gov/dataQuery/find?fq=survey:[ap]&s=popularity:D)
- Big Mac Index [The Economist](https://github.com/TheEconomist/big-mac-data)
- Vaccination by sex and age [Centers for Disease Control and Prevention](https://data.cdc.gov/Vaccinations/National-Immunization-Survey-Adult-COVID-Module-NI/akkj-j5ru/data)

