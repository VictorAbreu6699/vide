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
      error: function(xhr, textStatus, errorThrown) {
        result = { data: null, status: xhr.status };
      }
    });

    return result;;
  }

 function sendFile(file, url, callbackSuccess, callbackError) {
    var formData = new FormData();
    formData.append('file', file);

    $.ajax({
        url: url,
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
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
                response = xhr.responseJSON.detail
                callbackError(response);
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
