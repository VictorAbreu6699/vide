var report_update_visualization_modal = new bootstrap.Modal(document.getElementById('report-update-visualization-modal'), {
      keyboard: false
    })

function fillModalUpdateVisualization(report_visualization_id){
    $("#form-report-update-visualization-report-id").val(report_id)
    $("#form-report-update-visualization-report-visualization-id").val(report_visualization_id)
    result = request("GET", "/report-visualizations/get_report_visualizations_to_edit/"+report_visualization_id)
    if(result.status != 200)
        return;

    data = result.data.data

    $("#form-update-report-visualization-name").val(data.name)

    $('#report-update-visualization-modal').on('shown.bs.modal', function () {
        $('#form-update-report-visualization-visualization-id').select2({
            ajax: {
                url: '/visualizations/get-visualizations',
                data: function (params) {
                  var query = {
                    search: params.term
                  }

                  // Query parameters will be ?search=[term]
                  return query;
                },
                dataType: 'json',
                processResults: function (data) {
                    data = data.data
                    return {
                        results: data.map(visualization => ({
                            id: visualization.id,
                            text: visualization.name
                        }))
                    };
                },
                cache: true,
                maximumSelectionLength: 20,
                placeholder: "Selecione a visualização"
            }
        });

        let option = new Option(data.visualization_name, data.visualization_id, true, true); // true, true marca como selecionada
        $('#form-update-report-visualization-visualization-id').append(option).trigger('change');

        generateCreateVisualizationFields()
    });

    report_update_visualization_modal.show()
}
