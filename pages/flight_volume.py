import dash
from dash import html

dash.register_page(__name__, path="/flight_volume")

layout = html.Div([
    html.H2("Flight Volume")
])