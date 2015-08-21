var pieData = [
	{
		value : 30,
		color : "#4ACAB4",
		label: "Games Carried"
	},
	{
		value: 60,
		color:"#878BB6",
		label: "Games Not Carried"
	}

];

var countries= document.getElementById("post-carry-rate").getContext("2d");
new Chart(countries).Pie(pieData, pieOptions);

var pieOptions = {
	segmentShowStroke : false,
	animateScale : true
}