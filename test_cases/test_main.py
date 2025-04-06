import sys
import os
from fastapi.testclient import TestClient
import pytest
from datetime import datetime, timedelta

# Add the parent directory of 'test' to sys.path to import 'main.py'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app  # Import FastAPI app from main.py

client = TestClient(app)

# 1) Test Case: If Any Required Parameter is Not Set
def test_get_flight_info_missing_parameter():
    response = client.get("/flight-info", params={"airline_code": "AA", "flight_number": "123"})
    assert response.status_code == 422

# 2) Test Case: If Any Required Parameter Format is Not Correct
def test_get_flight_info_invalid_airline_code_format():
    response = client.get("/flight-info", params={"airline_code": "A1", "flight_number": "123", "date": "10-12-2023"})
    assert response.status_code == 422

def test_get_flight_info_invalid_flight_number_format():
    response = client.get("/flight-info", params={"airline_code": "AA", "flight_number": "ABC", "date": "10-12-2023"})
    assert response.status_code == 422

def test_get_flight_info_invalid_date_format():
    # Send a request with an invalid date format
    response = client.get("/flight-info", params={"airline_code": "AA", "flight_number": "123", "date": "2023-12-10"})
    
    # Assert that the response status code is 422
    assert response.status_code == 422
    
    # Check that the response contains a 'detail' field with a list of validation errors
    response_json = response.json()
    assert "detail" in response_json
    assert isinstance(response_json["detail"], list)
    
    # Extract the first validation error from the 'detail' list
    error = response_json["detail"][0]
    
    # Assert that the error message matches the expected string
    assert error["msg"] == "String should match pattern '^\\d{2}-\\d{2}-\\d{4}$'"

# 3) Test Case: Give Date as 7 Days Before Current Date and See What It Responds
def test_get_flight_info_seven_days_before():
    # Calculate the date 7 days before the current date
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%d-%m-%Y")
    
    # Make the request to the /flight-info endpoint with the calculated date
    response = client.get("/flight-info", params={"airline_code": "AA", "flight_number": "123", "date": seven_days_ago})
    
    # Assert that the status code is 200 (OK)
    assert response.status_code == 200
    
    # Assert that the response contains the 'source' and 'data' fields
    response_json = response.json()
    assert "source" in response_json
    assert "data" in response_json
    
    # Assert that the 'data' field contains the specific error message
    assert response_json["data"].get("error") == "No flights matching the search criteria. Please search the inputs."

# 4) Test Case: If API URI is Wrong
def test_get_flight_info_invalid_uri():
    response = client.get("/wrong-uri")
    assert response.status_code == 404

# 5) Test Case: If POST Method is Sent
def test_get_flight_info_post_method():
    response = client.post("/flight-info", json={"airline_code": "AA", "flight_number": "123", "date": "10-12-2023"})
    assert response.status_code == 405

# 6) Test Case: Success scenario
def test_get_flight_info_successful_response():
    # Set a valid date (ensure that the date is in dd-mm-yyyy format)
    valid_date = "07-04-2025"

    # Make a request to the /flight-info endpoint with valid parameters
    response = client.get("/flight-info", params={
        "airline_code": "AA",
        "flight_number": "1811",
        "date": valid_date
    })

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Extract the response JSON
    response_json = response.json()

    # Assert that the 'data' field is present in the response
    assert "data" in response_json

    # Assert that 'flight_number' is present inside the 'data'
    assert "flight_number" in response_json["data"]

