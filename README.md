# Flight Info Scraper

A FastAPI + Celery + Redis based app to scrape flight details from FlightStats.

## Design of solution

**✈️ Flight Info Scraper App - Algorithm Flow**

**1. User Request**

       User hits the FastAPI endpoint /flight-info with:
          airline_code
          flight_number
          date (dd-mm-yyyy)

**2. Input Validation**
       FastAPI validates:
       
       airline_code is 2-3 capital letters
       flight_number is numeric
       date matches dd-mm-yyyy

**3. Cache Check (Redis)**
       
       App constructs a cache key using the three parameters: AA:123:2025-04-05
       
     ✅ If cached → Return cached response immediately
     → Also trigger background refresh using Celery

     ❌ If not cached → Proceed to scraping (I have not used celery here to respond to user saying "Your request is accepted and processing, please come after 2 mins. Since the scrapping is mostly within 30sec which is a general API accepted timeout")

**4. Scraping (Playwright + BeautifulSoup)**

      Use Playwright to load the flight status page
      Parse flight data with BeautifulSoup

**5. Caching & Response**

      If data is valid:
                Save to Redis cache
                Return response to user

      If data is missing or invalid:
       Return error accordingly

**6. Background Task (Celery)**

        When cache hit:
              Trigger refresh_flight_info_task via Celery to scrape updated data in background. 
      
       Update Redis with fresh data

**🔄 Data Storage**
      Redis: Short-lived, fast cache for quick reads

**📦 Technologies Involved**

     FastAPI: API framework
     
     Celery: Background task queue
     
     Redis: Cache + Celery broker/backend
     
     Playwright + BeautifulSoup: Scraping and parsing


## Project Structure

              flight_info_scraper/
              ├── main.py                         # FastAPI app entrypoint
              ├── celery_worker.py                # Celery app config
              ├── requirements.txt                # Python dependencies
              
              ├── core/                           # Shared utilities (caching, config)
              │   └── cache.py                    # Redis caching functions
              
              ├── tasks/                          # Celery tasks
              │   └── flight_tasks.py             # Task to scrape and parse flight info
              
              ├── scraper/                        # Scraping logic
              │   ├── browser.py                  # Playwright browser logic
              │   ├── flight_page.py              # Abstractions over HTML structure
              │   └── parser.py                   # HTML parsing logic using BeautifulSoup 

		  ├── test_cases/                     # Unit Test cases
              │   ├── pytest                      # Pytest configuration
              │   └── test_main.py                # Test cases

## Python setup
      python -m venv venv
      
      venv\Scripts\activate

## dependancy setup 
      1. pip install -r requirements.txt
      2. pip install playwright (install playwright) - this is needed separately to install the required browsers
      3. Set up Redis locally (sudo systemctl start redis)
      4. ./start_app.sh

## test cases
      1. install pytest testing libraries (pip install pytest pytest-mock fastapi, pip install httpx)
      2. pytest test_cases/test_main.py

## Enhancements or Alternate ways
      1. We can use celery on the api request itself to make it asynchronous API.
      2. we can also do search page scraping instead of directly calling the result page.
      3. Instead of web scraping we could simply call the REST API of the flight tracker page and transform the response. In this case its a simple middleware integration which involves a call to external REST API and transform the message as needed by consumer.
      4. We can also integrate any DB and push the date to push the data to DB.