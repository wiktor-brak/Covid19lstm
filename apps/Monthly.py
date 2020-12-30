import pandas as pd
import plotly.graph_objs as go
import plotly.express as px


import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

def Earth():
    # Data optimalization

    url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
    df = pd.read_csv(url)
    df = df.drop(df.columns.difference(['iso_code', 'continent', 'location', 'date', 'total_cases']), axis=1)
    df = df[df['date'] != '2019-12-31']
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['continent'] != None]
    df = df[df['location'] != 'International']
    df = df[df['location'] != 'World']
    df['date'] = pd.to_datetime(df['date'])
    df = df.fillna(0.)
    iterList = list(df['location'].unique())
    d = {name: pd.DataFrame() for name in iterList}

    # Sum date on all locations

    for idx, val in enumerate(iterList):
        d[val] = df[df['location'] == val]
        d[val].date = pd.to_datetime(d[val].date)
        d[val].date = d[val].date.dt.year.astype('str') + '-' + d[val].date.dt.month.astype('str') + '-01'
        d[val].date = pd.to_datetime(d[val].date)
        d[val] = d[val].groupby('date').total_cases.sum().reset_index()
        d[val]['location'] = val
        iso = str(df[df['location'] == val].iso_code.unique()[0])
        d[val]['iso_code'] = iso
        cont = str(df[df['location'] == val].continent.unique()[0])
        d[val]['continent'] = cont
        d[val]['month'] = pd.DatetimeIndex(d[val].date).month

    df_new = pd.DataFrame()

    for idx, val in enumerate(iterList):
        df_new = pd.concat([df_new, d[val]])

    # df_new = df_new[df_new['months'] != 12]
    df_new = df_new.sort_values(by=['month'])
    # Plotting
    plot_data = px.scatter_geo(df_new, locations="iso_code", color="continent",
                               hover_name="location", size="total_cases",
                               animation_frame="month",
                               projection="natural earth"
                               )

    plot_layout = go.Layout(
        height=700,
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    Earth.fig = go.Figure(data=plot_data, layout=plot_layout)
    Earth.fig.update_layout(height=700, title="Map with slider for montlhy COVID-19 cases")


# Funcs

Earth()

layout = html.Div(
    [

        html.H4(
            children='COVID-19 Monthly cases',
            style={
                'marginTop': 20,
                'marginBottom': 30,
                'textAlign': 'center'
            }
        ),


        dbc.Row(dbc.Col(html.Div(
            dcc.Graph(
                figure=Earth.fig
            )
        )))
    ]
)

