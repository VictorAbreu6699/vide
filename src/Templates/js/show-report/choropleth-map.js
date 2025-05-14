function buildChoroplethMap(container_id, data) {
    buildSelectYear(data)
    data = groupDataByYear(data)
    // Inicializar o mapa usando a biblioteca Leaflet
    const map = L.map(container_id).setView([-14.2350, -51.9253], 4); // Centro aproximado do Brasil

    // Adicionar o tile layer (fundo do mapa)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
    }).addTo(map);

    // Dados fictícios (latitude, longitude e informações)
//    data = [
//    { lat: -23.55052, lng: -46.633308, name: 'São Paulo', cases: 500 },
//    { lat: -22.906847, lng: -43.172896, name: 'Rio de Janeiro', cases: 300 },
//    { lat: -19.916681, lng: -43.934493, name: 'Belo Horizonte', cases: 200 },
//    { lat: -3.119027, lng: -60.021731, name: 'Manaus', cases: 150 },
//    { lat: -8.047562, lng: -34.877, name: 'Recife', cases: 120 },
//    ];

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