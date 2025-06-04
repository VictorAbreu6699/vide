import json
import re

import numpy as np
import pandas as pd
import unicodedata

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
    # Pré-compilação das expressões regulares (mais rápido)
    RE_REMOVE_CHARS = re.compile(r"[^A-Za-z0-9\s-]")
    RE_NORMALIZE_SPACES = re.compile(r'[-\s]+')

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
        df_report_visualizations,
        df_dataset: pd.DataFrame,
        year: str = None,
        sickness: str = None,
        state_id: int = None,
        city_id: int = None
    ) -> pd.DataFrame:
        df_cities = CityService.get_or_create_parquet_to_cities(to_merge=True).rename(columns={"name": "city_name"})
        df_report_visualizations["filters"] = None
        df_report_visualizations["data"] = None

        data_to_graphs = None
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
                    if data_to_graphs is None:
                        data_to_graphs = ReportVisualizationService.get_data_to_graphs(
                            df_report_visualization_dataset_columns,
                            df_dataset,
                            df_cities,
                            year,
                            sickness,
                            state_id,
                            city_id
                        )

                    df_report_visualizations.at[index, "data"] = ReportVisualizationService.__build_polar_graph_for_sickness(
                        data_to_graphs
                    ).to_dict(orient="records")

                case "Gráfico polar por Estado":
                    if data_to_graphs is None:
                        data_to_graphs = ReportVisualizationService.get_data_to_graphs(
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
                        data_to_graphs
                    ).to_dict(orient="records")

                case "Histograma por Ano":
                    if data_to_graphs is None:
                        data_to_graphs = ReportVisualizationService.get_data_to_graphs(
                            df_report_visualization_dataset_columns,
                            df_dataset,
                            df_cities,
                            year,
                            sickness,
                            state_id,
                            city_id
                        )

                    df_report_visualizations.at[
                        index, "data"] = ReportVisualizationService.__build_histogram_graph_for_year(
                        data_to_graphs
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

        # Seleciona apenas as colunas necessárias do DataFrame original
        col_names = df_report_visualization_dataset_columns['dataset_column_name'].tolist()
        field_names = df_report_visualization_dataset_columns['field_name'].tolist()
        types = df_report_visualization_dataset_columns['dataset_column_type'].tolist()

        # Subset do DataFrame original com as colunas usadas
        df_data = df_dataset[col_names].copy()

        # Converte as colunas do tipo "date" para datetime
        for col_name, col_type in zip(col_names, types):
            if col_name == "date" or col_type == "date":
                df_data[col_name] = pd.to_datetime(df_data[col_name])

        # Renomeia as colunas com os field_names desejados
        df_data.columns = field_names
        df_data.rename(columns={
            "Data": "date", "Estado": "state_name", "Cidade": "city_name", "Doença": "sickness",
            "Indicador Numérico": "cases"
        }, inplace=True)
        df_data = df_data[df_data['city_name'].notnull()]
        df_data = df_data[df_data['state_name'].notnull()]

        def normalize_text(text: str) -> str:
            if not isinstance(text, str):
                return ""
            nfkd = unicodedata.normalize('NFKD', text)
            text = ''.join(c for c in nfkd if not unicodedata.combining(c))
            text = ReportVisualizationService.RE_REMOVE_CHARS.sub('', text)
            text = ReportVisualizationService.RE_NORMALIZE_SPACES.sub(' ', text)
            return text.upper().strip()

        # Cria dicionário de mapeamento apenas para valores únicos
        city_map = {val: normalize_text(val) for val in df_data['city_name'].unique()}
        state_map = {val: normalize_text(val) for val in df_data['state_name'].unique()}

        # Aplica usando map com dicionário — muito mais rápido
        df_data['city_name_to_merge'] = df_data['city_name'].map(city_map)
        df_data['state_name_to_merge'] = df_data['state_name'].map(state_map)

        # Obtem latitude, longitude e o geoJson:
        df_data = df_data.merge(
            df_cities,
            how="left",
            on=["state_name_to_merge", "city_name_to_merge"]
        )

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

        df_data = ReportVisualizationService.group_data_by_year(df_data.replace(np.nan, None))

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
    def get_data_to_graphs(
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

        # Seleciona apenas as colunas necessárias do DataFrame original
        col_names = df_report_visualization_dataset_columns['dataset_column_name'].tolist()
        field_names = df_report_visualization_dataset_columns['field_name'].tolist()
        types = df_report_visualization_dataset_columns['dataset_column_type'].tolist()

        # Subset do DataFrame original com as colunas usadas
        df_data = df_dataset[col_names].copy()

        # Converte as colunas do tipo "date" para datetime
        for col_name, col_type in zip(col_names, types):
            if col_name == "date" or col_type == "date":
                df_data[col_name] = pd.to_datetime(df_data[col_name])

        # Renomeia as colunas com os field_names desejados
        df_data.columns = field_names
        df_data.rename(columns={
            "Data": "date", "Estado": "state_name", "Cidade": "city_name", "Doença": "sickness",
            "Indicador Numérico": "cases"
        }, inplace=True)
        df_data = df_data[df_data['city_name'].notnull()]
        df_data = df_data[df_data['state_name'].notnull()]

        def normalize_text(text: str) -> str:
            if not isinstance(text, str):
                return ""
            nfkd = unicodedata.normalize('NFKD', text)
            text = ''.join(c for c in nfkd if not unicodedata.combining(c))
            text = ReportVisualizationService.RE_REMOVE_CHARS.sub('', text)
            text = ReportVisualizationService.RE_NORMALIZE_SPACES.sub(' ', text)
            return text.upper().strip()

        # Cria dicionário de mapeamento apenas para valores únicos
        city_map = {val: normalize_text(val) for val in df_data['city_name'].unique()}
        state_map = {val: normalize_text(val) for val in df_data['state_name'].unique()}

        # Aplica usando map com dicionário — muito mais rápido
        df_data['city_name_to_merge'] = df_data['city_name'].map(city_map)
        df_data['state_name_to_merge'] = df_data['state_name'].map(state_map)

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
        # Soma de casos por enfermidade
        dataframe = dataframe.groupby("sickness")['cases'].sum().reset_index()

        # Calcula a porcentagem em relação ao total
        total = dataframe['cases'].sum()
        dataframe['percentual'] = dataframe['cases'] / total * 100

        return dataframe

    @staticmethod
    def __build_polar_graph_for_state(dataframe: pd.DataFrame) -> pd.DataFrame:
        # Soma de casos por estado
        dataframe = dataframe.groupby("state_name")['cases'].sum().reset_index()

        # Calcula a porcentagem em relação ao total
        total = dataframe['cases'].sum()
        dataframe['percentual'] = dataframe['cases'] / total * 100

        return dataframe

    @staticmethod
    def __build_histogram_graph_for_year(dataframe: pd.DataFrame) -> pd.DataFrame:
        # Soma de casos por ano
        dataframe = ReportVisualizationService.group_data_by_year(dataframe)
        dataframe = dataframe.groupby(["year", "sickness"])['total_cases'].sum().reset_index()

        return dataframe

    @staticmethod
    def __build_filters_choropleth_map(df_report_visualization_dataset_columns: pd.DataFrame, df_dataset: pd.DataFrame) -> dict:
        # Seleciona apenas as colunas necessárias do DataFrame original
        col_names = df_report_visualization_dataset_columns['dataset_column_name'].tolist()
        field_names = df_report_visualization_dataset_columns['field_name'].tolist()
        types = df_report_visualization_dataset_columns['dataset_column_type'].tolist()

        # Subset do DataFrame original com as colunas usadas
        df_data = df_dataset[col_names].copy()

        # Converte as colunas do tipo "date" para datetime
        for col_name, col_type in zip(col_names, types):
            if col_name == "date" or col_type == "date":
                df_data[col_name] = pd.to_datetime(df_data[col_name])

        # Renomeia as colunas com os field_names desejados
        df_data.columns = field_names

        df_data.rename(columns={
            "Data": "date", "Estado": "state_name", "Cidade": "city_name", "Doença": "sickness",
            "Indicador Numérico": "cases"
        }, inplace=True)
        filters = {
            'years': sorted(df_data['date'].dt.year.unique().tolist()),
            'sicknesses': sorted(df_data['sickness'].unique().tolist())
        }

        return filters


