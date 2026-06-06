import dash
import requests
from dash import html, dcc, Input, Output
import plotly.express as px

API_URL = "http://127.0.0.1:8000"
dash.register_page(__name__, path="/flight_volume")

# Layout
layout = html.Div([
    html.H3("Flight Volume"),

    # Filters
    html.Div([
        dcc.Dropdown(
            id="airline-filter",
            placeholder="Select airline",
            className="filter-control"
        ),
        dcc.Dropdown(
            id="destination-filter",
            placeholder="Select destination",
            className="filter-control"
        ),
        dcc.DatePickerRange(
            id="date-range",
            className="dash-date-picker"
        ),
    ], className="filter-row"),

    # Graphs
    dcc.Graph(id="hourly-chart"),
    dcc.Graph(id="daily-chart"),
    dcc.Graph(id="airline-chart"),
    dcc.Graph(id="destination-chart"),

], className="content-div")

# Callbacks

@dash.callback(
    Output("airline-filter", "options"),
    Output("destination-filter", "options"),
    Input("airline-filter", "id")  # dummy input to trigger once
)
def load_dropdown_options(_):

    airlines = requests.get(f"{API_URL}/analytics/list-airlines").json()
    destinations = requests.get(f"{API_URL}/analytics/list-destinations").json()

    return airlines, destinations


@dash.callback(
    Output("hourly-chart", "figure"),
    Input("airline-filter", "value"),
    Input("destination-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date")
)

def update_hourly(airline, destination, start_date, end_date):

    params = {
        "airline": airline,
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date
    }

    data = requests.get(f"{API_URL}/analytics/flights-per-hour", params=params).json()

    print("Airline API response:", data)

    fig = px.bar(data, x="hour", y="flights", title="Flights per Hour")
    fig.update_layout(xaxis=dict(dtick=1))

    return fig

@dash.callback(
    Output("daily-chart", "figure"),
    Input("airline-filter", "value"),
    Input("destination-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date")
)

def update_daily(airline, destination, start_date, end_date):

    params = {
        "airline": airline,
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date
    }

    data = requests.get(f"{API_URL}/analytics/flights-per-day", params=params).json()

    fig = px.line(data, x="flight_date", y="flights", markers=True,
                  title="Flights per Day")

    return fig

@dash.callback(
    Output("airline-chart", "figure"),
    Input("airline-filter", "value"),
    Input("destination-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date")
)

def update_airline(airline, destination, start_date, end_date):

    params = {
        "airline": airline,
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date
    }

    resp = requests.get(f"{API_URL}/analytics/flights-per-airline", params=params)
    print("RAW RESPONSE:", resp.text)
    data = resp.json()

    fig = px.bar(data, x="airline", y="flights",
                 title="Flights per Airline")

    return fig

@dash.callback(
    Output("destination-chart", "figure"),
    Input("airline-filter", "value"),
    Input("destination-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date")
)

def update_destination(airline, destination, start_date, end_date):

    params = {
        "airline": airline,
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date
    }

    data = requests.get(f"{API_URL}/analytics/flights-per-destination", params=params).json()

    fig = px.bar(data, x="arr_airport_code", y="flights",
                 title="Flights per Destination")

    return fig
