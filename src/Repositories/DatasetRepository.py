import pandas as pd
from typing import Optional

from sqlalchemy import or_, func

from src.Database.Database import Database
from src.Models.Dataset import Dataset
from src.Models.User import User


class DatasetRepository:
    def __init__(self):
        self.db_session = Database().get_db()

    def create(self, data: dict) -> Dataset:
        """Cria um novo dataset no banco de dados."""
        dataset = Dataset(**data)
        self.db_session.add(dataset)
        self.db_session.commit()
        self.db_session.refresh(dataset)
        return dataset

    def get_by_id(self, dataset_id: int) -> Optional[Dataset]:
        """Retorna um dataset pelo ID."""
        return self.db_session.query(Dataset).filter(Dataset.id == dataset_id).first()

    def get_all(self, search: str = None) -> pd.DataFrame:
        query = self.db_session.query(Dataset, User).join(User, User.id == Dataset.user_id)

        query = query.with_entities(
            Dataset.id, Dataset.name, Dataset.description, User.name.label("user_name"), User.email.label("user_email")
        )

        if search:
            query = query.filter(
                or_(
                    func.lower(User.name).like(f"%{search.lower()}%"),
                    func.lower(User.email).like(f"%{search.lower()}%"),
                    func.lower(Dataset.name).like(f"%{search.lower()}%"),
                )
            )

        query = query.limit(30)

        return pd.read_sql(query.statement, self.db_session.bind)

    def update(self, dataset_id: int, data: dict) -> Optional[Dataset]:
        dataset = self.get_by_id(dataset_id)
        if dataset:
            for key, value in data.items():
                setattr(dataset, key, value)
            self.db_session.commit()
            self.db_session.refresh(dataset)
        return dataset
