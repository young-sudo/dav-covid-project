#!/usr/bin/env python3

import pandas as pd
from datetime import datetime, timedelta

import plotly.express as px

if __name__ == "__main__":
        
    us_deaths = pd.read_csv('../data/us-deaths-weekly.csv')
    us_deaths["date"] = pd.to_datetime(us_deaths["date"])
    us_deaths["country"] = "USA"
    us_deaths = us_deaths.head(175)

    pol_deaths = pd.read_csv('../data/pol-deaths-weekly.csv')
    pol_deaths["date"] = pd.to_datetime(pol_deaths["date"])
    pol_deaths["country"] = "Poland"
    pol_deaths = pol_deaths.head(175)

    deaths = pd.concat([us_deaths, pol_deaths], axis=0)

    # Variants
    # https://en.wikipedia.org/wiki/Variants_of_SARS-CoV-2
    # https://en.wikipedia.org/wiki/SARS-CoV-2#Variants
    # https://www.verywellhealth.com/covid-variants-timeline-6741198 - variants timeline and short description


    # Waves
    # https://pandem-ic.com/covid-waves-europe-and-us-compared/
    # Initial wave of 2020. The initial wave produced a higher peak in Europe but the tail was longer in the US.
    # Summer of 2020. The US continued to sustain high mortality rates in the summer of 2020, which were largely avoided in Europe.
    # Winter 2020/21. Europe and US were both affected the worst during this period, with the highest peaks observed in the US.
    # Autumn 2021 through spring 2022. The spread of Delta and subsequently Omicron raised mortality for a long time, again with higher peaks in the US.
    # Post-spring 2022. Mortality rates decreased considerably, even though again the US sustained higher rates than Europe.



    # Static lineplot of cases and deaths
    # Create the line plot using Plotly Express
    fig = px.line(deaths, x="date",
                y="New daily cases per 100k",
                color="country",
                labels={'New daily cases per 100k': 'New daily cases per 100k'},
                title='Daily new cases in USA per 100k',
                width=1000, height=600)


    # Vertical lines for variants
    # De facto all variants were first detected in late 2020
    variants = {
        "Alpha": "2020-12-18",
        "Beta": "2021-01-14",
        "Gamma": "2021-01-15",
        "Delta": "2021-05-06",
        "Omicron": "2021-11-26"
    }

    y_offset = [0, 10, -10, 0, 20]
    for i, (var, date) in enumerate(variants.items()):
        offset = len(var) * 7
        fig.add_vline(x=datetime.strptime(date, '%Y-%m-%d'), line=dict(color='black', dash='dash', width=1), opacity=0.5)
        fig.add_annotation(x=datetime.strptime(date, '%Y-%m-%d')+timedelta(days=offset),
                        y=120+y_offset[i], text=f" {var.split()[0]}",
                        showarrow=False, font=dict(size=10), align="left")

    # Fill between vertical lines (waves)
    waves = {
        "Wave 1": (datetime(2020, 1, 1), datetime(2020, 5, 1)),
        "Wave 2": (datetime(2020, 6, 1), datetime(2020, 9, 1)),
        "Wave 3": (datetime(2020, 10, 1), datetime(2021, 3, 1)),
        "Wave 4": (datetime(2021, 7, 1), datetime(2022, 4, 1)),
        "Wave 5": (datetime(2022, 5, 1), datetime(2022, 9, 1))
    }

    for wave, (start, stop) in waves.items():
        fig.add_shape(type="rect",
                    x0=start, x1=stop,
                    y0=0, y1=300,  # Ensure the rectangle spans the entire y-axis range
                    fillcolor="grey", opacity=0.3,
                    line_width=0)
        fig.add_annotation(x=start + timedelta(days=50),
                        y=75, text=f" {wave}",
                        showarrow=False,
                        font=dict(color="grey", size=15),
                        opacity=0.5, align="center")

    fig.update_layout(
        title="Average daily new deaths in USA per 100k",
        yaxis_title="Deaths per 100k",
        xaxis_title="Date",
        legend=dict(x=0.01, y=0.99),
        template="plotly_white",
        yaxis=dict(range=[0, 150]),
    )

    fig.show()

    fig.write_html("../plots/deaths_line.html")
