from datetime import datetime

from pydantic import BaseModel


class Flat(BaseModel):
    region: str | None = None  # Область – Алматы, Атырауская обл.
    rooms_count: int | None = None  # Количество комнат – 1, 2, 3 и более 3-х
    wall_type: str | None = None  # панельный … Формат текстовый
    year: int | None = None  # Год постройки – 1975, 2003, 2010
    floor: int | None = None  # Этаж – 2, 3, 5
    total_square_meters: int | None = None  # Общая площадь
    condition: str | None = None  # Состояние – свежий ремонт, не новый, но аккуратный ремонт
    bathroom: str | None = None  # Санузел – раздельный, совмещённый
    price: int | None = None  # Цена
    price_per_square_meter: float | None = None  # Стоимость 1 кв.м
    link: str | None = None
    ad_publication_date: datetime | None = None
    views: int | None = None
