import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import parsing as ps

unemployment = pd.read_csv('data/us-unemployment.csv')
unemployment.rename({'DATE' : 'date', 'UNRATE' : 'unrate'}, axis = 1, inplace = True)
unemployment.set_index('date', inplace = True)
unemployment = unemployment.loc['2020-01-01':'2023-05-01']
unemployment.reset_index(inplace = True)

cases = pd.read_csv('data/us-cases.csv')
cases.drop('New daily cases per million', axis = 1, inplace = True)
cases.bfill(inplace = True)
cases.set_index('date', inplace = True)
cases = cases.loc[:'2023-05-01']
cases.reset_index(inplace = True)

fig = make_subplots(specs=[[{"secondary_y": True}]])

cases_trace = px.line(cases,
                      x = 'date',
                      y = 'New daily cases per 100k').data[0]
cases_trace.name = 'New Daily Cases per 100k'
cases_trace.line.color = px.colors.qualitative.Plotly[0]
cases_trace.showlegend = True

fig.add_trace(cases_trace,
              secondary_y = False)

unemployment_trace = px.line(unemployment,
                             x = 'date',
                             y = 'unrate').data[0]
unemployment_trace.name = 'Unemployment Rate (%)'
unemployment_trace.line.color = px.colors.qualitative.Plotly[1]
unemployment_trace.showlegend = True

fig.add_trace(unemployment_trace,
              secondary_y = True)

fig.update_layout(width = 1200,
                  height = 600,
                  title_text='US Unemployment Rate and COVID-19 Cases Over Time',
                  xaxis_title='Date',
                  yaxis_title='New Daily <b>Cases</b> per 100k',
                  yaxis2_title='<b>Unemployment</b> Rate (%)',
                  template="plotly_white",
                  font = dict(size = 18),
                  legend=dict(xanchor = 'right',
                              x=0.90,
                              yanchor = 'top',
                              y=0.90,
                              bgcolor='rgba(255,255,255,0.5)',
                              bordercolor='rgba(0,0,0,0.5)',
                              borderwidth=1
                              ))

args = ps.parse()
if args.save == 0:
    fig.show()
if args.save == 1:
    path = 'plots/unemployment'
    fig.write_image(path + '.png')
    fig.write_html(path + '.html')
    print(f'Plot saved under: {path}')
