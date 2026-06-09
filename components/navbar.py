import dash_mantine_components as dmc

navbar = dmc.Paper(
    className="navbar",
    children=dmc.Group(
        justify="space-between",
        align="center",
        h="100%",
        px="lg",
        children=[
            dmc.Title(
                "Jersey Airport Dashboard",
                order=1,
                c="#E6EDF3",
                className="brand-title",
            ),

            dmc.Group(
                gap="xl",
                children=[
                    dmc.Anchor(
                        "Flight Volume",
                        href="/flight_volume",
                        className="nav-link",
                    ),
                    dmc.Anchor(
                        "Capacity",
                        href="/capacity",
                        className="nav-link",
                    ),
                    dmc.Anchor(
                        "Routes",
                        href="/routes",
                        className="nav-link",
                    ),
                ],
            ),
        ],
    ),
)