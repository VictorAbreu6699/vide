var polar_graph_sickness = null, polar_graph_state = null, polar_graph_city = null, histogram_graph_year_sickness = null

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
    let data = report_visualization.data.map(item => item.percentual);

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
    let data = report_visualization.data.map(item => item.percentual);

    polar_graph_state = buildPolarGraph(
        container_id, labels, data, "Percentual de Casos", "Concentração de casos por Estado"
    )
}

function buildHistogramGraphForYearAndSickness(container_id, report_visualization, reload = false) {
    if(histogram_graph_year_sickness != null){
        histogram_graph_year_sickness.destroy()
        histogram_graph_year_sickness = null
    }

    dados = report_visualization.data

    let years = [...new Set(dados.map(d => d.year))].sort();
    let sicknesses = [...new Set(dados.map(d => d.sickness))];

    const datasets = sicknesses.map((sickness, index) => {
        const color = `hsl(${index * 50}, 70%, 60%)`;

        const data = years.map(year => {
            const item = dados.find(d => d.year === year && d.sickness === sickness);
            return item ? item.total_cases : 0;
        });

        return {
            label: sickness,
            data: data,
            backgroundColor: color
        };
    });

    const ctx = document.getElementById(container_id).getContext('2d');
    histogram_graph_year_sickness = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: years,
            datasets: datasets
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Casos por Ano e Doença'
                },
                legend: {
                    position: 'top'
                }
            },
            scales: {
                x: {
                    stacked: false,
                    title: {
                        display: true,
                        text: 'Ano'
                    }
                },
                y: {
                    beginAtZero: true,
                    stacked: false,
                    title: {
                        display: true,
                        text: 'Total de Casos'
                    }
                }
            }
        }
    });
}