import dash_bootstrap_components as dbc
from dash import html

navbar = dbc.Navbar(
    dbc.Container(
        [
            # Brand on the left
            dbc.NavbarBrand("Airport Dashboard", href="/"),

            # Full-width nav links, equally spaced
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Flight Volume", href="/flight_volume")),
                    dbc.NavItem(dbc.NavLink("Capacity", href="/capacity")),
                    dbc.NavItem(dbc.NavLink("Routes", href="/routes")),
                ],
                className="nav-main",
                navbar=True,
            ),
        ],
        fluid=True,
    ),
    color="primary",
    dark=True,
    sticky="top",
)
