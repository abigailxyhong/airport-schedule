from dash import Dash, html
import dash
from components.navbar import navbar

def create_layout(app: Dash) -> html.Div: 
    print(navbar)
    return html.Div(
    className="app-div",
    children=[navbar, dash.page_container]
)