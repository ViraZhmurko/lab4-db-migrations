from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Головна таблиця з базовими даними
class WeatherInfo(Base):
    __tablename__ = 'weather_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String, nullable=False)
    wind_degree = Column(Integer)
    wind_kph = Column(Float)
    wind_direction = Column(String)
    last_updated = Column(String)
    sunrise = Column(String)

    # Зв'язок з таблицею опадів
    precipitation = relationship("Precipitation", back_populates="weather", uselist=False)

# Винесена таблиця для опадів (рефакторинг)
class Precipitation(Base):
    __tablename__ = 'precipitation_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    weather_id = Column(Integer, ForeignKey('weather_info.id'), nullable=False)
    
    precip_mm = Column(Float)
    precip_in = Column(Float)
    
    # Колонка: чи варто виходити на вулицю
    should_go_outside = Column(Boolean)

    # Зв'язок з головною таблицею
    weather = relationship("WeatherInfo", back_populates="precipitation")
    