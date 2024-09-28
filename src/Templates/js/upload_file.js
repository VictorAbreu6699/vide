// Ao selecionar/remover um arquivo, habilita ou desabilita o botão de envio
$('#input-file-upload').on('change', function(e){
    if($('#input-file-upload')[0].files.length){
        $('#btn-submit-file').prop("disabled", false);
    }
    else{
        $('#btn-submit-file').prop("disabled", true);
    }
    $('#alert-upload-file').hide()
})

$('#btn-submit-file').on('click', function(e){
    if($('#input-file-upload')[0].files.length){
        file = $('#input-file-upload').prop('files')[0]
        sendFile(
            file,
            '/upload-file',
            function(response){
                showAlertForm('alert-upload-file', response, false)
            },
            function(response){
                showAlertForm('alert-upload-file', response, true)
            }
        )
        $('#input-file-upload').val(null).trigger('change');
    }
})
