var network, fulltext, textByYear;
var keywords = [];
var chart, chart2, years;

d3.queue()
.defer(d3.json, "data/network.json")
.defer(d3.json, "data/fulltext.json")
.await(show_viz)

function show_viz(error, net, text) {
	network = net;

	fulltext = text;
	fulltext.forEach(function(d) {
		d.text = d.text.split(". ");
		d.title = network.nodes.filter(function(e) { return e.id == d.paper.toLowerCase(); })[0].title;
	})

	textByYear = d3.nest()
  	.key(function(d) { 
  		var a = d.paper.split(" ")
  		return parseInt(a[a.length - 1]); 
  	})
  	.object(text);

	years = ['x'];
	for (var i = 1999; i < 2019; i++) {
		years.push("01-01-"+String(i));
	}

	var keyword = "facebook"; // Example input
	keywords.push(keyword.toLowerCase());
	var data = find_normalized(keyword);

	chart = c3.generate({
		bindto: "#timeseries",
	    data: {
	        x: 'x',
	        xFormat: '%d-%m-%Y',
	        columns: [
	            years,
	            data
	        ]
	    },
	    axis: {
	        x: {
	            type: 'timeseries',
	            tick: {
	                format: '%Y',
	            }
	        },
	        y: {
	        	label: "% of Total Words",
	        	min: 0,
	        	padding: { bottom: 0 }
	        }
	    },
	    grid: {
	        x: {
	            show: true
	        },
	        y: {
	            show: true
	        }
	    }
	});

	var tag = d3.select("#keywords")
		.append("div");

	tag.append("p").
		text(keyword)
		.on("click", function() { show_context(keyword) });

	tag.append("p")
		.attr("class", "x")
		.text("x")
		.on("click", function() {
			chart.unload({ ids: [keyword] });
			d3.select(this.parentNode).remove();
			keywords.splice(keywords.indexOf(keyword), 1);
		});
}

d3.select("#enter-keyword").on("click", function() {
	var keyword = document.getElementById("search").value;
	if (keyword.trim() != "") {
		document.getElementById("search").value = "";
		show_chart(keyword);
	}
})

// Return papers, # of times, and context of keyword mention
function find(keyword) {
	var results = [];

	fulltext.forEach(function(f) {
		var count = 0;
		var sentences = [];

		f.text.forEach(function(sentence) {
			if (sentence.toLowerCase().indexOf(keyword.toLowerCase()) != -1) {
				count += 1;
				sentences.push(sentence);
			}
		})

		if (sentences.length > 0) {
			var yr = f.paper.split(" ");
			yr = parseInt(yr[yr.length - 1]);

			results.push({
				"paper": f.paper,
				"title": f.title,
				"year": yr,
				"count": count,
				"context": sentences
			})
		}
	})

	return results;
}

function find_normalized(keyword) {
	results = [keyword];

	for (var i = 1999; i < 2019; i++) {
		if (textByYear[i]) {
			var keyword_count = 0;
			var total_wordcount = 0;
			textByYear[i].forEach(function(f) {
				var txt = f.text.join(" ").toLowerCase();
				var re = new RegExp(keyword.toLowerCase(), 'g');
				if (txt.match(re)) keyword_count += txt.match(re).length * keyword.split(" ").length;
				total_wordcount += txt.split(" ").length;
			});
			results.push(parseFloat(keyword_count)/total_wordcount);
		} else {
			results.push(0);
		}
	}

	return results;
}

function show_chart(keyword) {
	keyword = keyword.toLowerCase();
	if (keywords.indexOf(keyword) == -1) {
		keywords.push(keyword);

	var results = find(keyword).sort(function(a,b) {
		if (a.count < b.count) return 1;
		if (a.count > b.count) return -1;
		return 0;
	});

	var data = find_normalized(keyword);

	// Update chart
	chart.load({columns: [data] });

	var tag = d3.select("#keywords")
		.append("div");

	tag.append("p").text(keyword)
		.on("click", function() { show_context(keyword) });

	tag.append("p")
		.attr("class", "x")
		.text("x")
		.on("click", function() {
			chart.unload({ ids: [keyword] });
			d3.select(this.parentNode).remove();
			keywords.splice(keywords.indexOf(keyword), 1);
		});
	}
}

function show_context(keyword) {
	var results = find(keyword);
	results = results.sort(function(a, b) {
		if (a.year < b.year) return -1;
		if (a.year > b.year) return 1;
		return 0;
	})

	var context_div = d3.select("#context");
	context_div.html("");
	context_div.append("h3").text("Context for \"" + keyword + "\"");

	results.forEach(function(paper) {
		context_div.append("h4").text(paper.title + " (" + paper.paper + ")");
		paper.context.forEach(function(sentence) {
			sentence = sentence.toLowerCase().split(keyword).join("<strong>" + keyword + "</strong>");
			context_div.append("p").html(sentence);
		})
	})

	$('html,body').animate({
   		scrollTop: $("#context").offset().top - 50
	});

}

d3.select("#top").on("click", function() {
	$('html,body').animate({scrollTop: 0}, 1000);

})