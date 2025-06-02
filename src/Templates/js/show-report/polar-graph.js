var polar_graph_sickness = null, polar_graph_state = null, polar_graph_city = null

function buildPolarGraph(container_id, labels, data, label_dataset, title, type = 'polarArea'){
    return new Chart(document.getElementById(container_id).getContext('2d'), {
      type: type,
      data: {
        labels: labels,
        datasets: [{
          label: label_dataset,
          data: data,
          backgroundColor: labels.map((_, i) => `hsl(${i * 60}, 70%, 60%)`)
        }]
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: title
          }
        }
      }
    });
}

function buildPolarGraphForSickness(container_id, report_visualization, reload = false) {
    if(polar_graph_sickness != null){
        polar_graph_sickness.destroy()
        polar_graph_sickness = null
    }

    let labels = report_visualization.data.map(item => item.sickness);
    let data = report_visualization.data.map(item => item.cases);

    polar_graph_sickness = buildPolarGraph(
        container_id, labels, data, "Percentual de Casos", "Concentração de casos por Enfermidade"
    )
}

function buildPolarGraphForState(container_id, report_visualization, reload = false) {
    if(polar_graph_state != null){
        polar_graph_state.destroy()
        polar_graph_state = null
    }

    let labels = report_visualization.data.map(item => item.state_name);
    let data = report_visualization.data.map(item => item.cases);

    polar_graph_state = buildPolarGraph(
        container_id, labels, data, "Percentual de Casos", "Concentração de casos por Estado"
    )
}