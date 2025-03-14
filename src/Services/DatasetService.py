import os
import uuid

from fastapi import UploadFile

from src.Helpers.JWTHelper import JWTHelper
from src.Repositories.DatasetRepository import DatasetRepository


class DatasetService:

    @staticmethod
    def upload_file(name: str, description: str, file: UploadFile, token: str):
        # Cria a pasta storage/datasets, caso não exista.
        if not os.path.exists("storage/datasets"):
            os.makedirs("storage/datasets")
        # Salva o arquivo na pasta storage
        _, extension = os.path.splitext(file.filename)
        file_path = os.path.join("storage/datasets", uuid.uuid4().__str__() + extension)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        user = JWTHelper.get_user_from_token(token)

        DatasetRepository().create({
            "name": name, "description": description, "extension": extension, "path": file_path, "user_id": user.id
        })
