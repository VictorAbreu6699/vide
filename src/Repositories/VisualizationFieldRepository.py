import pandas as pd

from src.Database.Database import Database
from src.Models.VisualizationField import VisualizationField


class VisualizationFieldRepository:
    def __init__(self):
        self.db_session = Database().get_db()

    def create(self, data: dict) -> VisualizationField:
        """Cria um novo relacionamento entre visualização e campo no banco de dados."""
        visualization_field = VisualizationField(**data)
        self.db_session.add(visualization_field)
        self.db_session.commit()
        self.db_session.refresh(visualization_field)
        return visualization_field

    def bulk_save_objects(self, data: list[dict]):
        """Salva vários registros no banco de dados simultaneamente"""
        fields = [VisualizationField(**item) for item in data]
        self.db_session.bulk_save_objects(fields)
        self.db_session.commit()

    def get_all(self, field_id: list[int] = None, visualization_id: list[int] = None) -> pd.DataFrame:
        query = self.db_session.query(VisualizationField)

        if field_id:
            query = query.filter(VisualizationField.field_id.in_(field_id))

        if visualization_id:
            query = query.filter(VisualizationField.visualization_id.in_(visualization_id))

        return pd.read_sql(query.statement, self.db_session.bind)
