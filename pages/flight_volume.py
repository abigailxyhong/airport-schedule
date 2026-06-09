import dash
import requests
import plotly.express as px
import dash_mantine_components as dmc

from dash import dcc, Input, Output

API_URL = "http://127.0.0.1:8000"

dash.register_page(__name__, path="/flight_volume")

def apply_dark_theme(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0F1623",
        plot_bgcolor="#0F1623",
        font=dict(color="#E6EDF3"),
        margin=dict(l=40, r=20, t=40, b=40),
    )
    return fig

layout = dmc.Container(
    fluid=True,
    className="page-container",
    children=[

        # ---------------- Header Card ----------------
        dmc.Paper(
            className="card header-card",
            p="lg",
            children=[

                dmc.Group(
                    justify="space-between",
                    align="center",
                    children=[

                        dmc.Title(
                            "Flight Volume",
                            order=3,
                            className="page-title",
                        ),

                        dmc.Select(
                            id="graph-selector",
                            value="hour",
                            data=[
                                {"label": "Flights per Hour", "value": "hour"},
                                {"label": "Flights per Day", "value": "day"},
                            ],
                            w=260,
                            className="select-control",
                        ),
                    ],
                ),

                dmc.Space(h="md"),

                dmc.Stack(
                    gap="sm",
                    children=[

                        dmc.Text("Airline", className="filter-label"),

                        dmc.RadioGroup(
                            id="airline-radio",
                            value="ALL",
                            children=dmc.Group(gap="sm"),
                        ),

                        dmc.Divider(),

                        dmc.Text("Destination", className="filter-label"),

                        dmc.RadioGroup(
                            id="destination-radio",
                            value="ALL",
                            children=dmc.Group(gap="sm"),
                        ),
                    ],
                ),
            ],
        ),

        dmc.Space(h="md"),

        # ---------------- Graph Card ----------------
        dmc.Paper(
            className="card graph-card",
            children=[
                dcc.Graph(
                    id="main-graph",
                    config={"displayModeBar": False},
                    className="graph",
                )
            ],
        ),
    ],
)


# ------------------------------------------------------------
# Load radio options
# ------------------------------------------------------------
@dash.callback(
    Output("airline-radio", "children"),
    Output("destination-radio", "children"),
    Output("airline-radio", "value"),
    Output("destination-radio", "value"),
    Input("graph-selector", "value"),
)
def load_radio_options(_):

    airlines = requests.get(f"{API_URL}/analytics/list-airlines").json()
    destinations = requests.get(f"{API_URL}/analytics/list-destinations").json()

    neon_blue = "#7DF9FF"
    neon_pink = "#FF6EC7"

    airline_buttons = dmc.Group(
        gap="sm",
        children=[
            dmc.Radio(
                label="All",
                value="ALL",
                styles={"label": {"color": "#E6EDF3"}},
            ),
            *[
                dmc.Radio(
                    label=a["label"],
                    value=a["value"],
                    styles={
                        "label": {
                            "color": "#B8C7D9",
                        },
                        "radio": {
                            "borderColor": neon_blue,
                        },
                    },
                )
                for a in airlines
            ],
        ],
    )

    destination_buttons = dmc.Group(
        gap="sm",
        children=[
            dmc.Radio(
                label="All",
                value="ALL",
                styles={"label": {"color": "#E6EDF3"}},
            ),
            *[
                dmc.Radio(
                    label=d["label"],
                    value=d["value"],
                    styles={
                        "label": {"color": "#B8C7D9"},
                        "radio": {"borderColor": neon_pink},
                    },
                )
                for d in destinations
            ],
        ],
    )

    return airline_buttons, destination_buttons, "ALL", "ALL"


# ------------------------------------------------------------
# Graph update
# ------------------------------------------------------------
@dash.callback(
    Output("main-graph", "figure"),
    Input("graph-selector", "value"),
    Input("airline-radio", "value"),
    Input("destination-radio", "value"),
)
def update_graph(graph_type, airline, destination):

    if airline == "ALL":
        airline = None
    if destination == "ALL":
        destination = None

    params = {"airline": airline, "destination": destination}

    if graph_type == "hour":
        data = requests.get(
            f"{API_URL}/analytics/flights-per-hour",
            params=params,
        ).json()

        fig = px.bar(
            data,
            x="hour",
            y="flights",
            title="Flights per Hour",
            color_discrete_sequence=["#7DF9FF"],  # neon cyan
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0F1623",
            plot_bgcolor="#0F1623",
            font=dict(color="#E6EDF3"),
            xaxis=dict(dtick=1, gridcolor="#1F2A3A"),
            yaxis=dict(gridcolor="#1F2A3A"),
        )

        return fig

    data = requests.get(
        f"{API_URL}/analytics/flights-per-day",
        params=params,
    ).json()

    fig = px.line(
        data,
        x="flight_date",
        y="flights",
        title="Flights per Day",
        markers=True,
        color_discrete_sequence=["#FF6EC7"],  # neon pink
    )

    fig = apply_dark_theme(fig)

    return fig