var polar_graph_sickness = null

function buildPolarGraphForSickness(container_id, report_visualization, reload = false) {
    if(polar_graph_sickness != null){
        polar_graph_sickness.destroy()
        polar_graph_sickness = null
    }

    let labels = report_visualization.data.map(item => item.sickness);
    let data = report_visualization.data.map(item => item.cases);

    polar_graph_sickness = new Chart(document.getElementById(container_id).getContext('2d'), {
      type: 'polarArea',
      data: {
        labels: labels,
        datasets: [{
          label: 'Indicador Médio por Doença',
          data: data,
          backgroundColor: labels.map((_, i) => `hsl(${i * 60}, 70%, 60%)`)
        }]
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: "Distribuição de Indicador por Doença"
          }
        }
      }
    });
}