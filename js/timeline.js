var eventData, networkData;
var year_counts;

var svg = d3.select("svg");
var height = svg.attr("height"), width = svg.attr("width");

var timeScale = d3.scaleTime().domain([new Date("01/01/1993"), new Date("12/31/2018")]).range([0, height]);

d3.queue()
.defer(d3.json, "data/network.json")
.defer(d3.tsv, "data/events.txt")
.await(show_viz)

function show_viz(error, network, events) {
	eventData = events;
	networkData = network;

	// Convert date strings to objects
	eventData.forEach(function(d) 			{ d.date = new Date(d.date); });
	networkData.nodes.forEach(function(d) 	{ d.year = new Date("01/01/" + String(d.year)); });

	networkData.nodes.sort(function(x, y) {
		return d3.ascending(x.year, y.year);
	});

	// Display date axis
	var yAxis = d3.axisLeft(timeScale);
	svg.append("g").attr("transform","translate(" + (width/3) + ",0)").attr("class","axis").call(yAxis);


	// How many papers for each year
	year_counts = d3.nest()
		.key(function(d) { return d.year.getFullYear() })
		.rollup(function(v) {return v.length})
		.entries(networkData.nodes);
	paper_num = [];
	year_counts.forEach(function(y) {
		for (var i = 0; i < y.value; i++) {
			paper_num.push(i);
		}
	})

	// Display links
	var citations = svg.selectAll(".cite-line")
		.data(networkData.links)
		.enter()
		.append("g").attr("class", "cite-line");

	citations.append("path")
		.attr("d", function(d) {
			var startNode = networkData.nodes.filter(function(n) { return n.id === d.source; })[0];
			var endNode = networkData.nodes.filter(function(n) { return n.id === d.target; })[0];

			var startY = parseFloat(timeScale(startNode.year)) + 40*paper_num[networkData.nodes.indexOf(startNode)];
			var endY = timeScale(endNode.year);

			return "M" + (width/3 + 20)  + " " + startY + "A 20 50 180 1,0 " + (width/3 + 20) + " " + endY + "";
		}).attr("fill", "none").attr("stroke", "#e8e8e8");

	// Display papers
	var paper = svg.selectAll(".paper")
		.data(networkData.nodes)
		.enter()
		.append("g").attr("class", "paper") 
		.attr("transform", function(d, i) {
			var h = parseFloat(timeScale(d.year)) + 40 * paper_num[i];
			var w = width/3 + 20;
			return "translate(" + w + ", " + h + ")" })
		
	paper.append("circle")
			.attr("r", 10)
			.attr("fill", "green")

	paper.append("text")
			.text(function (d) { return d.id; })
			.attr("alignment-baseline", "middle")
			.attr("transform", "translate(20,0)");

	// Display events
	svg.selectAll(".event")
		.data(eventData)
		.enter()
		.append("g").attr("class", "event") 
		.attr("transform", function(d, i) {
			var h = parseFloat(timeScale(d.date));
			return "translate(" + (width/3 - 60) + ", " + h + ")" })
		.append("text").attr("class", "title")
			.attr("text-anchor", "end")
			.text(function (d) { return d.title; });


	

	
}

