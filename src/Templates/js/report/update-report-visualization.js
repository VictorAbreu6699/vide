// Ao carregar a pagina, verifica se o usuário está logado
userIsNotLogged();

// Verifica se o usuário está logado de 60 em 60 segundos
setInterval(userIsNotLogged, 60000);

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

    let dataset_modal = new bootstrap.Modal(document.getElementById('report-add-new-visualization-modal'), {
      keyboard: false
    })

    dataset_modal.show()
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

$(document).ready(function(){
    let report_id = window.location.pathname.split("/").pop();
    $("#link-show-report").attr("href", "/relatorios/" + report_id);
    createVisualizationCells()
})
