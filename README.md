# 🌤️ FastAPI Weather Tracker

A simple FastAPI project to fetch and store weather data for cities.

## Overview

* Fetch current weather from an external API.
* Store and manage weather records in a database.
* Supports CRUD operations.

## Assumptions

* Temperature in Celsius, wind speed in m/s.
* Most recent weather record is considered current.
* External API failures handled gracefully.

## Database Table `weather`

* `id` (int, PK)
* `city` (string)
* `temperature` (float)
* `humidity` (int)
* `weather` (string)
* `wind_speed` (float)
* `timestamp` (datetime)

## Project Structure

```
app/
├── main.py
├── models.py
├── schemas.py
├── crud.py
├── external.py
├── database.py
└── utils.py

tests/
├── test_unit.py
└── test_integration.py
```

## How to Run

1. Clone repo: `git clone <repo_url>`
2. Create venv: `python -m venv venv` and activate.
3. Install dependencies: `pip install -r requirements.txt`
4. Create `.env` file with `DATABASE_URL` and `WEATHER_API_KEY`.
5. Run server: `uvicorn app.main:app --reload`
6. Open API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Example API Calls

* Fetch Weather (GET): `curl -X GET "http://127.0.0.1:8000/weather/current?city=Chennai"`
* Create Record (POST): `curl -X POST "http://127.0.0.1:8000/weather/" -H "Content-Type: application/json" -d '{"city":"Chennai","temperature":30,"humidity":70,"weather":"Sunny","wind_speed":4.3}'`

## Testing

Run tests: `pytest -v`
Async API calls are mocked. Tests cover CRUD and fetching weather.
