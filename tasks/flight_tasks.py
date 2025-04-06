from celery_worker import celery_app
from scraper.browser import get_rendered_html
from scraper.parser import parse_flight_info
from core.cache import set_cached_flight

def get_flight_info(airline_code, flight_number, year, month, date):
    url = f"https://www.flightstats.com/v2/flight-tracker/{airline_code}/{flight_number}?year={year}&month={month}&date={date}"
    html = get_rendered_html(url)
    parsed = parse_flight_info(html)

    cache_key = f"{airline_code}:{flight_number}:{year}-{month}-{date}"
    set_cached_flight(cache_key, parsed)

    return parsed

@celery_app.task(name="tasks.flight_tasks.scrape_flight_info_task")
def scrape_flight_info_task(airline_code, flight_number, year, month, date):
    return get_flight_info(airline_code, flight_number, year, month, date)

@celery_app.task(name="tasks.flight_tasks.refresh_flight_info_task")
def refresh_flight_info_task(airline_code, flight_number, year, month, date):
    return get_flight_info(airline_code, flight_number, year, month, date)
