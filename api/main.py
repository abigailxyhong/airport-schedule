from fastapi import FastAPI
from api.data_loader import load_data
from api import analytics

app = FastAPI()
df = load_data("./data/sample_flight_schedule.csv")

@app.get("/analytics/list-airlines")
def list_airlines():
    airlines = sorted(df["airline"].unique())
    return [{"label": a, "value": a} for a in airlines]


@app.get("/analytics/list-destinations")
def list_destinations():
    dests = sorted(df["arr_airport_code"].unique())
    return [{"label": d, "value": d} for d in dests]

@app.get("/analytics/flights-per-hour")
def get_flights_per_hour(airline: str | None = None,
                         destination: str | None = None,
                         start_date: str | None = None,
                         end_date: str | None = None):

    dff = analytics.apply_filters(df, airline, destination, start_date, end_date)
    result = analytics.flights_per_hour(dff)
    return result.to_dict(orient="records")

@app.get("/analytics/flights-per-day")
def get_flights_per_day(
    airline: str | None = None,
    destination: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None
):
    dff = analytics.apply_filters(df, airline, destination, start_date, end_date)
    result = analytics.flights_per_day(dff)
    return result.to_dict(orient="records")


@app.get("/analytics/flights-per-airline")
def get_flights_per_airline(
    airline: str | None = None,
    destination: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None
):
    try:
        print("FASTAPI received:", airline, destination, start_date, end_date)
        dff = analytics.apply_filters(df, airline, destination, start_date, end_date)
        print("Filtered rows:", len(dff))
        result = analytics.flights_per_airline(dff)
        print("Result rows:", len(result))
        return result.to_dict(orient="records")
    except Exception as e:
        print("ERROR in flights-per-airline:", e)
        raise e


@app.get("/analytics/flights-per-destination")
def get_flights_per_destination(
    airline: str | None = None,
    destination: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None
):
    dff = analytics.apply_filters(df, airline, destination, start_date, end_date)
    result = analytics.flights_per_destination(dff)
    return result.to_dict(orient="records")
