from sqlalchemy import Column, DateTime, Float, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Vehicles(Base):  # type: ignore
    __tablename__ = "vehicles_indexation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    drive_well = Column(String)
    price = Column(Integer)
    link = Column(String)
    city = Column(String)
    ad_publication_date = Column(DateTime(timezone=False), nullable=True)
    views = Column(Integer)
    brand = Column(String)
    model = Column(String)
    year = Column(Integer)
    body = Column(String)
    engine_volume = Column(Float)
    engine = Column(String)
    mileage = Column(Integer)
    transmission = Column(String)
    dump_created_date = Column(DateTime(timezone=False), server_default=func.now())

    def __repr__(self):
        return f"<Advert(id={self.id}, brand_model={self.model}, link={self.link})>"


class Flats(Base):  # type: ignore
    __tablename__ = "flats_indexation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    region = Column(String)
    rooms_number = Column(Integer)
    wall_type = Column(String)
    year = Column(Integer)
    floor = Column(Integer)
    total_square = Column(Float)
    condition = Column(String)
    bathroom = Column(String)
    price = Column(Integer)
    price_per_square_meters = Column(Float)
    link = Column(String)
    city = Column(String)
    ad_publication_date = Column(DateTime(timezone=False), nullable=True)
    views = Column(Integer)
    dump_created_date = Column(DateTime(timezone=False), server_default=func.now())


class House(Base):  # type: ignore
    __tablename__ = "house_indexation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    region = Column(String)
    building_material = Column(String)
    house_area = Column(Float)
    land_area = Column(Float)
    floors = Column(Integer)
    house_condition = Column(String)
    price = Column(Integer)
    price_per_square_meters = Column(Float)
    link = Column(String)
    published_date = Column(DateTime(timezone=False))
    views = Column(Integer)


class LandPlot(Base):  # type: ignore
    __tablename__ = "land_plot_indexation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    region = Column(String)
    total_area = Column(Float)
    area_unit = Column(String)
    divisibility = Column(String)
    price = Column(Integer)
    cost_per_100m2 = Column(Float)
    link = Column(String)
    ad_publication_date = Column(DateTime(timezone=False), nullable=True)
    views = Column(Integer)
