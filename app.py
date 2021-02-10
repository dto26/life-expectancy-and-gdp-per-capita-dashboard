import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('data/gapminderDataFiveYear.csv')
# print(df.head())

app = dash.Dash()

# Get a list of each year in data set
year_options = []
for year in df['year'].unique():
    year_options.append({'label':str(year), 'value':year})

app.layout = html.Div([
    dcc.Graph(id='graph'),
    dcc.Dropdown(
        id='year-picker',
        options=year_options,
        value=df['year'].min()) # defaults to lowest year
])

@app.callback(Output('graph', 'figure'), [Input('year-picker', 'value')])
def update_figure(selected_year):
    # data only for selected year
    filtered_df = df[df['year'] == selected_year]
    traces = []
    for continent_name in filtered_df['continent'].unique():
        df_continent = filtered_df[filtered_df['continent'] == continent_name]
        traces.append(go.Scatter(
            x = df_continent['gdpPercap'],
            y = df_continent['lifeExp'],
            mode = 'markers',
            opacity = 0.7,
            marker = {'size':15},
            name = continent_name,
            text=df_continent['country']
        ))

    return {'data':traces,
            'layout':go.Layout(title='Life Expectancy by GDP Per Capita',
                                xaxis={'title':'GDP Per Capita', 'type':'log'},
                                yaxis={'title':'Life Expectancy'},
                                plot_bgcolor="#F9F9F9",
                                )}

if __name__ == '__main__':
    app.run_server()

