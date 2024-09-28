from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import declarative_base
from src.Models.Report import Report
from src.Models.Visualization import Visualization

Base = declarative_base()


class ReportVisualization(Base):
    __tablename__ = 'report_visualization'
    id = Column(Integer, primary_key=True)
    visualization_id = Column(Integer, ForeignKey(Visualization.id), nullable=False)
    report_id = Column(Integer, ForeignKey(Report.id), nullable=False)
