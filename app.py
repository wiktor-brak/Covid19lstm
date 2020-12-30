import dash
import dash_bootstrap_components as dbc

application = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = application.server
application.config.suppress_callback_exceptions = True
