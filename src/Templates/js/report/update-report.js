// Ao carregar a pagina, verifica se o usuário está logado
userIsNotLogged();

// Verifica se o usuário está logado de 60 em 60 segundos
setInterval(userIsNotLogged, 60000);

function fillModalDataset(dataset_id){
    result = request("GET", "/datasets/show-dataset/"+dataset_id)
    if(result.status != 201)
        return;

    data = result.data.data
    $("#dataset-show-modal-label").text(data.name)
    $("#dataset-show-modal-description").text(data.description)
    created_at = moment(data.created_at, "YYYY-MM-DD HH:mm:ss").format('DD/MM/YYYY HH:mm:ss')
    $("#dataset-show-modal-created-at").text(created_at)
    $("#dataset-show-modal-download").attr("download", data.name + data.extension)
    $("#dataset-show-modal-download").attr("href", "/datasets/download-file/" + data.id)

    let dataset_modal = new bootstrap.Modal(document.getElementById('dataset-show-modal'), {
      keyboard: false
    })

    dataset_modal.show()
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

$("#form-report-dataset-id").on("change.select2", function(e) {
    if($(this).val() != null){
        $("#btn-dataset-visualization-modal").prop("disabled", false)
        $('#form-report-btn-submit').prop("disabled", false)
    }
    else{
        $("#btn-dataset-visualization-modal").prop("disabled", true)
        $('#form-report-btn-submit').prop("disabled", true)
    }
    $('#alert-form-report').hide()
})

$("#btn-dataset-visualization-modal").on("click", () => fillModalDataset($("#form-report-dataset-id").val()))

$('#form-report-dataset-id').select2({
    ajax: {
        url: '/datasets/get-datasets',
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
                results: data.map(dataset => ({
                    id: dataset.id,
                    text: dataset.name
                }))
            };
        },
        cache: true,
        allowClear: true,
        maximumSelectionLength: 20,
        placeholder: "Selecione a fonte de dados"
    }
});
$(document).ready(function(){
    let id = window.location.pathname.split("/").pop();
    $("#form-report-btn-update-visualization").attr("href", "/editar-relatorio/visualizacoes/" + id);
})
