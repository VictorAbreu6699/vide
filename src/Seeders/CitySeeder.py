import pandas as pd
from src.Repositories.CityRepository import CityRepository
from src.Repositories.StateRepository import StateRepository


class CitySeeder:
    """
    Seeder para preencher cidades brasileiras
    """

    @staticmethod
    def run():
        df_new_cities = pd.read_json("cidades_brasil.json")
        df_new_cities.rename(columns={"city": "name", "state": "state_name"}, inplace=True)

        city_repository = CityRepository()
        df_all_cities = city_repository.get_all().drop(columns=['id', 'state_name'])
        df_all_states = StateRepository().get_all().drop(columns=["latitude", "longitude"]).rename(
            columns={"id": "state_id", "name": "state_name"}
        )

        df_new_cities = df_new_cities.merge(
            df_all_states,
            how="left",
            on=["state_name"]
        )

        df_new_cities = df_new_cities.merge(
            df_all_cities,
            how="left",
            on=['state_id', 'name', "latitude", "longitude"],
            indicator=True
        )

        df_to_insert = df_new_cities[df_new_cities['_merge'] == "left_only"].drop(columns=['_merge'])
        df_to_insert = df_to_insert[['name', 'longitude', 'latitude', 'state_id']]
        if not df_to_insert.empty:
            city_repository.bulk_save_objects(df_to_insert.to_dict(orient="records"))


if __name__ == "__main__":
    CitySeeder.run()
