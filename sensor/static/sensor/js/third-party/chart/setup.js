// Register data labels plugin to all charts
Chart.register(ChartDataLabels);

const labels = [
    '',
    '',
    '',
    '',
    '',
    '',
    '',
];

const data = {
    labels: labels,
    datasets: [{
        label: 'Temperature',
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data: [0, 0, 0, 0, 0, 0, 0],
        fill: {
            target: 'origin',
            above: 'rgb(255, 99, 132)',   // Area will be red above the origin
            below: 'rgb(62,149,205)'    // And blue below the origin
        },
        lineTension: 0.5
    }]
};

const config = {
    type: 'line',
    data: data,
    options: {
        responsive: true,
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Time',
                    font: {
                        weight: 'bold',
                        size: 24,
                    }
                },
                ticks: {
                    font: {
                        size: 18,
                    },
                    padding: 30
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Temperature',
                    font: {
                        weight: 'bold',
                        size: 24,
                    }
                },
                min: -100,
                max: 100,
                ticks: {
                    font: {
                        size: 18,
                    },
                    padding: 20
                }
            }
        },
        layout: {
            padding: 120
        },
        plugins: {
            datalabels: { // This code is used to display data values
                anchor: 'center',
                align: 'top',
                color: 'black',
                formatter: Math.round,
                font: {
                    weight: 'bold',
                    size: 14,
                }
            },
            legend: {
                labels: {
                    font: {
                        weight: 'bold',
                        size: 20,
                    },
                    boxWidth: 60,
                },
                align: 'end'
            }
        },
    }
};

const context = document.getElementById('myChart').getContext("2d");

const myChart = new Chart(
    context,
    config
);
