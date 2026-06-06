import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    """
    Load and clean the airport flight schedule CSV.
    Handles:
    - Column renaming
    - Date parsing
    - Local time parsing (e.g., 700 → 07:00)
    - Creating datetime and hour fields
    - Ensuring correct dtypes
    """

    # Load raw CSV
    print("Loading CSV...")
    df = pd.read_csv(path)
    print("Initial columns:", df.columns.tolist())
    print("Initial shape:", df.shape)

    # Standardise column names
    df = df.rename(columns={
        "Carrier Code": "carrier",
        "Flight No": "flight_no",
        "ArrDep": "arr_dep",
        "Dep Airport Code": "dep_airport_code",
        "Dep Airport Name": "dep_airport_name",
        "Arr Airport Code": "arr_airport_code",
        "Arr Airport Name": "arr_airport_name",
        "Local Dep Time": "local_dep_time",
        "Local Arr Time": "local_arr_time",
        "Specific Aircraft Code": "aircraft_code",
        "Seats": "seats",
        "Time series": "flight_date"
    })
    print("After renaming:", df.columns.tolist())

    # Convert date column
    df["flight_date"] = pd.to_datetime(df["flight_date"], format="%d/%m/%Y")
    print("Converted flight_date to datetime. Example:", df["flight_date"].iloc[0])

    # Convert times like 700 → "07:00"
    def parse_time(t):
        if pd.isna(t):
            return None
        t = int(t)
        hour = t // 100
        minute = t % 100
        return f"{hour:02d}:{minute:02d}"

    df["dep_time_str"] = df["local_dep_time"].apply(parse_time)
    df["arr_time_str"] = df["local_arr_time"].apply(parse_time)
    print("Parsed times. Example dep_time_str:", df["dep_time_str"].iloc[0])
    
    # Create full datetime for departure
    df["dep_datetime"] = pd.to_datetime(
        df["flight_date"].dt.strftime("%Y-%m-%d") + " " + df["dep_time_str"],
        errors="coerce"
    )
    print("Created dep_datetime. Example:", df["dep_datetime"].iloc[0])

    # Extract hour for analytics
    df["hour"] = df["dep_datetime"].dt.hour
    print("Extracted hour. Unique hours:", sorted(df["hour"].unique())[:10])

    # Clean airline codes (e.g., "U2" vs "EZY")
    df["airline"] = df["carrier"].str.upper()
    print("Airline codes normalised. Unique airlines:", df["airline"].unique())

    # Ensure seats is numeric
    df["seats"] = pd.to_numeric(df["seats"], errors="coerce")
    print("Seats converted to numeric. Example:", df["seats"].iloc[0])

    print("Final dataframe shape:", df.shape)
    print("Final columns:", df.columns.tolist())
    
    return df
