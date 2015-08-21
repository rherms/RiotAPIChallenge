var pieData = [
	{
		value : 40,
		color : "#4ACAB4",
		label: "Games Carried"
	},
	{
		value: 20,
		color:"#878BB6",
		label: "Games Not Carried"
	}

];

var countries= document.getElementById("countries").getContext("2d");
new Chart(countries).Pie(pieData, pieOptions);

var pieOptions = {
	segmentShowStroke : false,
	animateScale : true
}