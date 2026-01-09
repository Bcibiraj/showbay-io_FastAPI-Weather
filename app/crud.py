from sqlalchemy.orm import Session
from . import models, schemas

def create_weather(db: Session, weather: schemas.WeatherCreate, api_data: dict):
    db_weather = models.Weather(
        city=weather.city,
        temperature=api_data["main"]["temp"],
        humidity=api_data["main"]["humidity"],
        weather=api_data["weather"][0]["main"],
        speed=api_data["wind"]["speed"]
    )
    db.add(db_weather)
    db.commit()
    db.refresh(db_weather)
    return db_weather

def get_weather(db: Session, weather_id: int):
    return db.query(models.Weather).filter(models.Weather.id == weather_id).first()

def update_weather(db: Session, weather_id: int, weather: schemas.WeatherUpdate):
    db_weather = get_weather(db, weather_id)
    if not db_weather:
        return None

    for field, value in weather.dict(exclude_unset=True).items():
        setattr(db_weather, field, value)

    db.commit()
    db.refresh(db_weather)
    return db_weather

def delete_weather(db: Session, weather_id: int):
    db_weather = get_weather(db, weather_id)
    if not db_weather:
        return None

    db.delete(db_weather)
    db.commit()
    return db_weather
