import dash
from dash import html, dcc, Input, Output, callback
import dash_mantine_components as dmc
import requests
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os

load_dotenv()
API_URL = os.getenv("API_URL", "http://api:8000")

dash.register_page(__name__, path="/")

date_info = requests.get(f"{API_URL}/analytics/date-range").json()

MIN_DATE = date_info["min_date"]
MAX_DATE = date_info["max_date"]

# -----------------------------
# PAGE LAYOUT
# -----------------------------
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
            # ---------------- HEADER ROW ----------------
            dmc.Group(
                justify="space-between",
                align="flex-end",
                children=[
                    # LEFT: TITLE + SUBTITLE
                    dmc.Stack(
                        gap=2,
                        children=[
                            dmc.Title(
                                "✈ Airport Daily Summary",
                                order=2,
                                c="#7DF9FF",
                                style={"letterSpacing": "1px"},
                            ),
                            dmc.Text(
                                "Operational snapshot of today’s airport activity",
                                c="dimmed",
                            ),
                        ],
                    ),
                    # RIGHT: DATE PICKER CARD
                    dmc.Paper(
                        p="sm",
                        withBorder=True,
                        style={
                            "backgroundColor": "#111827",
                            "borderColor": "#1F2A3A",
                            "borderRadius": "14px",
                        },
                        children=[
                            dmc.Group(
                                justify="space-between",
                                align="center",
                                children=[
                                    dmc.Text("Select Date", fw=600, c="#A5B4FC"),
                                    dmc.DatePickerInput(
                                        id="summary-date",
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
                ],
            ),
            dmc.Space(h=20),
            # ---------------- GRID ----------------
            dmc.SimpleGrid(
                cols=2,
                spacing="lg",
                children=[
                    # ---------------- TABLE CARD ----------------
                    dmc.Paper(
                        p="lg",
                        withBorder=True,
                        style={
                            "backgroundColor": "#0F172A",
                            "borderColor": "#1F2A3A",
                            "borderRadius": "16px",
                            "boxShadow": "0 0 20px rgba(125, 249, 255, 0.08)",
                            "maxHeight": "520px",
                            "overflowY": "auto",
                        },
                        children=[
                            dmc.Group(
                                justify="space-between",
                                children=[
                                    dmc.Title(
                                        "Key Metrics", order=4, c="#7DF9FF"
                                    ),
                                 
                                ],
                            ),
                            dmc.Space(h=10),
                            html.Div(id="summary-table"),
                        ],
                    ),
                    # ---------------- LINE GRAPH ----------------
                    dmc.Paper(
                        p="lg",
                        withBorder=True,
                        style={
                            "backgroundColor": "#0F172A",
                            "borderColor": "#1F2A3A",
                            "borderRadius": "16px",
                        },
                        children=[
                            dmc.Title("Flight Volume Over Day", order=4, c="#FF6EC7"),
                            dmc.Space(h=10),
                            html.Div(id="hourly-volume-chart"),
                        ],
                    ),
                ],
            ),
        ],
    ),
)


@callback(
    Output("summary-table", "children"),
    Output("hourly-volume-chart", "children"),
    Input("summary-date", "value"),
)
def load_summary(selected_date):

    if not selected_date:
        return "Select a date", ""

    params = {
        "start_date": selected_date,
        "end_date": selected_date,
    }

    # ---------------- DATA ----------------
    flights = requests.get(
        f"{API_URL}/analytics/flights-per-hour", params=params
    ).json()

    top_airline_resp = requests.get(
        f"{API_URL}/analytics/top-airline", params=params
    ).json()

    top_dest_resp = requests.get(
        f"{API_URL}/analytics/top-destination", params=params
    ).json()

    flights_df = pd.DataFrame(flights)

    # ---------------- KPIs ----------------
    total_flights = int(flights_df["flights"].sum()) if not flights_df.empty else 0

    top_airline = top_airline_resp.get("top_airline", {}).get("airline", "N/A")

    top_dest = top_dest_resp.get("top_destination", {}).get("arr_airport_code", "N/A")

    # ---------------- CHART (NEW) ----------------
    if flights_df.empty:
        chart = dmc.Text("No data available", c="dimmed")
    else:
        fig = px.line(
            flights_df,
            x="hour",
            y="flights",
            markers=True,
            title="Flights Per Hour",
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0F172A",
            plot_bgcolor="#0F172A",
            font=dict(color="#E6EDF3"),
            xaxis=dict(dtick=1, title="Hour of Day"),
            yaxis=dict(title="Flights"),
            hovermode="x unified",
            margin=dict(l=30, r=20, t=40, b=30),
        )

        chart = dcc.Graph(
            figure=fig,
            config={"displayModeBar": False},
            style={"height": "320px"},
        )

    # ---------------- TABLE ----------------
    table = dmc.Table(
        striped=False,
        highlightOnHover=True,
        withTableBorder=True,
        style={"color": "#E6EDF3"},
        children=[
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td("TOTAL FLIGHTS"),
                            html.Td(total_flights, style={"color": "#7DF9FF"}),
                        ]
                    ),
                    html.Tr(
                        [
                            html.Td("TOP AIRLINE"),
                            html.Td(top_airline, style={"color": "#A5B4FC"}),
                        ]
                    ),
                    html.Tr(
                        [
                            html.Td("TOP DESTINATION"),
                            html.Td(top_dest, style={"color": "#FF6EC7"}),
                        ]
                    ),
                ]
            )
        ],
    )

    return table, chart
