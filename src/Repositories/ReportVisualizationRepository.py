from typing import Optional

import pandas as pd
from sqlalchemy import or_, func

from src.Database.Database import Database
from src.Models.Dataset import Dataset
from src.Models.Report import Report
from src.Models.ReportVisualization import ReportVisualization
from src.Models.User import User


class ReportVisualizationRepository:
    def __init__(self):
        self.db_session = Database().get_db()

    def get_by_report_id(self, report_id: int) -> pd.DataFrame:
        """Retorna o registro buscando pelo ID do relatório."""
        query = self.db_session.query(ReportVisualization).filter(ReportVisualization.report_id == report_id)

        return pd.read_sql(query.statement, self.db_session.bind)
