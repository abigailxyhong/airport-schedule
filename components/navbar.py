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
                "JERSEY AIRPORT DASHBOARD",
                order=1,
                c="#E6EDF3",
                className="brand-title",
            ),

            dmc.Group(
                gap="xl",
                children=[
                    dmc.Anchor(
                        "OVERVIEW",
                        href="/",
                        underline="never",
                        className="nav-link",
                    ),
                    dmc.Anchor(
                        "FLIGHT VOLUME",
                        href="/flight_volume",
                        underline="never",
                        className="nav-link",
                    ),
                    dmc.Anchor(
                        "CAPACITY",
                        href="/capacity",
                        underline="never",
                        className="nav-link",
                    ),
                ],
            ),
        ],
    ),
)