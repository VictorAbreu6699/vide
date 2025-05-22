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