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

@app.get("/analytics/top-airline")
def get_top_airline(
    start_date: str | None = None,
    end_date: str | None = None,
    airline: str | None = None,
    destination: str | None = None,
):
    dff = analytics.apply_filters(
        df,
        airline=airline,
        destination=destination,
        start_date=start_date,
        end_date=end_date,
    )

    result = analytics.top_airline(dff)

    return {
        "top_airline": result
    }

@app.get("/analytics/top-destination")
def get_top_destination(
    start_date: str | None = None,
    end_date: str | None = None,
    airline: str | None = None,
    destination: str | None = None,
):
    dff = analytics.apply_filters(
        df,
        airline=airline,
        destination=destination,
        start_date=start_date,
        end_date=end_date,
    )

    result = analytics.top_destination(dff)

    return {
        "top_destination": result
    }

@app.get("/analytics/flights-per-hour")
def get_flights_per_hour(airline: str | None = None,
                         destination: str | None = None,
                         start_date: str | None = None,
                         end_date: str | None = None
                         ):

    dff = analytics.apply_filters(df, airline, destination, start_date, end_date)
    result = analytics.flights_per_hour(dff)
    return result.to_dict(orient="records")

@app.get("/analytics/flights-per-day")
def get_flights_per_day(
    airline: str | None = None,
    destination: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
):
    dff = analytics.apply_filters(
        df,
        airline,
        destination,
        start_date,
        end_date,
    )

    return analytics.flights_per_day(dff).to_dict("records")


@app.get("/analytics/flights-per-airline")
def get_flights_per_airline(
    airline: str | None = None,
    destination: str | None = None
):
    try:
        print("FASTAPI received:", airline, destination)
        dff = analytics.apply_filters(df, airline, destination)
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
):
    dff = analytics.apply_filters(df, airline, destination)
    result = analytics.flights_per_destination(dff)
    return result.to_dict(orient="records")

@app.get("/analytics/date-range")
def get_date_range():

    return {
        "min_date": df["flight_date"].min().strftime("%Y-%m-%d"),
        "max_date": df["flight_date"].max().strftime("%Y-%m-%d"),
    }

@app.get("/analytics/seats-per-hour")
def get_seats_per_hour(
    start_date: str | None = None,
    end_date: str | None = None,
):
    dff = analytics.apply_filters(
        df,
        airline=None,
        destination=None,
        start_date=start_date,
        end_date=end_date,
    )

    result = analytics.seats_per_hour(dff)
    return result.to_dict(orient="records")

@app.get("/analytics/summary-day-flights")
def get_summary_day_flights(
    start_date: str | None = None,
    end_date: str | None = None,
):
    dff = analytics.apply_filters(df, start_date=start_date, end_date=end_date)
    result = analytics.summary_day_flights(dff)
    return result.to_dict(orient="records")