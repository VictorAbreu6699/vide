from src.Models.ReportVisualization import ReportVisualization
from src.Models.ReportVisualizationDatasetColumn import ReportVisualizationDatasetColumn
from src.Repositories.BaseRepository import BaseRepository
from src.Repositories.ReportRepository import ReportRepository
from src.Repositories.VisualizationFieldRepository import VisualizationFieldRepository
from src.Requests.CreateReportVisualizationDatasetColumnRequest import CreateReportVisualizationDatasetColumnRequest


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
