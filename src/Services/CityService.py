import json
import os

import pandas as pd

from src.Helpers.DataframeHelper import DataframeHelper
from src.Repositories.CityRepository import CityRepository


class CityService:
    @staticmethod
    def get_or_create_parquet_to_cities(to_merge=False) -> pd.DataFrame:
        if not os.path.exists("storage/cities/parquets"):
            os.makedirs("storage/cities/parquets")

        file_path = os.path.join("storage/cities/parquets", "cities.parquet")

        if os.path.exists(file_path):
            df = pd.read_parquet(file_path, engine="fastparquet")
        else:
            df = CityRepository().get_all()
            if to_merge:
                df['city_name_to_merge'] = df['name'].map(DataframeHelper.remove_accents_and_capitalize)
                df['state_name_to_merge'] = df['state_name'].map(DataframeHelper.remove_accents_and_capitalize)

            df.to_parquet(file_path)

        return df
