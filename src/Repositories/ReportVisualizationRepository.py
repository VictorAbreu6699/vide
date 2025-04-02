from typing import Optional

import pandas as pd
from sqlalchemy import or_, func

from src.Database.Database import Database
from src.Helpers.ModelHelper import ModelHelper
from src.Models.Dataset import Dataset
from src.Models.Report import Report
from src.Models.ReportVisualization import ReportVisualization
from src.Models.User import User
from src.Models.Visualization import Visualization
from src.Repositories.DatasetRepository import DatasetRepository
from src.Repositories.ReportVisualizationDatasetColumnRepository import ReportVisualizationDatasetColumnRepository


class ReportVisualizationRepository:
    def __init__(self):
        self.db_session = Database().get_db()

    def get_by_report_id(self, report_id: int) -> pd.DataFrame:
        """Retorna o registro buscando pelo ID do relatório."""
        query = self.db_session.query(ReportVisualization).filter(ReportVisualization.report_id == report_id)

        return pd.read_sql(query.statement, self.db_session.bind)

    def get_by_id(self, report_visualization_id: int) -> ReportVisualization:
        """Retorna o registro buscando pelo ID."""
        query = self.db_session.query(ReportVisualization).filter(ReportVisualization.id == report_visualization_id)

        return query.first()

    def get_report_visualizations_to_edit(self, report_visualization_id: int) -> dict:
        """ Busca o registro e as colunas vinculadas a ele"""
        report_visualization = self.db_session.query(ReportVisualization).with_entities(
            ReportVisualization.id,
            ReportVisualization.report_id,
            ReportVisualization.visualization_id,
            Visualization.name.label("visualization_name"),
            ReportVisualization.name,
            ReportVisualization.position
        ).join(
            Visualization, ReportVisualization.visualization_id == Visualization.id
        ).filter(
            ReportVisualization.id == report_visualization_id
        ).first()

        report_visualization_dataset_columns = ReportVisualizationDatasetColumnRepository().\
            get_by_report_visualizations_id(report_visualization.id)

        report_visualization = ModelHelper.model_to_dict(report_visualization)
        report_visualization['report_visualization_dataset_columns'] = report_visualization_dataset_columns.to_dict(
            orient="records"
        )

        return report_visualization

    def get_report_visualizations_to_build_report(self, report_id: int) -> pd.DataFrame:
        """ Busca o registro e as colunas vinculadas a ele"""
        report_visualization_query = self.db_session.query(ReportVisualization).with_entities(
            ReportVisualization.id,
            ReportVisualization.report_id,
            ReportVisualization.visualization_id,
            Visualization.name.label("visualization_name"),
            ReportVisualization.name,
            ReportVisualization.position
        ).join(
            Visualization, ReportVisualization.visualization_id == Visualization.id
        ).filter(
            ReportVisualization.report_id == report_id
        ).order_by(ReportVisualization.id.asc())

        return pd.read_sql(report_visualization_query.statement, self.db_session.bind)

    def update(self, report_visualization_id: int, data: dict) -> Optional[Dataset]:
        report_visualization = self.get_by_id(report_visualization_id)
        if report_visualization:
            for key, value in data.items():
                setattr(report_visualization, key, value)
            self.db_session.commit()
            self.db_session.refresh(report_visualization)
        return report_visualization
