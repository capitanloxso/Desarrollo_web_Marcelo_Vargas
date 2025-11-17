document.addEventListener('DOMContentLoaded', function() {
    cargarEstadisticas();
});

function cargarEstadisticas() {
    // Gráfico 1: Avisos por día
    fetch('/api/estadisticas/avisos-por-dia')
        .then(response => response.json())
        .then(data => {
            const fechas = data.map(d => d.fecha);
            const cantidades = data.map(d => d.cantidad);
            
            Highcharts.chart('grafico1', {
                title: { text: 'Avisos por Día' },
                xAxis: { categories: fechas },
                yAxis: { title: { text: 'Cantidad' } },
                series: [{
                    name: 'Avisos',
                    data: cantidades,
                    type: 'line'
                }]
            });
        });

    // Gráfico 2: Avisos por tipo
    fetch('/api/estadisticas/avisos-por-tipo')
        .then(response => response.json())
        .then(data => {
            const seriesData = data.map(d => [d.tipo, d.cantidad]);
            
            Highcharts.chart('grafico2', {
                chart: { type: 'pie' },
                title: { text: 'Avisos por Tipo' },
                series: [{
                    name: 'Cantidad',
                    data: seriesData
                }]
            });
        });

    // Gráfico 3: Avisos por mes
    fetch('/api/estadisticas/avisos-por-mes')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('grafico3', {
                title: { text: 'Avisos por Mes' },
                xAxis: { categories: data.meses },
                yAxis: { title: { text: 'Cantidad' } },
                series: [{
                    name: 'Gatos',
                    data: data.gatos,
                    type: 'column'
                }, {
                    name: 'Perros',
                    data: data.perros,
                    type: 'column'
                }]
            });
        });
}