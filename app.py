from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import WeatherInfo, Precipitation

# Підключення до БД
engine = create_engine('postgresql+psycopg2://postgres:verandaaa@localhost:5432/weather')
Session = sessionmaker(bind=engine)
session = Session()

print("\n--- Консольний клієнт погоди ---")
while True:
    country_input = input("\nВведіть назву країни (англійською, наприклад Ukraine, або 'q' для виходу): ")
    if country_input.lower() == 'q':
        break
    
    date_input = input("Введіть дату (формат YYYY-MM-DD, наприклад 2024-05-16, або просто натисніть Enter щоб побачити всі дати): ")

    # Будуємо запит до БД (з'єднуємо обидві таблиці)
    query = session.query(WeatherInfo).join(Precipitation).filter(
        WeatherInfo.country.ilike(f"%{country_input}%")
    )
    
    # Якщо ввели дату - фільтруємо і по ній
    if date_input:
        query = query.filter(WeatherInfo.last_updated.like(f"{date_input}%"))

    results = query.all()

    if not results:
        print(" Даних для цієї країни/дати не знайдено в базі.")
        continue

    print(f"\n Результати для {country_input.title()}:")
    for w in results:
        print(f"Дата та час: {w.last_updated}")
        print(f"Схід сонця: {w.sunrise}")
        print(f"Вітер: {w.wind_kph} км/год, Напрямок: {w.wind_direction} ({w.wind_degree}°)")
        print(f"Опади: {w.precipitation.precip_mm} мм ({w.precipitation.precip_in} in)")
        
        # Наша кастомна колонка з рефакторингу
        if w.precipitation.should_go_outside:
            print("Чи варто виходити на вулицю? -> ТАК (опадів мало або немає)")
        else:
            print("Чи варто виходити на вулицю? -> НІ (очікуються значні опади)")
        print("-" * 40)