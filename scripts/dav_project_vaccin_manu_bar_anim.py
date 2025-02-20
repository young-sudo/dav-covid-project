import parsing as ps
import pandas as pd
import plotly.express as px

data = pd.read_csv('data/us-vaccinations-manu.csv')
data['date'] = pd.to_datetime(data['date'])
data = data.pivot(index = 'date', columns = 'vaccine', values= 'total_vaccinations')
data = data.asfreq(freq = 'M', method = 'ffill')
data = data.ffill()
data = data.reset_index()
data['date'] = data['date'].dt.strftime('%Y-%m')
data = data.drop(['Novavax'], axis = 1)
data = data.melt(id_vars='date', var_name='vaccine', value_name='total_vaccinations')

fig = px.bar(data, x = 'vaccine',
              y = 'total_vaccinations',
              color = 'vaccine',
              animation_frame = 'date',
              width = 600,
              height = 600,
              range_y=[0,400000000],
              title = 'US Total vaccinations by manufacturer',
              category_orders = {'vaccine':['Pfizer/BioNTech', 'Moderna', 'Johnson&Johnson']},
              labels = {'total_vaccinations':'Total Vaccinations',
                        'year_month':'Date',
                        'vaccine':'Manufacturer'})

fig.update_layout(font = dict(size = 16),
                  template="plotly_white",
                  showlegend = False)

args = ps.parse()
if args.save == 0:
    fig.show()
if args.save == 1:
    path = 'plots/vaccin_manu_bar_anim'
    fig.write_html(path + '.html')
    print(f'Plot saved under: {path}')
