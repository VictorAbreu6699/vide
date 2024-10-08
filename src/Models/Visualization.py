from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Visualization(Base):
    __tablename__ = 'visualizations'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
