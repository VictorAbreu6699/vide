function buildChoroplethMap(container_id, report_visualization) {
    buildSelectYear(report_visualization.filters)
    data = groupDataByYear(report_visualization.data)
    // Inicializar o mapa usando a biblioteca Leaflet
    const map = L.map(container_id).setView([-14.2350, -51.9253], 4); // Centro aproximado do Brasil

    // Adicionar o tile layer (fundo do mapa)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
    }).addTo(map);

    // Adicionar os marcadores no mapa
    data.forEach(row => {
        L.circleMarker([row.latitude, row.longitude], {
          color: 'red',
          radius: 10,
          fillColor: '#ff0000',
          fillOpacity: 0.7,
        })
        .addTo(map)
        .bindPopup(`<strong>${row.city_name}</strong><br>Casos: ${row.total_cases}`);
    });

}

function groupDataByYear(data) {
    const grouped = data.reduce((acc, item) => {
        const dateObj = new Date(item.date); // Converte a data para objeto Date
        const year = dateObj.getFullYear(); // Extrai o ano
        const key = `${item.sickness}_${item.state_name}_${item.city_name}_${year}`;

        if (!acc[key]) {
            acc[key] = {
                sickness: item.sickness,
                state_name: item.state_name,
                city_name: item.city_name,
                latitude: item.latitude,
                longitude: item.longitude,
                year: year,
                total_cases: 0
            };
        }

        acc[key].total_cases += item.cases;
        return acc;
    }, {});

    return Object.values(grouped);
}