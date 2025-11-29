// Chart.js 3.x 기반 동적 Multi Axis Chart
let ctx = null;
let chart = null;
let LABEL_SIZE = 10;
let tick = 0;

function drawCharts() {
    ctx = document.getElementById("multiChart").getContext("2d");

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: '온도 (°C)',
                    data: [],
                    borderColor: 'red',
                    backgroundColor: 'rgba(255, 0, 0, 0.2)',
                    yAxisID: 'y'
                },
                {
                    label: '습도 (%)',
                    data: [],
                    borderColor: 'blue',
                    backgroundColor: 'rgba(0, 0, 255, 0.2)',
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: false,
            animation: {
		    duration:300,
		    },
            interaction: {
                mode: 'index',
                intersect: false,
            },
            stacked: false,
            plugins: {
                title: {
                    display: true,
                    text: '실시간 온도 / 습도 '
                }
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left'
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    grid: {
                        drawOnChartArea: false
                    }
                }
            }
        }
    });
}

function addTempHumData(temp, hum) {
    if (!chart) return;

    const labels   = chart.data.labels;
    const tempData = chart.data.datasets[0].data;
    const humData  = chart.data.datasets[1].data;

    if (labels.length < LABEL_SIZE) {
        labels.push(tick);
        tempData.push(temp);
        humData.push(hum);
    } else {
        labels.push(tick);
        labels.shift();

        tempData.push(temp);
        tempData.shift();

        humData.push(hum);
        humData.shift();
    }

    tick = (tick + 1) % 100;
    chart.update();
}

