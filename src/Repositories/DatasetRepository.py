from typing import Optional, Type

from src.Database.Database import Database
from src.Models.Dataset import Dataset


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

    def get_all(self) -> list[Type[Dataset]]:
        return self.db_session.query(Dataset).all()

    def update(self, dataset_id: int, data: dict) -> Optional[Dataset]:
        dataset = self.get_by_id(dataset_id)
        if dataset:
            for key, value in data.items():
                setattr(dataset, key, value)
            self.db_session.commit()
            self.db_session.refresh(dataset)
        return dataset
