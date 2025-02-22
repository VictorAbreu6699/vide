from typing import Optional

import pandas as pd

from src.Database.Database import Database
from src.Models.Field import Field
from src.Models.Visualization import Visualization
from src.Models.VisualizationField import VisualizationField


class VisualizationRepository:
    def __init__(self):
        self.db_session = Database().get_db()

    def create(self, data: dict) -> Visualization:
        """Cria uma nova visualização no banco de dados."""
        visualization = Visualization(**data)
        self.db_session.add(visualization)
        self.db_session.commit()
        self.db_session.refresh(visualization)
        return visualization

    def get_by_name(self, name: int) -> Optional[Visualization]:
        """Retorna uma visualização pelo nome."""
        return self.db_session.query(Visualization).filter(Visualization.name == name).first()

    def get_all(self, name: list[str] = None) -> pd.DataFrame:
        query = self.db_session.query(Visualization)

        if name:
            query = query.filter(Visualization.name.in_(name))

        return pd.read_sql(query.statement, self.db_session.bind)

    def get_visualization_fields(self, visualization_id: int) -> pd.DataFrame:
        query = self.db_session.query(Field).join(VisualizationField, Field.id == VisualizationField.field_id)

        query = query.filter(VisualizationField.visualization_id == visualization_id)

        return pd.read_sql(query.statement, self.db_session.bind)
