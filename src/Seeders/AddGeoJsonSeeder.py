import json
import os

import pandas as pd

from src.Helpers.DataframeHelper import DataframeHelper
from src.Repositories.CityRepository import CityRepository
from src.Repositories.StateRepository import StateRepository


class AddGeoJsonSeeder:
    """
    Seeder para preencher geoJson dos estados e cidades brasileiras
    """

    @staticmethod
    def run():
        state_repository = StateRepository()
        city_repository = CityRepository()
        df_all_states = state_repository.get_all().drop(columns=['geo_json'])
        df_all_cities = city_repository.get_all()
        df_all_states['formated_name'] = df_all_states['name'].map(DataframeHelper.remove_accents_and_lowercase)
        df_all_cities['formated_name'] = df_all_cities['name'].map(DataframeHelper.remove_accents_and_lowercase)

        for index, row in df_all_states.iterrows():
            state_name = row['formated_name']
            file_path = os.path.join(os.path.dirname(__file__), 'GeoJsonBrasil', f'{state_name}.json')

            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    geojson_str = json.dumps(json.load(f))
                    df_all_states.at[index, "geo_json"] = geojson_str
            else:
                print(f"❌ Arquivo NÃO encontrado para {state_name} (esperado: {state_name}.json)")

        for index, row in df_all_states.iterrows():
            state_repository.update(row['id'], row.to_dict())


if __name__ == "__main__":
    AddGeoJsonSeeder.run()
