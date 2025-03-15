from src.Database.Database import Database


class BaseRepository:
    def __init__(self):
        self.db_session = Database().get_db()

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
