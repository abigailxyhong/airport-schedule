import dash_mantine_components as dmc
from dash import Dash
import dash
from components.flight_volume import flight_volume_layout


def create_layout(app: Dash):
    return dmc.MantineProvider(
        theme={
            "colorScheme": "dark",
            "fontFamily": "Inter, Nunito, sans-serif",
        },
        children=dmc.AppShell(
            header={"height": 80},
            children=[
                dmc.Title(
                    "JERSEY AIRPORT DASHBOARD",
                    order=1,
                    c="#E6EDF3",
                    className="brand-title",
                ),
                dmc.AppShellMain(flight_volume_layout),
            ],
        ),
    )
