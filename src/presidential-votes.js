var width = 500,
    height = 380;

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

var stack = d3.stack();
var x = d3.scaleLinear().domain([0, 100]).rangeRound([50, width]),
    y = d3.scaleBand().domain(['2012', '2008', '2004', '2000', '1996'].reverse()).rangeRound([0, height]).padding(0.25),
    color = d3.scaleOrdinal().domain(['Democrat', 'Independent', 'Republican']).range(['#b2182b', '#ddd', '#2166ac']);

d3.csv('data/processed/elections/voter-counts.csv', function(data) {

  // stack em high
  var results = stack.keys(color.domain())(data);

  // create svg group to append things to
  var parties = svg.selectAll('.party')
    .data(results)
    .enter().append('g')
    .attr('class', 'party')
    .attr('fill', function(d) { return color(d.key); });

  parties.selectAll('.rect')
    .data(function(d) { return d; })
    .enter().append('rect')
    .attr('x', function(d) { return x(d[0]); })
    .attr('y', function(d) { return y(d.data.Year); })
    .attr('width', function(d) { return x(d[1]) - x(d[0]); })
    .attr('height', y.bandwidth());


  // years axis
  svg.append('g')
    .attr('transform', 'translate(50,0)')
    .attr('class', 'axis')
    .call(d3.axisLeft(y));

  // add the % axis
  svg.append('g')
    .attr('transform', 'translate(0, 15)')
    .call(d3.axisTop(x));


  // add 50% line
  svg.append('line')
    .attr('class', 'indicator')
    .attr('x1', function() { return x(50); })
    .attr('x2', function() { return x(50); })
    .attr('y1', function() { return y('1996'); })
    .attr('y2', function() { return y('2012'); });

});
