import pandas as pd
import plotly.express as px
import parsing as ps

# Confidence intervals transformations

data = pd.read_csv('data/us-vaccines-groups.csv')
data[['Lower CI', 'Upper CI']] = data['95% CI (%)'].str.split('-', expand=True).apply(pd.to_numeric)
data['Estimate (%)'] = data['Estimate (%)'].apply(pd.to_numeric)
data = data.groupby(['Group Category', 'Group Name']).mean(numeric_only=True).reset_index()
data['Lower CI'] = data['Estimate (%)'] - data['Lower CI']
data['Upper CI'] = data['Upper CI'] - data['Estimate (%)']

data['Group Category'] = data['Group Category'].apply(lambda x: x.replace('years', '').strip())

# Facets

fig = px.bar(data,
             x='Group Category',
             y='Estimate (%)',
             color='Group Category',
             facet_col = 'Group Name',
             error_y='Upper CI',
             error_y_minus='Lower CI',
             title='US COVID-19 Vaccinations by Group (April 2024)',
             labels={'Estimate (%)': 'Vaccinated (%)', 'Group Category': ''},
             category_orders={'Group Category': ['Male', 'Female']},
             width = 1000,
             height = 500)

fig.update_xaxes(matches=None, showticklabels=True, visible=True)
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

fig.update_layout(font=dict(size=18),
                  template="plotly_white",
                  showlegend=False)

# Saving plot
args = ps.parse()
if args.save == 0:
    fig.show()
elif args.save == 1:
    path = 'plots/vaccin_groups'
    fig.write_image(path + '.png')
    fig.write_html(path + '.html')
    print(f'Plot saved under: {path}')
