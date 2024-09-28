from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

from src.Models.Field import Field
from src.Models.Visualization import Visualization

Base = declarative_base()


class VisualizationField(Base):
    __tablename__ = 'visualization_fields'
    id = Column(Integer, primary_key=True)
    visualization_id = Column(Integer, ForeignKey(Visualization.id), nullable=False)
    field_id = Column(Integer, ForeignKey(Field.id), nullable=False)
