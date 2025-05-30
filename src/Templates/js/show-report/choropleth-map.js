var map = null

function buildChoroplethMap(container_id, report_visualization, reload = false) {
    if(map != null){
        map.remove()
        map = null
    }
    if(!reload){
        buildSelectYear(report_visualization.filters.years)
        buildSelectSickness(report_visualization.filters.sicknesses)
        buildSelectState()
        buildSelectCity()
    }
    data = groupDataByYear(report_visualization.data)
    // Inicializar o mapa usando a biblioteca Leaflet
    map = L.map(container_id).setView([-14.2350, -51.9253], 4); // Centro aproximado do Brasil

    // Adicionar o tile layer (fundo do mapa)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
    }).addTo(map);
    let heatData = [];
    data.forEach(row => {
//      L.geoJSON(row.geo_json, {
//        onEachFeature: function (feature, layer) {
//          layer.bindPopup(
//            `<a onClick="applyStateAndCityFilter(${row.state_id}, ${row.city_id})" role="link" tabindex="0" style="color: #0078A8 !important; text-decoration: underline; cursor: pointer;">
//              <strong>${row.city_name} - ${row.state_name}</strong>
//            </a><br>Casos: ${row.total_cases}`
//          );
//        }
//      }).addTo(map);
      // Cálculo do centróide
      let layer = L.geoJSON(JSON.parse(row.geo_json));
      let bounds = layer.getBounds();
      let center = bounds.getCenter();

       // Adiciona marcador transparente com popup
      L.circleMarker(center, {
        radius: 5,
        color: 'transparent',
        fillOpacity: 0.0,
      })
      .bindPopup(
        `<a onClick="applyStateAndCityFilter(${row.state_id}, ${row.city_id})" role="link" tabindex="0" style="color: #0078A8 !important; text-decoration: underline; cursor: pointer;">
          <strong>${row.city_name} - ${row.state_name}</strong>
        </a><br>Casos: ${row.total_cases}`
      )
      .addTo(map);

      // Intensidade proporcional aos casos
      let intensity = row.total_cases / 100; // ou normalize se quiser (ex: row.total_cases / 100)

      heatData.push([center.lat, center.lng, intensity]);
    });

    // Adiciona a camada de calor ao mapa
    let heat = L.heatLayer(heatData, {
      radius: 25,
      blur: 15,
      maxZoom: 10,
      gradient: {
        0.2: 'blue',
        0.4: 'cyan',
        0.6: 'lime',
        0.8: 'yellow',
        1.0: 'red'
      }
    }).addTo(map);

}

function groupDataByYear(data) {
    const grouped = data.reduce((acc, item) => {
        const dateObj = new Date(item.date); // Converte a data para objeto Date
        const year = dateObj.getFullYear(); // Extrai o ano
        const key = `${item.sickness}_${item.state_name}_${item.city_name}_${year}`;

        if (!acc[key]) {
            acc[key] = {
                sickness: item.sickness,
                state_id: item.state_id,
                state_name: item.state_name,
                city_id: item.city_id,
                city_name: item.city_name,
                latitude: item.latitude,
                longitude: item.longitude,
                year: year,
                geo_json: item.geo_json,
                total_cases: 0
            };
        }

        acc[key].total_cases += item.cases;
        return acc;
    }, {});

    return Object.values(grouped);
}

function applyStateAndCityFilter(state_id, city_id){
    $('#select-filter-state').val(state_id).trigger("change.select2")
    $('#select-filter-city').val(city_id).trigger("change.select2")
    $('#loader').fadeIn(100, function(){
        buildVisualizations(true)
    });
}