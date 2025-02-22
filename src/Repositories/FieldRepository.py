import pandas as pd

from src.Database.Database import Database
from src.Models.Field import Field


class FieldRepository:
    def __init__(self):
        self.db_session = Database().get_db()

    def create(self, data: dict) -> Field:
        """Cria um novo campo no banco de dados."""
        field = Field(**data)
        self.db_session.add(field)
        self.db_session.commit()
        self.db_session.refresh(field)
        return field

    def bulk_save_objects(self, data: list[dict]):
        """Salva vários campos no banco de dados simultaneamente"""
        fields = [Field(**item) for item in data]
        self.db_session.bulk_save_objects(fields)
        self.db_session.commit()

    def get_all(self, name: list[str] = None) -> pd.DataFrame:
        query = self.db_session.query(Field)

        if name:
            query = query.filter(Field.name.in_(name))

        return pd.read_sql(query.statement, self.db_session.bind)
