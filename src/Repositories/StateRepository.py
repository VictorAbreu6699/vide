from typing import Optional

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

    def get_by_id(self, state_id: int) -> Optional[State]:
        """Retorna um estado pelo ID."""
        return self.db_session.query(State).filter(State.id == state_id).first()

    def update(self, state_id: int, data: dict) -> Optional[State]:
        db_state = self.get_by_id(state_id)
        if db_state:
            for key, value in data.items():
                setattr(db_state, key, value)
            self.db_session.commit()
            self.db_session.refresh(db_state)
        return db_state

    def get_all(self, name: list[str] = None) -> pd.DataFrame:
        query = self.db_session.query(State)

        if name:
            query = query.filter(State.name.in_(name))

        return pd.read_sql(query.statement, self.db_session.bind)
