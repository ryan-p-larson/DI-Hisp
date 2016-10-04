var margin = {top:20, right:50, bottom: 20, left:50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var svg = d3.select('#horizontalBars').append('svg')
  .attr('class', 'barChart')
  .attr('width', width + margin.left + margin.right)
  .attr('height', height + margin.top + margin.bottom)
    .append('g')
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// scales
// // x is value, y is year, color is race
var x = d3.scaleLinear().domain([0, 1482]).range([0, width]),
    y = d3.scaleBand()
      .domain(['1996', '2000', '2004', '2008', '2012'])
      .rangeRound([0, height])
      .padding(0.2)
      .align(0.1),
    color = d3.scaleOrdinal(d3.schemeCategory10);

var stack = d3.stack();

// save the races for use
var races = ['Hispanic', 'Black', 'Asian', 'White'];

d3.csv('data/processed/elections/election-voting-populations.csv', function(data) {

  var layers = stack.keys(races)(data);

  //Create svg groups from d3.stack()
  var g = svg.selectAll('.races')
    .data(layers)
    .enter().append('g')
    .attr('class', function(d) { return d.key; })
    .attr('fill', function(d) { console.log(d); return color(d.key); });

    // Temp mouseover titles until a universal tooltip can be written
    g.append('title').text(function(d) { console.log(d);return d.key; });

    //Add the bars
    g.selectAll('rect')
      .data(function(d) { return d; })
      .enter().append('rect')
      .attr('x', function(d) { return x(d[0]); })
      .attr('y', function(d) { return y(d.data.Year); })
      .attr('height', y.bandwidth())
      .attr('width', function(d) { return x(d[1]) - x(d[0]); });




});
