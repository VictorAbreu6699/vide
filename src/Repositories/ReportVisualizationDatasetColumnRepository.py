from typing import Optional

import pandas as pd
from sqlalchemy import or_, func

from src.Database.Database import Database
from src.Models.Dataset import Dataset
from src.Models.DatasetColumn import DatasetColumn
from src.Models.Field import Field
from src.Models.Report import Report
from src.Models.ReportVisualization import ReportVisualization
from src.Models.ReportVisualizationDatasetColumn import ReportVisualizationDatasetColumn
from src.Models.User import User
from src.Models.VisualizationField import VisualizationField


class ReportVisualizationDatasetColumnRepository:
    def __init__(self):
        self.db_session = Database().get_db()

    def get_by_report_visualizations_id(self, report_visualization_id: int) -> pd.DataFrame:
        """ Busca o registro e as colunas vinculadas a ele"""
        query = self.db_session.query(ReportVisualizationDatasetColumn)

        query = query.join(
            DatasetColumn, DatasetColumn.id == ReportVisualizationDatasetColumn.dataset_column_id
        ).join(
            VisualizationField, VisualizationField.id == ReportVisualizationDatasetColumn.visualization_field_id
        ).join(
            Field, Field.id == VisualizationField.field_id
        )

        query = query.with_entities(
            ReportVisualizationDatasetColumn.id,
            ReportVisualizationDatasetColumn.report_visualization_id,
            ReportVisualizationDatasetColumn.visualization_field_id,
            ReportVisualizationDatasetColumn.dataset_id,
            ReportVisualizationDatasetColumn.dataset_column_id,
            DatasetColumn.name.label("dataset_column_name"),
            DatasetColumn.type.label("dataset_column_type"),
            Field.id.label("field_id"),
            Field.name.label("field_name")
        ).filter(
            ReportVisualizationDatasetColumn.report_visualization_id == report_visualization_id
        ).order_by(ReportVisualizationDatasetColumn.id.asc())

        return pd.read_sql(query.statement, self.db_session.bind)
