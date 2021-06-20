
// This function initializes all the charts
const initCharts = () => {
    initVulsRiskLevelChart();
    initVulnsByScanChart();
}


const initVulsRiskLevelChart = () => {
    // Get element from DOM
    var canvas = document.getElementById("vulnerabilitiesByRiskLevel");
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
        labels: vulsRiskLevelChartLabels,
        datasets: [{
          data: vulsRiskLevelChartValues,
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
                      } else {
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
                        return "Risk level " + data.labels[i];
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
          var table = document.getElementById("vulnerabilitiesTable");
          var tr =  table.getElementsByTagName("tr");

          var i, td;
          for (i = 0; i < tr.length; i++) {
            td = tr[i].querySelector("td span");
            var regex = /^[a-zA-Z]+$/;
            if (!label.match(regex)) {
                td = tr[i].getElementsByTagName("td")[0];
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
          document.getElementById("vulnerabilitiesTableFilterText").innerHTML = text;
          $("#clearFilterVulnerabilities").removeClass("d-none");
        }
    };

    // on click event, clear filter
    document.getElementById("clearFilterVulnerabilities").onclick = function() {

        $("#clearFilterVulnerabilities").addClass("d-none");

        var table  = document.getElementById("vulnerabilitiesTable");
        var tr =  table.getElementsByTagName("tr");

        var i;
        for (i = 0; i < table.rows.length; i++) {
            tr[i].style.display = "";
        }

        $("#vulnerabilitiesTableFilterText").text("No filter applied to table. To filter per risk level click on the risk slice in the graph above.");
    }

};

const initVulnsByScanChart = () => {
    // Get element from DOM
    const ctx = document.getElementById('lineChart').getContext("2d");

    // Colors
    const chartColor = "#ed9dd8";
    const gradientFill = ctx.createLinearGradient(0, 170, 0, 50);
    gradientFill.addColorStop(0, "rgba(237, 157, 216, 0)");
    gradientFill.addColorStop(1, "rgba(237, 157, 216, 0.40)");

    // Draw chart
    myChart = new Chart(ctx, {
        type: 'line',
        responsive: true,
        data: {
            labels: vulnsByScanChartLabels,
            datasets: [{
                label: "Vulnerabilities found",
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
                data: vulnsByScanChartValues,
            }]
        },
        options: {
            responsive: true,
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        callback: function(value) {if (value % 1 === 0) {return value;}}
                    }
                }]
            }
        }
        //options: gradientChartOptionsConfiguration,
    });
}