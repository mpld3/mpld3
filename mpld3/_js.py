"""Some javascript snippets which are used in _objects.py"""


CONSTRUCT_SVG_PATH = """
    // This function constructs a mapped SVG path
    // from an input data array
    var construct_SVG_path = function(data, xmap, ymap){
       var result = "";
       for (var i=0;i<data.length;i++){
          result += data[i][0];
          if(data[i][0] == 'Z'){
            continue;
          }
          for (var j=0;j<data[i][1].length;j++){
            if(j % 2 == 0){
               result += " " + xmap(data[i][1][j]);
            }else{
               result += " " + ymap(data[i][1][j]);
            }
          }
          result += " ";
       }
       return result;
     };
"""


FIGURE_CLASS = """
    function Figure(figid, width, height){
      this.figid = figid;
      this.root = d3.select(figid);
      this.width = width;
      this.height = height;
      this.axes = [];
    }

    Figure.prototype.draw = function(){
      this.canvas = this.root.append('svg:svg')
                                 .attr('class', 'figure')
                                 .attr('width', this.width)
                                 .attr('height', this.height);
      for (var i=0; i<this.axes.length; i++){
        this.axes[i].draw();
      }
    };

    Figure.prototype.reset = function(duration){
      duration = (typeof duration !== 'undefined') ? duration : 750;
      for (var i=0; i<this.axes.length; i++){
        this.axes[i].prep_reset();
      }

      var transition = function(t){
        for (var i=0; i<this.axes.length; i++){
          this.axes[i].xdom(this.axes[i].xdom.domain(this.axes[i].ix(t)));
          this.axes[i].ydom(this.axes[i].ydom.domain(this.axes[i].iy(t)));

          // don't propagate: this will be done as part of the loop.
          this.axes[i].zoomed(false);
        }
      }.bind(this)

      d3.transition().duration(duration)
                     .tween("zoom", function(){return transition;});

      for (var i=0; i<this.axes.length; i++){
        this.axes[i].finalize_reset();
      }
    };
"""


AXES_CLASS = """
    function Axes(fig, bbox,
                  xlim, ylim,
                  xscale, yscale,
                  xdomain, ydomain,
                  xgridOn, ygridOn,
                  axclass, clipid){
      this.axnum = fig.axes.length;
      fig.axes.push(this);

      this.fig = fig;
      this.bbox = bbox;
      this.xlim = xlim;
      this.ylim = ylim;
      this.xdomain = xdomain;
      this.ydomain = ydomain;
      this.xscale = xscale;
      this.yscale = yscale;
      this.xgridOn = xgridOn;
      this.ygridOn = ygridOn;
      this.axclass = (typeof axclass !== 'undefined') ? axclass : "axes";
      this.clipid = (typeof clipid != 'undefined') ? clipid : "clip";

      this.sharex = [];
      this.sharey = [];
      this.elements = [];

      this.position = [this.bbox[0] * this.fig.width,
                       (1 - this.bbox[1] - this.bbox[3]) * this.fig.height];
      this.width = bbox[2] * this.fig.width;
      this.height = bbox[3] * this.fig.height;

      if(this.xscale === 'log'){
        this.xdom = d3.scale.log();
      }else if(this.xscale === 'date'){
        this.xdom = d3.time.scale();
      }else{
        this.xdom = d3.scale.linear();
      }

      if(this.yscale === 'log'){
        this.ydom = d3.scale.log();
      }else if(this.yscale === 'date'){
        this.ydom = d3.time.scale();
      }else{
        this.ydom = d3.scale.linear();
      }

      this.xdom.domain(this.xdomain)
            .range([0, this.width]);

      this.ydom.domain(this.ydomain)
            .range([this.height, 0]);

      if(this.xscale === 'date'){
         this.xmap = d3.time.scale()
                           .domain(this.xdomain)
                           .range(this.xlim);
         this.x = function(x){return this.xdom(this.xmap.invert(x));}
      }else if(this.xscale === 'log'){
         this.xmap = this.xdom;
         this.x = this.xdom;
      }else{
         this.xmap = this.xdom;
         this.x = this.xdom;
      }

      if(this.yscale === 'date'){
         this.ymap = d3.time.scale()
                              .domain(this.ydomain)
                              .range(this.ylim);
         this.y = function(y){return this.ydom(this.ymap.invert(y));}
      }else if(this.xscale === 'log'){
         this.ymap = this.ydom;
         this.y = this.ydom;
      }else{
         this.ymap = this.ydom;
         this.y = this.ydom;
      }
    }

    Axes.prototype.draw = function(){
      this.zoom = d3.behavior.zoom()
                          .x(this.xdom)
                          .y(this.ydom)
                          .on("zoom", this.zoomed.bind(this));

      this.baseaxes = this.fig.canvas.append("g")
                             .attr('transform', 'translate('
                                                 + this.position[0] + ','
                                                 + this.position[1] + ')')
                             .attr('width', this.width)
                             .attr('height', this.height)
                             .attr('class', "baseaxes")
                             .call(this.zoom);

      this.axesbg = this.baseaxes.append("svg:rect")
                             .attr("width", this.width)
                             .attr("height", this.height)
                             .attr("class", "axesbg");

      this.clip = this.baseaxes.append("svg:clipPath")
                          .attr("id", this.clipid)
                          .append("svg:rect")
                             .attr("x", 0)
                             .attr("y", 0)
                             .attr("width", this.width)
                             .attr("height", this.height)

      this.axes = this.baseaxes.append("g")
                           .attr("class", this.axclass)
                           .attr("clip-path", "url(#" + this.clipid + ")");

      for(var i=0; i<this.elements.length; i++){
        this.elements[i].draw();
      }
    };

    Axes.prototype.zoomed = function(propagate){
      // propagate is a boolean specifying whether to propagate movements
      // to shared axes, specified by sharex and sharey.  Default is true.
      propagate = (typeof propagate == 'undefined') ? true : propagate;

      //console.log(this.zoom.translate());
      //console.log(this.zoom.scale());
      //console.log(this.zoom.x().domain());
      //console.log(this.zoom.y().domain());

      for(var i=0; i<this.elements.length; i++){
        this.elements[i].zoomed();
      }

      if(propagate){
        // update shared x axes
        for(var i=0; i<this.sharex.length; i++){
          this.sharex[i].zoom.x().domain(this.zoom.x().domain());
          this.sharex[i].zoomed(false);
        }
        // update shared y axes
        for(var i=0; i<this.sharey.length; i++){
          this.sharey[i].zoom.y().domain(this.zoom.y().domain());
          this.sharey[i].zoomed(false);
        }
      }
    };

    Axes.prototype.add_element = function(element){
      this.elements.push(element);
    };

    Axes.prototype.prep_reset = function(){
      // interpolate() does not work on dates, so we map dates to numbers,
      // interpolate the numbers, and then invert the map.
      // we use the same strategy for log, so the interpolation will be smooth.
      // There probably is a cleaner approach...

      if (this.xscale === 'date'){
        var start = this.xdom.domain();
        var end = this.xdomain;
        var interp = d3.interpolate(
                [this.xmap(start[0]), this.xmap(start[1])],
                [this.xmap(end[0]), this.xmap(end[1])]);
        this.ix = function(t){
          return [this.xmap.invert(interp(t)[0]),
                  this.xmap.invert(interp(t)[1])];
        }
      }else{
        this.ix = d3.interpolate(this.xdom.domain(), this.xlim);
      }

      if (this.yscale === 'date'){
        var start = this.ydom.domain();
        var end = this.ydomain;
        var interp = d3.interpolate(
                [this.ymap(start[0]), this.ymap(start[1])],
                [this.ymap(end[0]), this.ymap(end[1])]);
        this.iy = function(t){
          return [this.ymap.invert(interp(t)[0]),
                  this.ymap.invert(interp(t)[1])];
        }
      }else{
        this.iy = d3.interpolate(this.ydom.domain(), this.ylim);
      }
    }

    Axes.prototype.finalize_reset = function(){
      this.zoom.scale(1).translate([0, 0]);
    }

    Axes.prototype.reset = function(){
      this.prep_reset();
      d3.transition().duration(750).tween("zoom", function() {
        return function(t) {
          this.zoom.x(this.xdom.domain(this.ix(t)))
                   .y(this.ydom.domain(this.iy(t)));
          this.zoomed();
        };
      });
      this.finalize_reset();
    };
"""


AXIS_CLASS = """
    function Axis(axes, position){
      this.axes = axes;
      this.position = position;
      if (position == "bottom"){
        this.transform = "translate(0," + this.axes.height + ")";
        this.scale = this.axes.xdom;
        this.class = "x axis";
      }else if (position == "top"){
        this.transform = "translate(0,0)"
        this.scale = this.axes.xdom;
        this.class = "x axis";
      }else if (position == "left"){
        this.transform = "translate(0,0)";
        this.scale = this.axes.ydom;
        this.class = "y axis";
      }else{
        this.transform = "translate(" + this.axes.width + ",0)";
        this.scale = this.axes.ydom;
        this.class = "y axis";
      }
    }

    Axis.prototype.draw = function(){
      this.axis = d3.svg.axis().scale(this.scale).orient(this.position);
      this.elem = this.axes.baseaxes.append('g')
                        .attr("transform", this.transform)
                        .attr("class", this.class)
                        .call(this.axis);
    };

    Axis.prototype.zoomed = function(){
      this.elem.call(this.axis);
    };
"""


GRID_CLASS = """
    function Grid(axes, xy){
      this.axes = axes;
      this.class = xy + " grid"
      if(xy == "x"){
        this.transform = "translate(0," + this.axes.height + ")";
        this.position = "bottom";
        this.scale = this.axes.xdom;
        this.tickSize = -this.axes.height;
      }else{
        this.transform = "translate(0,0)";
        this.position = "left";
        this.scale = this.axes.ydom;
        this.tickSize = -this.axes.width;
      }
    }

    Grid.prototype.draw = function(){
      this.grid = d3.svg.axis()
                          .scale(this.scale)
                          .orient(this.position)
                          .tickSize(this.tickSize, 0, 0)
                          .tickFormat("");
      this.elem = this.axes.axes.append("g")
                          .attr("class", this.class)
                          .attr("transform", this.transform)
                          .call(this.grid);
    };

    Grid.prototype.zoomed = function(){
      this.elem.call(this.grid);
    };
"""

ALL_FUNCTIONS = [FIGURE_CLASS, AXES_CLASS,
                 AXIS_CLASS, GRID_CLASS,
                 CONSTRUCT_SVG_PATH]
