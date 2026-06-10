import pandas as pd

# -----------------------------
# FILTERING HELPER
# -----------------------------
def apply_filters(
    df: pd.DataFrame,
    airline: str | None = None,
    destination: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> pd.DataFrame:

    dff = df.copy()

    if airline:
        dff = dff[dff["airline"] == airline]

    if destination:
        dff = dff[dff["arr_airport_code"] == destination]

    if start_date:
        dff = dff[dff["flight_date"] >= pd.to_datetime(start_date)]

    if end_date:
        dff = dff[dff["flight_date"] <= pd.to_datetime(end_date)]

    return dff


def flights_per_hour(df: pd.DataFrame) -> pd.DataFrame:
    """
    Time series: must always be sorted chronologically.
    """
    return (
        df.groupby("hour", as_index=False)
          .size()
          .rename(columns={"size": "flights"})
          .sort_values("hour")
    )


def flights_per_day(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns flights grouped by flight_date.
    """
    return (
        df.groupby("flight_date")
          .size()
          .reset_index(name="flights")
          .sort_values("flight_date")
    )


def flights_per_airline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns airlines ranked by number of flights (descending).
    """
    return (
        df.groupby("airline", as_index=False)
          .size()
          .rename(columns={"size": "flights"})
          .sort_values("flights", ascending=False)
          .reset_index(drop=True)
    )

def flights_per_destination(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns destinations ranked by traffic (descending).
    """
    return (
        df.groupby("arr_airport_code", as_index=False)
          .size()
          .rename(columns={"size": "flights"})
          .sort_values("flights", ascending=False)
          .reset_index(drop=True)
    )

def seats_per_hour(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns total seats offered grouped by departure hour.
    """

    return (
        df.groupby("hour", as_index=False)["seats"]
          .sum()
          .sort_values("hour")
    )

def top_airline(df):
    if df.empty or "airline" not in df.columns:
        return None

    counts = df.groupby("airline").size()

    top = counts.idxmax()
    value = counts.max()

    return {
        "airline": top,
        "flights": int(value)
    }

def top_destination(df):
    if df.empty or "arr_airport_code" not in df.columns:
        return None

    counts = df.groupby("arr_airport_code").size()

    top = counts.idxmax()
    value = counts.max()

    return {
        "arr_airport_code": top,
        "flights": int(value)
    }

def summary_day_flights(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns flight-level summary for a single day view:
    - carrier code
    - flight number
    - arrival airport code
    - departure time
    - aircraft code
    - seats
    """

    return (
        df[[
            "carrier",
            "flight_no",
            "arr_airport_code",
            "dep_time_str",
            "aircraft_code",
            "seats"
        ]]
        .rename(columns={
            "carrier": "carrier_code",
            "flight_no": "flight_number",
            "arr_airport_code": "arrival_airport",
            "dep_time_str": "departure_time",
            "aircraft_code": "aircraft_code",
            "seats": "seats"
        })
        .sort_values("departure_time")
        .reset_index(drop=True)
    )