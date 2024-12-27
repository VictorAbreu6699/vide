from sqlalchemy import Column, Integer, String, ForeignKey, Text, func, TIMESTAMP
from sqlalchemy.orm import declarative_base

from src.Models.User import User

Base = declarative_base()


class Dataset(Base):
    __tablename__ = 'datasets'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    extension = Column(String(10), nullable=True)
    path = Column(String(1000), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id))
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
