var colors = d3.scaleSequential(d3.interpolateViridis).domain([1999,2018]);

var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height"),
    node,
    link;

svg.append('defs').append('marker')
    .attrs({'id':'arrowhead',
        'viewBox':'-0 -5 10 10',
        'refX':13,
        'refY':0,
        'orient':'auto',
        'markerWidth':5,
        'markerHeight':5,
        'xoverflow':'visible'})
    .append('svg:path')
    .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
    .attr('fill', '#999')
    .style('stroke','none');

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function (d) {return d.id;}))
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(width / 2, height / 2));

d3.json("data/network.json", function (error, graph) {
    if (error) throw error;
    update(graph.links, graph.nodes);
})

function update(links, nodes) {
    link = svg.selectAll(".link")
        .data(links)
        .enter()
        .append("line")
        .attr("class", "link")
        .attr("stroke", "#999")
        .attr('marker-end','url(#arrowhead)')

    edgepaths = svg.selectAll(".edgepath")
        .data(links)
        .enter()
        .append('path')
        .attrs({
            'class': 'edgepath',
            'fill-opacity': 0,
            'stroke-opacity': 0,
            'id': function (d, i) {return 'edgepath' + i}
        })
        .style("pointer-events", "none");

    node = svg.selectAll(".node")
        .data(nodes)
        .enter()
        .append("g")
        .attr("class", "node")
        .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                //.on("end", dragended)
        );

    node.append("circle")
        .attr("r", 5)
        .style("fill", function (d, i) {
            return colors(d.year);
        })

    simulation
        .nodes(nodes)
        .on("tick", ticked);

    simulation.force("link")
        .links(links);
}

function ticked() {
    link
        .attr("x1", function (d) {return d.source.x;})
        .attr("y1", function (d) {return d.source.y;})
        .attr("x2", function (d) {return d.target.x;})
        .attr("y2", function (d) {return d.target.y;});

    node
        .attr("transform", function (d) {return "translate(" + d.x + ", " + d.y + ")";})
        .attr("cx", function(d) { return d.x = Math.max(10, Math.min(width - 10, d.x)); })
        .attr("cy", function(d) { return d.y = Math.max(10, Math.min(height - 10, d.y)); });;

    edgepaths.attr('d', function (d) {
        return 'M ' + d.source.x + ' ' + d.source.y + ' L ' + d.target.x + ' ' + d.target.y;
    });

}

function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart()
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}
