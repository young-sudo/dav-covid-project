#!/usr/bin/env python3

import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

if __name__ == "__main__":

    # consumer price index
    eggs = pd.read_csv('../data/eggs_doz.csv')
    eggs['Product'] = 'eggs (doz)'
    bananas = pd.read_csv('../data/bananas_lb.csv')
    bananas['Product'] = 'bananas (lb)'
    coffee = pd.read_csv('../data/coffee_lb.csv')
    coffee['Product'] = 'coffee (lb)'
    oranges = pd.read_csv('../data/oranges_lb.csv')
    oranges['Product'] = 'oranges (lb)'

    products = pd.concat([eggs, bananas, coffee, oranges], axis=0)
    products["Date"] = products.apply(lambda x: datetime(int(x['Year']), int(x['Period'][1:]), 1), axis=1)

    fig = px.line(products, x="Date",
                y="Value",
                color="Product",
                labels={'Value': 'Consumer Price Index (CPI)'},
                title='Consumer Price Indices for selected products',
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
        offset = len(var) * 6
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
                        y=3, text=f" {wave}",
                        showarrow=False,
                        font=dict(color="grey", size=13),
                        opacity=0.5, align="center")

    # Footnote
    note = 'Dashed lines show declaration of a variant as VOC'
    fig.add_annotation(
        showarrow=False,
        text=note,
        font=dict(size=10), 
        xref='x domain',
        x=0.5,
        yref='y domain',
        y=-5
        )

    fig.update_layout(
        title="Consumer Price Index of selected products",
        yaxis_title="Consumer Price Index",
        xaxis_title="Date",
        legend=dict(x=0.01, y=0.99),
        template="plotly_white",
        yaxis=dict(range=[0, 10]),
    )

    fig.show()
    fig.write_html('../plots/products_cpi.html')

