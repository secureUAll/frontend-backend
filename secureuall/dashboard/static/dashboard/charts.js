// This function initializes all the charts
const initCharts = () => {
    initVulnsNumbersChart();
    initMachinesRiskLevelChart();
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


const initMachinesRiskLevelChart = () => {
    // Get element from DOM
    var canvas = document.getElementById("machinesRiskLevelChart");
    var ctx = canvas.getContext("2d");

    //Colors
    const gradientFill = [
        'rgba(146, 212, 0, 0.7)',
        'rgba(54, 162, 235, 0.7)',
        'rgba(245,230,52, 0.7)',
        'rgba(243,178,27, 0.7)',
        'rgba(240, 89, 42, 0.7)',
        'rgba(218, 223, 230, 0.7)',
    ];
    const gradientFillHover = [
        'rgba(146, 212, 0, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(245,230,52, 1)',
        'rgba(243,178,27, 1)',
        'rgba(240, 89, 42, 1)',
        'rgba(218, 223, 230, 1)',
    ];
    const borderColor = [
        'rgba(146, 212, 0)',
        'rgba(54, 162, 235)',
        'rgba(245,230,52)',
        'rgba(243,178,27)',
        'rgba(240, 89, 42)',
        'rgba(218, 223, 230)',
      ];

    // Data
    const data = {
        labels: machinesRiskLevelChartLabels,
        datasets: [{
          data: machinesRiskLevelChartValues,
          backgroundColor: gradientFill,
          hoverBackgroundColor: gradientFillHover,
          borderColor: borderColor,
          fill: true,
          borderWidth: 1,
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
                /* labels: {
                     render: 'value',
                     fontColor: '#fff',
                     fontStyle: 'bold',
                     precision: 2
                 } */
                datalabels: {
                    formatter: (value, ctx) => {
                        let datasets = ctx.chart.data.datasets;
                        if (datasets.indexOf(ctx.dataset) === datasets.length - 1) {
                            let sum = datasets[0].data.reduce((a, b) => a + b, 0);
                            let percentage = Math.round((value / sum) * 100) + '%';
                            return percentage;
                        }   else {
                            return percentage;
                       }
                    },
                color: '#fff',
                }
            },
            tooltips: {
                enabled: true,
                mode: 'single',
                callbacks: {
                    label: function (tooltipItems, data) {
                        var i = tooltipItems.index;
                        return "Risk level " + data.labels[i] + ": " + data.datasets[0].data[i] + " %";
                    }
                }
            },
        },
        animation: {
            animateScale: true,
            animateRotate: true
        },
    };

    var pieChart = new Chart(ctx, myChart);

    // Render machines table
    machinesTable = $('#machinesTable').DataTable({
        "lengthMenu": [ 25, 50, 100 ]
    });

    // Listen for search
    machinesTable.on('search', (e, settings) => {
        var search = machinesTable.search();
        console.log("SEARCH by", search);
        // If searching, give feedback and show option to clear
        if (search != "") {
            var text = "Filtered by <strong>" + search + "</strong>.";
            document.getElementById("machinesTableFilterText").innerHTML = text;
            $("#clearFilterMachines").removeClass("d-none");
        // Else, remove clear btn and display message suggesting filtering
        } else {
            $("#machinesTableFilterText").text("No filter applied to table. To filter per risk level click on the risk slice in the graph on the right.");
            $("#clearFilterMachines").addClass("d-none");
        }
    });

    // Listen for clicks on pie chart slices for filtering
    canvas.onclick = function(evt) {
        var activePoints = pieChart.getElementsAtEvent(evt);
        if (activePoints[0]) {
          var chartData = activePoints[0]['_chart'].config.data;
          var idx = activePoints[0]['_index'];
          var label = chartData.labels[idx];

          machinesTable.search("RISK-" + label.toUpperCase());
          machinesTable.draw();
        }
    };

    // on click event, clear filter
    document.getElementById("clearFilterMachines").onclick = function() {
        machinesTable.search("");
        machinesTable.draw();
    }
    
};