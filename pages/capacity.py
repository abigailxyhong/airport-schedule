import requests
import dash
from dash import dcc, Input, Output, callback
import plotly.express as px
import dash_mantine_components as dmc

API_URL = "http://localhost:8000"

dash.register_page(__name__, path="/capacity")

date_info = requests.get(f"{API_URL}/analytics/date-range").json()
MIN_DATE = date_info["min_date"]
MAX_DATE = date_info["max_date"]


layout = dmc.MantineProvider(
    theme={
        "colorScheme": "dark",
        "primaryColor": "cyan",
        "fontFamily": "Inter, sans-serif",
    },
    children=dmc.Container(
        fluid=True,
        style={
            "backgroundColor": "#0B0F1A",
            "minHeight": "100vh",
            "padding": "30px",
        },
        children=[

            # ---------------- TITLE ----------------
            dmc.Title(
                "Seat Capacity by Hour",
                order=2,
                c="#7DF9FF",
                style={"letterSpacing": "1px"},
            ),

            dmc.Text(
                "Hourly seat supply distribution for selected day",
                c="dimmed",
                mb=20,
            ),

            # ---------------- CONTROL CARD ----------------
            dmc.Paper(
                p="md",
                withBorder=True,
                style={
                    "backgroundColor": "#111827",
                    "borderColor": "#1F2A3A",
                    "borderRadius": "14px",
                },
                children=[
                    dmc.Group(
                        justify="space-between",
                        children=[
                            dmc.Text("Select Date", fw=600, c="#A5B4FC"),
                            dmc.DatePickerInput(
                                id="date-picker",
                                value=MIN_DATE,
                                minDate=MIN_DATE,
                                maxDate=MAX_DATE,
                                clearable=False,
                                style={
                                    "backgroundColor": "#0F172A",
                                    "borderRadius": "10px",
                                },
                            ),
                        ],
                    )
                ],
            ),

            dmc.Space(h=20),

            # ---------------- CHART CARD ----------------
            dmc.Paper(
                p="lg",
                withBorder=True,
                style={
                    "backgroundColor": "#0F172A",
                    "borderColor": "#1F2A3A",
                    "borderRadius": "16px",
                    "boxShadow": "0 0 20px rgba(125, 249, 255, 0.08)",
                },
                children=[
                    dmc.Group(
                        justify="space-between",
                        children=[
                            dmc.Text("Hourly Seat Distribution", c="#7DF9FF", fw=600),
                        ],
                    ),

                    dmc.Space(h=10),

                    dcc.Graph(
                        id="seats-per-hour-chart",
                        config={"displayModeBar": False},
                        style={"height": "65vh"},
                    ),
                ],
            ),
        ],
    ),
)


@callback(
    Output("seats-per-hour-chart", "figure"),
    Input("date-picker", "value"),
)
def update_seats_per_hour(selected_date):

    params = {
        "start_date": selected_date,
        "end_date": selected_date,
    }

    response = requests.get(
        f"{API_URL}/analytics/seats-per-hour",
        params=params,
        timeout=10,
    )

    data = response.json()

    fig = px.line(
        data,
        x="hour",
        y="seats",
        markers=True,
        title=f"Seats Offered Per Hour ({selected_date})",
    )

    fig.update_layout(
        xaxis=dict(dtick=1),
        hovermode="x unified",
    )

    return fig
