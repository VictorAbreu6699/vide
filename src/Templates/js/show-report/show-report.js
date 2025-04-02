// Pega o id do relátorio
var report_id = window.location.pathname.split("/").pop();

function buildVisualizations()
{
    result = request("GET", "/report-visualizations/get_report_visualizations_to_build_report/"+report_id)
    if(result.status != 200)
        return;

    data = result.data.data

    data.forEach(function(report_visualization, index) {
        switch (report_visualization.visualization_name) {
            case "Mapa Coroplético":
                buildChoroplethMap("map", [])
                break;

            default:
                console.error("Tipo de visualização não reconhecido.");
                // Código para tratar visualizações desconhecidas
                break;
        }
    });


}

$(document).ready(function(){
    buildVisualizations()
})
