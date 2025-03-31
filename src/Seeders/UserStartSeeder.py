import pandas as pd

from src.Enums.FieldTypeEnum import FieldTypeEnum
from src.Repositories.FieldRepository import FieldRepository
from src.Repositories.UserRepository import UserRepository


class UserStartSeeder:
    """
    Seeder para criar um usuário padrão logo quando criada uma instancia do projeto.
    """

    @staticmethod
    def run():
        data = [
            {"name": "Admin", "email": "admin@vide.com.br", "password": "admin123"}
        ]
        user_repository = UserRepository()
        df_new_users = pd.DataFrame(data)
        df_all_users = user_repository.get_all().drop(columns=['id', 'password'])

        df_new_users = df_new_users.merge(
            df_all_users,
            how="left",
            on=["name", "email"],
            indicator=True
        )

        df_to_insert = df_new_users[df_new_users['_merge'] == "left_only"].drop(columns=['_merge'])
        for index, user in df_to_insert.iterrows():
            user_repository.create(user.to_dict())


if __name__ == "__main__":
    UserStartSeeder.run()
