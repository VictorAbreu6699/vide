from typing import Optional, Type

import pandas as pd

from src.Database.Database import Database
from src.Helpers.CryptHelper import CryptHelper
from src.Models.User import User


class UserRepository:
    def __init__(self):
        self.db_session = Database().get_db()

    def create(self, data: dict) -> User:
        """Cria um novo usuário no banco de dados."""
        db_user = User(**data)
        password = CryptHelper().encrypt(data["password"])
        db_user.password = password
        db_user.is_active = True
        self.db_session.add(db_user)
        self.db_session.commit()
        self.db_session.refresh(db_user)
        return db_user

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Retorna um usuário pelo ID."""
        return self.db_session.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Retorna um usuário pelo email."""
        return self.db_session.query(User).filter(User.email == email).first()

    def get_all(self) -> pd.DataFrame:
        query = self.db_session.query(User)

        return pd.read_sql(query.statement, self.db_session.bind)

    def update(self, user_id: int, data: dict) -> Optional[User]:
        db_user = self.get_by_id(user_id)
        if db_user:
            for key, value in data.items():
                if key == "password":
                    value = CryptHelper().encrypt(value)
                setattr(db_user, key, value)
            self.db_session.commit()
            self.db_session.refresh(db_user)
        return db_user

    def delete(self, user_id: int) -> Optional[User]:
        """Remove um usuário pelo ID."""
        db_user = self.get_by_id(user_id)
        if db_user:
            self.db_session.delete(db_user)
            self.db_session.commit()
        return db_user
