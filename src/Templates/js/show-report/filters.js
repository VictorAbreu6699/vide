function buildSelectYear(data) {
    data_select = data.years.map(function(item){
        return {"id": item, "text": item}
    })

    console.log(data)
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
}