import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv


class Database:
    def __init__(self):
        # Carregar variáveis de ambiente do arquivo .env
        load_dotenv()

        # URL de conexão com o banco de dados
        self.DATABASE_URL = os.getenv("STR_CONNECTION")

        # Cria o engine do SQLAlchemy
        self.engine = create_engine(self.DATABASE_URL, echo=True)

        # Cria a fábrica de sessões
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        # Base para os modelos ORM
        self.Base = declarative_base()

    def get_db(self) -> Session:
        """Retorna uma sessão de banco de dados."""
        db = self.SessionLocal()
        return db
