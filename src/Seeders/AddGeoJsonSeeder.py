import json
import os
import geopandas as gpd
import numpy as np
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
        df_cities_final = pd.DataFrame()

        for index, row in df_all_states.iterrows():
            state_name = row['formated_name']
            file_path = os.path.join(os.path.dirname(__file__), 'GeoJsonBrasil', f'{state_name}.json')

            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    geojson_str = json.dumps(json.load(f))
                    df_all_states.at[index, "geo_json"] = geojson_str
                    df_cities_of_state = df_all_cities[df_all_cities['state_id'] == row['id']].copy()
                    gdf = gpd.read_file(filename=file_path)
                    gdf['formated_name'] = gdf['name'].map(DataframeHelper.remove_accents_and_lowercase)
                    for city_index, city_row in df_cities_of_state.iterrows():
                        city = gdf[gdf['formated_name'] == city_row['formated_name']].drop(columns=['formated_name'])

                        if not city.empty:
                            # Converte para GeoJSON no formato dict
                            city_geojson = json.loads(city.to_json())

                            # Se quiser apenas o primeiro (em caso de múltiplas features com o mesmo nome)
                            city_geojson = city_geojson["features"][0]
                            df_cities_of_state.at[city_index, "geo_json"] = json.dumps(city_geojson)

                    df_cities_final = pd.concat([df_cities_final, df_cities_of_state], ignore_index=True)

            else:
                print(f"❌ Arquivo NÃO encontrado para {state_name} (esperado: {state_name}.json)")

        for index, row in df_all_states.replace(np.nan, None).iterrows():
            state_repository.update(row['id'], row.to_dict())

        for index, row in df_cities_final.replace(np.nan, None).iterrows():
            city_repository.update(row['id'], row.to_dict())


if __name__ == "__main__":
    AddGeoJsonSeeder.run()
