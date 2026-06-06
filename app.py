import dash
from dash import Dash, html, dcc, Input, Output
from dash_bootstrap_components.themes import LUX
import plotly.express as px
import pandas as pd

from components.layout import create_layout
from api.data_loader import load_data

# ------------------------------------------------------------
# App initialisation
# ------------------------------------------------------------
def main() -> None:
    app = Dash(external_stylesheets=[LUX], use_pages=True)
    app.title = "Jersey Airport Dashboard"
    app.layout = create_layout(app)
    app.run(debug=True)

# ------------------------------------------------------------
# Callbacks
# ------------------------------------------------------------


# ------------------------------------------------------------
# Entry point
# ------------------------------------------------------------
if __name__ == "__main__":
    main()
