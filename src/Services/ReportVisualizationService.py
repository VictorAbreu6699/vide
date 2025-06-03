import json

import numpy as np
import pandas as pd
from src.Helpers.DataframeHelper import DataframeHelper
from src.Models.Report import Report
from src.Models.ReportVisualization import ReportVisualization
from src.Models.ReportVisualizationDatasetColumn import ReportVisualizationDatasetColumn
from src.Repositories.BaseRepository import BaseRepository
from src.Repositories.CityRepository import CityRepository
from src.Repositories.ReportRepository import ReportRepository
from src.Repositories.ReportVisualizationDatasetColumnRepository import ReportVisualizationDatasetColumnRepository
from src.Repositories.ReportVisualizationRepository import ReportVisualizationRepository
from src.Repositories.VisualizationFieldRepository import VisualizationFieldRepository
from src.Requests.CreateReportVisualizationDatasetColumnRequest import CreateReportVisualizationDatasetColumnRequest
from src.Requests.UpdateReportVisualizationDatasetColumnRequest import UpdateReportVisualizationDatasetColumnRequest
from src.Services.CityService import CityService
from src.Services.DatasetService import DatasetService


class ReportVisualizationService:

    @staticmethod
    def store_report_visualization(request: CreateReportVisualizationDatasetColumnRequest):
        report = ReportRepository().get_by_id(request.report_id)

        report_visualization = {
            "name": request.name if request.name is not None else "",
            "visualization_id": request.visualization_id,
            "report_id": report.id
        }

        report_visualization = BaseRepository().create(ReportVisualization, report_visualization)
        df_visualization_fields = VisualizationFieldRepository().get_all(
            field_id=request.field_id, visualization_id=[request.visualization_id]
        )

        list_report_visualization_dataset_column = []
        for i, field_id in enumerate(request.field_id):
            visualization_field_id = df_visualization_fields.loc[
                (df_visualization_fields['field_id'] == field_id) &
                (df_visualization_fields['visualization_id'] == request.visualization_id),
                "id"
            ].iloc[0]
            report_visualization_dataset_column = {
                "report_visualization_id": report_visualization.id,
                "visualization_field_id": visualization_field_id,
                "dataset_id": report.dataset_id,
                "dataset_column_id": request.field_value[i]
            }

            list_report_visualization_dataset_column.append(report_visualization_dataset_column)

        BaseRepository().bulk_insert(ReportVisualizationDatasetColumn, list_report_visualization_dataset_column)

    @staticmethod
    def edit_report_visualization(report_visualization_id: int, request: UpdateReportVisualizationDatasetColumnRequest):
        """
        Deleta e cria de novo o vinculo com as colunas
        :param report_visualization_id: int
        :param request: UpdateReportVisualizationDatasetColumnRequest
        """
        BaseRepository().delete_record(
            ReportVisualizationDatasetColumn,
            report_visualization_id=report_visualization_id
        )

        report = ReportRepository().get_by_id(request.report_id)

        report_visualization_dict = {
            "name": request.name if request.name is not None else "",
            "visualization_id": request.visualization_id
        }

        report_visualization = ReportVisualizationRepository().update(
            report_visualization_id, report_visualization_dict
        )
        df_visualization_fields = VisualizationFieldRepository().get_all(
            field_id=request.field_id, visualization_id=[request.visualization_id]
        )

        list_report_visualization_dataset_column = []
        for i, field_id in enumerate(request.field_id):
            visualization_field_id = df_visualization_fields.loc[
                (df_visualization_fields['field_id'] == field_id) &
                (df_visualization_fields['visualization_id'] == request.visualization_id),
                "id"
            ].iloc[0]
            report_visualization_dataset_column = {
                "report_visualization_id": report_visualization.id,
                "visualization_field_id": visualization_field_id,
                "dataset_id": report.dataset_id,
                "dataset_column_id": request.field_value[i]
            }

            list_report_visualization_dataset_column.append(report_visualization_dataset_column)

        BaseRepository().bulk_insert(ReportVisualizationDatasetColumn, list_report_visualization_dataset_column)

    @staticmethod
    def delete_report(report_id: int):
        df_report_visualizations = ReportVisualizationRepository().get_by_report_id(report_id)
        for report_visualization_id in df_report_visualizations['id'].tolist():
            BaseRepository().delete_record(
                ReportVisualizationDatasetColumn,
                report_visualization_id=report_visualization_id
            )
        BaseRepository().delete_record(ReportVisualization, report_id=report_id)
        BaseRepository().delete_record(Report, id=report_id)

    @staticmethod
    def delete_report_visualization(report_visualization_id: int):
        BaseRepository().delete_record(
            ReportVisualizationDatasetColumn,
            report_visualization_id=report_visualization_id
        )
        BaseRepository().delete_record(ReportVisualization, id=report_visualization_id)

    @staticmethod
    def get_report_visualizations_to_build_report(
        report_id: int,
        year: str = None,
        sickness: str = None,
        state_id: int = None,
        city_id: int = None
    ) -> pd.DataFrame:

        df_report_visualizations = ReportVisualizationRepository().get_report_visualizations_to_build_report(report_id)
        df_report_visualizations['report_visualization_dataset_columns'] = None

        for index, row in df_report_visualizations.iterrows():
            df_report_visualization_dataset_columns = ReportVisualizationDatasetColumnRepository(). \
                get_by_report_visualizations_id(row["id"])
            df_report_visualizations.at[
                index, 'report_visualization_dataset_columns'] = df_report_visualization_dataset_columns.to_dict(
                orient="records"
            )

        df_report_visualizations = ReportVisualizationService.__get_column_values_from_dataset(
            df_report_visualizations, report_id, year, sickness, state_id, city_id
        )

        return df_report_visualizations

    @staticmethod
    def __get_column_values_from_dataset(
        df_report_visualizations: pd.DataFrame,
        report_id: int,
        year: str = None,
        sickness: str = None,
        state_id: int = None,
        city_id: int = None
    ):
        df_dataset = DatasetService.get_dataset_by_report_id(report_id)

        df_report_visualizations = ReportVisualizationService.__create_visualization_schemas(
            df_report_visualizations, df_dataset, year, sickness, state_id, city_id
        )

        return df_report_visualizations

    @staticmethod
    def __create_visualization_schemas(
        df_report_visualizations, df_dataset: pd.DataFrame,
        year: str = None,
        sickness: str = None,
        state_id: int = None,
        city_id: int = None
    ) -> pd.DataFrame:
        df_cities = CityService.get_or_create_parquet_to_cities(to_merge=True).rename(columns={"name": "city_name"})
        df_report_visualizations["filters"] = None
        df_report_visualizations["data"] = None

        data_to_polar_graph = None
        for index, row in df_report_visualizations.iterrows():
            df_report_visualization_dataset_columns = pd.DataFrame(row.get("report_visualization_dataset_columns"))
            match row.get("visualization_name"):
                case "Mapa Coroplético":
                    df_report_visualizations.at[index, "filters"] = ReportVisualizationService.__build_filters_choropleth_map(
                        df_report_visualization_dataset_columns, df_dataset
                    )
                    df_report_visualizations.at[index, "data"] = ReportVisualizationService.__build_choropleth_map(
                        df_report_visualization_dataset_columns,
                        df_dataset,
                        df_cities,
                        year,
                        sickness,
                        state_id,
                        city_id
                    ).to_dict(orient="records")

                case "Gráfico polar por Enfermidade":
                    if data_to_polar_graph is None:
                        data_to_polar_graph = ReportVisualizationService.get_data_to_polar_graph(
                            df_report_visualization_dataset_columns,
                            df_dataset,
                            df_cities,
                            year,
                            sickness,
                            state_id,
                            city_id
                        )

                    df_report_visualizations.at[index, "data"] = ReportVisualizationService.__build_polar_graph_for_sickness(
                        data_to_polar_graph
                    ).to_dict(orient="records")

                case "Gráfico polar por Cidade":
                    if data_to_polar_graph is None:
                        data_to_polar_graph = ReportVisualizationService.get_data_to_polar_graph(
                            df_report_visualization_dataset_columns,
                            df_dataset,
                            df_cities,
                            year,
                            sickness,
                            state_id,
                            city_id
                        )

                    df_report_visualizations.at[index, "data"] = ReportVisualizationService.__build_polar_graph_for_city(
                        data_to_polar_graph
                    ).to_dict(orient="records")

                case "Gráfico polar por Estado":
                    if data_to_polar_graph is None:
                        data_to_polar_graph = ReportVisualizationService.get_data_to_polar_graph(
                            df_report_visualization_dataset_columns,
                            df_dataset,
                            df_cities,
                            year,
                            sickness,
                            state_id,
                            city_id
                        )

                    df_report_visualizations.at[
                        index, "data"] = ReportVisualizationService.__build_polar_graph_for_state(
                        data_to_polar_graph
                    ).to_dict(orient="records")

        df_report_visualizations.drop(columns=["report_visualization_dataset_columns"], inplace=True)

        return df_report_visualizations

    @staticmethod
    def __build_choropleth_map(
        df_report_visualization_dataset_columns: pd.DataFrame,
        df_dataset: pd.DataFrame,
        df_cities: pd.DataFrame,
        year: str = None,
        sickness: str = None,
        state_id: int = None,
        city_id: int = None
    ) -> pd.DataFrame:
        df_cities = df_cities.copy()[[
            "id", "state_id", "state_name", "city_name", "latitude", "longitude", "geo_json", "city_name_to_merge",
            "state_name_to_merge"
        ]].rename(
            columns={"id": "city_id"}
        )

        list_of_columns = []
        for index, column in df_report_visualization_dataset_columns.iterrows():
            dataset_column = df_dataset[column['dataset_column_name']]
            if column['dataset_column_type'] == "date":
                dataset_column = dataset_column.dt.strftime("%Y-%m-%d")

            list_of_columns.append({
                "field_name": column.get("field_name"),
                "field_data": dataset_column.tolist()
            })

        df_data = pd.DataFrame(data={item.get("field_name"): item.get("field_data") for item in list_of_columns})
        df_data.rename(columns={
            "Data": "date", "Estado": "state_name", "Cidade": "city_name", "Doença": "sickness",
            "Indicador Numérico": "cases"
        }, inplace=True)
        df_data = df_data[df_data['city_name'].notnull()]
        df_data = df_data[df_data['state_name'].notnull()]
        df_data['city_name_to_merge'] = df_data['city_name'].map(DataframeHelper.remove_accents_and_capitalize)
        df_data['state_name_to_merge'] = df_data['state_name'].map(DataframeHelper.remove_accents_and_capitalize)

        # Obtem latitude, longitude e o geoJson:
        df_data = df_data.merge(
            df_cities,
            how="left",
            on=["state_name_to_merge", "city_name_to_merge"]
        ).replace(np.nan, None)

        df_data["state_name"] = np.where(
            df_data["state_name_y"].notnull(),
            df_data["state_name_y"],
            df_data["state_name_x"]
        )

        df_data["city_name"] = np.where(
            df_data["city_name_y"].notnull(),
            df_data["city_name_y"],
            df_data["city_name_x"]
        )

        if state_id is not None:
            df_data = df_data[df_data['state_id'] == state_id]

        if city_id is not None:
            df_data = df_data[df_data['city_id'] == city_id]

        if sickness is not None:
            df_data = df_data[df_data['sickness'] == sickness]

        if year is not None:
            df_data['date_parsed'] = pd.to_datetime(df_data['date'])
            df_data = df_data[df_data['date_parsed'].dt.year == int(year)]
            df_data.drop(inplace=True, columns=["date_parsed"])

        df_data.drop(inplace=True, columns=[
            "state_name_to_merge", "city_name_to_merge", "state_name_y", "state_name_x", "city_name_y", "city_name_x"
        ])

        df_data = ReportVisualizationService.group_data_by_year(df_data)

        return df_data

    @staticmethod
    def group_data_by_year(df: pd.DataFrame) -> pd.DataFrame:
        # Converte a coluna de data para datetime
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # Extrai o ano
        df['year'] = df['date'].dt.year

        # Agrupamento pelos mesmos campos da chave usada no JS
        grouped = df.groupby([
            'sickness',
            'state_id',
            'state_name',
            'city_id',
            'city_name',
            'latitude',
            'longitude',
            'geo_json',
            'year'
        ]).agg(total_cases=('cases', 'sum')).reset_index()

        grouped = grouped[grouped['total_cases'].notnull()]

        return grouped

    @staticmethod
    def get_data_to_polar_graph(
        df_report_visualization_dataset_columns: pd.DataFrame,
        df_dataset: pd.DataFrame,
        df_cities: pd.DataFrame,
        year: str = None,
        sickness: str = None,
        state_id: int = None,
        city_id: int = None
    ):
        df_cities = df_cities.copy()[[
            "id", "state_id", "state_name", "city_name", "latitude", "longitude", "geo_json", "city_name_to_merge",
            "state_name_to_merge"
        ]].rename(
            columns={"id": "city_id"}
        )

        list_of_columns = []
        for index, column in df_report_visualization_dataset_columns.iterrows():
            dataset_column = df_dataset[column['dataset_column_name']]
            if column['dataset_column_type'] == "date":
                dataset_column = dataset_column.dt.strftime("%Y-%m-%d")

            list_of_columns.append({
                "field_name": column.get("field_name"),
                "field_data": dataset_column.tolist()
            })

        df_data = pd.DataFrame(data={item.get("field_name"): item.get("field_data") for item in list_of_columns})
        df_data.rename(columns={
            "Data": "date", "Estado": "state_name", "Cidade": "city_name", "Doença": "sickness",
            "Indicador Numérico": "cases"
        }, inplace=True)

        df_data['city_name_to_merge'] = df_data['city_name'].map(DataframeHelper.remove_accents_and_capitalize)
        df_data['state_name_to_merge'] = df_data['state_name'].map(DataframeHelper.remove_accents_and_capitalize)

        # Obtem latitude, longitude e o geoJson:
        df_data = df_data.merge(
            df_cities,
            how="left",
            on=["state_name_to_merge", "city_name_to_merge"]
        ).replace(np.nan, None)

        df_data["state_name"] = np.where(
            df_data["state_name_y"].notnull(),
            df_data["state_name_y"],
            df_data["state_name_x"]
        )

        df_data["city_name"] = np.where(
            df_data["city_name_y"].notnull(),
            df_data["city_name_y"],
            df_data["city_name_x"]
        )

        if state_id is not None:
            df_data = df_data[df_data['state_id'] == state_id]

        if city_id is not None:
            df_data = df_data[df_data['city_id'] == city_id]

        if sickness is not None:
            df_data = df_data[df_data['sickness'] == sickness]

        if year is not None:
            df_data['date_parsed'] = pd.to_datetime(df_data['date'])
            df_data = df_data[df_data['date_parsed'].dt.year == int(year)]
            df_data.drop(inplace=True, columns=["date_parsed"])

        df_data.drop(inplace=True, columns=[
            "state_name_to_merge", "city_name_to_merge", "state_name_y", "state_name_x", "city_name_y", "city_name_x"
        ])

        return df_data


    @staticmethod
    def __build_polar_graph_for_sickness(dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe = dataframe.groupby("sickness")['cases'].mean().reset_index()

        return dataframe

    @staticmethod
    def __build_polar_graph_for_state(dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe = dataframe.groupby("state_name")['cases'].mean().reset_index()

        return dataframe

    @staticmethod
    def __build_polar_graph_for_city(dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe = dataframe.groupby("city_name")['cases'].mean().reset_index()

        return dataframe

    @staticmethod
    def __build_filters_choropleth_map(df_report_visualization_dataset_columns: pd.DataFrame, df_dataset: pd.DataFrame) -> dict:
        list_of_columns = []
        for index, column in df_report_visualization_dataset_columns.iterrows():
            dataset_column = df_dataset[column['dataset_column_name']]
            if column['dataset_column_name'] == "date" or column['dataset_column_type'] == "date":
                dataset_column = pd.to_datetime(dataset_column)

            list_of_columns.append({
                "field_name": column.get("field_name"),
                "field_data": dataset_column.tolist()
            })

        df_data = pd.DataFrame(data={item.get("field_name"): item.get("field_data") for item in list_of_columns})
        df_data.rename(columns={
            "Data": "date", "Estado": "state_name", "Cidade": "city_name", "Doença": "sickness",
            "Indicador Numérico": "cases"
        }, inplace=True)

        filters = {
            'years': sorted(df_data['date'].dt.year.unique().tolist()),
            'sicknesses': sorted(df_data['sickness'].unique().tolist())
        }

        return filters


