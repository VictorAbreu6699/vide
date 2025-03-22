// Ao carregar a pagina, verifica se o usuário está logado
userIsNotLogged();

// Verifica se o usuário está logado de 60 em 60 segundos
setInterval(userIsNotLogged, 60000);

var report_id = window.location.pathname.split("/").pop();

$('#form-report-btn-submit').on('click', function(e){
    $("#alert-form-report").hide()
    requestPost(
        "/reports",
        getFormData("#form-report"),
        function(response){
            message = response.message
            showAlertForm('alert-form-report', message, false)
            // Após 2 segundos, redireciona para os relatorios
            setTimeout(function () {
                window.location.href = "/relatorios";
            }, 2000);
        },
        function(response){
            response = response.responseJSON.message
            showAlertForm('alert-form-report', response, true)
        }
    )
})

function createVisualizationCells() {
    result = request("GET", "/report-visualizations/"+report_id)
    if(result.status != 200)
        return;
    report_visualizations = result.data.data
    let html = ''
    $("#row-visualizations").empty()
    for (let i = 0; i < report_visualizations.length; i++) {
        html += `<div style="cursor: pointer;" id="visualization-${i}" data-bs-toggle="tooltip" title="${report_visualizations[i].name}" class="col-3 cell-visualization">
                    <i style="font-size: 30px; color: white" class="fa fa-bar-chart" aria-hidden="true"></i>
                    <input type="hidden" name="report_visualization_id" value="${report_visualizations[i].id}">
                </div>`
    }
    let cell_add_new_visualization = `<div style="cursor: pointer;" id="add-new-visualization" class="col-3 cell-visualization">
                   <i style="font-size: 30px; color: white" class="fa fa-plus" aria-hidden="true"></i>
               </div>`
    html += cell_add_new_visualization
    $("#row-visualizations").append(html);

    $("#add-new-visualization").on("click", () => fillModalVisualization())
    $(".cell-visualization:not(#add-new-visualization)").on("click", function(){
        report_visualization_id = $(this).children("input[name='report_visualization_id']").val()
        fillModalUpdateVisualization(report_visualization_id)
    })

    // Inicializar o tooltip do Bootstrap
    let tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    let tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    // Muda o icone ao passar o mouse em cima
    $(".cell-visualization:not(#add-new-visualization)").hover(
      function() {
        $(this).children("i").removeClass("fa-bar-chart").addClass("fa-pencil");
      },
      function() {
        $(this).children("i").removeClass("fa-pencil").addClass("fa-bar-chart");
      }
    );
}

function buildType(data){
    data = data.map(function(item){
        typeFormat = null;
        switch (item.type) {
          case "date":
            typeFormat = "Data"
            break;
          case "string":
            typeFormat = "Texto"
            break;
          case "number":
            typeFormat = "Numérico"
            break;
          default:
            typeFormat = "Indefinido"
        }

        item.typeFormat = typeFormat
        return item
    })

    return data
}

$(document).ready(function(){
    $("#link-show-report").attr("href", "/relatorios/" + report_id);
    createVisualizationCells()
})
