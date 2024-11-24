from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ModelHelper:
    @staticmethod
    def model_to_dict(model: Base):
        return {column.name: getattr(model, column.name) for column in model.__table__.columns}
