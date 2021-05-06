// Global configurations
// General configuration for the charts with Line gradientStroke
gradientChartOptionsConfiguration = {
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
        caretPadding: 10
    },
    responsive: true,
    scales: {
        yAxes: [{
            display: 0,
            gridLines: 0,
            ticks: {
                display: false
            },
            gridLines: {
                zeroLineColor: "transparent",
                drawTicks: false,
                display: false,
                drawBorder: false
            }
        }],
        xAxes: [{
            display: 0,
            gridLines: 0,
            ticks: {
                display: false
            },
            gridLines: {
                zeroLineColor: "transparent",
                drawTicks: false,
                display: false,
                drawBorder: false
            }
        }]
    },
    layout: {
        padding: {
            left: 0,
            right: 0,
            top: 15,
            bottom: 15
        }
    }
};

// This function initializes all the charts
const initCharts = () => {
    initHeaderChart();
    initLineChart();
    initBarChart();
    initPieChart();
}

const initHeaderChart = () => {
    // Get element from DOM
    const ctx = document.getElementById('bigDashboardChart').getContext("2d");

    // Colors
    const chartColor = "#FFFFFF";
    const gradientFill = ctx.createLinearGradient(0, 200, 0, 50);
    gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
    gradientFill.addColorStop(1, "rgba(255, 255, 255, 0.24)");


    // Draw chart
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ["08 APR", "09 APR", "10 APR", "11 APR", "12 APR", "13 APR", "14 APR", "15 APR", "16 APR", "17 APR", "18 APR", "19 APR"],
            datasets: [{
                label: "Vulnerabilities",
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
                data: [50, 150, 100, 190, 130, 90, 150, 160, 120, 140, 190, 95]
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
                    }
                }]
            }
        }
    });
}

const initLineChart = () => {
    // Get element from DOM
    const ctx = document.getElementById('lineChart').getContext("2d");

    // Colors
    const chartColor = "#92d400";
    const gradientFill = ctx.createLinearGradient(0, 170, 0, 50);
    gradientFill.addColorStop(0, "rgba(146, 212, 0, 0)");
    gradientFill.addColorStop(1, "rgba(146, 212, 0, 0.40)");

    // Draw chart
    myChart = new Chart(ctx, {
        type: 'line',
        responsive: true,
        data: {
            labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            datasets: [{
                label: "Active Users",
                borderColor: chartColor,
                pointBorderColor: "#FFF",
                pointBackgroundColor: chartColor,
                pointBorderWidth: 2,
                pointHoverRadius: 4,
                pointHoverBorderWidth: 1,
                pointRadius: 4,
                fill: true,
                backgroundColor: gradientFill,
                borderWidth: 2,
                data: [542, 480, 430, 550, 530, 453, 380, 434, 568, 610, 700, 630]
            }]
        },
        options: gradientChartOptionsConfiguration
    });
}

const initBarChart = () => {
    // Get element from DOM
    var ctx = document.getElementById("barChart").getContext("2d");

    // Colors
    const chartColor = "#92d400";
    const gradientFill = ctx.createLinearGradient(0, 170, 0, 50);
    gradientFill.addColorStop(0, "rgba(146, 212, 0, 0)");
    gradientFill.addColorStop(1, "rgba(146, 212, 0, 0.40)");

    // Draw chart
    var myChart = {
        type: "bar",
        data: {
            labels: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            datasets: [{
                label: "Active Countries",
                backgroundColor: gradientFill,
                borderColor: chartColor,
                pointBorderColor: "#FFF",
                pointBackgroundColor: chartColor,
                pointBorderWidth: 2,
                pointHoverRadius: 4,
                pointHoverBorderWidth: 1,
                pointRadius: 4,
                fill: true,
                borderWidth: 1,
                data: [80, 99, 86, 96, 123, 85, 100, 75, 88, 90, 123, 155]
            }]
        },
        options: {
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
                caretPadding: 10
            },
            responsive: 1,
            scales: {
                yAxes: [{
                    gridLines: 0,
                    gridLines: {
                        zeroLineColor: "transparent",
                        drawBorder: false
                    }
                }],
                xAxes: [{
                    display: 0,
                    gridLines: 0,
                    ticks: {
                        padding: 10,
                        fontColor: "rgba(255,255,255,0.4)",
                        fontStyle: "bold"
                    },
                    gridLines: {
                        zeroLineColor: "transparent",
                        drawTicks: false,
                        display: false,
                        drawBorder: false
                    }
                }]
            },
            layout: {
                padding: {
                    left: 0,
                    right: 0,
                    top: 15,
                    bottom: 15
                }
            }
        }
    };

    var viewsChart = new Chart(ctx, myChart);
}

const initPieChart = () => {
    // Get element from DOM
    var ctx = document.getElementById("pieChart").getContext("2d");

    // Colors
    const chartColor = "#92d400";
    const gradientFill = ctx.createLinearGradient(0, 170, 0, 50);
    gradientFill.addColorStop(0, "rgba(146, 212, 0, 0)");
    gradientFill.addColorStop(1, "rgba(146, 212, 0, 0.40)");

    // Data
    const DATA_COUNT = 5;
    const NUMBER_CFG = { count: DATA_COUNT, min: 0, max: 100 };
    const data = {
        labels: ['Red', 'Orange', 'Yellow', 'Green', 'Blue'],
        datasets: {
            labels: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            datasets: [{
                label: "Active Countries",
                backgroundColor: gradientFill,
                borderColor: chartColor,
                pointBorderColor: "#FFF",
                pointBackgroundColor: chartColor,
                pointBorderWidth: 2,
                pointHoverRadius: 4,
                pointHoverBorderWidth: 1,
                pointRadius: 4,
                fill: true,
                borderWidth: 1,
                data: [80, 99, 86, 96, 123, 85, 100, 75, 88, 90, 123, 155]
            }]
        },
    };

    // Draw chart
    const myChart = {
        type: 'pie',
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Chart.js Pie Chart'
                }
            }
        },
    };

    var pieChart = new Chart(ctx, myChart);
}