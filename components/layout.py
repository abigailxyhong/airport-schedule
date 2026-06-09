import dash_mantine_components as dmc
from dash import Dash
import dash
from components.navbar import navbar


def create_layout(app: Dash):
    return dmc.MantineProvider(
        theme={
            "colorScheme": "dark",
            "fontFamily": "Inter, Nunito, sans-serif",
        },
        children=dmc.AppShell(
            header={"height": 80},
            children=[
                navbar,
                dmc.AppShellMain(dash.page_container),
            ],
        ),
    )
