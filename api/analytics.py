import pandas as pd

# -----------------------------
# FILTERING HELPER
# -----------------------------
def apply_filters(df: pd.DataFrame,
                  airline: str | None = None,
                  destination: str | None = None) -> pd.DataFrame:
    """
    Apply optional filters to the flight dataframe.
    Works with your load_data() output.
    """

    dff = df.copy()

    if airline:
        dff = dff[dff["airline"] == airline]

    if destination:
        dff = dff[dff["arr_airport_code"] == destination]

    return dff


# -----------------------------
# FLIGHTS PER HOUR
# -----------------------------
def flights_per_hour(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns flights grouped by departure hour.
    Requires df['hour'] from load_data().
    """
    return (
        df.groupby("hour")
          .size()
          .reset_index(name="flights")
          .sort_values("hour")
    )


# -----------------------------
# FLIGHTS PER DAY
# -----------------------------
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


# -----------------------------
# FLIGHTS PER AIRLINE
# -----------------------------
def flights_per_airline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns flights grouped by airline, with debug prints.
    """

    print("\n=== flights_per_airline DEBUG ===")
    print("Incoming DF shape:", df.shape)
    print("DF columns:", df.columns.tolist())

    # Show first few rows
    print("Head of DF:")
    print(df.head())

    # Check if airline column exists
    if "airline" not in df.columns:
        print("ERROR: 'airline' column NOT FOUND in dataframe!")
        return pd.DataFrame()  # return empty to avoid crashing

    try:
        grouped = (
            df.groupby("airline")
              .size()
              .reset_index(name="flights")
              .sort_values("flights", ascending=False)
        )

        print("Grouped result:")
        print(grouped)

        return grouped

    except Exception as e:
        print("ERROR inside flights_per_airline:", e)
        raise e



# -----------------------------
# FLIGHTS PER DESTINATION
# -----------------------------
def flights_per_destination(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns flights grouped by destination airport.
    """
    return (
        df.groupby("arr_airport_code")
          .size()
          .reset_index(name="flights")
          .sort_values("flights", ascending=False)
    )
