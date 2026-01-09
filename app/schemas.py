from pydantic import BaseModel, Field
from datetime import datetime

class WeatherCreate(BaseModel):
    city: str = Field(..., min_length=2)

class WeatherUpdate(BaseModel):
    temperature: float | None = None
    humidity: float | None = None
    weather: str | None = None
    speed: str | None = None

class WeatherResponse(BaseModel):
    id: int
    city: str
    temperature: float
    humidity: float
    weather: str
    speed: str
    timestamp: datetime

    class Config:
        orm_mode = True