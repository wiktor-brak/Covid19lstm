import plotly.graph_objects as go
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import pandas as pd
import dash
from app import application


pd.set_option("display.max_rows", 1000)
pd.set_option("display.max_columns", 1000)

url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
df_raw = pd.read_csv(url)
df_raw = df_raw[df_raw['location'] != 'International']
df_raw = df_raw.drop(
    df_raw.columns.difference(
        ['location', 'new_cases', 'total_cases', 'total_deaths', 'new_deaths', 'total_tests', 'new_tests', 'date',
         'aged_65_older', 'population', 'median_age', 'extreme_poverty', 'male_smokers', 'female_smokers']),
    axis=1)

iterList = df_raw.location.unique()

LAYOUT_STYLE = {
    "background-color": "#f8f9fa"
}

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.P(id='population', className="card-text"),
            dbc.Button(
                "More Info", id="popover-target", color="secondary"
            ),
            dbc.Popover(
                [
                    dbc.PopoverHeader("Population"),
                    dbc.PopoverBody(
                        "Population in 2020, Source:  	United Nations, Department of Economic and Social Affairs, "
                        "Population Division, World Population Prospects: The 2019 Revision"),
                ],
                id="popover",
                is_open=False,
                target="popover-target",
            )
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P(id='deathrate-output', className="card-text"),
            dbc.Button(
                "More Info", id="popover-target", color="secondary"
            ),
            dbc.Popover(
                [
                    dbc.PopoverHeader("Death rate"),
                    dbc.PopoverBody("Death rate from COVID-19(Total deaths/Total cases)"),
                ],
                id="popover",
                is_open=False,
                target="popover-target",
            )
        ]
    ),
    className="mt-3",
)

tab3_content = dbc.Card(
    dbc.CardBody(
        [
            html.P(id='aged-output', className="card-text"),
            dbc.Button(
                "More Info", id="popover-target", color="secondary"
            ),
            dbc.Popover(
                [
                    dbc.PopoverHeader("Aged 65+"),
                    dbc.PopoverBody("Share of the population that is 65 years and older, most recent year available. "
                                    "Source: World Bank – World Development Indicators, based on age/sex distributions "
                                    "of United Nations Population Division's World Population Prospects: 2017 Revision"),
                ],
                id="popover",
                is_open=False,
                target="popover-target",
            )
        ]
    ),
    className="mt-3",
)

tab4_content = dbc.Card(
    dbc.CardBody(
        [
            html.P(id='median_age', className="card-text"),
            dbc.Button(
                "More Info", id="popover-target", color="secondary"
            ),
            dbc.Popover(
                [
                    dbc.PopoverHeader("Median age"),
                    dbc.PopoverBody("Median age of the population, UN projection for 2020. "
                                    "Source:  	UN Population Division, World Population Prospects, 2017 Revision"),
                ],
                id="popover",
                is_open=False,
                target="popover-target",
            )
        ]
    ),
    className="mt-3",
)

tab5_content = dbc.Card(
    dbc.CardBody(
        [
            html.P(id='extreme_poverty', className="card-text"),
            dbc.Button(
                "More Info", id="popover-target", color="secondary"
            ),
            dbc.Popover(
                [
                    dbc.PopoverHeader("Extreme Poverty"),
                    dbc.PopoverBody(
                        "Share of the population living in extreme poverty, most recent year available since 2010."
                        "Source: World Bank – World Development Indicators, sourced from World Bank "
                        "Development Research Group"),
                ],
                id="popover",
                is_open=False,
                target="popover-target",
            )
        ]
    ),
    className="mt-3",
)

tab6_content = dbc.Card(
    dbc.CardBody(
        [
            html.P(id='male_smokers', className="card-text"),
            dbc.Button(
                "More Info", id="popover-target", color="secondary"
            ),
            dbc.Popover(
                [
                    dbc.PopoverHeader("Male smokers"),
                    dbc.PopoverBody("Share of men who smoke, most recent year available. "
                                    "Source: World Bank – World Development Indicators, sourced from World Health "
                                    "Organization, Global Health Observatory Data Repository"),
                ],
                id="popover",
                is_open=False,
                target="popover-target",
            )
        ]
    ),
    className="mt-3",
)

tab7_content = dbc.Card(
    dbc.CardBody(
        [
            html.P(id='female_smokers', className="card-text"),
            dbc.Button(
                "More Info", id="popover-target", color="secondary"
            ),
            dbc.Popover(
                [
                    dbc.PopoverHeader("Female smokers"),
                    dbc.PopoverBody("Share of women who smoke, most recent year available. "
                                    "Source: World Bank – World Development Indicators, sourced from World Health "
                                    "Organization, Global Health Observatory Data Repository"),
                ],
                id="popover",
                is_open=False,
                target="popover-target",
            )
        ]
    ),
    className="mt-3",
)


@application.callback(
    dash.dependencies.Output('dd-output-container', 'figure'),
    [dash.dependencies.Input('switch-dropdown', 'value'),
     dash.dependencies.Input('countries-dropdown', 'value')])
def update_output(value_nt, value_ct):
    fig = go.Figure()
    fig.add_traces(
        go.Scatter(x=df_raw[df_raw.location == value_ct].date,
                   y=df_raw[df_raw.location == value_ct].loc[:, value_nt],
                   name=str(value_nt)))
    return go.Figure(fig)


@application.callback(
    dash.dependencies.Output('deathrate-output', 'children'),
    [dash.dependencies.Input('countries-dropdown', 'value')])
def update_outputDeathRate(value):
    dr1 = df_raw[df_raw.location == value].total_deaths.sum()
    dr2 = df_raw[df_raw.location == value].total_cases.sum()
    if dr2 != 0:
        deathRate = dr1 / dr2
    returnString = "Death rate: " + str(round(deathRate, 5)) + "%"
    return returnString


@application.callback(
    dash.dependencies.Output('aged-output', 'children'),
    [dash.dependencies.Input('countries-dropdown', 'value')])
def update_outputAged(value):
    val = str(df_raw[df_raw.location == value].aged_65_older.unique())[1:-1]
    if val is None or val == '' or val == "nan" or val == '0':
        return "No data"
    return "Aged 65 and older: " + val + "%"


@application.callback(
    dash.dependencies.Output('population', 'children'),
    [dash.dependencies.Input('countries-dropdown', 'value')])
def update_outputPopulation(value):
    pop = str(df_raw[df_raw.location == value].population.unique())[1:-1]
    po = float(pop)
    return "Population: " + str(int(po))


@application.callback(
    dash.dependencies.Output('median_age', 'children'),
    [dash.dependencies.Input('countries-dropdown', 'value')])
def update_outputMedianAge(value):
    val = str(df_raw[df_raw.location == value].median_age.unique())[1:-1]
    if val is None or val == '' or val == "nan" or val == '0':
        return "No data"
    return "Median age: " + val


@application.callback(
    dash.dependencies.Output('extreme_poverty', 'children'),
    [dash.dependencies.Input('countries-dropdown', 'value')])
def update_outputExtremePoverty(value):
    val = str(df_raw[df_raw.location == value].extreme_poverty.unique())[1:-1]
    if val is None or val == '' or val == "nan" or val == '0':
        return "No data"
    return "Extreme poverty: " + val + "%"


@application.callback(
    dash.dependencies.Output('male_smokers', 'children'),
    [dash.dependencies.Input('countries-dropdown', 'value')])
def update_outputMaleSmokers(value):
    val = str(df_raw[df_raw.location == value].male_smokers.unique())[1:-1]
    if val is None or val == '' or val == "nan" or val == '0':
        return "No data"
    return "Male smokers: " + val + "%"


@application.callback(
    dash.dependencies.Output('female_smokers', 'children'),
    [dash.dependencies.Input('countries-dropdown', 'value')])
def update_outputFemaleSmokers(value):
    val = str(df_raw[df_raw.location == value].female_smokers.unique())[1:-1]
    if val is None or val == '' or val == "nan" or val == '0':
        return "No data"
    return "Female smokers: " + val + "%"


@application.callback(
    dash.dependencies.Output("popover", "is_open"),
    [dash.dependencies.Input("popover-target", "n_clicks")],
    [dash.dependencies.State("popover", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open


@application.callback(dash.dependencies.Output("content", "children"),
              [dash.dependencies.Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        return tab1_content
    elif at == "tab-2":
        return tab2_content
    elif at == "tab-3":
        return tab3_content
    elif at == "tab-4":
        return tab4_content
    elif at == "tab-5":
        return tab5_content
    elif at == "tab-6":
        return tab6_content
    elif at == "tab-7":
        return tab7_content
    return html.P("This shouldn't ever be displayed...")


# update layout with buttons, and show the figure

layout = html.Div(
    [
        html.H4(
            children='COVID-19 Country Info',
            style={
                'marginTop': 20,
                'marginBottom': 30,
                'textAlign': 'center'
            }
        ),
        html.H6(children="Select country"),
        dcc.Dropdown(
            id='countries-dropdown',
            options=[{'label': val, 'value': val} for idx, val in enumerate(iterList)],
            value='United States',  # default value to show
            searchable=True),
        html.Br(),
        html.H6(children="Select value to display(per date)"),
        dcc.Dropdown(
            id='switch-dropdown',
            options=[
                {'label': 'Total cases', 'value': 'total_cases'},
                {'label': 'New cases', 'value': 'new_cases'},
                {'label': 'Total deaths', 'value': 'total_deaths'},
                {'label': 'New deaths', 'value': 'new_deaths'},
                {'label': 'Total tests', 'value': 'total_tests'},
                {'label': 'New tests', 'value': 'new_tests'}
            ],
            value='total_cases'
        ),
        dbc.Row(dbc.Col(html.Div(
            dcc.Graph(
                id='dd-output-container',
                figure=go.Figure()
            )
        ))),
        html.Br(),
        dbc.Tabs(
            [
                dbc.Tab(label="Population", tab_id="tab-1"),
                dbc.Tab(label="Death rate", tab_id="tab-2"),
                dbc.Tab(label="Aged 65+", tab_id="tab-3"),
                dbc.Tab(label="Median age", tab_id="tab-4"),
                dbc.Tab(label="Extreme Poverty", tab_id="tab-5"),
                dbc.Tab(label="Male smokers", tab_id="tab-6"),
                dbc.Tab(label="Female smokers", tab_id="tab-7"),
            ],
            id="tabs",
            active_tab="tab-1",
        ),
        html.Div(id="content"),

    ]
)
