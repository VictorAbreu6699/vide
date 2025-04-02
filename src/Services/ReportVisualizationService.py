import pandas as pd

from src.Models.Report import Report
from src.Models.ReportVisualization import ReportVisualization
from src.Models.ReportVisualizationDatasetColumn import ReportVisualizationDatasetColumn
from src.Repositories.BaseRepository import BaseRepository
from src.Repositories.ReportRepository import ReportRepository
from src.Repositories.ReportVisualizationDatasetColumnRepository import ReportVisualizationDatasetColumnRepository
from src.Repositories.ReportVisualizationRepository import ReportVisualizationRepository
from src.Repositories.VisualizationFieldRepository import VisualizationFieldRepository
from src.Requests.CreateReportVisualizationDatasetColumnRequest import CreateReportVisualizationDatasetColumnRequest
from src.Requests.UpdateReportVisualizationDatasetColumnRequest import UpdateReportVisualizationDatasetColumnRequest
from src.Services.DatasetService import DatasetService
from src.VisualizationSchemas.ChoroplethMap import ChoroplethMap


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
    def get_report_visualizations_to_build_report(report_id: int) -> pd.DataFrame:

        df_report_visualizations = ReportVisualizationRepository().get_report_visualizations_to_build_report(report_id)
        df_report_visualizations['report_visualization_dataset_columns'] = None

        for index, row in df_report_visualizations.iterrows():
            df_report_visualization_dataset_columns = ReportVisualizationDatasetColumnRepository(). \
                get_by_report_visualizations_id(row["id"])
            df_report_visualizations.at[
                index, 'report_visualization_dataset_columns'] = df_report_visualization_dataset_columns.to_dict(
                orient="records"
            )

        ReportVisualizationService.__get_column_values_from_dataset(df_report_visualizations, report_id)

        return df_report_visualizations

    @staticmethod
    def __get_column_values_from_dataset(df_report_visualizations: pd.DataFrame, report_id: int):
        df_dataset = DatasetService.get_dataset_by_report_id(report_id)

        # for index, row in df_report_visualizations.iterrows():
        #     list_columns = list()
        #     for i, field in enumerate(row.get("report_visualization_dataset_columns")):
        #         dataset_column = df_dataset[field['dataset_column_name']]
        #         if field['dataset_column_type'] == "date":
        #             dataset_column = dataset_column.dt.strftime("%Y-%m-%d")
        #
        #         field["values"] = dataset_column.tolist()
        #
        #         list_columns.append(field)
        #     df_report_visualizations.at[index, 'report_visualization_dataset_columns'] = list_columns
        df_report_visualizations = ReportVisualizationService.__create_visualization_schemas(
            df_report_visualizations, df_dataset
        )

        return df_report_visualizations

    @staticmethod
    def __create_visualization_schemas(df_report_visualizations, df_dataset: pd.DataFrame) -> pd.DataFrame:
        df_report_visualizations["data"] = None
        for index, row in df_report_visualizations.iterrows():
            df_report_visualization_dataset_columns = pd.DataFrame(row.get("report_visualization_dataset_columns"))
            match row.get("visualization_name"):
                case "Mapa Coroplético":
                    df_report_visualizations.at[index, "data"] = ReportVisualizationService.__build_choropleth_map(
                        df_report_visualization_dataset_columns, df_dataset
                    )


        return df_report_visualizations

    @staticmethod
    def __build_choropleth_map(
        df_report_visualization_dataset_columns: pd.DataFrame, df_dataset: pd.DataFrame
    ) -> list[dict]:
        df_dataset = df_dataset.tail(10)

        list_of_columns = []
        for index, column in df_report_visualization_dataset_columns.iterrows():
            dataset_column = df_dataset[column['dataset_column_name']]
            if column['dataset_column_type'] == "date":
                dataset_column = dataset_column.dt.strftime("%Y-%m-%d")

            list_of_columns.append({
                "field_name": column.get("field_name"),
                "field_data": dataset_column.tolist()
            })

            # sickness
            # latitude
            # longitude
            # city_name
            # cases

        exit(list_of_columns)

        ChoroplethMap()
