var barData = {
    labels : ["Infinity Edge","BoRK","BloodThirster","Banshee's Veil","Phantom Dancer","Guardian Angel"],
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
var income = document.getElementById("income").getContext("2d");
new Chart(income).Bar(barData, {
    scaleShowGridLines: false,
    barStrokeWidth : 1,
    barDatasetSpacing : 1, 
});