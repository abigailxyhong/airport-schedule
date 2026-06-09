import dash
from dash import Dash, html, dcc, Input, Output
import dash_mantine_components as dmc
import plotly.express as px
import pandas as pd
import plotly.io as pio

from components.layout import create_layout
from api.data_loader import load_data

# ------------------------------------------------------------
# App initialisation
# ------------------------------------------------------------
def main() -> None:
    app = Dash(__name__)
    app.title = "Jersey Airport Dashboard"
    app.layout = create_layout(app)
    app.run(debug=True)

if __name__ == "__main__":
    main()
