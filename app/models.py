from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database import Base

class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    weather = Column(String, nullable=False)
    speed = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)  