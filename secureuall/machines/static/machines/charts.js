// This function initializes all the charts
const initCharts = () => {
    initVulnsByGroupChart();
    initVulsRiskLevelChart();
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
            labels: initVulnsByGroupChartLabels,
            datasets: [{
                label: "Amount",
                backgroundColor: gradientFill,
                hoverBackgroundColor: gradientFillHover,
                borderColor: chartColor,
                fill: true,
                borderWidth: 1,
                data: initVulnsByGroupChartValues
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


const initVulsRiskLevelChart = () => {
    // Get element from DOM
    var ctx = document.getElementById("vulnerabilitiesByRiskLevel").getContext("2d");

    // Colors
    const chartColor = "#92d400";

    // Data
    const DATA_COUNT = 5;
    const NUMBER_CFG = { count: DATA_COUNT, min: 0, max: 100 };
    const data = {
        labels: [ '1', '2', '3', '4', '5' ],
        datasets: [{
          data: vulsRiskLevelChartValues,
          /*
          // Multicolor
          backgroundColor: [ '#92d400', '#42d3b8', '#9878d3', '#f3b21b', '#f0592a' ],
          pointHoverBackgroundColor: [ '#7ab300', '#2cbaa0', '#7b52c7', '#da9c0b','#d73e0f' ]
          */
          /*
          // Green variation
          backgroundColor: [ '#92d400', '#7ab300', '#578000', '#344d00', '#111a00' ],
          pointHoverBackgroundColor: [ '#8bcc00', '#699900', '#466600', '#233300','#000000' ]
          */
          // Green variation smooth
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
                }
            },
            tooltips: {
                 enabled: true
            }
        },
    };

    var pieChart = new Chart(ctx, myChart);
};