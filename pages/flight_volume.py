import dash
import requests
import plotly.express as px
import dash_mantine_components as dmc

from dash import dcc, Input, Output

API_URL = "http://127.0.0.1:8000"

dash.register_page(__name__, path="/flight_volume")

# ------------------------------------------------------------
# Load dataset date bounds once at startup
# ------------------------------------------------------------
date_info = requests.get(f"{API_URL}/analytics/date-range").json()

MIN_DATE = date_info["min_date"]
MAX_DATE = date_info["max_date"]

layout = dmc.Container(
    fluid=True,
    className="page-container",
    children=[
        # ---------------- MAIN CONTENT ROW ----------------
        dmc.SimpleGrid(
            cols=2,
            spacing="md",
            children=[
                # ---------------- GRAPH ----------------
                dmc.Paper(
                    className="card",
                    p="md",
                    children=[
                        dcc.Graph(
                            id="main-graph",
                            config={"displayModeBar": False},
                            className="graph",
                            style={"height": "70vh"},
                        )
                    ],
                ),
                # ---------------- FILTERS ----------------
                dmc.Stack(
                    gap="md",
                    children=[
                        # ---------- SELECT + DATE PICKER ROW ----------
                        dmc.Group(
                            justify="flex-start",
                            align="center",
                            children=[
                                dmc.Select(
                                    id="graph-selector",
                                    value="hour",
                                    data=[
                                        {"label": "Flights per Hour", "value": "hour"},
                                        {"label": "Flights per Day", "value": "day"},
                                    ],
                                    styles={
                                        "option": {
                                            "color": "#222",
                                        },
                                        "dropdown": {
                                            "backgroundColor": "white",
                                        },
                                    },
                                    w=220,
                                ),
                                dmc.DatePickerInput(
                                    id="date-picker",
                                    type="range",
                                    value=[MIN_DATE, MAX_DATE],
                                    minDate=MIN_DATE,
                                    maxDate=MAX_DATE,
                                    clearable=True,
                                ),
                            ],
                        ),
                        # ---------- AIRLINE ----------
                        dmc.Paper(
                            className="card",
                            p="md",
                            children=[
                                dmc.Text("AIRLINE", className="filter-label"),
                                dmc.Space(h="sm"),
                                dmc.RadioGroup(
                                    id="airline-radio",
                                    value="ALL",
                                    children=dmc.Stack(gap="xs"),
                                ),
                            ],
                        ),
                        # ---------- DESTINATION ----------
                        dmc.Paper(
                            className="card",
                            p="md",
                            children=[
                                dmc.Text("DESTINATION", className="filter-label"),
                                dmc.Space(h="sm"),
                                dmc.RadioGroup(
                                    id="destination-radio",
                                    value="ALL",
                                    children=dmc.Stack(gap="xs"),
                                ),
                            ],
                        ),
                    ],
                ),
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
    Input("date-picker", "value"),
)
def update_graph(
    graph_type,
    airline,
    destination,
    date_range,
):

    if airline == "ALL":
        airline = None

    if destination == "ALL":
        destination = None

    # ---------------- Date Range ----------------
    start_date = None
    end_date = None

    if date_range and len(date_range) == 2:
        start_date, end_date = date_range

    params = {
        "airline": airline,
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date,
    }

    # ---------------- Flights per Hour ----------------
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
            color_discrete_sequence=["#7DF9FF"],
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0F1623",
            plot_bgcolor="#0F1623",
            font=dict(color="#E6EDF3"),
            xaxis=dict(
                dtick=1,
                gridcolor="#1F2A3A",
            ),
            yaxis=dict(
                gridcolor="#1F2A3A",
            ),
            margin=dict(
                l=40,
                r=20,
                t=40,
                b=40,
            ),
        )

        return fig

    # ---------------- Flights per Day ----------------
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
        color_discrete_sequence=["#FF6EC7"],
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0F1623",
        plot_bgcolor="#0F1623",
        font=dict(color="#E6EDF3"),
        margin=dict(
            l=40,
            r=20,
            t=40,
            b=40,
        ),
        xaxis=dict(
            gridcolor="#1F2A3A",
        ),
        yaxis=dict(
            gridcolor="#1F2A3A",
        ),
    )

    return fig
