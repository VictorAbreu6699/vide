import pandas as pd
from typing import Optional

from sqlalchemy import or_, func

from src.Database.Database import Database
from src.Models.Dataset import Dataset
from src.Models.DatasetColumn import DatasetColumn
from src.Models.User import User


class DatasetColumnRepository:
    def __init__(self):
        self.db_session = Database().get_db()

    def get_by_dataset_id(self, dataset_id: int) -> pd.DataFrame:
        query = self.db_session.query(DatasetColumn).filter(DatasetColumn.dataset_id == dataset_id)

        return pd.read_sql(query.statement, self.db_session.bind)
