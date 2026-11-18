import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import WeatherInfo, Precipitation

# Підключення до бази даних
engine = create_engine('postgresql+psycopg2://postgres:verandaaa@localhost:5432/weather')
Session = sessionmaker(bind=engine)
session = Session()

print("Чтение данных из CSV-файла...")
df = pd.read_csv('GlobalWeatherRepository.csv')

# Беремо перші 500 записів, щоб скрипт відпрацював швидко 
df_sample = df.head(500)

print("Загрузка данных в базу...")
for index, row in df_sample.iterrows():
    # 1. Заповнюємо головну таблицю
    weather_record = WeatherInfo(
        country=row['country'],
        wind_degree=row['wind_degree'],
        wind_kph=row['wind_kph'],
        wind_direction=row['wind_direction'],
        last_updated=row['last_updated'],
        sunrise=row['sunrise']
    )
    session.add(weather_record)
    session.flush() # Отримуємо згеенрований айді для зв'язку

    # 2. Формула для "Чи варто виходити на вулицю"
    # Якщо опадів (precip_mm) більше 2.0 мм - не варто виходити (False)
    precip = float(row['precip_mm'])
    go_outside = False if precip > 2.0 else True

    # 3. заповнюємо таблицю опадів (наш ерфакторинг)
    precip_record = Precipitation(
        weather_id=weather_record.id,
        precip_mm=precip,
        precip_in=float(row['precip_in']),
        should_go_outside=go_outside
    )
    session.add(precip_record)

# Зберігаємо все в базу
session.commit()
print("Данные успешно загружены!")