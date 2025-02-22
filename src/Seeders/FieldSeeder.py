import pandas as pd

from src.Enums.FieldTypeEnum import FieldTypeEnum
from src.Repositories.FieldRepository import FieldRepository


class FieldSeeder:
    """
    Seeder para preencher campos que uma visualização de relatorio pode ter. Sempre que ouver a necessidade de um novo campo ele será
    adicionado aqui.
    """

    @staticmethod
    def run():
        data = [
            {"name": "Data", "type": FieldTypeEnum.DATE.value},
            {"name": "Casos", "type": FieldTypeEnum.NUMBER.value},
            {"name": "Estado", "type": FieldTypeEnum.STRING.value},
            {"name": "Cidade", "type": FieldTypeEnum.STRING.value},
            {"name": "Doença", "type": FieldTypeEnum.STRING.value},
            {"name": "Tipo de Doença", "type": FieldTypeEnum.STRING.value},
            {"name": "Tipo de Variante", "type": FieldTypeEnum.STRING.value},
        ]
        field_repository = FieldRepository()
        df_new_fields = pd.DataFrame(data)
        df_all_fields = field_repository.get_all().drop(columns=['id'])

        df_new_fields = df_new_fields.merge(
            df_all_fields,
            how="left",
            on=["name", "type"],
            indicator=True
        )

        df_to_insert = df_new_fields[df_new_fields['_merge'] == "left_only"].drop(columns=['_merge'])

        field_repository.bulk_save_objects(df_to_insert.to_dict(orient="records"))


if __name__ == "__main__":
    FieldSeeder.run()
