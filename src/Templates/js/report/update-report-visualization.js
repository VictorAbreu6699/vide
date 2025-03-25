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
    $('#report-update-visualization-modal').off('shown.bs.modal')
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

        generateUpdateVisualizationFields(
            "update-visualization-fields-div", data.visualization_id, report_id, data.report_visualization_dataset_columns
        )
    });

    report_update_visualization_modal.show()
}

/*
    Gera um elemento hmtl contendo campos a serem preenchidos para gerar uma visualização
*/
function generateUpdateVisualizationFields(container_id, visualization_id, report_id, report_visualization_dataset_columns) {
    $("#form-update-report-visualization-report-id").val(report_id)
    result = request('GET', '/visualizations/get-visualization-fields/' + visualization_id)
    if (result.status != 200) return;

    result_dataset_columns = request('GET', '/datasets/get-dataset-columns/' + report_id)
    if (result_dataset_columns.status != 200) return;

    data_visualization_fields = result.data.data
    data_visualization_fields_dataset_columns = result_dataset_columns.data.data
    html = ""
    $("#"+container_id).empty()

    data_visualization_fields_dataset_columns = buildType(data_visualization_fields_dataset_columns)
    data_visualization_fields = buildType(data_visualization_fields)

    options = data_visualization_fields_dataset_columns.map(function(item){
        return `<option value="${item.id}">${item.name} (${item.typeFormat})</option>`
    })
    options = options.join()
    for (let i = 0; i < data_visualization_fields.length; i++) {
        html += `<div class="mb-3 text-start">
                    <label class="mb-2">${data_visualization_fields[i].name} (${data_visualization_fields[i].typeFormat})</label>
                    <div class="d-flex">
                        <select id="select-visualization-field-value-${i}" required style="background-color: #4E598D; color: white" name="field_value" class="form-control text-start visualization_field">
                            <option value="" disabled selected >Selecione uma opção</option>
                            ${options}
                        </select>
                        <input data-field-value-id="${i}" class="select-visualization-field" id="select-visualization-field-id-${i}" name="field_id" type="hidden" value="${data_visualization_fields[i].id}">
                    </div>
                </div>`
    }

    $("#"+container_id).append(html)

    for (let i = 0; i < data_visualization_fields.length; i++) {
        $('#select-visualization-field-value-'+i).off('change');
        $('#select-visualization-field-value-'+i).select2({allowClear: true, "placeholder": "Selecione uma coluna"});
        $('#select-visualization-field-value-'+i).on('change', validateSelect2ReportVisualizationField);
        $('#select-visualization-field-value-'+i).on('change', () => allowSendForm("form-update-report-visualization-btn-submit"));
    }
    report_visualization_dataset_columns = buildType(report_visualization_dataset_columns, "dataset_column_type")
    fields = $(".select-visualization-field")
    for (let i = 0; i < report_visualization_dataset_columns.length; i++) {
        report_visualization_dataset_column = report_visualization_dataset_columns[i]
        field_value_id = $(".select-visualization-field").filter(function() {
            return $(this).val() == report_visualization_dataset_column.field_id;
        }).attr("data-field-value-id")

        $('#select-visualization-field-value-'+field_value_id).val(report_visualization_dataset_column.dataset_column_id).trigger('change');
    }

    $("#form-update-report-visualization-btn-submit").prop("disabled", true)

    $("#"+container_id).show()
}

$('#form-update-report-visualization-btn-submit').on('click', function(e){
    $("#alert-form-update-report-visualization").hide()
    requestPut(
        "/report-visualizations/" + $("#form-report-update-visualization-report-visualization-id").val(),
        getFormData("#form-update-report-visualization"),
        function(response){
            message = response.message
            showAlertForm('alert-form-update-report-visualization', message, false)
            createVisualizationCells()
            setTimeout(
                function(){
                    report_update_visualization_modal.hide()
                }, 2000
            )
        },
        function(response){
            response = response.responseJSON.message
            showAlertForm('alert-form-report-visualization', response, true)
        }
    )
})

function clearModalUpdate(){
    $("#update-visualization-fields").empty()
    $('#form-update-report-visualization-name').val(null).trigger("change")
    $('#form-update-report-visualization-visualization-id').val(null).trigger("change.select2")
}

$(document).ready(function(){
    $("#report-update-visualization-modal").on('hidden.bs.modal', function(){
        clearModalUpdate()
    })
})