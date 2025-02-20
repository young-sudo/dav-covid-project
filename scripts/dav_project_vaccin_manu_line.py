import parsing as ps
import pandas as pd
import plotly.express as px

data = pd.read_csv('data/us-vaccinations-manu.csv')
data = data[data['vaccine'] != 'Novavax']

fig = px.line(data,
              x = 'date',
              y = 'total_vaccinations',
              color = 'vaccine',
              width = 600,
              height = 600,
              title = 'US Total vaccinations by manufacturer',
              category_orders = {'vaccine':['Pfizer/BioNTech', 'Moderna', 'Johnson&Johnson']},
              labels = {'total_vaccinations':'Total Vaccinations',
                        'date':'Date',
                        'vaccine':'Manufacturer'},)

fig.update_layout(font = dict(size = 16),
                  template="plotly_white",
                  legend = dict(yanchor="top",
                                y = 0.99,
                                xanchor="left",
                                x = 0.01))

args = ps.parse()
if args.save == 0:
    fig.show()
if args.save == 1:
    path = 'plots/vaccin_manu_line'
    fig.write_image(path + '.png')
    fig.write_html(path + '.html')
    print(f'Plot saved under: {path}')
