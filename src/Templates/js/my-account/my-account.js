
function updateAccount() {
    $("#alert-form-user-update").hide()
    requestPost(
        "/auth/update-account",
        getFormData("#form-user-update"),
        function(response){
            response = response.message
            showAlertForm('alert-form-user-update', response, false)
        },
        function(response){
            response = response.responseJSON.message
            showAlertForm('alert-form-user-update', response, true)
        }
    )
}

$('#form-user-update-btn-submit').on('click', (e) => updateAccount())
$("#form-user-update").on("change", function(e){
    $(this)
})