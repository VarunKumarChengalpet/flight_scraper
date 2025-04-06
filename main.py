from fastapi import FastAPI, Query, HTTPException
from datetime import datetime
from tasks.flight_tasks import scrape_flight_info_task, refresh_flight_info_task
from core.cache import get_cached_flight

app = FastAPI()

@app.get("/flight-info")
def get_flight_info(
    airline_code: str = Query(..., min_length=2, max_length=3, regex="^[A-Z]+$"),
    flight_number: str = Query(..., min_length=1, max_length=6, regex="^[0-9]+$"),
    date: str = Query(..., regex=r"^\d{2}-\d{2}-\d{4}$")
):

    if not airline_code or not flight_number or not date:
        raise HTTPException(status_code=400, detail="All query parameters are required")

    try:
        parsed_date = datetime.strptime(date, "%d-%m-%Y")
        year = parsed_date.year
        month = parsed_date.month
        day = parsed_date.day
    except ValueError:
        raise HTTPException(status_code=400, detail="Date must be in dd-mm-yyyy format")

    cache_key = f"{airline_code}:{flight_number}:{year}-{month}-{day}"
    cached_data = get_cached_flight(cache_key)

    if cached_data:
        refresh_flight_info_task.delay(airline_code, flight_number, year, month, date)
        return {"source": "cache", "data": cached_data}

    try:
        result = scrape_flight_info_task(airline_code, flight_number, year, month, day)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {"source": "live", "data": result}
