from src.Seeders.AddGeoJsonSeeder import AddGeoJsonSeeder
from src.Seeders.CitySeeder import CitySeeder
from src.Seeders.FieldSeeder import FieldSeeder
from src.Seeders.NeighborhoodSeeder import NeighborhoodSeeder
from src.Seeders.StateSeeder import StateSeeder
from src.Seeders.UserStartSeeder import UserStartSeeder
from src.Seeders.VisualizationSeeder import VisualizationSeeder


class StartProjectSeeder:
    """Classe responsavel por iniciar todos os seeders necessarios para a aplicação funcionar."""

    @staticmethod
    def run():
        FieldSeeder.run()
        VisualizationSeeder.run()
        StateSeeder.run()
        CitySeeder.run()
        NeighborhoodSeeder.run()
        UserStartSeeder.run()
        AddGeoJsonSeeder.run()

        print("Seeders executados com sucesso!")


if __name__ == "__main__":
    StartProjectSeeder.run()
