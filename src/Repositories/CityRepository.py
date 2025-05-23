import pandas as pd
from src.Database.Database import Database
from src.Models.City import City
from src.Models.State import State


class CityRepository:
    def __init__(self):
        self.db_session = Database().get_db()

    def bulk_save_objects(self, data: list[dict]):
        """Salva várias cidades no banco de dados simultaneamente"""
        cities = [City(**item) for item in data]
        self.db_session.bulk_save_objects(cities)
        self.db_session.commit()

    def get_all(self, name: list[str] = None, state_id: int = None) -> pd.DataFrame:
        query = self.db_session.query(City).join(State, State.id == City.state_id)

        query = query.with_entities(
            City.id,
            City.state_id,
            State.name.label("state_name"),
            City.name,
            City.latitude,
            City.longitude
        )

        if name:
            query = query.filter(City.name.in_(name))

        if state_id:
            query = query.filter(City.state_id == state_id)

        return pd.read_sql(query.statement, self.db_session.bind)
