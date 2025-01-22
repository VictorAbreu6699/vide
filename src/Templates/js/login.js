
function login() {
    $("#alert-login").hide()
    requestPost(
        "/auth/login",
        getFormData("#form-login"),
        function(response){
            message = response.message
            showAlertForm('alert-login', message, false)
            setCookie("authToken", `${response.token_type} ${response.access_token}`, 60); // Expira em 60 minutos
            // Após 2 segundos, redireciona para o login
            setTimeout(function () {
                window.location.href = "/";
            }, 2000);
        },
        function(response){
            response = response.responseJSON.message
            showAlertForm('alert-login', response, true)
        }
    )
}

function userIsLogged(){
    token = getCookie("authToken")
    // Caso o token exista e não esteja expirado, redireciona para a home
    if(token != null && !isTokenExpired(token))
        window.location.href = "/";
}
$('#form-login').on('keydown', function (e) {
    if (e.key === "Enter" || e.keyCode === 13) {
        e.preventDefault();
        login();
    }
});
$('#form-login-btn-submit').on('click', (e) => login())
$(document).ready(userIsLogged);
