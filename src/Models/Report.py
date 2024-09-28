from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

from src.Models.Dataset import Dataset
from src.Models.User import User

Base = declarative_base()


class Report(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    dataset_id = Column(Integer, ForeignKey(Dataset.id), nullable=False)
