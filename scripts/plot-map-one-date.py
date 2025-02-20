#!/usr/bin/env python3

import pandas as pd
import plotly.express as px
import geopandas as gpd

from urllib.request import urlopen
import json


if __name__ == "__main__":

    states='https://eric.clst.org/assets/wiki/uploads/Stuff/gz_2010_us_040_00_5m.json'
    with urlopen(states) as response:
        # states_gpd = json.load(response)
        states_gpd = gpd.read_file(response)

    states_gpd["geometry"] = (
        states_gpd.to_crs(states_gpd.estimate_utm_crs()).simplify(10000).to_crs(states_gpd.crs)
    )
    states_gpd.dropna(axis=0, subset="geometry", how="any", inplace=True)

    states_gpd = states_gpd.to_crs(epsg=4326)
    states = states_gpd.__geo_interface__

    selected_date = "2020-11"

    states_cases = pd.read_csv('../data/us-states.csv')
    states_cases["date"] = pd.to_datetime(states_cases[["year", "month"]].assign(day=1))
    states_cases["date_str"] = states_cases["date"].dt.strftime('%Y-%m')

    states_cases = states_cases.sort_values(["date_str", "state"], ascending=True).reset_index(drop=True)

    states_sample = states_cases[states_cases["date"] == selected_date].copy()

    fig = px.choropleth(states_sample, geojson=states, locations='state', color='cases_avg_per_100k', featureidkey='properties.NAME',
                            color_continuous_scale="magma_r",
                            range_color=(0, 150),
                            scope="usa",
                            animation_frame="date",
                            labels={'cases_avg_per_100k':'Avg Cases per 100k'}
                            )
    fig.update_layout(title="Average daily new cases in Nov 2020",
        margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()
    fig.write_html("../data/states_cases_map_2020-11.html")
