
function createAccount() {
    $("#alert-create-account").hide()
    requestPost(
        "/auth/create-account",
        getFormData("#form-create-account"),
        function(response){
            response = response.message
            showAlertForm('alert-create-account', response, false)
            // Após 2 segundos, redireciona para o login
            setTimeout(function () {
                window.location.href = "/login";
            }, 2000);
        },
        function(response){
            response = response.responseJSON.message
            showAlertForm('alert-create-account', response, true)
        }
    )
}

$('#form-create-account-btn-submit').on('click', (e) => createAccount())
