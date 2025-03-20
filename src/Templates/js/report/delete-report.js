var report_id = window.location.pathname.split("/").pop();

$('#btn-confirm-delete-report').on('click', function(e){
    $("#alert-form-report").hide()
    requestDelete(
        "/reports/" + report_id,
        function(response){
            message = response.message
            showAlertForm('alert-form-report-delete', message, false)
            // Após 2 segundos, redireciona para os relatorios
            setTimeout(function () {
                window.location.href = "/";
            }, 2000);
        },
        function(response){
            response = response.responseJSON.message
            showAlertForm('alert-form-report-delete', response, true)
        }
    )
})

function OpenModalDeleteReport(){
    let report_delete_modal = new bootstrap.Modal(document.getElementById('report-delete-modal'), {
      keyboard: false
    })

    report_delete_modal.show()
}

$("#btn-delete-report").on("click", OpenModalDeleteReport)
