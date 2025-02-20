import parsing as ps
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Data preparation
cumulative_data = pd.read_csv('data/us-vaccinations-manu.csv')

data = cumulative_data.pivot(index = 'date', columns = 'vaccine', values= 'total_vaccinations')
data.index = pd.to_datetime(data.index)
data = data.asfreq(freq = 'M', method = 'ffill')
data = data.ffill()
data = data.reset_index()
data['date'] = data['date'].dt.strftime('%Y-%m')
data = data.drop(['Novavax'], axis = 1)
data = data.melt(id_vars='date', var_name='vaccine', value_name='total_vaccinations')

# Plots
fig = make_subplots(cols=2)

bar = go.Bar(x = data['vaccine'],
              y = data['total_vaccinations'],
              color = 'vaccine',
              animation_frame = 'date',
              width = 1200,
              height = 600,
              range_y=[0,400000000],
              title = 'Total vaccinations by manufacturer in the USA',
              category_orders = {'vaccine':['Pfizer/BioNTech', 'Moderna', 'Johnson&Johnson']},
              labels = {'total_vaccinations':'Total Vaccinations',
                        'year_month':'Date',
                        'vaccine':'Manufacturer'}).data[0]

fig.add_trace(bar, row = 1, col = 1)

fig.update_layout(font = dict(size = 18),
                  template="plotly_white",
                  showlegend = False)

args = ps.parse()
if args.save == 0:
    fig.show()
if args.save == 1:
    path = 'plots/vaccin_manu_anim'
    fig.write_html(path + '.html')
    print(f'Plot saved under: {path}')
