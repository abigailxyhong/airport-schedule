import dash
from dash import html

dash.register_page(__name__, path="/capacity")

layout = html.Div([
    html.H2("Capacity Utilisation")
])