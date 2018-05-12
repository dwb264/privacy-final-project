var network, fulltext, textByYear;
var keywords = [];
var chart, years;

d3.queue()
.defer(d3.json, "data/network.json")
.defer(d3.json, "data/fulltext.json")
.await(show_viz)

function show_viz(error, net, text) {
	network = net;

	fulltext = text;
	fulltext.forEach(function(d) {
		d.text = d.text.split(". ");
	})

	textByYear = d3.nest()
  	.key(function(d) { 
  		var a = d.paper.split(" ")
  		return parseInt(a[a.length - 1]); 
  	})
  	.rollup(function(v) { 
  		return v;
  	})
  	.object(text);

	years = ['x'];
	for (var i = 1999; i < 2019; i++) {
		years.push("01-01-"+String(i));
	}
}

d3.select("#search").on("change", function() {
	var keyword = this.value;
	if (keywords.indexOf(keyword) == -1) {
		keywords.push(keyword);

	var results = find(keyword).sort(function(a,b) {
		if (a.count < b.count) return 1;
		if (a.count > b.count) return -1;
		return 0;
	});

	var data = find_normalized(keyword);

	if (!(chart)) {
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
		    }
		});

	} else {
		chart.load({columns: [data] });
	}

	var tag = d3.select("#keywords")
		.append("div");
	tag.append("p").text(keyword);
	tag.append("p")
		.attr("class", "x")
		.text("x")
		.on("click", function() {
			chart.unload({ ids: [keyword] });
			d3.select(this.parentNode).remove();
			keywords.splice(keywords.indexOf(keyword), 1);
		});
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
