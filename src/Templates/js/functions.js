function request(metod, url, params = []) {
    var result = null;    
    let query;

    if(params.length > 0)
    {        
        for (let i = 0; i < params.length; i++) {            
            query = '';
            
            if (i == 0) {
                query += '?';
            } else {
                query += '&';
            }
            url += query + encodeURIComponent(params[i].name) + '=' + encodeURIComponent(params[i].value);            
        }
    }

    $.ajax({
      url: url,
      type: metod,
      async: false,
      success: function(data, textStatus, xhr) {
        result = { data: data, status: xhr.status };
      },
      beforeSend: function(xhr) {
        // Adiciona o token JWT no header Authorization
        token = getCookie("authToken")
        if (token){
            xhr.setRequestHeader("Authorization", token);
        }
      },
      error: function(xhr, textStatus, errorThrown) {
        result = { data: null, status: xhr.status };
      }
    });

    return result;
  }

  function getFormData(formElement) {
    var formData = {};
    $(formElement).serializeArray().forEach(function(field) {
        // Verifica se já existe uma chave com esse nome no objeto
        if (formData[field.name]) {
            // Se já for um array, adiciona o novo valor
            if (Array.isArray(formData[field.name])) {
                formData[field.name].push(field.value);
            } else {
                // Se for um valor único, transforma em array
                formData[field.name] = [formData[field.name], field.value];
            }
        } else {
            formData[field.name] = field.value;
        }
    });
    return formData;
}

  function requestPost(endpoint, data, successCallback, errorCallback) {
    $.ajax({
        url: endpoint,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        beforeSend: function(xhr) {
            // Adiciona o token JWT no header Authorization
            token = getCookie("authToken")
            if (token){
                xhr.setRequestHeader("Authorization", token);
            }
        },
        success: function(response) {
            if (typeof successCallback === 'function') {
                successCallback(response);
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            if (typeof errorCallback === 'function') {
                errorCallback(jqXHR, textStatus, errorThrown);
            }
        }
    });
}

function requestPut(endpoint, data, successCallback, errorCallback) {
    $.ajax({
        url: endpoint,
        type: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify(data),
        beforeSend: function(xhr) {
            // Adiciona o token JWT no header Authorization
            token = getCookie("authToken")
            if (token){
                xhr.setRequestHeader("Authorization", token);
            }
        },
        success: function(response) {
            if (typeof successCallback === 'function') {
                successCallback(response);
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            if (typeof errorCallback === 'function') {
                errorCallback(jqXHR, textStatus, errorThrown);
            }
        }
    });
}

function setCookie(name, value, minutes) {
    let expires = "";
    if (minutes) {
        const date = new Date();
        date.setTime(date.getTime() + minutes * 60 * 1000); // Converte minutos em milissegundos
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = `${name}=${value || ""}${expires}; path=/; secure; samesite=strict`;
}

function expireCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; secure; samesite=strict`;
}

function isTokenExpired(token) {
    if (!token) return true; // Considera expirado se não houver token

    // Decodifica o token para acessar o payload
    const payload = JSON.parse(atob(token.split('.')[1]));

    // Verifica se o tempo atual está além do tempo de expiração
    const currentTime = Math.floor(Date.now() / 1000); // Tempo atual em segundos
    return currentTime > payload.exp; // Retorna true se expirado
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return null; // Retorna null se o cookie não existir
}

 function sendFile(file, props, url, callbackSuccess, callbackError) {
    var formData = new FormData();
    formData.append('file', file);

    if(props != null)
        Object.keys(props).forEach(key => {
            formData.append(key, props[key])
        });

    $.ajax({
        url: url,
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        beforeSend: function(xhr) {
            // Adiciona o token JWT no header Authorization
            xhr.setRequestHeader("Authorization", getCookie("authToken"));
        },
        success: function(response) {
            if (typeof callbackSuccess === 'function') {
                callbackSuccess(response.message);
            }
            else{
                console.log('Arquivo foi enviado com sucesso.')
            }
        },
        error: function(xhr, status, error) {
            if (typeof callbackError === 'function') {
                callbackError(xhr.responseJSON);
            }
            else{
                console.error('Erro ao enviar arquivo:', error);
            }
        }
    });
}

function showAlertForm(alertElementId, response, isError){
    alertElement = $('#'+alertElementId)
    if(!$(alertElement).length){
        return;
    }
    if(isError){
        $(alertElement).addClass('alert-danger');
        $(alertElement).removeClass('alert-success');
    }
    else{
        $(alertElement).addClass('alert-success');
        $(alertElement).removeClass('alert-danger');
    }

    $(alertElement).text(response)
    alertElement.css({'display': 'block'})
    if(!isError){
        alertElement.delay(3000).fadeOut('slow');
    }
}

function buildSelect2(elementId, placeholder, options){
    options.forEach(function(option) {
        let newOption = new Option(option.text, option.id, false, false);
        $('#'+elementId).append(newOption);
    });

    $('#'+elementId).select2({
        language: {
            noResults: function() {
                return "Nenhum resultado encontrado";
            },
            searching: function() {
                return "Procurando...";
            },
            removeAllItems: function() {
                return "Remover todos os itens";
            }
        },
        placeholder: placeholder,
        allowClear: true
    });

    $('#'+elementId).val(null).trigger('change.select2');
}

function buildSelect2Regions(){
    let result = request('GET', '/get-regions')
    let options = []

    if (result.status == 200) {
        options = result.data.data
    }

    options_formated = options.map(function(option){
        return {
            'id': option.id,
            'text': option.name
        }
    })

    buildSelect2('input-regions', 'Região', options_formated)
}

function buildSelect2States(regions = null){
    let result = null
    if(regions){
        let regions_id = regions.map((region_id) => { return {'name': 'region_id', 'value': region_id}})

        result = request('GET', '/get-states', regions_id)
    }
    else{
        result = request('GET', '/get-states')
    }
    let options = []

    if (result.status == 200) {
        options = result.data.data
    }

    options = options.map(function(option){
        return {
            'id': option.id,
            'text': option.name
        }
    })

    buildSelect2('input-states', 'Estado', options)
    $('#input-states').prop('disabled', false).trigger('change.select2')
}

function buildSelect2Cities(states = null){

    let result = null
    if(states){
        let states_id = states.map((state_id) => { return {'name': 'state_id', 'value': state_id}})

        result = request('GET', '/get-cities', states_id)
    }
    else{
        result = request('GET', '/get-cities')
    }
    let options = []

    if (result.status == 200) {
        options = result.data.data
    }

    options = options.map(function(option){
        return {
            'id': option.id,
            'text': option.name
        }
    })

    buildSelect2('input-cities', 'Cidade', options)
}

function buildFlatpickr(elementId, mode = 'range')
{
    $("#"+elementId).flatpickr({
        mode: mode,
        dateFormat: "d/m/Y",
        locale: {
            firstDayOfWeek: 1,
            weekdays: {
                shorthand: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'],
                longhand: ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado'],
            },
            months: {
                shorthand: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
                longhand: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
            },
            rangeSeparator: " até ",
            weekAbbreviation: "Sem",
            scrollTitle: "Role para aumentar",
            toggleTitle: "Clique para alternar",
            amPM: ["AM", "PM"],
            yearAriaLabel: "Ano",
            time_24hr: true
        }
    });
}

function buildSelect2Sickness(){
    let result = request('GET', '/get-sickness')
    let options = []

    if (result.status == 200) {
        options = result.data.data
    }

    options_formated = options.map(function(option){
        return {
            'id': option.id,
            'text': option.name
        }
    })

    buildSelect2('input-sickness', 'Enfermidades', options_formated)
}

function userIsNotLogged(){
    token = getCookie("authToken")
    // Caso o token não exista ou esteja expirado, redireciona para o login
    if(token == null || isTokenExpired(token))
        window.location.href = "/login";
}

function checkUserLogin(){
    token = getCookie("authToken")

    return token != null && !isTokenExpired(token)
}

function setUrlParam(param) {
    let urlAtual = window.location.href;
    param = `${param.key}=${param.value}`
    // Verifica se a URL já tem parâmetros
    const novaUrl = urlAtual.includes("?") ? `${urlAtual}&${param}` : `${urlAtual}?${param}`;
    // Atualiza a URL sem recarregar
    window.history.pushState(null, null, novaUrl);
}

function removeURLParam(key) {
    // Obter a URL atual
    const currentUrl = new URL(window.location.href);

    // Usar URLSearchParams para manipular os parâmetros da query
    const params = currentUrl.searchParams;

    // Remover o parâmetro pela chave
    params.delete(key);

    // Atualizar a URL sem recarregar a página
    const newUrl = `${currentUrl.origin}${currentUrl.pathname}?${params.toString()}`;
    window.history.pushState(null, null, newUrl);
}

function setSidebarActiveMenu() {
    sidebar = $("#sidebar").first()
    if(sidebar.length < 0) return;

    // Obter a URL atual
    const currentUrl = window.location.pathname;

    // Encontra o elemento <a> com href correspondente à URL atual
    const matchingElement = sidebar.find("a").filter(function () {
        const href = $(this).attr("href");
        // Compara o href absoluto ou relativo com a URL atual
        return href && href === currentUrl;
    }).first();

    matchingElement.addClass("active")
}

function changeSidebarAfterLogin() {
    userIsLogged = checkUserLogin()

    if(userIsLogged) {
        $("#sidebar-my-account-button").show()
        $("#sidebar-user-icon").addClass("fa-user-circle-o")
        $("#sidebar-user-icon").removeClass("fa-sign-in")
        $("#sidebar-dropdown-divider").show()
        $("#sidebar-login-button").hide()
        $("#sidebar-logout-button").show()
    }
    else{
        $("#sidebar-my-account-button").hide()
        $("#sidebar-user-icon").addClass("fa-sign-in")
        $("#sidebar-user-icon").removeClass("fa-user-circle-o")
        $("#sidebar-dropdown-divider").hide()
        $("#sidebar-login-button").show()
        $("#sidebar-logout-button").hide()
    }
}

function logout(){
    userIsLogged = checkUserLogin()
    if(userIsLogged){
        requestPost(
            "/auth/logout",
            {},
            function(response){
                message = response.message
                console.log(message)
                expireCookie("authToken")
                // atualiza a pagina
                window.location.reload()
            },
            function(response){
                message = response.responseJSON.message
                alert("Erro ao fazer logout. Erro: "+message)
            }
        )
    }
}
