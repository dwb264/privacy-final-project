var network, fulltext;

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

}

d3.select("#search").on("keyup", function() {
	var keyword = this.value;
	var results = find(keyword).sort(function(a,b) {
		if (a.count < b.count) return 1;
		if (a.count > b.count) return -1;
		return 0;
	});

	var cols = ["count"];
	cols.push.apply(cols, results.map(function(d) { return d.count; }));
	var cats = results.map(function(d) { return d.paper; });

	var chart = c3.generate({
	    bindto: '#frequency',
	    data: {
	      columns: [
	        cols,
	      ],
	      type: "bar",
	    },

	    axis: {
	        x: {
	            type: 'category',
	            categories: cats
	        },
	        rotated: true
    	}
	});

	var years = ['x'];
	for (var i = 1999; i < 2019; i++) {
		years.push(String(i));
	}

	var data = ["count of " + keyword];
	for (var i = 1999; i < 2019; i++) {
		var r = results.filter(function(d) { return d.year == i});
		if (!(r)) {
			data.push(0);
		} else {
			data.push(d3.sum(r, function(d) { return d.count }));
		}
	}

	var chart2 = c3.generate({
	    bindto: '#timeseries',
	    data: {
	        x: 'x',
	        xFormat: '%Y',
	        columns: [
	            years,
	            data
	        ]
	    },
	    axis: {
	        x: {
	            type: 'timeseries',
	            tick: {
	                format: '%Y'
	            },
	            padding: {top:0, bottom:0}
	        },
	        y: {
	        	padding: {top:10, bottom:0}
	        }
	    }
	});

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

