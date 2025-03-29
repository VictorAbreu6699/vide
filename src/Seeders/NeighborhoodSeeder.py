import pandas as pd
from src.Repositories.CityRepository import CityRepository
from src.Repositories.NeighborhoodRepository import NeighborhoodRepository
from src.Repositories.StateRepository import StateRepository


class NeighborhoodSeeder:
    """
    Seeder para preencher bairros brasileiros
    """

    @staticmethod
    def run():
        df_new_neighborhoods = pd.read_json("bairros_brasil.json")
        # 'state', 'city', 'neighborhood', 'longitude', 'latitude'
        df_new_neighborhoods.rename(
            columns={"city": "city_name", "state": "state_name", "neighborhood": "neighborhood_name"},
            inplace=True
        )

        df_all_states = StateRepository().get_all().drop(columns=["latitude", "longitude"]).rename(
            columns={"id": "state_id", "name": "state_name"}
        )

        df_new_neighborhoods = df_new_neighborhoods.merge(
            df_all_states,
            how="left",
            on=["state_name"]
        ).drop(columns=["state_name"])

        city_repository = CityRepository()
        df_all_cities = city_repository.get_all().drop(columns=['state_name', "latitude", "longitude"]).rename(
            columns={"id": "city_id", "name": "city_name"}
        )

        df_new_neighborhoods = df_new_neighborhoods.merge(
            df_all_cities,
            how="left",
            on=['state_id', 'city_name']
        ).drop(columns=["city_name", "state_id"])

        df_all_neighborhoods = NeighborhoodRepository().get_all().drop(columns=['id']).rename(
            columns={"name": "neighborhood_name"}
        )

        df_new_neighborhoods = df_new_neighborhoods.merge(
            df_all_neighborhoods,
            how="left",
            on=['city_id', 'neighborhood_name', "latitude", "longitude"],
            indicator=True
        )

        df_to_insert = df_new_neighborhoods[df_new_neighborhoods['_merge'] == "left_only"].drop(columns=['_merge'])
        df_to_insert = df_to_insert[['neighborhood_name', 'longitude', 'latitude', 'city_id']].rename(
            columns={"neighborhood_name": "name"}
        )
        if not df_new_neighborhoods.empty:
            NeighborhoodRepository().bulk_save_objects(df_to_insert.to_dict(orient="records"))


if __name__ == "__main__":
    NeighborhoodSeeder.run()
