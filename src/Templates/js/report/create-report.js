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
    $("#dataset-show-modal-download").attr("download", data.name + data.extension)
    $("#dataset-show-modal-download").attr("href", "/datasets/download-file/" + data.id)

    let dataset_modal = new bootstrap.Modal(document.getElementById('dataset-show-modal'), {
      keyboard: false
    })

    dataset_modal.show()
}

$('#form-report-upload-btn-submit').on('click', function(e){
    if($('#input-file-upload')[0].files.length){
        file = $('#input-file-upload').prop('files')[0]
        name = $("#form-report-upload-name").val()
        description = $("#form-report-upload-description").val()
        sendFile(
            file,
            {"name": name, "description": description},
            '/reports/',
            function(response){
                showAlertForm('alert-form-report-upload', response, false)
                setTimeout(function () {
                    window.location.href = "/";
                }, 2000);
            },
            function(response){
                let message = ""

                if(!response){
                    message = "Erro interno!"
                }
                else if(response.detail){
                    message = response.detail
                }
                else if (response.message){
                    message = response.message
                }
                showAlertForm('alert-form-report-upload', message, true)
            }
        )
        $('#input-file-upload').val(null).trigger('change');
        $("#form-report-upload-name").val(null);
        $("#form-report-upload-description").val(null);
    }
})

// Ao selecionar/remover um arquivo, habilita ou desabilita o botão de envio
$('#input-file-upload').on('change', function(e){
    if($('#input-file-upload')[0].files.length){
        $('#form-report-upload-btn-submit').prop("disabled", false);
    }
    else{
        $('#form-report-upload-btn-submit').prop("disabled", true);
    }
    $('#alert-form-report-upload').hide()
})

$("#form-report-dataset-id").on("change.select2", function(e) {
    if($(this).val() != null){
        $("#btn-dataset-visualization-modal").prop("disabled", false)
    }
    else{
        $("#btn-dataset-visualization-modal").prop("disabled", true)
    }
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
