from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class State(Base):
    __tablename__ = 'states'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    latitude = Column(DECIMAL(40, 20))
    longitude = Column(DECIMAL(40, 20))
