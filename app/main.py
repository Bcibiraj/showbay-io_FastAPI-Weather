from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, crud, external
from app.schemas import *
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Weather Assessment")

# 1 POST - Create Weather Record (External API)
@app.post("/weather", response_model=WeatherResponse, status_code=status.HTTP_201_CREATED)
async def create_weather(weather: WeatherCreate, db: Session = Depends(get_db)):
    try:
        api_data = await external.fetch_weather(weather.city)
    except Exception:
        raise HTTPException(status_code=503, detail="Weather API unavailable")

    return crud.create_weather(db, weather, api_data)


# 2️ GET - Read Weather
@app.get("/weather/{weather_id}", response_model=WeatherResponse, status_code=status.HTTP_200_OK)
def get_weather(weather_id: int, db: Session = Depends(get_db)):
    db_weather = crud.get_weather(db, weather_id)
    if not db_weather:
        raise HTTPException(status_code=404, detail="Weather record not found")
    return db_weather


# 3️ PUT - Update Weather
@app.put("/weather/{weather_id}", response_model=WeatherResponse, status_code=status.HTTP_200_OK)
def update_weather(weather_id: int, weather: WeatherUpdate, db: Session = Depends(get_db)):
    db_weather = crud.update_weather(db, weather_id, weather)
    if not db_weather:
        raise HTTPException(status_code=404, detail="Weather record not found")
    return db_weather


# 4️ DELETE - Delete Weather
@app.delete("/weather/{weather_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_weather(weather_id: int, db: Session = Depends(get_db)):
    db_weather = crud.delete_weather(db, weather_id)
    if not db_weather:
        raise HTTPException(status_code=404, detail="Weather record not found")
    return None
