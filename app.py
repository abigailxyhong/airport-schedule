import dash
from dash import Dash, html, dcc, Input, Output
from dash_bootstrap_components.themes import LUX
import plotly.express as px
import pandas as pd

from src.components.layout import create_layout

# ------------------------------------------------------------
# Data loading
# ------------------------------------------------------------
def load_data():
    df = pd.read_csv("data/sample_flight_schedule.csv")
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Parse date
    df["flight_date"] = pd.to_datetime(df["time_series"], dayfirst=True)

    # Parse departure time (e.g., 700 → "07:00")
    def parse_time(t):
        t = str(int(t)).zfill(4)
        return f"{t[:2]}:{t[2:]}"
    df["dep_time_str"] = df["local_dep_time"].apply(parse_time)

    df["flight_datetime"] = pd.to_datetime(
        df["flight_date"].dt.strftime("%Y-%m-%d") + " " + df["dep_time_str"]
    )
    df["hour"] = df["flight_datetime"].dt.hour

    df = df.rename(columns={
        "carrier_code": "airline",
        "flight_no": "flight_number",
        "arr_airport_code": "destination",
        "specific_aircraft_code": "aircraft_type",
    })

    return df


df = load_data()

# ------------------------------------------------------------
# App initialisation
# ------------------------------------------------------------
def main() -> None:
    app = Dash(external_stylesheets=[LUX])
    app.title = "Jersey Airport Dashboard"
    app.layout = create_layout(app)
    app.run(debug=True)

# ------------------------------------------------------------
# Callbacks
# ------------------------------------------------------------


# ------------------------------------------------------------
# Entry point
# ------------------------------------------------------------
if __name__ == "__main__":
    main()
