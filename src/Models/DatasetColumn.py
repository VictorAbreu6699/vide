from sqlalchemy import Column, Integer, String, Enum, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import declarative_base

from src.Models.Dataset import Dataset

Base = declarative_base()


class DatasetColumn(Base):
    __tablename__ = 'dataset_columns'
    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey(Dataset.id), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(Enum('number', 'string', 'date'))
    order = Column(Integer, nullable=False, default=1)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())

