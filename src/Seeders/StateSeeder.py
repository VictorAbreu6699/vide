import pandas as pd
from src.Repositories.StateRepository import StateRepository


class StateSeeder:
    """
    Seeder para preencher estados brasileiros
    """

    @staticmethod
    def run():
        data = [
          {"name": "Acre", "latitude": -9.0238, "longitude": -70.8111},
          {"name": "Alagoas", "latitude": -9.5713, "longitude": -36.7820},
          {"name": "Amapá", "latitude": 0.9020, "longitude": -52.0030},
          {"name": "Amazonas", "latitude": -3.4168, "longitude": -65.8561},
          {"name": "Bahia", "latitude": -12.5797, "longitude": -41.7007},
          {"name": "Ceará", "latitude": -5.4984, "longitude": -39.3206},
          {"name": "Distrito Federal", "latitude": -15.8267, "longitude": -47.9218},
          {"name": "Espírito Santo", "latitude": -19.1834, "longitude": -40.3089},
          {"name": "Goiás", "latitude": -15.8270, "longitude": -49.8362},
          {"name": "Maranhão", "latitude": -4.9609, "longitude": -45.2744},
          {"name": "Mato Grosso", "latitude": -12.6819, "longitude": -56.9211},
          {"name": "Mato Grosso do Sul", "latitude": -20.7722, "longitude": -54.7852},
          {"name": "Minas Gerais", "latitude": -18.5122, "longitude": -44.5550},
          {"name": "Pará", "latitude": -3.4168, "longitude": -52.3445},
          {"name": "Paraíba", "latitude": -7.2399, "longitude": -36.7819},
          {"name": "Paraná", "latitude": -25.2521, "longitude": -52.0215},
          {"name": "Pernambuco", "latitude": -8.8137, "longitude": -36.9541},
          {"name": "Piauí", "latitude": -7.7183, "longitude": -42.7289},
          {"name": "Rio de Janeiro", "latitude": -22.9068, "longitude": -43.1729},
          {"name": "Rio Grande do Norte", "latitude": -5.4026, "longitude": -36.9541},
          {"name": "Rio Grande do Sul", "latitude": -30.0346, "longitude": -51.2177},
          {"name": "Rondônia", "latitude": -10.8291, "longitude": -63.3228},
          {"name": "Roraima", "latitude": 2.7376, "longitude": -62.0751},
          {"name": "Santa Catarina", "latitude": -27.2423, "longitude": -50.2189},
          {"name": "São Paulo", "latitude": -23.5505, "longitude": -46.6333},
          {"name": "Sergipe", "latitude": -10.5741, "longitude": -37.3857},
          {"name": "Tocantins", "latitude": -10.1753, "longitude": -48.2982}
        ]
        state_repository = StateRepository()
        df_new_states = pd.DataFrame(data)
        df_all_states = state_repository.get_all().drop(columns=['id'])

        df_new_states = df_new_states.merge(
            df_all_states,
            how="left",
            on=["name", "latitude", "longitude"],
            indicator=True
        )

        df_to_insert = df_new_states[df_new_states['_merge'] == "left_only"].drop(columns=['_merge'])

        state_repository.bulk_save_objects(df_to_insert.to_dict(orient="records"))


if __name__ == "__main__":
    StateSeeder.run()
