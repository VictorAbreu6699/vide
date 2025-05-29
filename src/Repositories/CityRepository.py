from typing import Optional

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
            City.longitude,
            City.geo_json
        )

        if name:
            query = query.filter(City.name.in_(name))

        if state_id:
            query = query.filter(City.state_id == state_id)

        return pd.read_sql(query.statement, self.db_session.bind)

    def update(self, state_id: int, data: dict) -> Optional[City]:
        db_city = self.get_by_id(state_id)
        if db_city:
            for key, value in data.items():
                setattr(db_city, key, value)
            self.db_session.commit()
            self.db_session.refresh(db_city)
        return db_city

    def get_by_id(self, city_id: int) -> Optional[City]:
        """Retorna um estado pelo ID."""
        return self.db_session.query(City).filter(City.id == city_id).first()
