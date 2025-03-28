import pandas as pd

from src.Database.Database import Database
from src.Models.State import State


class StateRepository:
    def __init__(self):
        self.db_session = Database().get_db()

    def create(self, data: dict) -> State:
        """Cria um novo estado no banco de dados."""
        state = State(**data)
        self.db_session.add(state)
        self.db_session.commit()
        self.db_session.refresh(state)
        return state

    def bulk_save_objects(self, data: list[dict]):
        """Salva vários estados no banco de dados simultaneamente"""
        states = [State(**item) for item in data]
        self.db_session.bulk_save_objects(states)
        self.db_session.commit()

    def get_all(self, name: list[str] = None) -> pd.DataFrame:
        query = self.db_session.query(State)

        if name:
            query = query.filter(State.name.in_(name))

        return pd.read_sql(query.statement, self.db_session.bind)
