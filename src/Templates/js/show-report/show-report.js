// Pega o id do relátorio
var report_id = window.location.pathname.split("/").pop();

function buildVisualizations(reload = false)
{
    showLoader()
    filters = createUrlParams(getFormData("#form-filters"))
    result = request("GET", "/report-visualizations/get_report_visualizations_to_build_report/"+report_id+filters)
    if(result.status != 200)
        return;

    data = result.data.data

    data.forEach(function(report_visualization, index) {
        switch (report_visualization.visualization_name) {
            case "Mapa Coroplético":
                buildChoroplethMap("map", report_visualization)
                break;
            case "Gráfico polar por Enfermidade":
                buildPolarGraphForSickness("polar-graph-sickness", report_visualization)
                break;
            case "Histograma por Ano":
                buildHistogramGraphForYearAndSickness("histogram-graph-sickness", report_visualization)
                break;
            case "Gráfico polar por Estado":
                buildPolarGraphForState("polar-graph-state", report_visualization)
                break;
            default:
                console.error("Tipo de visualização não implementada.");
                // Código para tratar visualizações desconhecidas
                break;
        }
    });
    hideLoader()
}

function buildMockTemplate(){
    // Gráfico de Linha
  const lineCtx = document.getElementById('chart-line').getContext('2d');
  new Chart(lineCtx, {
    type: 'line',
    data: {
      labels: ['Janeiro', 'Fevereiro', 'Março', 'Abril'],
      datasets: [
        {
          label: 'Confirmados',
          data: [20, 40, 60, 80],
          borderColor: '#8be9fd',
          backgroundColor: 'rgba(139, 233, 253, 0.2)',
        },
        {
          label: 'Prováveis',
          data: [30, 50, 70, 90],
          borderColor: '#bd93f9',
          backgroundColor: 'rgba(189, 147, 249, 0.2)',
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        x: {
          ticks: { color: '#ffffff' },
          grid: { color: '#44475a' },
        },
        y: {
          ticks: { color: '#ffffff' },
          grid: { color: '#44475a' },
        },
      },
      plugins: {
        legend: { labels: { color: '#ffffff' } },
      },
    },
  });

  // Gráfico de Barras
  const barCtx = document.getElementById('chart-bar').getContext('2d');
  new Chart(barCtx, {
    type: 'bar',
    data: {
      labels: ['Janeiro', 'Fevereiro', 'Março'],
      datasets: [
        {
          label: 'Casos',
          data: [70, 90, 50],
          backgroundColor: ['#50fa7b', '#ffb86c', '#ff5555'],
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { labels: { color: '#ffffff' } },
      },
    },
  });
}

$(document).ready(function(){
    buildVisualizations()
//    buildMockTemplate()

    $("#form-filters").on("change", function(){
        $('#loader').fadeIn();
        buildVisualizations(true)
    })
})
