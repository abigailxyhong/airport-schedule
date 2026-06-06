import dash
from dash import html

dash.register_page(__name__, path="/routes")

layout = html.Div([
    html.H2("Routes")
])