
function login(callbackSuccess, callbackError) {
    var formData = new FormData();
    console.log(formData)
    $.ajax({
        url: "/auth/login",
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            if (typeof callbackSuccess === 'function') {
                callbackSuccess(response.message);
            }
            else{
                console.error('Login realizado com sucesso!');
            }
        },
        error: function(xhr, status, error) {
            if (typeof callbackError === 'function') {
                response = xhr.responseJSON.detail
                callbackError(response);
            }
            else{
                console.error('Erro ao fazer login:', error);
            }
        }
    });
}

$('#form-login-btn-submit').on('click', function(e){
    console.log('entrou')
})
