var margin = {top:20, right:20, bottom: 20, left: 50};

var width = 750 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

var svg = d3.select("#horizontalBars").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var stack = d3.stack();
var x = d3.scaleLinear()
        .domain([0, 100])
        .rangeRound([0, width]),
    y = d3.scaleBand()
        .domain(['2012', '2008', '2004', '2000', '1996'].reverse())
        .rangeRound([0, height])
        .padding(0.33),
    color = d3.scaleOrdinal()
        .domain(['Democrat', 'Independent', 'Republican'])
        .range(['#2166ac', '#ddd', '#b2182b']),
    partyLabels = d3.scaleOrdinal()
        .domain(color.domain())
        .range([1, 47, 88]),
    labels = d3.format(".1f");

d3.csv('data/processed/elections/voter-counts.csv', function(data) {

  // stack em high
  var results = stack.keys(color.domain())(data);

  // create svg group to append things to
  var parties = svg.selectAll('.party')
    .data(results)
      .enter().append('g')
    .attr('class', function(d) { return d.key + '-party party'; })
    .style('fill', function(d) { return color(d.key); });

  // Add the bars for each group
  parties.selectAll('.rect')
    .data(function(d) { return d; })
      .enter().append('rect')
    .attr('x', function(d) { return x(d[0]); })
    .attr('y', function(d) { return y(d.data.Year); })
    .attr('width', function(d) { return x(d[1]) - x(d[0]); })
    .attr('height', y.bandwidth());

  // Add label text to each bar
  parties.selectAll('text')
    .data(function(d) { return d; })
      .enter().append('text')
    //.attr('class', 'title')
    .attr('x', function(d) { return (d[0] < 50) ? x(d[0]) + 5: x(d[1]) - 5; })
    .attr('text-anchor', function(d) { return (d[0] < 50) ? 'start' : 'end'; })
    .attr('y', function(d) { return y(d.data.Year); })
    .attr('dy', y.bandwidth() / 2 + 5)
    .text(function(d) { return labels(d[1] - d[0]) + '%'; })
    .style('fill', function(d) { return ((d[1] - d[0]) > 10) ? '#fff' : '#222'; })
    .style('visibility', function(d) { return ((d[1] - d[0]) > 8) ? 'visible' : 'hidden'; });

  // titles
  svg.selectAll('.text')
    .data(color.domain())
      .enter().append('text')
    .attr('x', function(d) { return x(partyLabels(d)); })
    .text(function(d) { return d; });


  // years axis
  svg.append('g')
    .attr('transform', 'translate(0,0)')
    .attr('class', 'axis')
    .call(d3.axisLeft(y));

  // add the % axis
  //svg.append('g').attr('transform', 'translate(0, 0').call(d3.axisTop(x));

  // add 50% line
  svg.append('line')
    .attr('class', 'indicator')
    .attr('x1', function() { return x(50); })
    .attr('x2', function() { return x(50); })
    .attr('y1', function() { return y('1996'); })
    .attr('y2', function() { return y('2012'); });

});
