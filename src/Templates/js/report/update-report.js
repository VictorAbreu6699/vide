// Ao carregar a pagina, verifica se o usuário está logado
userIsNotLogged();

// Verifica se o usuário está logado de 60 em 60 segundos
setInterval(userIsNotLogged, 60000);

var report_id = window.location.pathname.split("/").pop();

$('#form-report-update-btn-submit').on('click', function(e){
    $("#alert-form-report").hide()
    requestPut(
        "/reports/" + report_id,
        getFormData("#form-report-update"),
        function(response){
            message = response.message
            showAlertForm('alert-form-report', message, false)
            $("#form-report-update-btn-submit").prop("disabled", true)
        },
        function(response){
            response = response.responseJSON.message
            showAlertForm('alert-form-report', response, true)
        }
    )
})


function fillReportOptions()
{
    result = request('GET', '/reports/show-report/' + report_id)
    if (result.status != 200) return;
    report = result.data.data

    $('#form-report-dataset-id').select2();
    let newOption = new Option(report.dataset_name, report.dataset_id, false, false);
    $('#form-report-dataset-id').append(newOption).trigger('change.select2');
    $('#form-report-dataset-id').val(report.dataset_id).trigger('change.select2')
    $("#form-report-name").val(report.name)
    $('#form-report-dataset-id').val(report.dataset_id).trigger("change")
    $("#form-report-description").val(report.description)
}

$(document).ready(function(){
    $("#form-report-btn-update-visualization").attr("href", "/editar-relatorio/visualizacoes/" + report_id);
    fillReportOptions()
    $("#form-report-update").on("input", function(){
        $("#form-report-update-btn-submit").prop("disabled", false)
    })
})
