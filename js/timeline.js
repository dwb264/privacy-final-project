var eventData, networkData;
var year_counts;
var social_colors;
var event_key = {"Law": "⚖️", "Technology": "🌐", "Revelations": "😮", "Theory": "👩‍🎓", "Social Media": "👥", "Controversy": "🤔"};

var svg = d3.select("svg");
var height = svg.attr("height"), width = svg.attr("width");

var timeScale = d3.scaleTime().domain([new Date("01/01/1993"), new Date("12/31/2018")]).range([0, height]);

d3.queue()
.defer(d3.json, "data/network.json")
.defer(d3.tsv, "data/events.txt")
.defer(d3.json, "data/colors.json")
.await(show_viz)

function show_viz(error, network, events, colors) {
	eventData = events;
	networkData = network;
	social_colors = colors;

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
			var endY = parseFloat(timeScale(endNode.year)) + 40*paper_num[networkData.nodes.indexOf(endNode)];

			return "M" + (width/3 + 40)  + " " + startY + "A 20 50 180 1,0 " + (width/3 + 40) + " " + endY + "";
		})
		.attr("fill", "none")
		.attr("data-start", function(d) { return d.source })
		.attr("data-end", function(d) { return d.target })
		.attr("stroke", "#e8e8e8");

	// Display papers
	var paper = svg.selectAll(".paper")
		.data(networkData.nodes)
		.enter()
		.append("g").attr("class", "paper") 
		.attr("transform", function(d, i) {
			var h = parseFloat(timeScale(d.year)) + 40 * paper_num[i];
			var w = width/3 + 40;
			return "translate(" + w + ", " + h + ")" })
		.on("mouseover", showPaperTooltip)
		.on("mouseout", function(d) {
			d3.select("#paperTooltip").remove();
		})
		
	paper.append("circle")
			.attr("r", 10)
			.attr("fill", function(d) { return social_colors[d.social_network[0]]})
			.on("click", function(d) {
				paths = d3.selectAll(".cite-line path");
				paths.attr("stroke", function() {
					if (d3.select(this).attr("data-start") == d.id || d3.select(this).attr("data-end") == d.id ) {
						return "#4286f4";
					} 
					return "#e8e8e8";
				})
			});

	paper.append("text")
			.text(function (d) { 
				if (d.title.length > 50) return d.title.slice(0,50) + "... (" + d.id + ")" ; 
				return d.title + " (" + d.id + ")";
			})
			.attr("alignment-baseline", "middle")
			.attr("transform", "translate(20,0)");

	// Display events
	svg.selectAll(".event")
		.data(eventData)
		.enter()
		.append("g").attr("class", "event") 
		.attr("transform", function(d, i) {
			var h = parseFloat(timeScale(d.date));
			return "translate(" + (width/3 - 50) + ", " + h + ")" })
		.append("text").attr("class", "title")
			.attr("text-anchor", "end")
			.text(function (d) { return d.title + " " + event_key[d.type]; })
		.on("mouseover", showEventTooltip)
		.on("mouseout", function(d) {
			d3.select("#eventTooltip").remove();
		});

	// Display legend
	svg.append("image")
		.attr("xlink:href", "img/about@2x.png")
		.attr("x", width/3 + 50)
		.attr("y", 100)
		.attr("width", 400)
		.attr("height", 1000)
}

function makeMultiline(text,linelength) {
	var txt = text.split(" ");
	var lines = [];
	var line = "";
	txt.forEach(function(word) {
		if (line.length + word.length < linelength) {
			line += " " + word;
		} else {
			lines.push(line);
			line = word;
		}
	})
	lines.push(line);
	return lines;
}

function showPaperTooltip(d) {
	var g = svg.append("g")
		.attr("id", "paperTooltip")
		.attr("transform", function() {
			return "translate(" + d3.mouse(this)[0] + "," + d3.mouse(this)[1] + ")";
	}) 

	var r = g.append("rect")
		.attr("width", 400)
		.attr("height", 200)
		.attr("fill", "#f8f8f8")
		.attr("stroke", "#4286f4")
		.attr("stroke-width", "2px");

	// Paper title
	var titletext = d.title + " (" + d.id + ")";
	var title = makeMultiline(titletext,50);
	var linenum = 0;
	for (var i = 0; i < title.length; i++) {
		linenum += 1;
		g.append("text")
			.attr("class", "title")
			.text(function() { return title[i]; })
			.attr("y", function() { return 20 * i + 24})
			.attr("x", 10)
			.attr("fill", "#000")
			.attr("font-weight", "bold");
	}

	// Other facts
	g.append("text")
		.attr("class", "paperData")
		.text(function() { return "Sample Size: " + d.sample_size + " | Citations: " + d.citations; })
		.attr("y", function() { return (20 * linenum) + 30})
		.attr("x", 10);
	linenum += 1;
	g.append("text")
		.attr("class", "paperData")
		.text(function() { return "Social Network: " + d.social_network.join(", "); })
		.attr("y", function() { return (20 * linenum) + 40})
		.attr("x", 10);
	linenum += 1;
	g.append("text")
		.attr("class", "paperData")
		.text(function() { return "Sample Country: " + d.sample_country.join(", "); })
		.attr("y", function() { return (20 * linenum) + 40})
		.attr("x", 10);
	linenum += 1;
	g.append("text")
		.attr("class", "paperData")
		.text(function() { return "Method: " + d.study_type.join(", "); })
		.attr("y", function() { return (20 * linenum) + 40})
		.attr("x", 10);
	linenum += 1;

	var variables = makeMultiline("Variables: " + d.variables.join(", "),50);
	for (var i = 0; i < variables.length; i++) {
		g.append("text")
		.attr("class", "paperData")
		.text(function() { return variables[i]})
		.attr("y", function() { return (20 * linenum) + 50})
		.attr("x", 10);
		linenum += 1;
	}
	r.attr("height", linenum * 20 + 50);
}

function showEventTooltip(d) {
	var g = svg.append("g")
		.attr("id", "eventTooltip")
		.attr("transform", function() {
			return "translate(" + (d3.mouse(this)[0]) + "," + d3.mouse(this)[1] + ")";
	}) 

	var r = g.append("rect")
		.attr("width", 400)
		.attr("height", 200)
		.attr("fill", "#f8f8f8")
		.attr("stroke", "#4286f4")
		.attr("stroke-width", "2px");

	// Event facts
	var titletext = d.description;
	var title = makeMultiline(titletext,50);
	var linenum = 0;
	for (var i = 0; i < title.length; i++) {
		linenum += 1;
		g.append("text")
			.attr("class", "title")
			.text(function() { return title[i]; })
			.attr("y", function() { return 20 * i + 24})
			.attr("x", 10)
			.attr("fill", "#000");
	}
	r.attr("height", linenum * 20 + 20);
}

