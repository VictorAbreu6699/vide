from typing import Optional

import pandas as pd
from sqlalchemy import or_, func

from src.Database.Database import Database
from src.Models.Dataset import Dataset
from src.Models.Report import Report
from src.Models.ReportVisualization import ReportVisualization
from src.Models.ReportVisualizationDatasetColumn import ReportVisualizationDatasetColumn
from src.Models.User import User


class ReportVisualizationDatasetColumnRepository:
    def __init__(self):
        self.db_session = Database().get_db()

    def get_by_report_visualizations_id(self, report_visualization_id: int) -> pd.DataFrame:
        """ Busca o registro e as colunas vinculadas a ele"""
        query = self.db_session.query(ReportVisualizationDatasetColumn).filter(
            ReportVisualizationDatasetColumn.report_visualization_id == report_visualization_id
        )

        return pd.read_sql(query.statement, self.db_session.bind)
