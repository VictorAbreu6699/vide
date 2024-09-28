from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

from src.Models.Dataset import Dataset
from src.Models.ReportVisualization import ReportVisualization
from src.Models.VisualizationField import VisualizationField

Base = declarative_base()


class ReportVisualizationDatasetColumn(Base):
    __tablename__ = 'report_visualization_dataset_columns'
    id = Column(Integer, primary_key=True)
    report_visualization_id = Column(Integer, ForeignKey(ReportVisualization.id), nullable=False)
    visualization_field_id = Column(Integer, ForeignKey(VisualizationField.id), nullable=False)
    dataset_id = Column(Integer, ForeignKey(Dataset.id), nullable=False)
    column = Column(String(255), nullable=False)

