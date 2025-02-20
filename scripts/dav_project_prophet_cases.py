from prophet import Prophet
import pandas as pd
import plotly.express as px
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import TimeSeriesSplit
import parsing as ps

def load_dataset():
    cases = pd.read_csv('data/us-cases.csv')
    cases.dropna(inplace = True)
    cases.rename(columns = {'date':'ds', 'New daily cases per 100k': 'y'}, inplace = True)
    cases['floor'] = 0
    cases['cap'] = 300000000

    return cases

def modelling(train, test):
    model = Prophet(growth = 'logistic')
    model.fit(train)

    predictions = model.predict(test)
    predictions['yhat'] = predictions['yhat'].clip(lower=0)

    time_frame = model.make_future_dataframe(freq = 'D', periods = 365, include_history = False)
    time_frame['floor'] = 0
    time_frame['cap'] = 300000000

    forecast = model.predict(time_frame)
    forecast['yhat'] = forecast['yhat'].clip(lower=0)

    return predictions, forecast

def plot_prophet(df, country_name):

    fig = px.line(df, x = 'ds',
                  y = 'y',
                  color = 'time',
                  title = f' New daily COVID-19 cases in the {country_name}',
                  labels = {'ds':'Date', 'y':'Cases per 100k'},
                  width = 1200,
                  height = 500)
    
    fig.add_scatter(x = df['ds'], y = df['yhat_lower'],
                    mode='lines',
                    line=dict(color='rgba(239, 85, 53, 0.3)'),
                    name = f'95% CI',
                    showlegend = False)
    
    fig.add_scatter(x = df['ds'], y = df['yhat_upper'],
                    mode='lines', 
                    line = dict(color = 'rgba(239, 85, 53, 0.3)'),
                    fill='tonexty',
                    name = f'95% CI',
                    showlegend = False)

    fig.update_layout(font = dict(size = 20),
                      template="plotly_white",
                      legend_title_text = None,
                      legend = dict(yanchor="top",
                                    y = 0.99,
                                    xanchor="right",
                                    x = 0.99))
    
    fig.update_yaxes(range=[0, 250])

    args = ps.parse()
    if args.save == 0:
        fig.show()
    if args.save == 1:
        path = 'plots/prophet_cases_'
        fig.write_image(path + '.png')
        fig.write_html(path + '.html')
        print(f'Plot saved under: {path}')

def prophet_error(df):
    mean_error = 0
    splits = 5
    tscv = TimeSeriesSplit(n_splits=splits)

    for train_index, test_index in tscv.split(df):
        train, test = df.iloc[train_index], df.iloc[test_index]
        predictions, _ = modelling(train, test)
        mean_error += mean_absolute_error(test['y'], predictions['yhat'])

    mean_error /= splits
    print(f'The mean error: {mean_error}')

    return mean_error

def calculations(df):
    _, forecast = modelling(df, df)
    mean_error = prophet_error(df)

    return forecast, mean_error

def main():
    country_name = 'USA'
    cases = load_dataset()
    cases_forecast, _ = calculations(cases)

    cases_forecast = cases_forecast[['ds', 'yhat', 'yhat_upper', 'yhat_lower']]
    cases_forecast.rename(columns = {'yhat': 'y'}, inplace = True)
    cases['time'] = 'past'
    cases_forecast['time'] = 'forecast'
    
    df = pd.concat([cases, cases_forecast], ignore_index = True)
    
    plot_prophet(df, country_name)

if __name__ == "__main__":
    main()
