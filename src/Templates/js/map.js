document.addEventListener('DOMContentLoaded', () => {
  // Inicializar o mapa usando a biblioteca Leaflet
  const map = L.map('map').setView([-14.2350, -51.9253], 4); // Centro aproximado do Brasil

  // Adicionar o tile layer (fundo do mapa)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
  }).addTo(map);

  // Dados fictícios (latitude, longitude e informações)
  const data = [
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

  // Gráfico de Pizza
  const pieCtx = document.getElementById('chart-pie').getContext('2d');
  new Chart(pieCtx, {
    type: 'pie',
    data: {
      labels: ['Janeiro', 'Fevereiro', 'Março'],
      datasets: [
        {
          data: [30, 40, 30],
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
});
