var created_filters = []

function buildSelectYear(data) {
    if(created_filters.includes("years")){
        return;
    }
    data_select = data.map(function(item){
        return {"id": item, "text": item}
    })

    $("#filters-div").show()
    $("#filter-year").show()
    $('#select-filter-year').select2({
        data: data_select,
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
        placeholder: "Selecione uma opção",
        allowClear: true
    });
    created_filters.push("years")
}

function buildSelectSickness(data) {
    if(created_filters.includes("sickness")){
        return;
    }
    data_select = data.map(function(item){
        return {"id": item, "text": item}
    })

    $("#filters-div").show()
    $("#filter-sickness").show()
    $('#select-filter-sickness').select2({
        data: data_select,
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
        placeholder: "Selecione uma opção",
        allowClear: true
    });
    created_filters.push("sickness")
}

function buildSelectState() {
    if(created_filters.includes("state")){
        return;
    }

    result = request("GET", "/states/get-states")
    if(result.status != 200)
        return;
    data = result.data.data

    data_select = data.map(function(item){
        return {"id": item.id, "text": item.name}
    })

    $("#filters-div").show()
    $("#filter-state").show()
    $('#select-filter-state').select2({
        data: data_select,
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
        placeholder: "Selecione uma opção",
        allowClear: true
    });
    created_filters.push("state")

    $('#select-filter-state').on('select2:select', function(e){
        created_filters = created_filters.filter(item => item !== "city")
        buildSelectCity($(this).val())
    })
}

function buildSelectCity(state_id = null) {
    if(created_filters.includes("city")){
        return;
    }

    result = request("GET", "/cities/get-cities" + (state_id ? "?state_id="+state_id : ""))
    if(result.status != 200)
        return;
    data = result.data.data

    data_select = data.map(function(item){
        return {"id": item.id, "text": item.name, "state_id": item.state_id}
    })

    if(state_id){
        $('#select-filter-city').select2('destroy');
        // (opcional) Limpa o conteúdo se for necessário
        $('#select-filter-city').empty();
    }

    $("#filters-div").show()
    $("#filter-city").show()
    $('#select-filter-city').select2({
        data: data_select,
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
        placeholder: "Selecione uma opção",
        allowClear: true
    });
    $('#select-filter-city').val(null).trigger('change.select2');
    created_filters.push("city")

    // Neste ponto, e.params.data terá state_id
    $('#select-filter-city').on('select2:select', function(e) {
        let stateId = e.params.data.state_id;
        if (stateId) {
            $('#select-filter-state').val(stateId).trigger('change.select2');
        }
    });
}