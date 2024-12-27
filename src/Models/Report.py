from sqlalchemy import Column, Integer, String, ForeignKey, Text, func, TIMESTAMP
from sqlalchemy.orm import declarative_base

from src.Models.Dataset import Dataset
from src.Models.User import User

Base = declarative_base()


class Report(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    dataset_id = Column(Integer, ForeignKey(Dataset.id), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
