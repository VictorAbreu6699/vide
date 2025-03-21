from typing import Optional

import pandas as pd
from sqlalchemy import or_, func

from src.Database.Database import Database
from src.Helpers.ModelHelper import ModelHelper
from src.Models.Dataset import Dataset
from src.Models.Report import Report
from src.Models.ReportVisualization import ReportVisualization
from src.Models.User import User
from src.Repositories.ReportVisualizationDatasetColumnRepository import ReportVisualizationDatasetColumnRepository


class ReportVisualizationRepository:
    def __init__(self):
        self.db_session = Database().get_db()

    def get_by_report_id(self, report_id: int) -> pd.DataFrame:
        """Retorna o registro buscando pelo ID do relatório."""
        query = self.db_session.query(ReportVisualization).filter(ReportVisualization.report_id == report_id)

        return pd.read_sql(query.statement, self.db_session.bind)

    def get_report_visualizations_to_edit(self, report_visualization_id: int) -> dict:
        """ Busca o registro e as colunas vinculadas a ele"""
        report_visualization = self.db_session.query(ReportVisualization).filter(
            ReportVisualization.id == report_visualization_id
        ).first()

        report_visualization_dataset_columns = ReportVisualizationDatasetColumnRepository().\
            get_by_report_visualizations_id(report_visualization.id)

        report_visualization = ModelHelper.model_to_dict(report_visualization)
        report_visualization['report_visualization_dataset_columns'] = report_visualization_dataset_columns.to_dict(
            orient="records"
        )

        return report_visualization
