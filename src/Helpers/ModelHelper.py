from datetime import datetime

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ModelHelper:
    @staticmethod
    def model_to_dict(model: Base):
        model_as_dict = {column.name: getattr(model, column.name) for column in model.__table__.columns}

        for key in model_as_dict.keys():
            column = model_as_dict[key]
            if isinstance(column, datetime):
                model_as_dict[key] = column.strftime('%Y-%m-%d %H:%M:%S')

        return model_as_dict
