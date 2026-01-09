import pytest
from unittest.mock import AsyncMock
from app import crud, schemas
from app.external import fetch_weather


# Fake DB for Unit Tests

class FakeDB:
    def __init__(self):
        self.data = []
        self.committed = False

    def add(self, obj):
        self.data.append(obj)

    def commit(self):
        self.committed = True

    def refresh(self, obj):
        obj.id = 1

    def query(self, model):
        return self

    def filter(self, condition):
        return self

    def first(self):
        return self.data[0] if self.data else None

    def delete(self, obj):
        self.data.remove(obj)


# UNIT: create_weather

def test_create_weather_unit():
    db = FakeDB()

    weather_schema = schemas.WeatherCreate(city="Chennai")
    api_data = {
        "main": {"temp": 30, "humidity": 70},
        "weather": [{"main": "Clouds"}],
        "wind": {"speed": "3.4"}
    }

    result = crud.create_weather(db, weather_schema, api_data)

    assert result.city == "Chennai"
    assert result.temperature == 30
    assert result.humidity == 70
    assert result.weather == "Clouds"
    assert db.committed is True


# UNIT: get_weather

def test_get_weather_unit():
    db = FakeDB()

    weather_schema = schemas.WeatherCreate(city="Chennai")
    api_data = {
        "main": {"temp": 28, "humidity": 65},
        "weather": [{"main": "Rain"}],
        "wind": {"speed": "2.1"}
    }

    crud.create_weather(db, weather_schema, api_data)
    result = crud.get_weather(db, 1)

    assert result.city == "Chennai"


# UNIT: update_weather

def test_update_weather_unit():
    db = FakeDB()

    weather_schema = schemas.WeatherCreate(city="Chennai")
    api_data = {
        "main": {"temp": 25, "humidity": 60},
        "weather": [{"main": "Clear"}],
        "wind": {"speed": "1.5"}
    }

    crud.create_weather(db, weather_schema, api_data)

    update_data = schemas.WeatherUpdate(temperature=35)
    result = crud.update_weather(db, 1, update_data)

    assert result.temperature == 35


# UNIT: delete_weather

def test_delete_weather_unit():
    db = FakeDB()

    weather_schema = schemas.WeatherCreate(city="Chennai")
    api_data = {
        "main": {"temp": 22, "humidity": 55},
        "weather": [{"main": "Mist"}],
        "wind": {"speed": "2.0"}
    }

    crud.create_weather(db, weather_schema, api_data)
    deleted = crud.delete_weather(db, 1)

    assert deleted.city == "Chennai"
    assert len(db.data) == 0


# -----------------------# UNIT: fetch_weather (Mock API)

@pytest.mark.asyncio
async def test_fetch_weather_unit(mocker):
    fake_response = {
        "main": {"temp": 33, "humidity": 50},
        "weather": [{"main": "Sunny"}],
        "wind": {"speed": "4.3"}
    }

    # Correct AsyncMock setup
    mock_response = AsyncMock()
    mock_response.json = AsyncMock(return_value=fake_response)  
    mock_response.raise_for_status.return_value = None        

    mocker.patch("httpx.AsyncClient.get", return_value=mock_response)

    result = await fetch_weather("Chennai")

    assert result["main"]["temp"] == 33
    assert result["main"]["humidity"] == 50
    assert result["weather"][0]["main"] == "Sunny"
    assert result["wind"]["speed"] == "4.3"
