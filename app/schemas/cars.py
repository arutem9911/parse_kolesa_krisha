from datetime import datetime

from pydantic import BaseModel


class Vehicles(BaseModel):
    brand: str | None = None  # Марка –Toyota, Hyuindai
    model: str | None = None  # Модель –Camry, Accent
    body: str | None = None  # Кузов – кроссовер
    engine_volume: float | None = None  # Числовой, один знак после целых
    engine: str | None = None  # Тип топлива – (бензин)
    mileage: float | None = None  # Пробег – 20 000
    year: int | None = None  # Год выпуска –2004, 2006, 2010
    transmission: str | None = None  # Тип КПП –Механика, Автомат
    drive_well: str | None = None  # Привод – полный привод
    price: int | None = None
    link: str | None = None
    city: str | None = None
    ad_publication_date: datetime | None = None
    views: int | None = None
