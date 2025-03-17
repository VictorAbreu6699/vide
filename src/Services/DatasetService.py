import os
import uuid

import pandas as pd
from fastapi import UploadFile

from src.Helpers.JWTHelper import JWTHelper
from src.Models.DatasetColumn import DatasetColumn
from src.Repositories.BaseRepository import BaseRepository
from src.Repositories.DatasetRepository import DatasetRepository


class DatasetService:

    @staticmethod
    async def upload_file(name: str, description: str, file: UploadFile, token: str):
        # Cria a pasta storage/datasets, caso não exista.
        if not os.path.exists("storage/datasets"):
            os.makedirs("storage/datasets")
        # Salva o arquivo na pasta storage
        _, extension = os.path.splitext(file.filename)
        file_path = os.path.join("storage/datasets", uuid.uuid4().__str__() + extension)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        user = JWTHelper.get_user_from_token(token)

        dataset_columns = DatasetService.get_dataset_columns(file_path, extension)

        if not dataset_columns:
            raise RuntimeError("Nenhuma coluna foi encontrada no arquivo!")
        elif not DatasetService.check_dataset_is_valid(dataset_columns):
            raise RuntimeError("O arquivo deve possuir pelo menos duas colunas nomeadas!")

        dataset = DatasetRepository().create({
            "name": name, "description": description, "extension": extension, "path": file_path, "user_id": user.id
        })

        dataset_columns_to_insert = [{**dataset_column, "dataset_id": dataset.id} for dataset_column in dataset_columns]

        BaseRepository().bulk_insert(DatasetColumn, dataset_columns_to_insert)

    @staticmethod
    def get_dataset_columns(file_path: str, file_extension: str) -> list[dict]:
        df_dataset = DatasetService.read_dataset_file(file_path, file_extension)
        dataset_columns = DatasetService.get_column_types(df_dataset)

        return dataset_columns

    @staticmethod
    def get_column_types(df_dataset: pd.DataFrame) -> list[dict]:
        def map_data_type(series):
            if pd.api.types.is_numeric_dtype(series):
                return "number"
            elif pd.api.types.is_datetime64_any_dtype(series):
                return "date"
            else:
                return "string"

        columns_info = []

        for i, col in enumerate(df_dataset.columns):
            has_column_name = True if "Unnamed" not in col else False

            columns_info.append({
                "name": f"coluna {i}" if not has_column_name else col, "type": map_data_type(df_dataset[col]),
                "order": i, "has_column_name": has_column_name
            })

        return columns_info

    @staticmethod
    def check_dataset_is_valid(dataset_columns: list[dict]) -> True:
        len_has_column_name = sum(1 for col in dataset_columns if col["has_column_name"])
        print(len_has_column_name)
        if len_has_column_name < 2:
            return False

        return True

    @staticmethod
    def read_dataset_file(file_path: str, file_extension: str):
        match file_extension:
            case ".xlsx" | ".xls":
                df_dataset = pd.read_excel(file_path)
            case ".csv":
                df_dataset = pd.read_csv(file_path)
            case ".json":
                df_dataset = pd.read_json(file_path)
            case _:
                raise ValueError(f"Unsupported file format: {file_extension}")

        return df_dataset
