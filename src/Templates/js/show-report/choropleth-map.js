function buildChoroplethMap(container_id, data = []) {
    // Inicializar o mapa usando a biblioteca Leaflet
    const map = L.map(container_id).setView([-14.2350, -51.9253], 4); // Centro aproximado do Brasil

    // Adicionar o tile layer (fundo do mapa)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    }).addTo(map);

    // Dados fictícios (latitude, longitude e informações)
    data = [
    { lat: -23.55052, lng: -46.633308, name: 'São Paulo', cases: 500 },
    { lat: -22.906847, lng: -43.172896, name: 'Rio de Janeiro', cases: 300 },
    { lat: -19.916681, lng: -43.934493, name: 'Belo Horizonte', cases: 200 },
    { lat: -3.119027, lng: -60.021731, name: 'Manaus', cases: 150 },
    { lat: -8.047562, lng: -34.877, name: 'Recife', cases: 120 },
    ];

    // Adicionar os marcadores no mapa
    data.forEach(location => {
    L.circleMarker([location.lat, location.lng], {
      color: 'red',
      radius: 10,
      fillColor: '#ff0000',
      fillOpacity: 0.7,
    })
      .addTo(map)
      .bindPopup(`<strong>${location.name}</strong><br>Casos: ${location.cases}`);
    });
}