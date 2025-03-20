from sqlalchemy.exc import SQLAlchemyError

from src.Database.Database import Database


class BaseRepository:
    def __init__(self):
        self.db_session = Database().get_db()

    def create(self, model, data: dict):
        """Cria um novo campo no banco de dados."""
        item = model(**data)
        self.db_session.add(item)
        self.db_session.commit()
        self.db_session.refresh(item)
        return item

    def bulk_insert(self, model, data: list[dict]):
        """
        Insere múltiplos registros em uma tabela usando SQLAlchemy.

        :param model: Modelo SQLAlchemy (Classe ORM)
        :param data: Lista de dicionários representando os dados
        """
        try:
            self.db_session.bulk_insert_mappings(model, data)
            self.db_session.commit()
            print("Insert realizado com sucesso!")
        except Exception as e:
            self.db_session.rollback()
            print(f"Erro ao inserir: {e}")

    def delete_record(self, model, **filters):
        """
        Função genérica para deletar registros do banco de dados.

        :param model: Classe do modelo SQLAlchemy.
        :param filters: Filtros de busca para o registro a ser deletado.
        :return: True se a exclusão for bem-sucedida, False caso contrário.
        """
        try:
            query = self.db_session.query(model).filter_by(**filters)
            if query.first() is not None:
                query.delete()
                self.db_session.commit()
                return True
            else:
                print("Registro(s) não encontrado(s).")
                return False
        except SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Erro ao tentar deletar o registro: {e}")
            return False
