from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from app.database.models import Flats, House, LandPlot, Vehicles
from app.settings.config import settings


class DatabaseConnection:
    def __init__(self):
        database_url = settings.DATABASE_URL
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        print(self.engine.connect())

    def check_connection(self):
        try:
            # Пытаемся установить соединение с базой данных
            with self.engine.connect():
                print("Successfully connected to the database!")
                return True
        except OperationalError as e:
            print(f"Error connecting to the database: {e}")
            return False

    async def insert_data_car(self, df):
        for index, row in df.iterrows():
            # print(row.to_dict())
            try:
                # Проверяем, существует ли запись с таким же полем 'link'
                existing_vehicle = self.session.query(Vehicles).filter_by(link=row["link"]).first()

                if existing_vehicle is None:
                    # Если записи нет, создаем новую и добавляем в сессию
                    vehicle = Vehicles(
                        drive_well=row["drive_well"],
                        price=row["price"],
                        link=row["link"],
                        city=row["city"],
                        ad_publication_date=row["ad_publication_date"],
                        views=row["views"],
                        brand=row["brand"],
                        model=row["model"],
                        year=row["year"],
                        body=row["body"],
                        engine_volume=row["engine_volume"],
                        engine=row["engine"],
                        mileage=row["mileage"],
                        transmission=row["transmission"],
                    )
                    self.session.add(vehicle)
                    print("+++++++++++++")
                else:
                    print(f"Запись с link {row['link']} уже существует в базе данных.")

                # Сохраняем изменения в базе данных для каждой записи
                self.session.commit()

            except Exception as e:
                self.session.rollback()  # откатим изменения, если возникла ошибка
                print(f"Ошибка при записи данных для записи с link {row['link']}: {e}")
        # Закрываем сессию
        self.session.close()

    async def insert_data_flats(self, df):
        for index, row in df.iterrows():
            try:
                # Проверяем, существует ли запись с таким же полем 'link'
                existing_flat = self.session.query(Flats).filter_by(link=row["link"]).first()

                if existing_flat is None:
                    # Если записи нет, создаем новую и добавляем в сессию
                    flat = Flats(
                        region=row["region"],
                        rooms_number=row["rooms_number"],
                        wall_type=row["wall_type"],
                        year=row["year"],
                        floor=row["floor"],
                        total_square=row["total_square"],
                        condition=row["condition"],
                        bathroom=row["bathroom"],
                        price=row["price"],
                        price_per_square_meters=row["price_per_square_meters"],
                        link=row["link"],
                        city=row["city"],
                        ad_publication_date=datetime.now(),
                        views=row["views"],
                    )
                    self.session.add(flat)
                    print("+++++++++++++")
                else:
                    print(f"Запись с link {row['link']} уже существует в базе данных.")

                # Сохраняем изменения в базе данных для каждой записи
                self.session.commit()

            except Exception as e:
                self.session.rollback()  # откатим изменения, если возникла ошибка
                print(f"Ошибка при записи данных для записи с link {row['link']}: {e}")

            # Закрываем сессию
        self.session.close()

    async def insert_data_land(self, df):
        for index, row in df.iterrows():
            try:
                # Проверяем, существует ли запись с таким же полем 'link'
                existing_land = self.session.query(Flats).filter_by(link=row["link"]).first()

                if existing_land is None:
                    # Если записи нет, создаем новую и добавляем в сессию
                    flat = LandPlot(
                        region=row["region"],
                        total_area=row["total_area"],
                        area_unit=row["area_unit"],
                        divisibility=row["divisibility"],
                        price=row["price"],
                        cost_per_100m2=row["cost_per_100m2"],
                        ad_publication_date=datetime.now(),
                        link=row["link"],
                        views=row["views"],
                    )
                    self.session.add(flat)
                    print("+++++++++++++")
                else:
                    print(f"Запись с link {row['link']} уже существует в базе данных.")

                # Сохраняем изменения в базе данных для каждой записи
                self.session.commit()

            except Exception as e:
                self.session.rollback()  # откатим изменения, если возникла ошибка
                print(f"Ошибка при записи данных для записи с link {row['link']}: {e}")

            # Закрываем сессию
        self.session.close()

    async def insert_data_houses(self, df):
        for index, row in df.iterrows():
            try:
                # Проверяем, существует ли запись с таким же полем 'link'
                existing_house = self.session.query(Flats).filter_by(link=row["link"]).first()

                if existing_house is None:
                    # Если записи нет, создаем новую и добавляем в сессию
                    flat = House(
                        region=row["region"],
                        building_material=row["building_material"],
                        house_area=row["house_area"],
                        land_area=row["land_area"],
                        floors=row["floors"],
                        house_condition=row["condition"],
                        price=row["price"],
                        price_per_square_meters=row["price_per_square_meters"],
                        published_date=datetime.now(),
                        link=row["link"],
                        views=row["views"],
                    )
                    self.session.add(flat)
                    print("+++++++++++++")
                else:
                    print(f"Запись с link {row['link']} уже существует в базе данных.")

                # Сохраняем изменения в базе данных для каждой записи
                self.session.commit()

            except Exception as e:
                self.session.rollback()  # откатим изменения, если возникла ошибка
                print(f"Ошибка при записи данных для записи с link {row['link']}: {e}")

            # Закрываем сессию
        self.session.close()
