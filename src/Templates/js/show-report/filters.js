function buildSelectYear(data) {
    console.log(data)
    $("#filters-div").show()
    $("#filter-year").show()
    $('#select-filter-year').select2({
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