from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, JSON
from sqlalchemy.orm import declarative_base

from src.Models.State import State

Base = declarative_base()


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    state_id = Column(Integer, ForeignKey(State.id), nullable=False)
    name = Column(String(255), nullable=False)
    latitude = Column(DECIMAL(40, 20))
    longitude = Column(DECIMAL(40, 20))
    geo_json = Column(JSON)
