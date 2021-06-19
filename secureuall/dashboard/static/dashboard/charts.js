// This function initializes all the charts
const initCharts = () => {
    initVulnsNumbersChart();
    initMachinesRiskLevelChart();
    //initVulnsByGroupChart();
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
    const gradientFill = [
        'rgba(2239, 231, 106, 0.2)',
        'rgba(132, 90, 169, 0.2)',
        'rgba(175, 198, 173, 0.2)',
        'rgba(249, 149, 225, 0.2)',
        'rgba(240, 42, 102, 0.2)',
        'rgba(42, 216, 240, 0.2)',
        'rgba(255, 152, 13, 0.2)',
        'rgba(26, 184, 131, 0.2)',
        'rgba(11, 42, 182, 0.2)',
        'rgba(255, 128, 16, 0.2)',
    ];
    const gradientFillHover = [
        'rgba(239, 231, 106, 0.6)',
        'rgba(132, 90, 169, 0.6)',
        'rgba(175, 198, 173, 0.6)',
        'rgba(249, 149, 225, 0.6)',
        'rgba(240, 42, 102, 0.6)',
        'rgba(42, 216, 240, 0.6)',
        'rgba(255, 152, 13, 0.6)',
        'rgba(26, 184, 131, 0.6)',
        'rgba(11, 42, 182, 0.6)',
        'rgba(255, 128, 16, 0.6)',
    ];
    const borderColor = [
        'rgb(239, 231, 106)',
        'rgb(132, 90, 169)',
        'rgb(175, 198, 173)',
        'rgb(249, 149, 225)',
        'rgb(240, 42, 102)',
        'rgb(42, 216, 240)',
        'rgb(255, 152, 13)',
        'rgba(26, 184, 131)',
        'rgba(11, 42, 182)',
        'rgba(255, 128, 16)',
    ];

    // Draw chart
    var myChart = {
        type: "bar",
        data: {
            labels: vulnsByGroupChartLabels,
            datasets: [{
                label: "Amount",
                backgroundColor: gradientFill,
                hoverBackgroundColor: gradientFillHover,
                borderColor: borderColor,
                fill: true,
                borderWidth: 1,
                data: vulnsByGroupChartValues
            }]
        },
        options: {
            responsive: true,
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

    // on click event, filter
    canvas.onclick = function(evt) {
        var activePoints = pieChart.getElementsAtEvent(evt);
        if (activePoints[0]) {
          var chartData = activePoints[0]['_chart'].config.data;
          var idx = activePoints[0]['_index'];
  
          var label = chartData.labels[idx];
          var table = document.getElementById("machinesTable");
          var tr =  table.getElementsByTagName("tr");

          var i, td;
          for (i = 0; i < tr.length; i++) {
            td = tr[i].querySelector("td span");
            var regex = /^[a-zA-Z]+$/;
            if (!label.match(regex)) {
                td = tr[i].getElementsByTagName("td")[1];
            }
            if (td) {
                if (td.innerText.indexOf(label) > -1) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
          }
          var text = "Filtered by risk level <strong>" + label + "</strong>.";
          document.getElementById("machinesTableFilterText").innerHTML = text;
          $("#clearFilterMachines").removeClass("d-none");
        }
    };

    // on click event, clear filter
    document.getElementById("clearFilterMachines").onclick = function() {
        var table  = document.getElementById("machinesTable");
        var tr =  table.getElementsByTagName("tr");

        var i;
        for (i = 0; i < table.rows.length; i++) {
            tr[i].style.display = "";
        }

        $("#machinesTableFilterText").text("No filter applied to table. ");
        $("#clearFilterMachines").addClass("d-none");
    }
    
};