def d3_linechart(df, ycol='y', xcol=None, interactive=True, fname='linechart.html'):
    """Create a D3 line plot from a pandas numeric series.
    This is a prototype of how to do this and we can think about making
    more elaborate plots.
    Parameters
    ----------
    df: DataFrame
        DataFrame with y values in column `ycol`
    ycol: str, optional
        Name of the column containing y values. Default: 'y'
    xcol: str, optional
        Name of the column containing x values. Default: None in which case
        y values are plotted in order.
    interactive: bool
        Should we open your html in a web browser. Default: True.
    fname: str
        If `interactive` we need to save the html to a file so we can open it
        in the browser.
    Returns
    -------
    html: str
        The html of the barchart
    Reference
    ---------
    http://bl.ocks.org/mbostock/3883245
    """

    plot_df = pd.DataFrame()
    plot_df['y'] = df[ycol]
    if xcol:
        plot_df['x'] = df[xcol]
    else:
        plot_df['x'] = np.arange(plot_df.shape[0])

    html = Template("""<!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    <style>
    body {
      font: 10px sans-serif;
    }
    .axis path,
    .axis line {
      fill: none;
      stroke: #000;
      shape-rendering: crispEdges;
    }
    .line {
      fill: none;
      stroke: steelblue;
      stroke-width: 1.5px;
    }
    </style>
    </style>
    </head>
    <body>
    <!-- TODO source this script locally -->
    <script src="http://d3js.org/d3.v3.min.js"></script>
    <script>
    var margin = {top: 20, right: 20, bottom: 30, left: 50},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;
    var data = JSON.parse(' $json ');
    var svg = d3.select("body").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    var x = d3.scale.linear()
        .range([0, width])
        .domain(d3.extent(data, function(d) {return d.x; }))
    var y = d3.scale.linear()
        .range([height, 0])
        .domain(d3.extent(data, function(d) {return d.y; }))
    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");
    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");
    var line = d3.svg.line()
        .x(function(d) { return x(d.x); })
        .y(function(d) { return y(d.y); });
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);
    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
    var path = svg.append("path")
        .datum(data)
        .attr("class", "line")
    </script>
    </body>
    </html>
    """).substitute(json=df.to_json(orient='records'))

    # TODO write file to standardized PLOT_DIR
    with open(fname, 'w') as f:
        f.write(html)
    if interactive:
        webbrowser.open_new_tab('file://' + os.path.join(os.getcwd(), fname))
    return html
