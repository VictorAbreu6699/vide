import pandas as pd
from src.Database.Database import Database
from src.Models.Neighborhood import Neighborhood


class NeighborhoodRepository:
    def __init__(self):
        self.db_session = Database().get_db()

    def create(self, data: dict) -> Neighborhood:
        """Cria um novo bairro no banco de dados."""
        neighborhood = Neighborhood(**data)
        self.db_session.add(neighborhood)
        self.db_session.commit()
        self.db_session.refresh(neighborhood)
        return neighborhood

    def bulk_save_objects(self, data: list[dict]):
        """Salva vários estados no banco de dados simultaneamente"""
        neighborhoods = [Neighborhood(**item) for item in data]
        self.db_session.bulk_save_objects(neighborhoods)
        self.db_session.commit()

    def get_all(self, name: list[str] = None) -> pd.DataFrame:
        query = self.db_session.query(Neighborhood)

        if name:
            query = query.filter(Neighborhood.name.in_(name))

        return pd.read_sql(query.statement, self.db_session.bind)
