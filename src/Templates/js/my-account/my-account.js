// Ao carregar a pagina, verifica se o usuário está logado
userIsNotLogged();

// Verifica se o usuário está logado de 60 em 60 segundos
setInterval(userIsNotLogged, 60000);

function updateAccount() {
    $("#alert-form-user-update").hide()
    requestPost(
        "/auth/update-account",
        getFormData("#form-user-update"),
        function(response){
            response = response.message
            $("#form-user-update-btn-submit").prop("disabled", true)
            showAlertForm('alert-form-user-update', response, false)
        },
        function(response){
            response = response.responseJSON.message
            showAlertForm('alert-form-user-update', response, true)
        }
    )
}

function fillUpdateForm(){
    result = request("GET", "/auth/show-logged-user")
    if(result.status != 200)
        return;

    data = result.data.data
    $("#form-user-update-name").val(data.name).trigger("change")
    $("#form-user-update-email").val(data.email).trigger("change")
    $("form-user-update-password").val(null)
}

$('#form-user-update-btn-submit').on('click', (e) => updateAccount())
$("#form-user-update").on("change", function(e){
    $("#form-user-update-btn-submit").prop("disabled", false)
})

$(document).ready(function(){
    fillUpdateForm()
})