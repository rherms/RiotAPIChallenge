var barData = {
    labels : ["Thresh","Bard","Nami","Janna","Braum","Brand"],
    datasets : [
      {
        fillColor : "#48A497",
        strokeColor : "#48A4D1",
        data : [456,479,324,569,702,600]
      },
      {
        fillColor : "rgba(73,188,170,0.4)",
        strokeColor : "rgba(72,174,209,0.4)",
        data : [364,504,605,400,345,320]
      }
    ]
}
var graph = document.getElementById("champion-champion-graph").getContext("2d");
new Chart(graph).Bar(barData, {
    scaleShowGridLines: false,
    barStrokeWidth : 1,
    barDatasetSpacing : 1, 
});