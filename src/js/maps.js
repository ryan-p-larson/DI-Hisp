var width = 250,
    height = 175;

/*var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);*/

var path = d3.geoPath()
    .pointRadius(2);

var color = d3.scaleQuantile()
    // Most sensible threshold based on histogram of values
    //.domain([2, 4, 6, 8, 12, 16])
    .range(['#ffffb2','#fed976','#feb24c','#fd8d3c','#fc4e2a','#e31a1c']);


// small multiples
d3.json('data/processed/maps/county-populations.json', function(data) {

  //save the geo data
  var counties = topojson.feature(data, data.objects.counties),
    iowa = topojson.merge(data, data.objects.counties.geometries);

  // Set up the projections using the data to set projection scale
  path.projection(d3.geoConicConformal()
      .parallels([42 + 4 / 60, 43 + 16 / 60])
      .rotate([93 + 30 / 60, -41 - 30 / 60])
      .fitSize([width, height], counties));

  // years
  var years = ['1992', '1996', '2000', '2004', '2008', '2012'];

  color.domain(createEqualizedScale(counties.features, years, 6));

  //loop to make each map
  years.forEach(function(d) {

    // hold the year
    var year = d;

    //add small multiple map
    var svg = d3.select("#multiples").append("svg")
        .attr('id', year)
        .attr("width", width)
        .attr("height", height);

    svg.selectAll('path')
            .data(counties.features)
        .enter().append('path')
        .attr('class', 'tract')
        .attr('d', path)
        .style('fill', function(d) { return color(d.properties[year]); });

    // State outline
    svg.append('path')
        .datum(iowa)
        .attr('class', 'state')
        .attr('d', path);

    // And finally the year
    svg.append('text')
      .attr('class', 'title')
      .attr('x', width / 2)
      .attr('y', height)
        .text(year);
  });
//end json call
});

// Create large map
d3.json('data/processed/maps/2014-tracts.json', function(data) {

  var width = 600,
    height = 450;

    var svg = d3.select("body").append("svg")
      .attr("width", width)
      .attr("height", height);

    // Create vars to hold different levels of granulairty
    var tracts = topojson.feature(data, data.objects.tracts),
        counties = topojson.mesh(data, data.objects.tracts, function(a, b) {
            return census(a.id) !== census(b.id);
        }),
        iowa = topojson.merge(data, data.objects.tracts.geometries);

    // Set up the projections using the data to set projection scale
    path.projection(d3.geoConicConformal()
        .parallels([42 + 4 / 60, 43 + 16 / 60])
        .rotate([93 + 30 / 60, -41 - 30 / 60])
        .fitSize([width, height], tracts));

    // Census tracts
    svg.selectAll('path')
            .data(tracts.features)
        .enter().append('path')
        .attr('class', 'tract')
        .attr('d', path)
        .style('fill', function(d) {
          return color(d.properties.hisp_perc);
        })
        .on('mouseover', mouseover);

    // Counties
    svg.append('path')
        .datum(counties)
        .attr('class', 'county')
        .attr('d', path);

    // State outline
    svg.append('path')
        .datum(iowa)
        .attr('class', 'state')
        .attr('d', path);

    // And finally the year
    svg.append('text')
      .attr('class', 'title')
      .attr('x', width / 2)
      .attr('y', height-15)
        .text('2014 Hispanic Population Density\nCensus tracts');
});



//====| Interactions |=====\\

//Mouse over
function mouseover(geoFeature) {
  console.log(geoFeature);
}

//Quantile from all points
function createEqualizedScale(data, vars, binN) {
  // create an array that will hold every percentage from every county
  var points = [];

  data.forEach(function(d) {
    // Keep the  string outside of scope
    var tempCounty = d;

    // Push all of it's percentages
    vars.forEach(function(d) { points.push(tempCounty.properties[d]); });
  });

  return points;
}

function census(tract) {
    var county = tract.substring(0, 5);
    return county;
}


//legend stuff
var legend = svg.append("g")
  .attr("class", "legend")
  .attr("transform", "translate(20,20)");

var legendQuant = d3.legendColor()
  .labelFormat(d3.format(".2f"))
  //.useClass(true)
  .title('Hispanic Population Density')
  .shapeHeight(20)
  .shapeWidth(20)
  .shapePadding(10)
  .labels(['< 0.5%', '  0.75%', '  1.25%', '  2.0%', '  3.5%', '> 5.0%'])
  .scale(color);

svg.select(".legend")
  .call(legendQuant);