import pandas as pd
from typing import Optional

from src.Database.Database import Database
from src.Models.RevokedToken import RevokedToken


class RevokedTokenRepository:
    def __init__(self):
        self.db_session = Database().get_db()

    def create(self, data: dict) -> RevokedToken:
        """Cria um novo revoked_token no banco de dados."""
        revoked_token = RevokedToken(**data)
        self.db_session.add(revoked_token)
        self.db_session.commit()
        self.db_session.refresh(revoked_token)
        return revoked_token

    def get_by_id(self, revoked_token_id: int) -> Optional[RevokedToken]:
        """Retorna um revoked_token pelo ID."""
        return self.db_session.query(RevokedToken).filter(RevokedToken.id == revoked_token_id).first()

    def get_by_token(self, token: str) -> Optional[RevokedToken]:
        """Retorna um revoked_token pelo Token."""
        return self.db_session.query(RevokedToken).filter(RevokedToken.token == token).first()

    def get_all(self, token: list[str] = None) -> pd.DataFrame:
        query = self.db_session.query(RevokedToken)

        if token:
            query = query.filter(
                RevokedToken.token.in_(token)
            )

        query = query.limit(30)

        return pd.read_sql(query.statement, self.db_session.bind)

    def update(self, revoked_token_id: int, data: dict) -> Optional[RevokedToken]:
        revoked_token = self.get_by_id(revoked_token_id)
        if revoked_token:
            for key, value in data.items():
                setattr(revoked_token, key, value)
            self.db_session.commit()
            self.db_session.refresh(revoked_token)
        return revoked_token
