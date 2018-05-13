var links = [
	{
		"href": "about.html",
		"title": "About"
	},
	{
		"href": "index.html#svg-container",
		"title": "Timeline"
	},
	{
		"href": "search.html",
		"title": "Keyword Trends"
	},
	{
		"href": "data.html",
		"title": "Raw Data"
	}
]

var nav = d3.select("#nav");

links.forEach(function(link) {
	nav.append("a")
	.attr("href", link.href)
	.text(link.title);
})