let report_visualization_delete_modal = new bootstrap.Modal(document.getElementById('report-delete-visualization-modal'), {
  keyboard: false
})

$('#btn-confirm-report-delete-visualization').on('click', function(e){
    $("#alert-form-report-visualization-delete").hide()
    requestDelete(
        "/report-visualizations/" + $("#form-report-update-visualization-report-visualization-id").val(),
        function(response){
            message = response.message
            showAlertForm('alert-form-report-visualization-delete', message, false)
            createVisualizationCells()
            setTimeout(
                function(){
                    report_visualization_delete_modal.hide()
                    report_update_visualization_modal.hide()
                }, 2000
            )
        },
        function(response){
            response = response.responseJSON.message
            showAlertForm('alert-form-report-visualization-delete', response, true)
        }
    )
})

function OpenModalDeleteReport(){
    report_visualization_delete_modal.show()
}

$("#btn-report-delete-visualization").on("click", OpenModalDeleteReport)
