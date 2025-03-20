from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy.engine.row import Row
from sqlalchemy.orm import DeclarativeMeta

Base = declarative_base()


class ModelHelper:

    @staticmethod
    def model_to_dict(model):
        if isinstance(model, Row):
            model_as_dict = dict(model._mapping)  # Acessa os dados do Row como um dicionário
        elif isinstance(model.__class__, DeclarativeMeta):  # Verifica se é um modelo SQLAlchemy
            model_as_dict = {column.name: getattr(model, column.name) for column in model.__table__.columns}
        else:
            raise ValueError("O objeto fornecido não é um modelo SQLAlchemy válido nem um Row.")

        for key, value in model_as_dict.items():
            if isinstance(value, datetime):
                model_as_dict[key] = value.strftime('%Y-%m-%d %H:%M:%S')

        return model_as_dict
