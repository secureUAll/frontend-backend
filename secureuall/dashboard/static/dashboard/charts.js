// This function initializes all the charts
const initCharts = () => {
    initVulnsNumbersChart();
    initMachinesRiskLevelChart();
    initVulnsByGroupChart();
}


const initVulnsNumbersChart = () => {
    // Get element from DOM
    const ctx = document.getElementById('vulnerabilitiesNumbersChart').getContext("2d");

    // Colors
    const chartColor = "#FFFFFF";
    const gradientFill = ctx.createLinearGradient(0, 200, 0, 50);
    gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
    gradientFill.addColorStop(1, "rgba(255, 255, 255, 0.24)");

    // Draw chart
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: vulnsNumbersLabels,
            datasets: [{
                labels: "Vulnerabilities",
                borderColor: chartColor,
                pointBorderColor: chartColor,
                pointBackgroundColor: chartColor,
                pointHoverBackgroundColor: chartColor,
                pointHoverBorderColor: chartColor,
                pointBorderWidth: 1,
                pointHoverRadius: 7,
                pointHoverBorderWidth: 2,
                pointRadius: 5,
                fill: true,
                backgroundColor: gradientFill,
                borderWidth: 2,
                data: vulnsNumbersValues
            }]
        },
        options: {
            layout: {
                padding: {
                    left: 20,
                    right: 20,
                    top: 0,
                    bottom: 0
                }
            },
            maintainAspectRatio: false,
            tooltips: {
                backgroundColor: '#fff',
                titleFontColor: '#333',
                bodyFontColor: '#666',
                bodySpacing: 4,
                xPadding: 12,
                mode: "nearest",
                intersect: 0,
                position: "nearest"
            },
            legend: {
                position: "bottom",
                fillStyle: "#000",
                display: false
            },
            scales: {
                yAxes: [{
                    ticks: {
                        fontColor: "rgba(255,255,255,0.4)",
                        fontStyle: "bold",
                        beginAtZero: true,
                        maxTicksLimit: 5,
                        padding: 10
                    },
                    gridLines: {
                        drawTicks: true,
                        drawBorder: false,
                        display: true,
                        color: "rgba(255,255,255,0.1)",
                        zeroLineColor: "transparent"
                    }

                }],
                xAxes: [{
                    gridLines: {
                        zeroLineColor: "transparent",
                        display: false,

                    },
                    ticks: {
                        padding: 10,
                        fontColor: "rgba(255,255,255,0.4)",
                        fontStyle: "bold"
                    },
                }]
            },
        }
    });
}

const initVulnsByGroupChart = () => {
    // Get element from DOM
    const ctx = document.getElementById('vulnerabilitiesByGroupChart').getContext("2d");

    // Colors
    const chartColor = "#92d400";
    const gradientFill = ctx.createLinearGradient(0, 170, 0, 50);
    gradientFill.addColorStop(0, "rgba(146, 212, 0, 0)");
    gradientFill.addColorStop(1, "rgba(146, 212, 0, 0.40)");

    const gradientFillHover = ctx.createLinearGradient(0, 170, 0, 50);
    gradientFillHover.addColorStop(0, "rgba(146, 212, 0, 0)");
    gradientFillHover.addColorStop(1, "rgba(146, 212, 0, 1)");

    // Draw chart
    var myChart = {
        type: "bar",
        data: {
            labels: vulnsByGroupChartLabels,
            datasets: [{
                label: "Amount",
                backgroundColor: gradientFill,
                hoverBackgroundColor: gradientFillHover,
                borderColor: chartColor,
                fill: true,
                borderWidth: 1,
                data: vulnsByGroupChartValues
            }]
        },
        options: {
            layout: {
                padding: {
                    top: 20
                }
            },
            maintainAspectRatio: false,
            legend: {
                display: false
            },
            tooltips: {
                bodySpacing: 4,
                mode: "nearest",
                intersect: 0,
                position: "nearest",
                xPadding: 10,
                yPadding: 10,
                caretPadding: 10,
            },
            responsive: 1,
            scales: {
                yAxes: [{
                    gridLines: 0,
                    gridLines: {
                        zeroLineColor: "transparent",
                        drawBorder: false
                    },
                    ticks: {
                        beginAtZero: true
                    }
                }],
                xAxes: [{
                    display: 1,
                }]
            },
            plugins: {
                labels: false
            },
        }
    };

    var viewsChart = new Chart(ctx, myChart);
}


const initMachinesRiskLevelChart = () => {
    // Get element from DOM
    var ctx = document.getElementById("machinesRiskLevelChart").getContext("2d");

    // Data
    const data = {
        labels: machinesRiskLevelChartLabels,
        datasets: [{
          data: machinesRiskLevelChartValues,
          backgroundColor: [ 'rgba(146, 212, 0, .6)', 'rgba(122, 179, 0, .6)', 'rgba(87, 128, 0, .6)', 'rgba(52, 77, 0, .6)', 'rgba(17, 26, 0, .6)' ],
          hoverBackgroundColor: [ '#92d400', '#7ab300', '#578000', '#344d00', '#111a00' ],
        }]
  };

    // Draw chart
    const myChart = {
        type: 'pie',
        data: data,
        options: {
            legend: {
                display: true,
                position: 'left',
            },
            responsive: true,
            plugins: {
                labels: {
                    render: 'value',
                    fontColor: '#fff',
                    fontStyle: 'bold',
                    precision: 2
                }
            },
            tooltips: {
                 enabled: false
            }
        },
    };

    var pieChart = new Chart(ctx, myChart);
};