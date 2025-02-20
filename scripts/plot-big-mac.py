#!/usr/bin/env python3

import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

if __name__ == "__main__":

    data = pd.read_csv('../data/big-mac-source-data-v2.csv')

    data['date'] = pd.to_datetime(data['date'], format = "%Y-%m-%d")
    data = data[data['date'] > datetime(2019,7,1)]

    data = data[data['name'].isin(['United States', 'Poland'])]


    prices = []

    for i, row in data.iterrows():
        if row['name'] == 'Poland':
            prices.append(row['local_price'] / row['dollar_ex'])
        elif row['name'] == 'United States':
            prices.append(row['local_price'])

    data['burger'] = prices
    data = data.sort_values(['name', 'date'], ascending=[False, True]).reset_index(drop=True)


    fig = px.line(data, x="date",
                y="burger",
                color="name",
                labels={'name': 'Country'},
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

    y_offset = [0, .5, -.5, 0, 0]
    for i, (var, date) in enumerate(variants.items()):
        offset = len(var) * 7
        fig.add_vline(x=datetime.strptime(date, '%Y-%m-%d'), line=dict(color='black', dash='dash', width=1), opacity=0.5)
        fig.add_annotation(x=datetime.strptime(date, '%Y-%m-%d')+timedelta(days=offset),
                        y=8+y_offset[i], text=f" {var.split()[0]}",
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
        fig.add_annotation(x=start + timedelta(days=45),
                        y=2, text=f" {wave}",
                        showarrow=False,
                        font=dict(color="grey", size=13),
                        opacity=0.5, align="center")

    # Footnote
    note = 'Dashed lines show declaration of a variant as VOC'
    fig.add_annotation(
        showarrow=False,
        text=note,
        font=dict(size=8), 
        xref='x domain',
        x=0.5,
        yref='y domain',
        y=-5
        )

    fig.update_layout(
        title="The Big Mac Index",
        yaxis_title="Price for a Big Mac (USD)",
        xaxis_title="Date",
        legend=dict(x=0.01, y=0.99),
        template="plotly_white",
        yaxis=dict(range=[0, 10]),
    )

    fig.show()
    fig.write_html('../plots/big-mac.html')
