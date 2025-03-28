from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import declarative_base

from src.Models.City import City

Base = declarative_base()


class Neighborhood(Base):
    __tablename__ = 'neighborhoods'
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey(City.id), nullable=False)
    name = Column(String(255), nullable=False)
    latitude = Column(DECIMAL(40, 20))
    longitude = Column(DECIMAL(40, 20))
