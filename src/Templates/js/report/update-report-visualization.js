// Ao carregar a pagina, verifica se o usuário está logado
userIsNotLogged();

// Verifica se o usuário está logado de 60 em 60 segundos
setInterval(userIsNotLogged, 60000);

var report_new_visualization_modal = new bootstrap.Modal(document.getElementById('report-add-new-visualization-modal'), {
      keyboard: false
    })

function fillModalVisualization(){
//    result = request("GET", "/datasets/show-dataset/"+dataset_id)
//    if(result.status != 201)
//        return;
//
//    data = result.data.data
//    $("#dataset-show-modal-label").text(data.name)
//    $("#dataset-show-modal-description").text(data.description)
//    created_at = moment(data.created_at, "YYYY-MM-DD HH:mm:ss").format('DD/MM/YYYY HH:mm:ss')
//    $("#dataset-show-modal-created-at").text(created_at)
//    $("#dataset-show-modal-download").attr("download", data.name + data.extension)
//    $("#dataset-show-modal-download").attr("href", "/datasets/download-file/" + data.id)
    let report_id = window.location.pathname.split("/").pop();
    $("#form-report-visualization-report-id").val(report_id)
    report_new_visualization_modal.show()
}

function createVisualizationCells() {
//    result = request("GET", "/datasets/get-datasets?" + $("#form-input-datasets").serialize())
//    if(result.status != 201)
//        return;
    let html = ''
    for (let i = 1; i <= 4; i++) {
        html += `<div id="visualization-${i}" class="col-3 cell-visualization">
                    <i style="font-size: 30px; color: white" class="fa fa-bar-chart" aria-hidden="true"></i>
                    <input type="hidden" name="icon-visualization[]">
                </div>`
    }
    let cell_add_new_visualization = `<div id="add-new-visualization" class="col-3 cell-visualization">
                   <i style="font-size: 30px; color: white" class="fa fa-plus" aria-hidden="true"></i>
                   <input type="hidden" name="icon-visualization[]">
               </div>`
    html += cell_add_new_visualization
    $("#row-visualizations").append(html);

    $("#add-new-visualization").on("click", () => fillModalVisualization())

//    data = result.data.data
//    data.forEach(function(dataset) {
//        hmtl = `<div class="col-3 mb-4">
//                    <div class="card card-datasets">
//                      <div class="card-body text-center" style="color: white">
//                          <div class="card-title">${dataset.name}</div>
//                          <div class="text-center card-text">
//                              <i style="font-size: 150px; color: white" class="fa fa-database" aria-hidden="true"></i>
//                              </br>
//                              <div class="dataset-title mt-2">Criado por <i data-bs-toggle="tooltip" data-bs-placement="top" title="${dataset.user_email}">${dataset.user_name}</i></div>
//                              <button dataset-id="${dataset.id}" type="button" style="background-color: #4E598D; color: white" class="btn mt-3 btn-visualization-modal">
//                                  Visualizar
//                              </button>
//                          </div>
//                      </div>
//                    </div>
//                </div>`
//        $("#row-datasets").append(hmtl);
//    });
}

$('#form-report-btn-submit').on('click', function(e){
    $("#alert-form-report").hide()
    requestPost(
        "/reports",
        getFormData("#form-report"),
        function(response){
            message = response.message
            showAlertForm('alert-form-report', message, false)
            // Após 2 segundos, redireciona para os relatorios
            setTimeout(function () {
                window.location.href = "/relatorios";
            }, 2000);
        },
        function(response){
            response = response.responseJSON.message
            showAlertForm('alert-form-report', response, true)
        }
    )
})

$('#form-report-visualization-visualization-id').select2({
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
        allowClear: true,
        maximumSelectionLength: 20,
        placeholder: "Selecione a visualização"
    }
});

$('#form-report-visualization-visualization-id').on("change.select2", function(){
    visualization_id = $('#form-report-visualization-visualization-id').val()
    if (visualization_id != null){
        let report_id = window.location.pathname.split("/").pop();
        $("#visualization-fields-div").show()
        generateVisualizationFields("visualization-fields", visualization_id, report_id)
    }
    else{
        $("#visualization-fields-div").hide()
    }
})

/*
    Gera um elemento hmtl contendo campos a serem preenchidos para gerar uma visualização
*/
function generateVisualizationFields(container_id, visualization_id, report_id) {
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
                            <option value="" disabled selected>Selecione uma opção</option>
                            ${options}
                        </select>
                        <input id="select-visualization-field-id-${i}" name="field_id" type="hidden" value="${data_visualization_fields[i].id}">
                    </div>
                </div>`
    }

    $("#"+container_id).append(html)

    for (let i = 0; i < data_visualization_fields.length; i++) {
        $('#select-visualization-field-value-'+i).off('change');
        $('#select-visualization-field-value-'+i).select2({allowClear: true, "placeholder": "Selecione uma coluna"});
        $('#select-visualization-field-value-'+i).on('change', validateSelect2ReportVisualizationField);
        $('#select-visualization-field-value-'+i).on('change', allowSendForm);
    }

}

function buildType(data){
    data = data.map(function(item){
        typeFormat = null;
        switch (item.type) {
          case "date":
            typeFormat = "Data"
            break;
          case "string":
            typeFormat = "Texto"
            break;
          case "number":
            typeFormat = "Numérico"
            break;
          default:
            typeFormat = "Indefinido"
        }

        item.typeFormat = typeFormat
        return item
    })

    return data
}

function validateSelect2ReportVisualizationField() {
    let selectedValues = [];

    // Coletar todos os valores selecionados
    $('.visualization_field').each(function() {
        let val = $(this).val();
        if (val) {
            selectedValues.push(val);
        }
    });
    // Desativar opções já selecionadas nos outros select2
    $('.visualization_field').each(function() {
        let currentSelect = $(this);
        let currentValue = currentSelect.val();

        currentSelect.find('option').each(function() {
            let optionValue = $(this).val();

            if (optionValue && optionValue !== currentValue) {
                $(this).prop('disabled', selectedValues.includes(optionValue));
            }
        });
    });

    // Atualizar Select2 para refletir mudanças
    $('.visualization_field').trigger("change.select2");
}

function allowSendForm(){
    var allFilled = true;

    $('.visualization_field').each(function() {
        if ($(this).val() === null || $(this).val().length === 0) {
            allFilled = false;
            return false; // Interrompe o loop se encontrar um vazio
        }
    });

    if(allFilled){
        $("#form-report-visualization-btn-submit").prop("disabled", false)
    }
    else{
        $("#form-report-visualization-btn-submit").prop("disabled", true)
    }
}

$('#form-report-visualization-btn-submit').on('click', function(e){
    $("#alert-form-report-visualization").hide()
    requestPost(
        "/report-visualizations/",
        getFormData("#form-report-visualization"),
        function(response){
            message = response.message
            showAlertForm('alert-form-report', message, false)
            setTimeout(report_new_visualization_modal.show(), 2000)
        },
        function(response){
            response = response.responseJSON.message
            showAlertForm('alert-form-report', response, true)
        }
    )
})


$(document).ready(function(){
    let report_id = window.location.pathname.split("/").pop();
    $("#link-show-report").attr("href", "/relatorios/" + report_id);
    createVisualizationCells()
})
