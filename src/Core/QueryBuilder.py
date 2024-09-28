import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
load_dotenv()

Base = declarative_base()


class QueryBuilder:
    def __init__(self):
        str_connection = os.getenv('STR_CONNECTION')
        self.engine = create_engine(str_connection)
        self.Session = sessionmaker(bind=self.engine)

    def start_query(self, model: Base):
        session = self.Session()
        return session.query(model)
    