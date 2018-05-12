var network, fulltext;
var keywords = [];
var chart;

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

	var years = ['x'];
	for (var i = 1999; i < 2019; i++) {
		years.push(String(i));
	}

	chart = c3.generate({
		bindto: "#timeseries",
	    data: {
	        x: 'x',
	        xFormat: '%Y',
	        columns: [
	            years,
	            ['Count of Papers', 1,0,0,1,1,1,3,1,4,1,4,7,7,10,5,10,7,8,0,1]
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
	        	min: 0,
	        	padding: { bottom: 0 }
	        }
	    }
	});
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

	var data = [keyword];
	for (var i = 1999; i < 2019; i++) {
		var r = results.filter(function(d) { return d.year == i});
		if (!(r)) {
			data.push(0);
		} else {
			data.push(d3.sum(r, function(d) { return d.count }));
		}
	}

	chart.load({columns: [data] });

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

