import pandas as pd

from src.Repositories.FieldRepository import FieldRepository
from src.Repositories.VisualizationFieldRepository import VisualizationFieldRepository
from src.Repositories.VisualizationRepository import VisualizationRepository


class VisualizationSeeder:
    """
    Seeder para preencher visualizações que um relatorio pode ter. Sempre que ouver a necessidade de um novo campo ele será
    adicionado aqui.
    """

    @staticmethod
    def run():
        data = [
            {
                "name": "Grafico de linhas com número diário de casos por cidade e estado",
                "fields": [
                    "Data", "Casos", "Estado", "Cidade"
                ]
            }
        ]
        visualization_repository = VisualizationRepository()
        df_new_visualizations = pd.DataFrame(data)
        df_fields = FieldRepository().get_all()
        for index, row in df_new_visualizations.iterrows():
            visualization = visualization_repository.get_by_name(row['name'])
            visualization_fields = row['fields']
            if not visualization:
                visualization = visualization_repository.create({"name": row['name']})

            df_visualization_fields = visualization_repository.get_visualization_fields(visualization.id)
            if not df_visualization_fields.empty:
                visualization_fields = list(set(row['fields']) - set(df_visualization_fields['name'].tolist()))

            if visualization_fields:
                visualization_fields_to_create = []
                for field in visualization_fields:
                    visualization_fields_to_create.append({
                        "visualization_id": visualization.id,
                        "field_id": df_fields.loc[df_fields['name'] == field, "id"].iloc[0]
                    })
                VisualizationFieldRepository().bulk_save_objects(visualization_fields_to_create)


if __name__ == "__main__":
    VisualizationSeeder.run()
