from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Field(Base):
    __tablename__ = 'fields'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    type = Column(Enum('number', 'string', 'date'))

