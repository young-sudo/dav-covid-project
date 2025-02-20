#!/usr/bin/env python3

import pandas as pd
import seaborn as sns
import plotly.express as px

from urllib.request import urlopen
import json


if __name__ == "__main__":

    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    counties_cases = pd.read_csv('../data/us-counties-clean.csv')
    counties_cases["date"] = pd.to_datetime(counties_cases[["year", "month"]].assign(day=1))
    counties_cases["date_str"] = counties_cases["date"].dt.strftime('%Y-%m')

    fig = px.choropleth(counties_cases, geojson=counties, locations='id', color='cases_avg_per_100k',
                            color_continuous_scale="magma_r",
                            range_color=(0, 100),
                            scope="usa",
                            animation_frame="date",
                            labels={'cases_avg_per_100k':'Avg Cases per 100k'}
                            )
    fig.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()

    fig.write_html("../plots/counties_cases_map.html")
