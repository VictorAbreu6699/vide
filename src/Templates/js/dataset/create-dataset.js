// Ao carregar a pagina, verifica se o usuário está logado
userIsNotLogged();

// Verifica se o usuário está logado de 60 em 60 segundos
setInterval(userIsNotLogged, 60000);

$('#form-dataset-upload-btn-submit').on('click', function(e){
    if($('#input-file-upload')[0].files.length){
        file = $('#input-file-upload').prop('files')[0]
        name = $("#form-dataset-upload-name").val()
        description = $("#form-dataset-upload-description").val()
        sendFile(
            file,
            {"name": name, "description": description},
            '/datasets/',
            function(response){
                showAlertForm('alert-form-dataset-upload', response, false)
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
                showAlertForm('alert-form-dataset-upload', message, true)
            }
        )
        $('#input-file-upload').val(null).trigger('change');
        $("#form-dataset-upload-name").val(null);
        $("#form-dataset-upload-description").val(null);
    }
})

// Ao selecionar/remover um arquivo, habilita ou desabilita o botão de envio
$('#input-file-upload').on('change', function(e){
    if($('#input-file-upload')[0].files.length){
        $('#form-dataset-upload-btn-submit').prop("disabled", false);
    }
    else{
        $('#form-dataset-upload-btn-submit').prop("disabled", true);
    }
    $('#alert-form-dataset-upload').hide()
})